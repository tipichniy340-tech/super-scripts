"""
Unit tests for system_info module.
"""
import pytest
from unittest.mock import patch, MagicMock
from rich.console import Console
from rich.table import Table

from system_info import (
    get_cpu_info,
    get_memory_info,
    get_disk_info,
    format_bytes,
    create_system_table,
    display_system_info,
    get_all_system_info,
)


class TestFormatBytes:
    """Tests for format_bytes function."""

    def test_zero_bytes(self):
        """Test formatting zero bytes."""
        assert format_bytes(0) == "0 B"

    def test_bytes(self):
        """Test formatting bytes."""
        assert format_bytes(512) == "512.00 B"

    def test_kilobytes(self):
        """Test formatting kilobytes."""
        assert format_bytes(1024) == "1.00 KB"
        assert format_bytes(2048) == "2.00 KB"

    def test_megabytes(self):
        """Test formatting megabytes."""
        assert format_bytes(1024 * 1024) == "1.00 MB"
        assert format_bytes(2 * 1024 * 1024) == "2.00 MB"

    def test_gigabytes(self):
        """Test formatting gigabytes."""
        assert format_bytes(1024 * 1024 * 1024) == "1.00 GB"
        assert format_bytes(4 * 1024 * 1024 * 1024) == "4.00 GB"

    def test_terabytes(self):
        """Test formatting terabytes."""
        assert format_bytes(1024 * 1024 * 1024 * 1024) == "1.00 TB"

    def test_decimal_precision(self):
        """Test decimal precision in formatting."""
        result = format_bytes(1536)  # 1.5 KB
        assert result == "1.50 KB"


class TestGetCpuInfo:
    """Tests for get_cpu_info function."""

    @patch('system_info.psutil')
    def test_get_cpu_info_returns_dict(self, mock_psutil):
        """Test that get_cpu_info returns a dictionary with correct keys."""
        mock_psutil.cpu_percent.return_value = 25.5
        mock_psutil.cpu_count.side_effect = [4, 8]  # physical, logical

        result = get_cpu_info()

        assert isinstance(result, dict)
        assert 'percent' in result
        assert 'cores' in result
        assert 'logical_cores' in result
        assert result['percent'] == 25.5
        assert result['cores'] == 4
        assert result['logical_cores'] == 8

    @patch('system_info.psutil')
    def test_get_cpu_info_handles_none_cores(self, mock_psutil):
        """Test handling of None values for core counts."""
        mock_psutil.cpu_percent.return_value = 10.0
        mock_psutil.cpu_count.side_effect = [None, None]

        result = get_cpu_info()

        assert result['cores'] == 0
        assert result['logical_cores'] == 0


class TestGetMemoryInfo:
    """Tests for get_memory_info function."""

    @patch('system_info.psutil')
    def test_get_memory_info_returns_dict(self, mock_psutil):
        """Test that get_memory_info returns a dictionary with correct keys."""
        mock_memory = MagicMock()
        mock_memory.total = 16 * 1024 * 1024 * 1024  # 16 GB
        mock_memory.available = 8 * 1024 * 1024 * 1024  # 8 GB
        mock_memory.percent = 50.0
        mock_psutil.virtual_memory.return_value = mock_memory

        result = get_memory_info()

        assert isinstance(result, dict)
        assert 'total' in result
        assert 'available' in result
        assert 'percent' in result
        assert result['total'] == 16 * 1024 * 1024 * 1024
        assert result['available'] == 8 * 1024 * 1024 * 1024
        assert result['percent'] == 50.0


class TestGetDiskInfo:
    """Tests for get_disk_info function."""

    @patch('system_info.psutil')
    def test_get_disk_info_returns_dict(self, mock_psutil):
        """Test that get_disk_info returns a dictionary with correct keys."""
        mock_disk = MagicMock()
        mock_disk.total = 500 * 1024 * 1024 * 1024  # 500 GB
        mock_disk.used = 250 * 1024 * 1024 * 1024  # 250 GB
        mock_disk.free = 250 * 1024 * 1024 * 1024  # 250 GB
        mock_disk.percent = 50.0
        mock_psutil.disk_usage.return_value = mock_disk

        # Use a path within allowed directories (/tmp is in the whitelist)
        with patch('system_info.os.path.exists', return_value=True), \
             patch('system_info.os.path.isdir', return_value=True), \
             patch('system_info.os.open', return_value=3), \
             patch('system_info.os.close'):
            result = get_disk_info("/tmp")

        assert isinstance(result, dict)
        assert 'total' in result
        assert 'used' in result
        assert 'free' in result
        assert 'percent' in result
        assert result['percent'] == 50.0

    @patch('system_info.psutil')
    def test_get_disk_info_handles_exception(self, mock_psutil):
        """Test that get_disk_info handles exceptions gracefully."""
        mock_psutil.disk_usage.side_effect = Exception("Disk not found")

        result = get_disk_info("/nonexistent")

        assert result['total'] == 0
        assert result['used'] == 0
        assert result['free'] == 0
        assert result['percent'] == 0

    @patch('system_info.psutil')
    def test_get_disk_info_custom_path(self, mock_psutil):
        """Test get_disk_info with custom path."""
        mock_disk = MagicMock()
        mock_disk.total = 100
        mock_disk.used = 50
        mock_disk.free = 50
        mock_disk.percent = 50.0
        mock_psutil.disk_usage.return_value = mock_disk
        
        # Mock os.path.exists and os.path.isdir to return True for the test path
        # Use a path within allowed directories (/tmp is in the whitelist)
        with patch('system_info.os.path.exists', return_value=True), \
             patch('system_info.os.path.isdir', return_value=True), \
             patch('system_info.os.open', return_value=3), \
             patch('system_info.os.close'):
            get_disk_info("/tmp/custom")

        mock_psutil.disk_usage.assert_called_once()


