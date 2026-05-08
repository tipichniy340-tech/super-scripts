#!/usr/bin/env python3
"""
🤖 File Organizer
Автоматическая сортировка файлов по папкам в зависимости от типа.
"""

import os
import shutil
import sys
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress
from rich.prompt import Prompt, Confirm

console = Console()

# Категории файлов и их расширения
FILE_CATEGORIES = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico'],
    'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'],
    'Music': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma'],
    'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx'],
    'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
    'Code': ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.h', '.cs', '.php', '.rb', '.go'],
    'Web': ['.html', '.htm', '.css', '.scss', '.json', '.xml'],
    'Executables': ['.exe', '.msi', '.deb', '.rpm', '.app', '.dmg'],
    'Fonts': ['.ttf', '.otf', '.woff', '.woff2'],
    'Other': []
}

def get_file_category(file_path):
    """Определяет категорию файла по его расширению."""
    ext = Path(file_path).suffix.lower()
    
    for category, extensions in FILE_CATEGORIES.items():
        if ext in extensions:
            return category
    
    return 'Other'

def organize_files(target_directory, dry_run=False):
    """Сортирует файлы в указанной директории."""
    target_path = Path(target_directory)
    
    if not target_path.exists():
        console.print(f"[bold red]❌ Директория не найдена: {target_directory}[/bold red]")
        return None
    
    # Сбор статистики
    stats = {category: 0 for category in FILE_CATEGORIES.keys()}
    moved_files = []
    errors = []
    
    # Получаем список всех файлов
    files = [f for f in target_path.iterdir() if f.is_file()]
    
    if not files:
        console.print("[yellow]⚠️ Нет файлов для сортировки[/yellow]")
        return {'stats': stats, 'moved': moved_files, 'errors': errors}
    
    console.print(f"\n[bold cyan]📁 Найдено файлов: {len(files)}[/bold cyan]\n")
    
    with Progress() as progress:
        task = progress.add_task("[green]Сортировка файлов...", total=len(files))
        
        for file_path in files:
            try:
                category = get_file_category(file_path)
                stats[category] += 1
                
                # Создаём папку категории если не существует
                category_folder = target_path / category
                if not dry_run:
                    category_folder.mkdir(exist_ok=True)
                    
                    # Перемещаем файл
                    dest_path = category_folder / file_path.name
                    
                    # Если файл с таким именем уже существует, добавляем timestamp
                    if dest_path.exists():
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        stem = file_path.stem
                        suffix = file_path.suffix
                        dest_path = category_folder / f"{stem}_{timestamp}{suffix}"
                    
                    shutil.move(str(file_path), str(dest_path))
                    moved_files.append({
                        'file': file_path.name,
                        'category': category,
                        'destination': str(dest_path)
                    })
                else:
                    moved_files.append({
                        'file': file_path.name,
                        'category': category,
                        'destination': str(category_folder / file_path.name)
                    })
                
                progress.advance(task)
                
            except Exception as e:
                errors.append({
                    'file': file_path.name,
                    'error': str(e)
                })
                progress.advance(task)
    
    return {'stats': stats, 'moved': moved_files, 'errors': errors}

def display_results(results, dry_run=False):
    """Отображает результаты сортировки."""
    if not results:
        return
    
    mode_text = "[yellow]РЕЖИМ ПРОСМОТРА (dry-run)[/yellow]" if dry_run else "[green]РЕЖИМ СОРТИРОВКИ[/green]"
    console.print(Panel(f"{mode_text}", title="📊 Режим работы", border_style="yellow"))
    
    # Таблица статистики
    table = Table(title="📈 Статистика по категориям")
    table.add_column("Категория", style="cyan")
    table.add_column("Файлов", style="green", justify="right")
    
    for category, count in results['stats'].items():
        if count > 0:
            table.add_row(category, str(count))
    
    console.print(table)
    
    # Список перемещённых файлов (первые 10)
    if results['moved']:
        console.print(f"\n[bold]Всего перемещено: {len(results['moved'])} файлов[/bold]")
        
        if len(results['moved']) <= 10:
            table = Table(title="📦 Перемещённые файлы")
            table.add_column("Файл", style="white")
            table.add_column("Категория", style="cyan")
            table.add_column("Назначение", style="green")
            
            for item in results['moved']:
                table.add_row(item['file'], item['category'], item['destination'])
            
            console.print(table)
        else:
            console.print("\n[italic]Показаны первые 10 файлов:[/italic]")
            table = Table(title="📦 Перемещённые файлы (первые 10)")
            table.add_column("Файл", style="white")
            table.add_column("Категория", style="cyan")
            table.add_column("Назначение", style="green")
            
            for item in results['moved'][:10]:
                table.add_row(item['file'], item['category'], item['destination'])
            
            console.print(table)
            console.print(f"\n[yellow]... и ещё {len(results['moved']) - 10} файлов[/yellow]")
    
    # Ошибки
    if results['errors']:
        console.print(f"\n[bold red]❌ Ошибки: {len(results['errors'])}[/bold red]")
        for error in results['errors'][:5]:
            console.print(f"  • {error['file']}: {error['error']}")
        if len(results['errors']) > 5:
            console.print(f"  ... и ещё {len(results['errors']) - 5} ошибок")

def main():
    console.print(Panel.fit(
        "[bold blue]🤖 File Organizer[/bold blue]\n\n"
        "Автоматическая сортировка файлов по папкам",
        border_style="blue"
    ))
    
    try:
        # Выбор директории
        default_dir = os.getcwd()
        target_dir = Prompt.ask(
            "\n📂 Укажите директорию для сортировки",
            default=default_dir
        )
        
        # Проверка существования
        if not Path(target_dir).exists():
            console.print(f"[bold red]❌ Директория не найдена: {target_dir}[/bold red]")
            sys.exit(1)
        
        console.print(f"\n[bold]Целевая директория:[/bold] {target_dir}")
        
        # Выбор режима
        dry_run = not Confirm.ask("\nЗапустить сортировку? (No = режим просмотра)", default=True)
        
        # Запуск сортировки
        console.print("\n[bold cyan]⚙️ Начало обработки...[/bold cyan]\n")
        results = organize_files(target_dir, dry_run=dry_run)
        
        # Отображение результатов
        display_results(results, dry_run=dry_run)
        
        # Итоговое сообщение
        if results and results['moved']:
            if dry_run:
                console.print(f"\n[green]✅ Готово! В режиме просмотра найдено {len(results['moved'])} файлов для сортировки.[/green]")
                console.print("[italic]Запустите снова без режима просмотра чтобы реально переместить файлы.[/italic]")
            else:
                console.print(f"\n[green]✅ Готово! Успешно отсортировано {len(results['moved'])} файлов.[/green]")
        elif results:
            console.print("\n[yellow]⚠️ Файлы не найдены или не требуют сортировки.[/yellow]")
        
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️ Программа прервана пользователем[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[bold red]❌ Ошибка: {e}[/bold red]")
        sys.exit(1)

if __name__ == "__main__":
    main()
