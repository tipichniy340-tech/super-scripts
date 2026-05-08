#!/usr/bin/env python3
"""
📊 System Resource Monitor
Мониторинг использования ресурсов системы в реальном времени.
"""

import psutil
import sys
import time
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.layout import Layout
from rich.text import Text

console = Console()

def get_cpu_info():
    """Получает информацию о CPU."""
    cpu_percent = psutil.cpu_percent(interval=0.5)
    cpu_count = psutil.cpu_count(logical=True)
    cpu_freq = psutil.cpu_freq()
    
    per_cpu = psutil.cpu_percent(interval=0.1, percpu=True)
    
    return {
        'percent': cpu_percent,
        'count': cpu_count,
        'freq': round(cpu_freq.current / 1000, 2) if cpu_freq else 0,
        'per_cpu': per_cpu
    }

def get_memory_info():
    """Получает информацию о памяти."""
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    
    return {
        'total_gb': round(mem.total / (1024**3), 2),
        'used_gb': round(mem.used / (1024**3), 2),
        'percent': mem.percent,
        'swap_total_gb': round(swap.total / (1024**3), 2),
        'swap_used_gb': round(swap.used / (1024**3), 2),
        'swap_percent': swap.percent
    }

def get_disk_info():
    """Получает информацию о дисках."""
    disk_info = []
    
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_info.append({
                'device': partition.device,
                'mountpoint': partition.mountpoint,
                'total_gb': round(usage.total / (1024**3), 2),
                'used_gb': round(usage.used / (1024**3), 2),
                'percent': usage.percent,
                'fstype': partition.fstype
            })
        except PermissionError:
            continue
    
    return disk_info

def get_network_info():
    """Получает информацию о сети."""
    net_io = psutil.net_io_counters()
    
    return {
        'bytes_sent_mb': round(net_io.bytes_sent / (1024**2), 2),
        'bytes_recv_mb': round(net_io.bytes_recv / (1024**2), 2),
        'packets_sent': net_io.packets_sent,
        'packets_recv': net_io.packets_recv
    }

