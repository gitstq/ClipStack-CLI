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
  <strong>轻量级终端剪贴板历史智能管理引擎</strong>
</p>

<p align="center">
  零依赖 · 跨平台 · 智能分类 · TUI仪表板 · 本地存储
</p>

---

## 🎉 项目介绍

**ClipStack-CLI** 是一款专为开发者设计的终端剪贴板历史管理工具。它能够自动监控并保存您的剪贴板内容，支持智能分类、全文搜索、标签管理等功能，让您再也不用担心复制的内容丢失。

### 🎯 解决的痛点

- 🔥 **复制内容丢失**：复制新内容后旧内容被覆盖，无法找回
- 🔥 **重复复制**：频繁复制相同内容，效率低下
- 🔥 **内容混乱**：复制的链接、代码、文本混在一起，难以管理
- 🔥 **隐私担忧**：云端剪贴板工具存在数据泄露风险

### ✨ 自研差异化亮点

| 特性 | ClipStack-CLI | 其他工具 |
|------|---------------|----------|
| 零依赖 | ✅ 纯Python标准库 | ❌ 需要安装多个依赖 |
| 智能分类 | ✅ 自动识别15+种类型 | ❌ 需手动分类 |
| TUI仪表板 | ✅ 美观的终端界面 | ❌ 只有命令行 |
| 隐私优先 | ✅ 本地存储 | ❌ 云端同步 |
| 跨平台 | ✅ Win/Mac/Linux | ⚠️ 部分支持 |

---

## ✨ 核心特性

### 📋 智能剪贴板监控
- **自动捕获**：实时监控剪贴板变化，自动保存新内容
- **去重机制**：智能识别重复内容，更新访问计数而非重复存储
- **静默运行**：后台运行不干扰正常工作

### 🏷️ 智能内容分类
自动识别 **15+ 种内容类型**：
- 🔗 URL链接
- 📧 电子邮件
- 📞 电话号码
- 🌐 IP地址
- 📊 JSON数据
- 📄 XML/HTML
- 💻 代码（支持Python/JS/Java/Go/Rust等）
- 📝 Markdown
- 📁 文件路径
- ⚡ Shell命令
- 🔢 数字/日期
- 💳 敏感信息（自动标记）

### 🔍 强大的搜索功能
- **全文搜索**：快速搜索所有历史记录
- **类型过滤**：按内容类型筛选
- **标签搜索**：通过标签快速定位

### 🎨 美观的TUI仪表板
- 直观的列表视图
- 详细的条目详情
- 键盘快捷键操作
- 彩色高亮显示

### 🔐 隐私与安全
- **本地存储**：所有数据保存在本地SQLite数据库
- **可选加密**：敏感内容可加密存储
- **无网络请求**：完全离线运行

### 📊 数据管理
- **收藏功能**：标记常用内容
- **标签管理**：自定义标签分类
- **统计分析**：查看使用频率和类型分布
- **多格式导出**：支持JSON/CSV/Markdown导出

---

## 🚀 快速开始

### 环境要求

- Python 3.8 或更高版本
- 无需安装任何外部依赖

### 安装

```bash
# 从PyPI安装（推荐）
pip install clipstack-cli

# 或从源码安装
git clone https://github.com/gitstq/ClipStack-CLI.git
cd ClipStack-CLI
pip install -e .
```

### 启动TUI仪表板

```bash
clipstack
```

### 基本命令

```bash
# 列出最近20条记录
clipstack list

# 搜索包含"python"的记录
clipstack search python

# 复制指定ID的条目到剪贴板
clipstack copy 1

# 显示统计信息
clipstack stats

# 导出历史记录
clipstack export json -o history.json

# 开始监控剪贴板
clipstack monitor
```

---

## 📖 详细使用指南

### TUI快捷键

| 快捷键 | 功能 |
|--------|------|
| `↑/↓` | 上下移动 |
| `Enter` | 查看详情 |
| `s` | 搜索 |
| `f` | 过滤类型 |
| `Space` | 收藏/取消收藏 |
| `c` | 复制到剪贴板 |
| `d` | 删除条目 |
| `e` | 导出 |
| `h` | 帮助 |
| `q` | 退出 |

### 命令行参数详解

#### 列表命令
```bash
# 显示最近50条记录
clipstack list -n 50

# 只显示URL类型
clipstack list -t url

# 只显示收藏
clipstack list -f
```

#### 搜索命令
```bash
# 搜索内容
clipstack search "关键词"

# 搜索并过滤类型
clipstack search "api" -t url
```

#### 导出命令
```bash
# 导出为JSON
clipstack export json -o clipboard.json

# 导出为CSV
clipstack export csv -o clipboard.csv

# 导出为Markdown
clipstack export markdown -o clipboard.md
```

### 数据存储位置

- **Linux/macOS**: `~/.clipstack/history.db`
- **Windows**: `%USERPROFILE%\.clipstack\history.db`

### 典型使用场景

1. **开发者日常**
   - 复制代码片段，自动识别语言
   - 复制API URL，自动分类
   - 快速搜索历史命令

2. **内容创作**
   - 收集素材链接
   - 管理引用文本
   - 标签分类整理

3. **系统管理**
   - 保存常用命令
   - 记录IP地址和配置
   - 快速访问服务器信息

---

## 💡 设计思路与迭代规划

### 设计理念

ClipStack-CLI 的设计遵循以下原则：

1. **零依赖优先**：使用Python标准库，避免依赖地狱
2. **隐私优先**：本地存储，无网络请求
3. **效率优先**：键盘操作为主，减少鼠标依赖
4. **跨平台优先**：支持主流操作系统

### 技术选型

| 组件 | 技术选择 | 原因 |
|------|----------|------|
| 存储 | SQLite | 轻量、无服务、跨平台 |
| 界面 | curses | 标准库、跨平台终端 |
| 分类 | 正则表达式 | 无依赖、速度快 |
| 监控 | 多后端适配 | 兼容不同平台 |

### 后续迭代计划

- [ ] 支持图片剪贴板
- [ ] 添加云同步选项（可选）
- [ ] 支持插件扩展
- [ ] 添加AI智能标签
- [ ] 支持多语言界面

---

## 📦 打包与部署指南

### 开发环境设置

```bash
# 克隆仓库
git clone https://github.com/gitstq/ClipStack-CLI.git
cd ClipStack-CLI

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 代码格式化
black clipstack tests
isort clipstack tests

# 类型检查
mypy clipstack
```

### 构建发布包

```bash
# 安装构建工具
pip install build twine

# 构建
python -m build

# 检查
twine check dist/*

# 上传到PyPI
twine upload dist/*
```

---

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出建议！

### 如何贡献

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

### 提交规范

使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

- `feat:` 新功能
- `fix:` 修复问题
- `docs:` 文档更新
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建/工具相关

### 问题反馈

请使用 [GitHub Issues](https://github.com/gitstq/ClipStack-CLI/issues) 报告问题。

---

## 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/gitstq">SOLO Agent</a>
</p>

<p align="center">
  如果这个项目对你有帮助，请给一个 ⭐ Star 支持一下！
</p>
