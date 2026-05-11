# AutoDiag Pro

**Professional Automotive Diagnostic Tool for Windows 7/8/10/11**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/autodiag-pro/autodiag-pro/actions/workflows/tests.yml/badge.svg)](https://github.com/autodiag-pro/autodiag-pro/actions)

## 🚗 Features

AutoDiag Pro is a comprehensive automotive diagnostic tool supporting OBD/ELM interfaces for multiple vehicle manufacturers.

### Supported Manufacturers
- **Japanese**: Toyota, Lexus, Nissan, Mazda, Honda
- **Russian**: GAZ (ГАЗ), Lada (Лада)

### Vehicle Types
- Passenger cars (легковые автомобили)
- Trucks (грузовые автомобили)

### Core Features

#### 🔍 Basic Diagnostics
- Read Diagnostic Trouble Codes (DTC)
- Clear DTCs
- View freeze frame data
- Real-time data monitoring

#### 📊 Live Data Monitoring
- Engine RPM
- Vehicle speed
- Coolant temperature
- Throttle position
- Battery voltage
- And more...

#### 🔧 Advanced Tests
- Actuator tests (fuel pump, cooling fan, EGR valve, etc.)
- Module encoding (ECM, TCM, BCM, ABS, SRS)
- ECU flashing/reflashing

#### 🌐 Bilingual Interface
- English (EN)
- Russian (RU)

## 🖥️ Interfaces

### CLI (Command Line Interface)
Modern terminal interface with rich formatting using the `rich` library.

```bash
python -m autodiag_pro.cli
```

### GUI (Graphical User Interface)
Full-featured graphical interface using `tkinter`.

```bash
python -m autodiag_pro.gui
```

## 📋 Requirements

- **OS**: Windows 7/8/10/11
- **Python**: 3.8 or higher
- **Dependencies**: See `requirements.txt`

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/autodiag-pro.git
cd autodiag-pro
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## 💻 Usage

### Running CLI
```bash
# Start CLI interface
python -m autodiag_pro.cli

# Or directly
python main.py --cli
```

### Running GUI
```bash
# Start GUI interface
python -m autodiag_pro.gui

# Or directly
python main.py --gui
```

### Using as a Library
```python
from core.diagnostic import DiagnosticSession, Language

# Create session
session = DiagnosticSession(language=Language.EN)

# Connect to vehicle
session.connect("COM3", "AUTO")

# Read DTCs
dtcs = session.read_dtcs()
for dtc in dtcs:
    print(f"{dtc.code}: {dtc.description}")

# Read live data
data = session.read_live_data()
for param in data:
    print(f"{param.name}: {param.value} {param.unit}")

# Disconnect
session.disconnect()
```

## 🏗️ Project Structure

```
autodiag_pro/
├── core/
│   ├── __init__.py
│   └── diagnostic.py      # Core diagnostic logic
├── interfaces/
│   ├── __init__.py
│   ├── cli.py             # Command-line interface
│   └── gui.py             # Graphical interface
├── protocols/
│   └── __init__.py        # OBD protocols (future)
├── utils/
│   └── __init__.py        # Utility functions
├── tests/
│   ├── __init__.py
│   └── test_diagnostic.py # Unit tests
├── docs/                  # Documentation
├── assets/                # Icons and resources
├── main.py                # Main entry point
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── LICENSE                # MIT License
└── setup.py               # Package installation
```

## 🧪 Testing

Run all tests:
```bash
pytest tests/ -v
```

Run with coverage:
```bash
pytest tests/ --cov=core --cov-report=html
```

## 🔒 Safety Warning

⚠️ **IMPORTANT**: 
- ECU flashing can potentially brick your vehicle's computer
- Always ensure stable power supply during flashing operations
- Use at your own risk
- The authors are not responsible for any damage caused by this software

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [python-OBD](https://github.com/brendan-w/python-obd) - OBD-II protocol implementation
- [rich](https://github.com/willmcgugan/rich) - Beautiful terminal output
- [tkinter](https://docs.python.org/3/library/tkinter.html) - Python GUI toolkit

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/autodiag-pro/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/autodiag-pro/discussions)
- **Email**: support@autodiag-pro.com

## 🗺️ Roadmap

- [ ] Real OBD hardware integration (currently simulated)
- [ ] Support for additional manufacturers (BMW, Mercedes, VAG)
- [ ] Custom PID creation
- [ ] Report generation (PDF, HTML)
- [ ] Database of DTCs with solutions
- [ ] Remote diagnostics capability
- [ ] Mobile app version

---

**Made with ❤️ for the automotive community**

© 2024 AutoDiag Pro Team
