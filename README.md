# 🚀 Audio Steganography Tool

Professional audio steganography tool for hiding and extracting secret messages from audio files.

## 🔒 Features

- **LSB Steganography** - Hide messages using Least Significant Bit encoding
- **AES-256 Encryption** - Optional encryption for hidden messages
- **Multi-format Support** - WAV, MP3, FLAC, OGG, M4A, AAC, WMA (requires ffmpeg)
- **Audio Analysis** - Detailed file statistics and capacity estimation
- **Format Conversion** - Convert between audio formats
- **Silence Detection** - Find optimal locations for hiding data
- **Comparison Tools** - Detect modifications in audio files

## 📦 Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install ffmpeg (optional, for format conversion):
```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

## 🚀 Quick Start

### Hide a message in audio
```bash
python main.py encode -i audio.wav -m "Secret message" -o output.wav
```

### Extract a hidden message
```bash
python main.py decode -i output.wav
```

### With encryption
```bash
# Encode with password
python main.py encode -i audio.wav -m "Secret" -o out.wav --encrypt -p mypassword

# Decode with password
python main.py decode -i out.wav --decrypt -p mypassword
```

### Convert audio format
```bash
python main.py convert -i song.mp3 -f wav
python main.py convert -i audio.wav -f mp3 -b 320k
```

### Analyze audio file
```bash
python main.py analyze -i audio.wav
python main.py analyze -i audio.wav --capacity
python main.py analyze -i original.wav --compare modified.wav
```

### Show capabilities
```bash
python main.py info
```

## 📖 CLI Commands

| Command | Description |
|---------|-------------|
| `encode` | Hide a message in an audio file |
| `decode` | Extract a hidden message |
| `convert` | Convert between audio formats |
| `analyze` | Analyze audio properties |
| `info` | Show tool information |

## 🔧 Module Architecture

```
audio_stego/
├── __init__.py          # Package initialization
├── cli.py               # Command-line interface
└── modules/
    ├── core.py          # LSB steganography engine
    ├── converter.py     # Audio format conversion
    ├── encryption.py    # AES encryption module
    └── analyzer.py      # Audio analysis tools
```

## 💡 Usage Examples

### Basic steganography
```python
from audio_stego import AudioStegoCore

stego = AudioStegoCore()
stego.encode('audio.wav', 'Secret message', 'output.wav')
message = stego.decode('output.wav')
print(message)  # "Secret message"
```

### Encrypted steganography
```python
from audio_stego import CryptoModule, EncryptedStegoWrapper, AudioStegoCore

crypto = CryptoModule()
stego = AudioStegoCore()
wrapper = EncryptedStegoWrapper(crypto, stego)

wrapper.encode_encrypted('audio.wav', 'Top secret', 'mypassword', 'encrypted.wav')
message = wrapper.decode_decrypted('encrypted.wav', 'mypassword')
```

### Audio analysis
```python
from audio_stego import AudioAnalyzer

analyzer = AudioAnalyzer()
info = analyzer.get_wave_info('audio.wav')
print(f"Duration: {info['duration_seconds']}s")
print(f"Channels: {info['channels']}")

capacity = analyzer.estimate_capacity('audio.wav')
print(f"Max capacity: {capacity['capacities']['lsb_1bit']['chars']} characters")
```

## ⚙️ Advanced Options

### Encoding options
- `-i, --input` - Input audio file (WAV format recommended)
- `-m, --message` - Message to hide
- `-o, --output` - Output audio file path
- `--encrypt` - Enable AES-256 encryption
- `-p, --password` - Encryption password

### Conversion options
- `-f, --format` - Target format (wav, mp3, flac, ogg, m4a, aac, wma)
- `-b, --bitrate` - Bitrate for lossy formats (default: 192k)

### Analysis options
- `--capacity` - Show steganographic capacity estimates
- `--compare` - Compare with another audio file

## 🔐 Security Notes

- Always use strong passwords for encryption
- LSB steganography is detectable by statistical analysis
- For maximum security, combine encryption with steganography
- Lossy formats (MP3, OGG) may corrupt hidden data

## 📄 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please read CONTRIBUTING.md first.

---

Made with ❤️ by tipichniy340-tech
