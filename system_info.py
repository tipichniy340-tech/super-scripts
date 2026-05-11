"""
System Info Module - Displays system information using rich and psutil.
"""
import os
import logging
import time
import fcntl
import psutil
from rich.console import Console
from rich.table import Table
from collections import defaultdict
from typing import Dict, Any, Optional

# Configure logging for security events
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='/var/log/system_info_security.log'
)
logger = logging.getLogger(__name__)

# Rate limiting configuration
RATE_LIMIT_MAX_REQUESTS = 100  # Maximum requests per window
RATE_LIMIT_WINDOW_SECONDS = 60  # Time window in seconds

# Path length limit
MAX_PATH_LENGTH = 4096

# Rate limiting storage (in production, use Redis or similar)
_request_timestamps: Dict[str, list] = defaultdict(list)


def check_rate_limit(client_id: str = "default") -> bool:
    """
    Check if the client has exceeded the rate limit.
    
    Args:
        client_id: Identifier for the client (e.g., IP address, user ID)
    
    Returns:
        True if request is allowed, False if rate limit exceeded
    """
    current_time = time.time()
    window_start = current_time - RATE_LIMIT_WINDOW_SECONDS
    
    # Clean old timestamps
    _request_timestamps[client_id] = [
        ts for ts in _request_timestamps[client_id] 
        if ts > window_start
    ]
    
    # Check if limit exceeded
    if len(_request_timestamps[client_id]) >= RATE_LIMIT_MAX_REQUESTS:
        logger.warning(f"Rate limit exceeded for client: {client_id}")
        return False
    
    # Record this request
    _request_timestamps[client_id].append(current_time)
    return True


class SecurePathValidator:
    """Context manager for secure path validation and file access."""
    
    def __init__(self, path: str, allowed_roots: list):
        self.path = path
        self.allowed_roots = allowed_roots
        self.real_path = None
        self.fd = None
    
    def __enter__(self):
        # Validate path length
        if not self.path or len(self.path) > MAX_PATH_LENGTH:
            logger.warning(f"Path length violation: path length={len(self.path) if self.path else 0}")
            raise ValueError(f"Invalid path: path exceeds maximum length of {MAX_PATH_LENGTH} characters")
        
        # Check for null bytes
        if '\x00' in self.path:
            logger.warning(f"Null byte injection attempt in path: {repr(self.path[:100])}")
            raise ValueError("Invalid path: null bytes are not allowed")
        
        # Ensure path is absolute and normalized
        abs_path = os.path.abspath(os.path.normpath(self.path))
        
        # Resolve symbolic links to get the real path
        self.real_path = os.path.realpath(abs_path)
        
        # Check if the resolved path is within allowed roots
        path_allowed = False
        for allowed_root in self.allowed_roots:
            if self.real_path == allowed_root or self.real_path.startswith(allowed_root + os.sep):
                path_allowed = True
                break
        
        if not path_allowed:
            logger.warning(f"Access denied: path '{self.path}' (resolved: '{self.real_path}') is outside allowed directories")
            raise ValueError(f"Access denied: path '{self.path}' is outside allowed directories")
        
        # Check if path exists
        if not os.path.exists(self.real_path):
            logger.info(f"Path does not exist: {self.path}")
            raise ValueError(f"Path does not exist: {self.path}")
        
        # Verify it's a valid directory
        if not os.path.isdir(self.real_path):
            logger.warning(f"Path is not a directory: {self.path}")
            raise ValueError(f"Path is not a directory: {self.path}")
        
        # Use os.open with O_NOFOLLOW to prevent symlink attacks during access
        try:
            self.fd = os.open(self.real_path, os.O_RDONLY | os.O_NOFOLLOW)
        except OSError as e:
            if e.errno == 40:  # ELOOP - too many symbolic links
                logger.warning(f"Symlink attack detected: {self.path}")
                raise ValueError(f"Access denied: potential symlink attack")
            elif e.errno == 17:  # EISDIR - expected when opening directory
                # This is expected for directories, we can still proceed
                pass
            else:
                logger.error(f"Error opening path {self.real_path}: {e}")
                raise
        
        logger.info(f"Secure path validated: {self.path} -> {self.real_path}")
        return self.real_path
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.fd is not None:
            try:
                os.close(self.fd)
            except OSError:
                pass
        return False


