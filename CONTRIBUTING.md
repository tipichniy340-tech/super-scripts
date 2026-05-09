# 🤝 Contributing to Super Scripts Collection

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)

---

## 🌟 Code of Conduct

Please be respectful and constructive in your interactions. We welcome contributors of all backgrounds and experience levels.

---

## 🚀 Getting Started

1. **Fork the repository**
2. **Clone your fork**:
   ```bash
   git clone https://github.com/your-username/super-scripts.git
   cd super-scripts
   ```
3. **Create a branch** (see [BRANCH_RULES.md](BRANCH_RULES.md)):
   ```bash
   git checkout -b feature/your-feature-name
   ```

---

## 💻 Development Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies (if any)
pip install pytest pytest-mock
```

### Running Tests
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest test_system_info.py
```

---

## 📝 Pull Request Process

1. **Ensure your code follows the guidelines**:
   - Follow branch naming conventions ([BRANCH_RULES.md](BRANCH_RULES.md))
   - Write clear commit messages (Conventional Commits)
   - Add/update tests for new functionality
   - Update documentation if needed

2. **Before submitting**:
   - [ ] All tests pass (`pytest`)
   - [ ] Code is properly formatted
   - [ ] No sensitive data committed
   - [ ] Documentation is updated

3. **Create Pull Request**:
   - Provide a clear description of changes
   - Reference any related issues
   - Wait for review from maintainers

4. **After approval**:
   - Your PR will be merged by a maintainer
   - The branch will be deleted after merging

---

## 📏 Coding Standards

### Python Style Guide
- Follow [PEP 8](https://pep8.org/) style guidelines
- Use type hints where appropriate
- Keep functions focused and single-purpose
- Maximum line length: 100 characters

### Documentation
- Use docstrings for all public functions and classes
- Follow Google-style docstring format
- Include examples in docstrings when helpful

### Testing
- Write unit tests for all new functionality
- Aim for high test coverage
- Use descriptive test names
- Test edge cases and error conditions

### Commit Messages
Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting, no code change
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Example:**
```
feat(system_info): add network monitoring

Add network interface monitoring capabilities

- Add get_network_info() function
- Display network stats in table
- Support for multiple interfaces

Closes #42
```

---

## 📞 Questions?

Feel free to open an issue for any questions or clarifications.

**Made with ❤️ by tipichniy340-tech**