class TestCreateSystemTable:
    """Tests for create_system_table function."""

    @patch('system_info.get_cpu_info')
    @patch('system_info.get_memory_info')
    @patch('system_info.get_disk_info')
    def test_create_system_table_returns_table(self, mock_disk, mock_mem, mock_cpu):
        """Test that create_system_table returns a Table object."""
        mock_cpu.return_value = {
            'percent': 25.0,
            'cores': 4,
            'logical_cores': 8
        }
        mock_mem.return_value = {
            'total': 16 * 1024 * 1024 * 1024,
            'available': 8 * 1024 * 1024 * 1024,
            'percent': 50.0
        }
        mock_disk.return_value = {
            'total': 500 * 1024 * 1024 * 1024,
            'used': 250 * 1024 * 1024 * 1024,
            'free': 250 * 1024 * 1024 * 1024,
            'percent': 50.0
        }

        table = create_system_table()

        assert isinstance(table, Table)

    @patch('system_info.get_cpu_info')
    @patch('system_info.get_memory_info')
    @patch('system_info.get_disk_info')
    def test_create_system_table_with_custom_console(self, mock_disk, mock_mem, mock_cpu, mocker):
        """Test create_system_table with custom console."""
        mock_console = MagicMock(spec=Console)
        mock_cpu.return_value = {
            'percent': 25.0,
            'cores': 4,
            'logical_cores': 8
        }
        mock_mem.return_value = {
            'total': 16 * 1024 * 1024 * 1024,
            'available': 8 * 1024 * 1024 * 1024,
            'percent': 50.0
        }
        mock_disk.return_value = {
            'total': 500 * 1024 * 1024 * 1024,
            'used': 250 * 1024 * 1024 * 1024,
            'free': 250 * 1024 * 1024 * 1024,
            'percent': 50.0
        }

        table = create_system_table(mock_console)

        assert isinstance(table, Table)


class TestDisplaySystemInfo:
    """Tests for display_system_info function."""

    @patch('system_info.create_system_table')
    @patch('system_info.Console')
    def test_display_system_info_prints_table(self, mock_console_class, mock_create_table):
        """Test that display_system_info prints the table."""
        mock_console = MagicMock()
        mock_console_class.return_value = mock_console
        mock_table = MagicMock(spec=Table)
        mock_create_table.return_value = mock_table

        display_system_info()

        mock_console_class.assert_called_once()
        mock_create_table.assert_called_once()
        mock_console.print.assert_called_once_with(mock_table)

    @patch('system_info.create_system_table')
    def test_display_system_info_with_custom_console(self, mock_create_table, mocker):
        """Test display_system_info with custom console."""
        mock_console = MagicMock(spec=Console)
        mock_table = MagicMock(spec=Table)
        mock_create_table.return_value = mock_table

        display_system_info(mock_console)

        mock_console.print.assert_called_once_with(mock_table)


class TestGetAllSystemInfo:
    """Tests for get_all_system_info function."""

    @patch('system_info.get_cpu_info')
    @patch('system_info.get_memory_info')
    @patch('system_info.get_disk_info')
    def test_get_all_system_info_returns_dict(self, mock_disk, mock_mem, mock_cpu):
        """Test that get_all_system_info returns a dictionary with correct structure."""
        cpu_data = {'percent': 25.0, 'cores': 4, 'logical_cores': 8}
        mem_data = {'total': 16000000000, 'available': 8000000000, 'percent': 50.0}
        disk_data = {'total': 500000000000, 'used': 250000000000, 'free': 250000000000, 'percent': 50.0}

        mock_cpu.return_value = cpu_data
        mock_mem.return_value = mem_data
        mock_disk.return_value = disk_data

        result = get_all_system_info()

        assert isinstance(result, dict)
        assert 'cpu' in result
        assert 'memory' in result
        assert 'disk' in result
        assert result['cpu'] == cpu_data
        assert result['memory'] == mem_data
        assert result['disk'] == disk_data

    @patch('system_info.get_cpu_info')
    @patch('system_info.get_memory_info')
    @patch('system_info.get_disk_info')
    def test_get_all_system_info_calls_all_functions(self, mock_disk, mock_mem, mock_cpu):
        """Test that get_all_system_info calls all info functions."""
        mock_cpu.return_value = {}
        mock_mem.return_value = {}
        mock_disk.return_value = {}

        get_all_system_info()

        mock_cpu.assert_called_once()
        mock_mem.assert_called_once()
        mock_disk.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