def get_process_info(limit=5):
    """Получает информацию о топ процессах по использованию CPU."""
    processes = []
    
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            processes.append({
                'pid': proc.info['pid'],
                'name': proc.info['name'][:30],
                'cpu': proc.info['cpu_percent'] or 0,
                'memory': proc.info['memory_percent'] or 0
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    # Сортируем по CPU
    processes.sort(key=lambda x: x['cpu'], reverse=True)
    
    return processes[:limit]

def create_progress_bar(percent, width=30):
    """Создаёт текстовый прогресс-бар."""
    filled = int(width * percent / 100)
    empty = width - filled
    
    if percent >= 90:
        color = "red"
    elif percent >= 70:
        color = "yellow"
    else:
        color = "green"
    
    bar = "█" * filled + "░" * empty
    return f"[{color}]{bar}[/{color}] {percent}%"

def generate_layout():
    """Генерирует макет для отображения."""
    cpu_info = get_cpu_info()
    memory_info = get_memory_info()
    disk_info = get_disk_info()
    network_info = get_network_info()
    processes = get_process_info()
    
    # CPU Panel
    cpu_text = Text()
    cpu_text.append(f"Общая загрузка: ", style="bold")
    cpu_text.append(f"{cpu_info['percent']}%\n", style="green" if cpu_info['percent'] < 70 else "yellow" if cpu_info['percent'] < 90 else "red")
    cpu_text.append(f"Ядер: {cpu_info['count']} | Частота: {cpu_info['freq']} GHz\n\n", style="dim")
    
    for i, cpu in enumerate(cpu_info['per_cpu'][:8]):
        bar = create_progress_bar(cpu, 20)
        cpu_text.append(f"Ядро {i+1}: ", style="dim")
        cpu_text.append(f"{bar}\n")
    
    cpu_panel = Panel(cpu_text, title="🖥️ CPU", border_style="cyan")
    
    # Memory Panel
    mem_text = Text()
    mem_text.append(f"Всего: {memory_info['total_gb']} GB\n", style="dim")
    mem_text.append(f"Использовано: {memory_info['used_gb']} GB\n", style="dim")
    mem_text.append(f"\n", style="")
    mem_bar = create_progress_bar(memory_info['percent'], 30)
    mem_text.append(f"RAM: {mem_bar}\n\n", style="")
    
    swap_bar = create_progress_bar(memory_info['swap_percent'], 30)
    mem_text.append(f"Swap: {swap_bar}", style="")
    
    memory_panel = Panel(mem_text, title="💾 Память", border_style="magenta")
    
    # Disk Panel
    disk_text = Text()
    for disk in disk_info[:4]:
        disk_text.append(f"{disk['mountpoint']} ({disk['device']})\n", style="bold cyan")
        disk_text.append(f"  Тип: {disk['fstype']} | Всего: {disk['total_gb']} GB\n", style="dim")
        bar = create_progress_bar(disk['percent'], 25)
        disk_text.append(f"  {bar}\n\n")
    
    disk_panel = Panel(disk_text, title="💿 Диски", border_style="blue")
    
    # Network Panel
    net_text = Text()
    net_text.append(f"Отправлено: {network_info['bytes_sent_mb']} MB ({network_info['packets_sent']} пакетов)\n", style="green")
    net_text.append(f"Получено: {network_info['bytes_recv_mb']} MB ({network_info['packets_recv']} пакетов)", style="blue")
    
    network_panel = Panel(net_text, title="🌐 Сеть", border_style="yellow")
    
    # Processes Panel
    proc_text = Text()
    proc_text.append(f"{'PID':<8} {'Имя':<30} {'CPU%':<8} {'RAM%':<8}\n", style="bold")
    proc_text.append("─" * 54 + "\n", style="dim")
    
    for proc in processes:
        cpu_color = "green" if proc['cpu'] < 30 else "yellow" if proc['cpu'] < 70 else "red"
        proc_text.append(f"{proc['pid']:<8} ", style="dim")
        proc_text.append(f"{proc['name']:<30} ", style="white")
        proc_text.append(f"{proc['cpu']:<8} ", style=cpu_color)
        proc_text.append(f"{proc['memory']:.1f}\n", style="magenta")
    
    processes_panel = Panel(proc_text, title="🔝 Топ процессов", border_style="green")
    
    # Создаём layout
    layout = Layout()
    layout.split_column(
        Layout(name="top"),
        Layout(name="bottom")
    )
    
    layout["top"].split_row(
        Layout(cpu_panel),
        Layout(memory_panel),
        Layout(network_panel)
    )
    
    layout["bottom"].split_row(
        Layout(disk_panel),
        Layout(processes_panel)
    )
    
    return layout

def main():
    console.print(Panel.fit(
        "[bold green]📊 System Resource Monitor[/bold green]\n\n"
        "Мониторинг ресурсов системы в реальном времени",
        border_style="green"
    ))
    
    console.print("\n[yellow]Нажмите Ctrl+C для выхода[/yellow]\n")
    time.sleep(1)
    
    try:
        with Live(generate_layout(), refresh_per_second=2, screen=True) as live:
            while True:
                live.update(generate_layout())
                time.sleep(0.5)
    except KeyboardInterrupt:
        console.print("\n[green]👋 Мониторинг остановлен[/green]")
        
        # Финальная статистика
        console.print("\n[bold]📈 Финальная статистика:[/bold]")
        
        cpu_info = get_cpu_info()
        memory_info = get_memory_info()
        
        table = Table()
        table.add_column("Ресурс", style="cyan")
        table.add_column("Значение", style="white")
        
        table.add_row("CPU", f"{cpu_info['percent']}%")
        table.add_row("RAM", f"{memory_info['percent']}%")
        table.add_row("Время завершения", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        console.print(table)
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[bold red]❌ Ошибка: {e}[/bold red]")
        sys.exit(1)

if __name__ == "__main__":
    main()
