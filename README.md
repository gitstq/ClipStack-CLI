<p align="center">
  <a href="README.md">English</a> | 
  <a href="README_CN.md">简体中文</a> | 
  <a href="README_TW.md">繁體中文</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/python-3.8+-green.svg" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-orange.svg" alt="License">
  <img src="https://img.shields.io/badge/platform-cross--platform-lightgrey.svg" alt="Platform">
</p>

<h1 align="center">🦞 ClipStack-CLI</h1>

<p align="center">
  <strong>Lightweight Terminal Clipboard History Intelligent Management Engine</strong><br>
  <sub>轻量级终端剪贴板历史智能管理引擎</sub>
</p>

---

## 🎉 Project Introduction

**ClipStack-CLI** is a powerful terminal-based clipboard history management tool designed for developers and power users. It automatically captures, classifies, and organizes your clipboard content with intelligent detection of sensitive data.

### Why ClipStack-CLI?

- 🔒 **Never lose important clipboard content again** - Everything is automatically saved
- 🧠 **Smart classification** - Code, URLs, emails, and more are automatically categorized
- ⚠️ **Sensitive data protection** - Automatic detection of passwords, API keys, and credentials
- 🎨 **Beautiful TUI dashboard** - Rich terminal interface for easy management
- 📦 **Zero-dependency core** - Minimal dependencies, maximum performance

### Inspiration

Inspired by the need for a simple yet powerful clipboard manager that works entirely in the terminal, respecting developer workflows and privacy.

---

## ✨ Core Features

### 📋 Clipboard Management
- **Real-time monitoring** - Automatically captures clipboard changes
- **Persistent storage** - SQLite database for reliable history
- **Deduplication** - Smart content hashing prevents duplicates
- **Access tracking** - See how often you use each item

### 🧠 Intelligent Classification
- **Content type detection** - Automatically identifies:
  - 💻 Code (Python, JavaScript, Go, Rust, etc.)
  - 🔗 URLs
  - 📧 Email addresses
  - 📁 File paths
  - ⚡ Shell commands
  - 📊 JSON data
  - 🌐 IP addresses

### 🔒 Security Features
- **Sensitive data detection** - Warns about:
  - 🔑 Passwords
  - 🔐 API keys (OpenAI, GitHub, AWS, etc.)
  - 📜 Private keys
  - 💳 Credit card numbers
- **Visual indicators** - Clear marking of sensitive content

### 🎨 Beautiful Interface
- **TUI Dashboard** - Interactive terminal UI with Rich
- **Syntax highlighting** - Code preview with language detection
- **Color-coded categories** - Easy visual identification
- **Keyboard navigation** - Fast and efficient

### 📤 Export Options
- **Multiple formats** - JSON, CSV, Markdown, HTML, Plain text
- **Search & filter** - Find content quickly
- **Batch operations** - Manage multiple entries

---

## 🚀 Quick Start

### Requirements

- Python 3.8 or higher
- Works on Linux, macOS, and Windows

### Installation

```bash
# Install from PyPI
pip install clipstack-cli

# Or install from source
git clone https://github.com/gitstq/ClipStack-CLI.git
cd ClipStack-CLI
pip install -e .
```

### Basic Usage

```bash
# Launch TUI dashboard
clipstack

# List recent entries
clipstack list

# Search clipboard history
clipstack search "python"

# View specific entry
clipstack view 1

# Copy entry to clipboard
clipstack copy 1

# Start monitoring mode
clipstack watch

# Export history
clipstack export --format json --output backup.json

# Show statistics
clipstack stats
```

---

## 📖 Detailed Usage Guide

### TUI Dashboard

Launch the interactive dashboard:

```bash
clipstack
```

**Keyboard shortcuts:**
- `v` - View entry details
- `c` - Copy entry to clipboard
- `d` - Delete entry
- `s` - Search
- `f` - Filter by category
- `e` - Export
- `q` - Quit

### Command Reference

#### List Entries

```bash
# List last 10 entries
clipstack list

# List last 20 entries
clipstack list --limit 20

# Filter by category
clipstack list --category code

# Output as JSON
clipstack list --json
```

#### Search

```bash
# Interactive search
clipstack search

# Direct search
clipstack search "github.com"

# Search with filter
clipstack search "api" --category credential
```

#### Monitor Mode

```bash
# Start monitoring with default settings
clipstack watch

# Custom polling interval (seconds)
clipstack watch --interval 1.0

# Quiet mode (no output)
clipstack watch --quiet
```

#### Export

```bash
# Export to JSON
clipstack export --format json

# Export to CSV
clipstack export --format csv --output history.csv

# Export to Markdown
clipstack export --format markdown

# Export to HTML
clipstack export --format html
```

### Configuration

ClipStack stores data in `~/.clipstack/`:

```
~/.clipstack/
├── history.db      # SQLite database
└── config.json     # Configuration (optional)
```

---

## 💡 Design Philosophy

### Why Terminal-First?

- **Speed** - No GUI overhead, instant response
- **Integration** - Works with your existing terminal workflow
- **Scriptability** - Easy to automate and extend
- **Privacy** - Everything stays local

### Technology Choices

- **Python** - Cross-platform, easy to extend
- **Rich/Textual** - Beautiful terminal UIs without complexity
- **SQLite** - Reliable, fast, zero-config storage
- **Click** - Intuitive CLI framework

### Future Plans

- [ ] Cloud sync support
- [ ] Plugin system
- [ ] Encryption for sensitive data
- [ ] Team sharing features
- [ ] Web UI companion

---

## 📦 Packaging & Deployment

### Build from Source

```bash
# Clone repository
git clone https://github.com/gitstq/ClipStack-CLI.git
cd ClipStack-CLI

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Build package
python -m build
```

### Cross-Platform Notes

- **Linux**: Requires `xclip` or `xsel` for clipboard access
  ```bash
  sudo apt install xclip  # Debian/Ubuntu
  sudo dnf install xclip  # Fedora
  ```

- **macOS**: Works out of the box with `pbcopy`/`bpaste`

- **Windows**: Works with built-in clipboard support

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'feat: add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Write tests for new features
- Update documentation
- Use conventional commits

### Reporting Issues

Found a bug? Have a suggestion?

- Open an [Issue](https://github.com/gitstq/ClipStack-CLI/issues)
- Include your OS, Python version, and steps to reproduce

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/gitstq">gitstq</a>
</p>

<p align="center">
  <sub>⭐ If you find this project useful, please consider giving it a star!</sub>
</p>
