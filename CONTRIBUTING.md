# Contributing to ClipStack-CLI

Thank you for your interest in contributing to ClipStack-CLI! This document provides guidelines and instructions for contributing.

## 🌟 Ways to Contribute

- **Bug Reports**: Submit a detailed bug report
- **Feature Requests**: Suggest new features or improvements
- **Code Contributions**: Submit pull requests
- **Documentation**: Improve or translate documentation
- **Testing**: Help test new releases

## 🐛 Bug Reports

When submitting a bug report, please include:

1. **Description**: Clear description of the bug
2. **Steps to Reproduce**: Detailed steps to reproduce the issue
3. **Expected Behavior**: What you expected to happen
4. **Actual Behavior**: What actually happened
5. **Environment**: OS, Python version, ClipStack-CLI version
6. **Logs/Screenshots**: If applicable

## 💡 Feature Requests

For feature requests, please include:

1. **Problem Statement**: What problem does this solve?
2. **Proposed Solution**: How would you like it to work?
3. **Alternatives**: Any alternative solutions you've considered
4. **Additional Context**: Any other relevant information

## 🔧 Development Setup

### Prerequisites

- Python 3.8+
- Git

### Setup Steps

```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/ClipStack-CLI.git
cd ClipStack-CLI

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or venv\Scripts\activate  # Windows

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
flake8 clipstack tests

# Run type checking
mypy clipstack
```

## 📝 Code Style

We follow these code style guidelines:

- **PEP 8**: Follow Python style guide
- **Black**: Code formatting (line length: 100)
- **isort**: Import sorting
- **Type Hints**: Use type hints for all functions

### Format Code

```bash
# Format with black
black clipstack tests

# Sort imports
isort clipstack tests

# Check with flake8
flake8 clipstack tests
```

## 🧪 Testing

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=clipstack

# Run specific test file
pytest tests/test_classifier.py
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files as `test_*.py`
- Name test functions as `test_*`
- Use descriptive test names

## 📤 Pull Request Process

1. **Create Branch**: Create a feature branch from `main`
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**: Implement your changes

3. **Commit**: Use conventional commit messages
   ```bash
   git commit -m "feat: add new feature"
   ```

4. **Push**: Push to your fork
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Submit PR**: Create a pull request on GitHub

### Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation only
- `refactor:` - Code refactoring
- `test:` - Adding/updating tests
- `chore:` - Build process or auxiliary tool changes

### PR Checklist

- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Documentation updated
- [ ] Commit messages follow convention

## 📋 Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism
- Focus on what's best for the community

## ❓ Questions?

Feel free to open an issue for any questions or discussions.

Thank you for contributing! 🎉