def get_cpu_info() -> Dict[str, Any]:
    """Get CPU information."""
    return {
        "percent": psutil.cpu_percent(interval=0),
        "cores": psutil.cpu_count(logical=False) or 0,
        "logical_cores": psutil.cpu_count(logical=True) or 0,
    }


def get_memory_info() -> Dict[str, Any]:
    """Get memory information."""
    mem = psutil.virtual_memory()
    return {
        "total": mem.total,
        "available": mem.available,
        "percent": mem.percent,
    }


def get_disk_info(path: str = "/") -> Dict[str, Any]:
    """Get disk information for specified path."""
    # Check rate limit first
    if not check_rate_limit():
        logger.error("Rate limit exceeded for get_disk_info")
        return {
            "total": 0,
            "used": 0,
            "free": 0,
            "percent": 0,
        }
    
    # Validate path to prevent directory traversal attacks
    try:
        # Check for empty or None path
        if not path or not isinstance(path, str):
            raise ValueError("Invalid path: path must be a non-empty string")
        
        # Define allowed root directories (whitelist approach) - REMOVED "/" for stricter security
        allowed_roots = ["/home", "/tmp", "/var", "/opt"]
        
        # Use context manager for atomic validation and access
        with SecurePathValidator(path, allowed_roots) as real_path:
            disk = psutil.disk_usage(real_path)
            logger.info(f"Successfully accessed disk info for: {path}")
            return {
                "total": disk.total,
                "used": disk.used,
                "free": disk.free,
                "percent": disk.percent,
            }
    except (ValueError, OSError, PermissionError) as e:
        # Log specific error types for debugging while returning safe defaults
        logger.warning(f"Error accessing disk info for path '{path}': {e}")
        return {
            "total": 0,
            "used": 0,
            "free": 0,
            "percent": 0,
        }


def format_bytes(bytes_value: int) -> str:
    """Format bytes to human-readable string."""
    if bytes_value == 0:
        return "0 B"
    
    units = ["B", "KB", "MB", "GB", "TB"]
    unit_index = 0
    value = float(bytes_value)
    
    while value >= 1024 and unit_index < len(units) - 1:
        value /= 1024
        unit_index += 1
    
    return f"{value:.2f} {units[unit_index]}"


def create_system_table(console: Optional[Console] = None) -> Table:
    """Create a rich table with system information."""
    if console is None:
        console = Console()
    
    table = Table(title="System Information")
    table.add_column("Component", style="cyan")
    table.add_column("Value", style="green")
    
    # CPU info
    cpu_info = get_cpu_info()
    table.add_row(
        "CPU Usage",
        f"{cpu_info['percent']}%"
    )
    table.add_row(
        "CPU Cores",
        f"{cpu_info['cores']} physical / {cpu_info['logical_cores']} logical"
    )
    
    # Memory info
    mem_info = get_memory_info()
    table.add_row(
        "Memory Usage",
        f"{format_bytes(mem_info['total'] - mem_info['available'])} / {format_bytes(mem_info['total'])} ({mem_info['percent']}%)"
    )
    
    # Disk info
    disk_info = get_disk_info()
    table.add_row(
        "Disk Usage",
        f"{format_bytes(disk_info['used'])} / {format_bytes(disk_info['total'])} ({disk_info['percent']}%)"
    )
    
    return table


def display_system_info(console: Optional[Console] = None) -> None:
    """Display system information using rich console."""
    if console is None:
        console = Console()
    
    table = create_system_table(console)
    console.print(table)


def get_all_system_info() -> Dict[str, Dict[str, Any]]:
    """Get all system information as a dictionary."""
    return {
        "cpu": get_cpu_info(),
        "memory": get_memory_info(),
        "disk": get_disk_info(),
    }


if __name__ == "__main__":
    display_system_info()
