# 🎵 Audio Steganography Tool

Современный инструмент для скрытия секретных сообщений в аудиофайлах с использованием LSB-стеганографии.

## ✨ Возможности

- 🔒 **Скрытие сообщений** - встраивание текста в WAV-аудиофайлы
- 🔓 **Извлечение сообщений** - декодирование скрытых сообщений
- 🎯 **LSB-алгоритм** - наименее значимые биты для незаметности
- ⚡ **Быстрая работа** - оптимизированный код на Python
- 🎨 **Красивый CLI** - цветной вывод с Rich
- ✅ **Полная обработка ошибок** - проверка форматов, размеров, битых файлов

## 🚀 Быстрый старт

### Установка зависимостей

```bash
pip install -r requirements.txt
```

### Генерация тестовых аудиофайлов

```bash
python examples/generate_examples.py
```

### Использование

**Закодировать сообщение:**
```bash
python main.py encode -i examples/test_tone.wav -o output.wav -m "Секретное сообщение"
```

**Декодировать сообщение:**
```bash
python main.py decode -i output.wav
```

## 📖 Примеры использования

### Кодирование

```bash
# Простое сообщение
python main.py encode -i audio.wav -o secret.wav -m "Hello World"

# Длинное сообщение
python main.py encode -i music.wav -o hidden.wav -m "Это очень длинное сообщение которое будет скрыто в аудиофайле"

# Сообщение со спецсимволами
python main.py encode -i tone.wav -o encoded.wav -m "Special: !@#$%^&*()"
```

### Декодирование

```bash
# Извлечь сообщение
python main.py decode -i secret.wav

# Из другого файла
python main.py decode -i hidden.wav
```

## 🧪 Тестирование

```bash
# Запустить все тесты
pytest tests/ -v

# Запустить конкретный тест
pytest tests/test_steganography.py::TestEncodeDecode::test_encode_and_decode_simple_message -v
```

## 📁 Структура проекта

```
├── main.py                 # CLI интерфейс
├── steganography/          # Основной модуль
│   ├── __init__.py
│   ├── encoder.py         # Кодирование сообщений
│   └── decoder.py         # Декодирование сообщений
├── tests/                  # Тесты
│   └── test_steganography.py
├── examples/               # Примеры и генераторы
│   └── generate_examples.py
├── requirements.txt        # Зависимости
└── README.md              # Документация
```

## 🔧 API для разработчиков

### Программное использование

```python
from steganography import encode_message, decode_message

# Кодирование
encode_message(
    audio_path="input.wav",
    message="Secret message",
    output_path="output.wav"
)

# Декодирование
message = decode_message("output.wav")
print(message)  # "Secret message"
```

## ⚙️ Технические детали

### Алгоритм

1. **Длина сообщения** - первые 32 бита содержат длину сообщения
2. **LSB стеганография** - каждый бит сообщения заменяет LSB аудио-сэмпла
3. **7-битная кодировка** - каждый символ кодируется 7 битами (ASCII)

### Поддерживаемые форматы

- **Каналы**: Mono (1) или Stereo (2)
- **Разрядность**: 8 или 16 бит
- **Формат**: WAV (PCM)

### Ограничения

- Максимальный размер сообщения зависит от длительности аудио
- Для 3-минутного трека (~10MB) можно скрыть ~1MB текста

## 🛠 Требования

- Python 3.7+
- Зависимости:
  - `rich` - красивый вывод в терминале
  - `numpy` - числовые операции (опционально)
  - `pytest` - тестирование

## 📝 Лицензия

MIT License - свободное использование и модификация.

## 👨‍💻 Автор

tipichniy340-tech

---

Made with ❤️ using Python
