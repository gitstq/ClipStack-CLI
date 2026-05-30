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
  <strong>轻量级终端剪贴板历史智能管理引擎</strong><br>
  <sub>Lightweight Terminal Clipboard History Intelligent Management Engine</sub>
</p>

---

## 🎉 项目介绍

**ClipStack-CLI** 是一款专为开发者和高级用户设计的强大终端剪贴板历史管理工具。它能够自动捕获、分类和整理您的剪贴板内容，并智能检测敏感数据。

### 为什么选择 ClipStack-CLI？

- 🔒 **再也不会丢失重要的剪贴板内容** - 一切自动保存
- 🧠 **智能分类** - 代码、URL、邮箱等自动归类
- ⚠️ **敏感数据保护** - 自动检测密码、API密钥和凭证
- 🎨 **美观的TUI仪表盘** - 丰富的终端界面，易于管理
- 📦 **零依赖核心** - 最小依赖，最大性能

### 灵感来源

灵感来源于对一款简单而强大的剪贴板管理器的需求，它完全在终端中运行，尊重开发者的工作流程和隐私。

---

## ✨ 核心特性

### 📋 剪贴板管理
- **实时监控** - 自动捕获剪贴板变化
- **持久化存储** - SQLite数据库确保历史可靠
- **去重机制** - 智能内容哈希防止重复
- **访问追踪** - 查看每项内容的使用频率

### 🧠 智能分类
- **内容类型检测** - 自动识别：
  - 💻 代码（Python、JavaScript、Go、Rust等）
  - 🔗 URL链接
  - 📧 邮箱地址
  - 📁 文件路径
  - ⚡ Shell命令
  - 📊 JSON数据
  - 🌐 IP地址

### 🔒 安全特性
- **敏感数据检测** - 警告以下内容：
  - 🔑 密码
  - 🔐 API密钥（OpenAI、GitHub、AWS等）
  - 📜 私钥
  - 💳 信用卡号
- **可视化标记** - 清晰标记敏感内容

### 🎨 美观界面
- **TUI仪表盘** - 基于Rich的交互式终端界面
- **语法高亮** - 代码预览支持语言检测
- **颜色编码分类** - 便于视觉识别
- **键盘导航** - 快速高效

### 📤 导出选项
- **多种格式** - JSON、CSV、Markdown、HTML、纯文本
- **搜索与过滤** - 快速查找内容
- **批量操作** - 管理多条记录

---

## 🚀 快速开始

### 环境要求

- Python 3.8 或更高版本
- 支持 Linux、macOS 和 Windows

### 安装方法

```bash
# 从PyPI安装
pip install clipstack-cli

# 或从源码安装
git clone https://github.com/gitstq/ClipStack-CLI.git
cd ClipStack-CLI
pip install -e .
```

### 基本用法

```bash
# 启动TUI仪表盘
clipstack

# 列出最近记录
clipstack list

# 搜索剪贴板历史
clipstack search "python"

# 查看特定记录
clipstack view 1

# 复制记录到剪贴板
clipstack copy 1

# 启动监控模式
clipstack watch

# 导出历史
clipstack export --format json --output backup.json

# 显示统计信息
clipstack stats
```

---

## 📖 详细使用指南

### TUI仪表盘

启动交互式仪表盘：

```bash
clipstack
```

**键盘快捷键：**
- `v` - 查看记录详情
- `c` - 复制记录到剪贴板
- `d` - 删除记录
- `s` - 搜索
- `f` - 按分类过滤
- `e` - 导出
- `q` - 退出

### 命令参考

#### 列出记录

```bash
# 列出最近10条记录
clipstack list

# 列出最近20条记录
clipstack list --limit 20

# 按分类过滤
clipstack list --category code

# JSON格式输出
clipstack list --json
```

#### 搜索

```bash
# 交互式搜索
clipstack search

# 直接搜索
clipstack search "github.com"

# 带过滤条件搜索
clipstack search "api" --category credential
```

#### 监控模式

```bash
# 使用默认设置启动监控
clipstack watch

# 自定义轮询间隔（秒）
clipstack watch --interval 1.0

# 静默模式（无输出）
clipstack watch --quiet
```

#### 导出

```bash
# 导出为JSON
clipstack export --format json

# 导出为CSV
clipstack export --format csv --output history.csv

# 导出为Markdown
clipstack export --format markdown

# 导出为HTML
clipstack export --format html
```

### 配置

ClipStack 数据存储在 `~/.clipstack/`：

```
~/.clipstack/
├── history.db      # SQLite数据库
└── config.json     # 配置文件（可选）
```

---

## 💡 设计思路

### 为什么选择终端优先？

- **速度** - 无GUI开销，即时响应
- **集成** - 与现有终端工作流程无缝配合
- **可脚本化** - 易于自动化和扩展
- **隐私** - 一切都在本地

### 技术选型

- **Python** - 跨平台，易于扩展
- **Rich/Textual** - 无需复杂即可实现美观的终端界面
- **SQLite** - 可靠、快速、零配置存储
- **Click** - 直观的CLI框架

### 后续规划

- [ ] 云同步支持
- [ ] 插件系统
- [ ] 敏感数据加密
- [ ] 团队共享功能
- [ ] Web UI伴侣

---

## 📦 打包与部署

### 从源码构建

```bash
# 克隆仓库
git clone https://github.com/gitstq/ClipStack-CLI.git
cd ClipStack-CLI

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest tests/

# 构建包
python -m build
```

### 跨平台说明

- **Linux**: 需要安装 `xclip` 或 `xsel`
  ```bash
  sudo apt install xclip  # Debian/Ubuntu
  sudo dnf install xclip  # Fedora
  ```

- **macOS**: 开箱即用，使用 `pbcopy`/`bpaste`

- **Windows**: 使用内置剪贴板支持

---

## 🤝 贡献指南

欢迎贡献！以下是开始方式：

1. **Fork** 本仓库
2. **创建** 功能分支 (`git checkout -b feature/amazing-feature`)
3. **提交** 更改 (`git commit -m 'feat: add amazing feature'`)
4. **推送** 到分支 (`git push origin feature/amazing-feature`)
5. **提交** Pull Request

### 开发规范

- 遵循 PEP 8 代码风格
- 为新功能编写测试
- 更新文档
- 使用约定式提交

### 问题反馈

发现Bug？有建议？

- 提交 [Issue](https://github.com/gitstq/ClipStack-CLI/issues)
- 包含您的操作系统、Python版本和复现步骤

---

## 📄 开源协议

本项目基于 **MIT协议** 开源 - 详见 [LICENSE](LICENSE) 文件。

---

<p align="center">
  由 <a href="https://github.com/gitstq">gitstq</a> 用 ❤️ 制作
</p>

<p align="center">
  <sub>⭐ 如果您觉得这个项目有用，请考虑给它一个星标！</sub>
</p>
