#!/usr/bin/env python3
"""
🔒 System Security Scanner
Сканирует систему на потенциальные уязвимости и проблемы безопасности.
"""

import psutil
import os
import sys
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress

console = Console()

def check_running_processes():
    """Проверяет запущенные процессы на подозрительную активность."""
    console.print(Panel("[bold blue]🔍 Сканирование запущенных процессов...[/bold blue]"))
    
    suspicious_keywords = ['miner', 'hack', 'keylog', 'spy', 'trojan']
    found_issues = []
    
    with Progress() as progress:
        task = progress.add_task("[cyan]Анализ процессов...", total=100)
        
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            try:
                name = proc.info['name'].lower()
                for keyword in suspicious_keywords:
                    if keyword in name:
                        found_issues.append({
                            'type': 'Подозрительный процесс',
                            'name': proc.info['name'],
                            'pid': proc.info['pid'],
                            'user': proc.info['username']
                        })
                progress.advance(task, 100 / len(list(psutil.process_iter())))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    
    return found_issues

def check_open_ports():
    """Проверяет открытые сетевые подключения."""
    console.print(Panel("[bold blue]🌐 Проверка сетевых подключений...[/bold blue]"))
    
    connections = psutil.net_connections(kind='inet')
    listening_ports = []
    
    for conn in connections:
        if conn.status == 'LISTEN':
            listening_ports.append({
                'port': conn.laddr.port if conn.laddr else 'N/A',
                'address': conn.laddr.ip if conn.laddr else 'N/A',
                'protocol': 'TCP' if conn.type == 1 else 'UDP'
            })
    
    return listening_ports

def check_disk_usage():
    """Проверяет использование диска на аномалии."""
    console.print(Panel("[bold blue]💾 Анализ использования диска...[/bold blue]"))
    
    disk_info = []
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_info.append({
                'device': partition.device,
                'mountpoint': partition.mountpoint,
                'total_gb': round(usage.total / (1024**3), 2),
                'used_gb': round(usage.used / (1024**3), 2),
                'percent': usage.percent
            })
        except PermissionError:
            continue
    
    return disk_info

def generate_report(process_issues, ports, disk_info):
    """Генерирует отчёт о безопасности."""
    console.print("\n[bold green]✅ Сканирование завершено![/bold green]\n")
    
    # Таблица процессов
    if process_issues:
        table = Table(title="⚠️ Подозрительные процессы")
        table.add_column("Тип", style="red")
        table.add_column("Имя", style="yellow")
        table.add_column("PID", style="cyan")
        table.add_column("Пользователь", style="magenta")
        
        for issue in process_issues:
            table.add_row(issue['type'], issue['name'], str(issue['pid']), str(issue['user']))
        
        console.print(table)
    else:
        console.print("[green]✓ Подозрительных процессов не найдено[/green]")
    
    # Таблица портов
    if ports:
        table = Table(title="🌐 Открытые порты")
        table.add_column("Протокол", style="cyan")
        table.add_column("Адрес", style="yellow")
        table.add_column("Порт", style="green")
        
        for port in ports:
            table.add_row(port['protocol'], port['address'], str(port['port']))
        
        console.print(table)
    else:
        console.print("[green]✓ Нет активных слушающих портов[/green]")
    
    # Таблица диска
    table = Table(title="💾 Использование диска")
    table.add_column("Устройство", style="cyan")
    table.add_column("Точка монтирования", style="yellow")
    table.add_column("Всего (GB)", style="green")
    table.add_column("Использовано (GB)", style="blue")
    table.add_column("% Использовано", style="magenta")
    
    for disk in disk_info:
        color = "green" if disk['percent'] < 70 else "yellow" if disk['percent'] < 90 else "red"
        table.add_row(
            disk['device'],
            disk['mountpoint'],
            str(disk['total_gb']),
            str(disk['used_gb']),
            f"[{color}]{disk['percent']}%[/{color}]"
        )
    
    console.print(table)
    
    # Общая статистика
    summary = Panel(
        f"[bold]Статистика сканирования:[/bold]\n\n"
        f"• Подозрительных процессов: {len(process_issues)}\n"
        f"• Открытых портов: {len(ports)}\n"
        f"• Разделов диска: {len(disk_info)}\n"
        f"• Время сканирования: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        title="📊 Итоговый отчёт",
        border_style="green"
    )
    console.print(summary)

def main():
    console.print(Panel.fit(
        "[bold red]🔒 System Security Scanner[/bold red]\n\n"
        "Инструмент для проверки безопасности системы",
        border_style="red"
    ))
    
    try:
        process_issues = check_running_processes()
        ports = check_open_ports()
        disk_info = check_disk_usage()
        generate_report(process_issues, ports, disk_info)
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️ Сканирование прервано пользователем[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[bold red]❌ Ошибка: {e}[/bold red]")
        sys.exit(1)

if __name__ == "__main__":
    main()
