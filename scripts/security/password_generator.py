#!/usr/bin/env python3
"""
🔐 Password Generator & Strength Checker
Генератор надёжных паролей и проверка их стойкости.
"""

import random
import string
import re
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt

console = Console()

def generate_password(length=16, use_special=True, use_numbers=True):
    """Генерирует надёжный пароль."""
    characters = string.ascii_letters
    
    if use_numbers:
        characters += string.digits
    if use_special:
        characters += string.punctuation
    
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def check_password_strength(password):
    """Проверяет стойкость пароля."""
    score = 0
    feedback = []
    
    # Длина
    if len(password) >= 8:
        score += 20
    else:
        feedback.append("❌ Пароль слишком короткий (минимум 8 символов)")
    
    if len(password) >= 12:
        score += 10
    if len(password) >= 16:
        score += 10
    
    # Заглавные буквы
    if re.search(r'[A-Z]', password):
        score += 15
    else:
        feedback.append("❌ Добавьте заглавные буквы")
    
    # Строчные буквы
    if re.search(r'[a-z]', password):
        score += 15
    else:
        feedback.append("❌ Добавьте строчные буквы")
    
    # Цифры
    if re.search(r'\d', password):
        score += 15
    else:
        feedback.append("❌ Добавьте цифры")
    
    # Спецсимволы
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 15
    else:
        feedback.append("❌ Добавьте специальные символы")
    
    # Разнообразие
    unique_chars = len(set(password))
    if unique_chars >= 10:
        score += 10
    
    # Определение уровня стойкости
    if score >= 90:
        strength = "🟢 Отличная"
        color = "green"
    elif score >= 70:
        strength = "🔵 Хорошая"
        color = "blue"
    elif score >= 50:
        strength = "🟡 Средняя"
        color = "yellow"
    elif score >= 30:
        strength = "🟠 Низкая"
        color = "orange"
    else:
        strength = "🔴 Очень слабая"
        color = "red"
    
    return {
        'score': score,
        'strength': strength,
        'color': color,
        'feedback': feedback
    }

def display_password_info(password, strength_info):
    """Отображает информацию о пароле."""
    console.print("\n")
    
    # Панель с паролем
    password_panel = Panel(
        f"[bold white]{password}[/bold white]\n\n"
        f"[italic]💡 Совет: Сохраните этот пароль в менеджере паролей[/italic]",
        title="🔑 Ваш новый пароль",
        border_style="green"
    )
    console.print(password_panel)
    
    # Таблица со стойкостью
    table = Table(title="📊 Анализ стойкости пароля")
    table.add_column("Параметр", style="cyan")
    table.add_column("Значение", style="white")
    
    table.add_row("Длина", str(len(password)))
    table.add_row("Уникальных символов", str(len(set(password))))
    table.add_row("Оценка", f"{strength_info['score']}/100")
    table.add_row("Стойкость", f"[{strength_info['color']}]{strength_info['strength']}[/{strength_info['color']}]")
    
    console.print(table)
    
    # Рекомендации
    if strength_info['feedback']:
        console.print("\n[bold yellow]💡 Рекомендации по улучшению:[/bold yellow]")
        for item in strength_info['feedback']:
            console.print(f"  • {item}")
    else:
        console.print("\n[bold green]✅ Пароль соответствует всем рекомендациям![/bold green]")

def main():
    console.print(Panel.fit(
        "[bold purple]🔐 Password Generator & Strength Checker[/bold purple]\n\n"
        "Генератор надёжных паролей и проверка их стойкости",
        border_style="purple"
    ))
    
    try:
        # Выбор режима
        console.print("\n[bold]Выберите режим:[/bold]")
        console.print("1. 🔑 Сгенерировать новый пароль")
        console.print("2. 🧪 Проверить существующий пароль")
        console.print("3. 🚀 Выход")
        
        choice = Prompt.ask("\nВаш выбор", choices=["1", "2", "3"], default="1")
        
        if choice == "1":
            # Настройки генерации
            length = int(Prompt.ask("\nДлина пароля", default="16"))
            use_special = Prompt.ask("Использовать спецсимволы (!@#$...)", choices=["y", "n"], default="y") == "y"
            use_numbers = Prompt.ask("Использовать цифры", choices=["y", "n"], default="y") == "y"
            
            console.print("\n[bold cyan]⚙️ Генерация паролей...[/bold cyan]\n")
            
            # Генерация нескольких вариантов
            passwords = []
            for i in range(3):
                pwd = generate_password(length, use_special, use_numbers)
                strength = check_password_strength(pwd)
                passwords.append((pwd, strength))
            
            # Отображение вариантов
            table = Table(title="🎲 Варианты паролей")
            table.add_column("№", style="cyan")
            table.add_column("Пароль", style="white")
            table.add_column("Стойкость", style="green")
            table.add_column("Оценка", style="yellow")
            
            for idx, (pwd, strength) in enumerate(passwords, 1):
                table.add_row(
                    str(idx),
                    pwd,
                    strength['strength'],
                    f"{strength['score']}/100"
                )
            
            console.print(table)
            
            # Выбор пароля для детального анализа
            selected = int(Prompt.ask("\nВыберите пароль для детального анализа (1-3)", default="1")) - 1
            if 0 <= selected < len(passwords):
                display_password_info(passwords[selected][0], passwords[selected][1])
        
        elif choice == "2":
            password = Prompt.ask("\nВведите пароль для проверки", password=True)
            if password:
                strength = check_password_strength(password)
                display_password_info(password, strength)
            else:
                console.print("[yellow]⚠️ Пароль не введён[/yellow]")
        
        elif choice == "3":
            console.print("[green]👋 До свидания![/green]")
            sys.exit(0)
        
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️ Программа прервана пользователем[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[bold red]❌ Ошибка: {e}[/bold red]")
        sys.exit(1)

if __name__ == "__main__":
    main()
