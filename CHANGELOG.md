# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-05-25

### Added
- 🎉 Initial release of ClipStack-CLI
- 📋 Clipboard monitoring with automatic content capture
- 🏷️ Intelligent content classification (15+ types)
  - URL, Email, Phone, IP Address
  - JSON, XML, HTML
  - Code (Python, JavaScript, Java, C, C++, Go, Rust, SQL, Shell)
  - Markdown, File Path, Command
  - Number, Date, Credit Card, Base64, Hash, UUID
- 🔍 Full-text search functionality
- 🎨 Beautiful TUI dashboard with curses
- 🔐 Local SQLite storage with optional encryption
- ⭐ Favorites and tag management
- 📊 Statistics and analytics
- 📤 Multi-format export (JSON, CSV, Markdown)
- 🖥️ Cross-platform support (Windows, macOS, Linux)
- 📚 Multi-language documentation (简体中文, English, 繁體中文)
- 🧪 Comprehensive test suite
- 📦 Zero external dependencies

### Features
- `clipstack` - Launch TUI dashboard
- `clipstack list` - List recent entries
- `clipstack search` - Search clipboard history
- `clipstack copy` - Copy entry to clipboard
- `clipstack delete` - Delete entry
- `clipstack favorite` - Toggle favorite status
- `clipstack stats` - Show statistics
- `clipstack export` - Export history
- `clipstack import` - Import history
- `clipstack clear` - Clear all history
- `clipstack monitor` - Start clipboard monitoring
- `clipstack add` - Add content manually

### Technical
- Pure Python standard library implementation
- SQLite database for local storage
- curses-based TUI interface
- Multi-backend clipboard support (win32, pbcopy, xclip, xsel, wl-copy)
- Thread-safe database operations
- Type hints throughout codebase

---

## Future Plans

### [1.1.0] - Planned
- Image clipboard support
- Configurable settings
- Custom keyboard shortcuts
- Search history

### [1.2.0] - Planned
- Plugin system
- AI-powered smart tags
- Cloud sync (optional)
- Multi-language UI

---

[1.0.0]: https://github.com/gitstq/ClipStack-CLI/releases/tag/v1.0.0
