# Contributing to AutoDiag Pro

Thank you for considering contributing to AutoDiag Pro! We welcome contributions from the community.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/yourusername/autodiag-pro/issues)
2. If not, create a new issue with:
   - Clear description of the problem
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Your environment (OS, Python version, etc.)

### Suggesting Features

1. Check if the feature has already been suggested
2. Create a new issue with:
   - Clear description of the feature
   - Use case explanation
   - Any relevant examples

### Code Contributions

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Write tests for new functionality
5. Ensure all tests pass
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/autodiag-pro.git
cd autodiag-pro

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
pip install -e .  # Install in development mode
```

## Code Style

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write docstrings for public functions and classes
- Keep functions small and focused

## Testing

Run all tests:
```bash
pytest tests/ -v
```

Run with coverage:
```bash
pytest tests/ --cov=core --cov-report=html
```

## Documentation

- Update README.md if adding new features
- Add docstrings to new functions/classes
- Update comments for complex logic

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
