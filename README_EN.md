<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey" alt="Platform">
  <img src="https://img.shields.io/badge/Dependencies-Zero-orange" alt="Dependencies">
</p>

<p align="center">
  <a href="README.md">简体中文</a> | <a href="README_EN.md">English</a> | <a href="README_TW.md">繁體中文</a>
</p>

<h1 align="center">📋 ClipStack-CLI</h1>

<p align="center">
  <strong>Lightweight Terminal Clipboard History Intelligent Manager</strong>
</p>

<p align="center">
  Zero Dependencies · Cross-Platform · Smart Classification · TUI Dashboard · Local Storage
</p>

---

## 🎉 Introduction

**ClipStack-CLI** is a terminal clipboard history manager designed specifically for developers. It automatically monitors and saves your clipboard content, supporting intelligent classification, full-text search, tag management, and more - so you never have to worry about losing copied content again.

### 🎯 Problems Solved

- 🔥 **Lost Clipboard Content**: Old content gets overwritten when copying new content
- 🔥 **Repeated Copying**: Frequently copying the same content, reducing efficiency
- 🔥 **Content Chaos**: Links, code, and text mixed together, hard to manage
- 🔥 **Privacy Concerns**: Cloud clipboard tools pose data leakage risks

### ✨ Unique Highlights

| Feature | ClipStack-CLI | Other Tools |
|---------|---------------|-------------|
| Zero Dependencies | ✅ Pure Python stdlib | ❌ Multiple dependencies required |
| Smart Classification | ✅ Auto-detect 15+ types | ❌ Manual categorization |
| TUI Dashboard | ✅ Beautiful terminal UI | ❌ Command-line only |
| Privacy First | ✅ Local storage | ❌ Cloud sync |
| Cross-Platform | ✅ Win/Mac/Linux | ⚠️ Partial support |

---

## ✨ Core Features

### 📋 Smart Clipboard Monitoring
- **Auto Capture**: Real-time clipboard monitoring, automatically saves new content
- **Deduplication**: Smart detection of duplicate content, updates access count instead of storing duplicates
- **Silent Operation**: Background running without interrupting normal work

### 🏷️ Intelligent Content Classification
Automatically recognizes **15+ content types**:
- 🔗 URLs
- 📧 Email addresses
- 📞 Phone numbers
- 🌐 IP addresses
- 📊 JSON data
- 📄 XML/HTML
- 💻 Code (Python/JS/Java/Go/Rust, etc.)
- 📝 Markdown
- 📁 File paths
- ⚡ Shell commands
- 🔢 Numbers/Dates
- 💳 Sensitive information (auto-tagged)

### 🔍 Powerful Search
- **Full-text Search**: Quickly search all history
- **Type Filtering**: Filter by content type
- **Tag Search**: Quick location via tags

### 🎨 Beautiful TUI Dashboard
- Intuitive list view
- Detailed entry information
- Keyboard shortcuts
- Colorful highlighting

### 🔐 Privacy & Security
- **Local Storage**: All data saved in local SQLite database
- **Optional Encryption**: Sensitive content can be encrypted
- **No Network Requests**: Completely offline operation

### 📊 Data Management
- **Favorites**: Mark frequently used content
- **Tag Management**: Custom tag categorization
- **Statistics**: View usage frequency and type distribution
- **Multi-format Export**: JSON/CSV/Markdown support

---

## 🚀 Quick Start

### Requirements

- Python 3.8 or higher
- No external dependencies required

### Installation

```bash
# Install from PyPI (Recommended)
pip install clipstack-cli

# Or install from source
git clone https://github.com/gitstq/ClipStack-CLI.git
cd ClipStack-CLI
pip install -e .
```

### Launch TUI Dashboard

```bash
clipstack
```

### Basic Commands

```bash
# List recent 20 entries
clipstack list

# Search entries containing "python"
clipstack search python

# Copy entry by ID to clipboard
clipstack copy 1

# Show statistics
clipstack stats

# Export history
clipstack export json -o history.json

# Start clipboard monitoring
clipstack monitor
```

---

## 📖 Detailed Usage Guide

### TUI Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `↑/↓` | Move up/down |
| `Enter` | View details |
| `s` | Search |
| `f` | Filter by type |
| `Space` | Toggle favorite |
| `c` | Copy to clipboard |
| `d` | Delete entry |
| `e` | Export |
| `h` | Help |
| `q` | Quit |

### Command Line Arguments

#### List Command
```bash
# Show recent 50 entries
clipstack list -n 50

# Show only URLs
clipstack list -t url

# Show only favorites
clipstack list -f
```

#### Search Command
```bash
# Search content
clipstack search "keyword"

# Search and filter by type
clipstack search "api" -t url
```

#### Export Command
```bash
# Export as JSON
clipstack export json -o clipboard.json

# Export as CSV
clipstack export csv -o clipboard.csv

# Export as Markdown
clipstack export markdown -o clipboard.md
```

### Data Storage Location

- **Linux/macOS**: `~/.clipstack/history.db`
- **Windows**: `%USERPROFILE%\.clipstack\history.db`

### Typical Use Cases

1. **Developer Daily Work**
   - Copy code snippets, auto-detect language
   - Copy API URLs, auto-classify
   - Quick search for historical commands

2. **Content Creation**
   - Collect material links
   - Manage reference text
   - Tag-based organization

3. **System Administration**
   - Save common commands
   - Record IP addresses and configurations
   - Quick access to server information

---

## 💡 Design Philosophy & Roadmap

### Design Principles

ClipStack-CLI follows these principles:

1. **Zero Dependencies First**: Use Python standard library, avoid dependency hell
2. **Privacy First**: Local storage, no network requests
3. **Efficiency First**: Keyboard-centric, reduce mouse dependency
4. **Cross-Platform First**: Support mainstream operating systems

### Technology Choices

| Component | Choice | Reason |
|-----------|--------|--------|
| Storage | SQLite | Lightweight, serverless, cross-platform |
| Interface | curses | Standard library, cross-platform terminal |
| Classification | Regex | No dependencies, fast |
| Monitoring | Multi-backend | Compatible with different platforms |

### Future Roadmap

- [ ] Image clipboard support
- [ ] Optional cloud sync
- [ ] Plugin extension support
- [ ] AI-powered smart tags
- [ ] Multi-language interface

---

## 📦 Build & Deployment

### Development Setup

```bash
# Clone repository
git clone https://github.com/gitstq/ClipStack-CLI.git
cd ClipStack-CLI

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or venv\Scripts\activate  # Windows

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Code formatting
black clipstack tests
isort clipstack tests

# Type checking
mypy clipstack
```

### Build Distribution

```bash
# Install build tools
pip install build twine

# Build
python -m build

# Check
twine check dist/*

# Upload to PyPI
twine upload dist/*
```

---

## 🤝 Contributing

Contributions, bug reports, and suggestions are welcome!

### How to Contribute

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'feat: Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Submit a Pull Request

### Commit Convention

Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation update
- `refactor:` Code refactoring
- `test:` Test related
- `chore:` Build/tool related

### Issue Reporting

Please use [GitHub Issues](https://github.com/gitstq/ClipStack-CLI/issues) to report problems.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/gitstq">SOLO Agent</a>
</p>

<p align="center">
  If this project helps you, please give it a ⭐ Star!
</p>
