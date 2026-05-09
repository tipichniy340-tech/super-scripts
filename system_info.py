"""
System Info Module - Displays system information using rich and psutil.
"""
import os
import psutil
from rich.console import Console
from rich.table import Table
from typing import Dict, Any, Optional


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
    # Validate path to prevent directory traversal attacks
    try:
        # Check for empty or None path
        if not path or not isinstance(path, str):
            raise ValueError("Invalid path: path must be a non-empty string")
        
        # Check for null bytes and other dangerous characters
        if '\x00' in path:
            raise ValueError("Invalid path: null bytes are not allowed")
        
        # Ensure path is absolute and normalized
        abs_path = os.path.abspath(os.path.normpath(path))
        
        # Resolve symbolic links to get the real path
        real_path = os.path.realpath(abs_path)
        
        # Define allowed root directories (whitelist approach)
        allowed_roots = ["/", "/home", "/tmp", "/var", "/opt"]
        
        # Check if the resolved path is within allowed roots
        path_allowed = False
        for allowed_root in allowed_roots:
            if real_path == allowed_root or real_path.startswith(allowed_root + os.sep):
                path_allowed = True
                break
        
        if not path_allowed:
            raise ValueError(f"Access denied: path '{path}' is outside allowed directories")
        
        # Check if path exists and is accessible
        if not os.path.exists(real_path):
            raise ValueError(f"Path does not exist: {path}")
        
        # Verify it's a valid mount point or directory
        if not os.path.isdir(real_path):
            raise ValueError(f"Path is not a directory: {path}")
        
        disk = psutil.disk_usage(real_path)
        return {
            "total": disk.total,
            "used": disk.used,
            "free": disk.free,
            "percent": disk.percent,
        }
    except (ValueError, OSError, PermissionError) as e:
        # Log specific error types for debugging while returning safe defaults
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
