# 🚀 Super Scripts Collection

Коллекция мощных и безопасных скриптов для автоматизации и мониторинга системы с акцентом на безопасность кода.

**Цели проекта:**
- 🔒 **Безопасность** — все скрипты проходят аудит на уязвимости (path traversal, injection, etc.)
- 📊 **Мониторинг** — инструменты для отслеживания ресурсов системы в реальном времени
- 🤖 **Автоматизация** — упрощение рутинных задач администрирования
- 🧪 **Тестирование** — полное покрытие тестами, включая сценарии безопасности
- 📚 **Обучение** — демонстрация лучших практик написания безопасного Python-кода

## 🛠 Tools Included

### 📊 System Info (`system_info.py`)
Мощная утилита для мониторинга системных ресурсов в реальном времени.

**Возможности:**
- 💻 **CPU Monitoring** — отображение загрузки процессора и количества ядер
- 🧠 **Memory Tracking** — мониторинг использования оперативной памяти
- 💾 **Disk Usage** — анализ использования дискового пространства
- 🎨 **Rich Output** — красивый табличный вывод с цветами

**Пример использования:**
```bash
python system_info.py
```

**Программный интерфейс:**
```python
from system_info import display_system_info, get_all_system_info

# Показать информацию в консоли
display_system_info()

# Получить данные как словарь
info = get_all_system_info()
print(info['cpu']['percent'])  # Загрузка CPU в %
```

---

### 🔒 Security & Privacy
*Coming soon...*

### 🤖 Automation
*Coming soon...*

## 📋 Requirements
- Python 3.x
- [rich](https://github.com/Textualize/rich) — красивый вывод в терминале
- [psutil](https://github.com/giampaolo/psutil) — кроссплатформенный мониторинг системы

## 🚀 Quick Start
1. Clone repo:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

3. Run scripts:
   ```bash
   python system_info.py
   ```

## 🧪 Testing
```bash
python test_system_info.py
```

---
Made with ❤️ by tipichniy340-tech
