# 🚀 Super Scripts Collection

Collection of unique and powerful PC automation tools and browser extensions.

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

### 🗂️ Tab Manager Pro (Browser Extension)

Powerful browser extension for managing your tabs efficiently!

**Features:**
- 🔍 **Smart Search** - Quickly find tabs by title or URL
- 📊 **Tab Statistics** - See total tab count at a glance
- 🗑️ **Close Duplicates** - Remove duplicate tabs with one click
- ➡️ **Close Tabs to Right** - Clean up tabs to the right
- 📁 **Group by Domain** - Automatically organize tabs by website
- ⌨️ **Keyboard Shortcut** - Quick access with `Ctrl+Shift+T`
- 🎨 **Beautiful UI** - Modern gradient design

**Installation:**
1. Navigate to `extensions/tab-manager-pro`
2. Open Chrome/Edge and go to `chrome://extensions/`
3. Enable "Developer mode"
4. Click "Load unpacked" and select the folder

📖 [Full Documentation](extensions/tab-manager-pro/README.md)

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
