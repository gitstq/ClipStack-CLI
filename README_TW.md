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
  <strong>輕量級終端剪貼簿歷史智慧管理引擎</strong><br>
  <sub>Lightweight Terminal Clipboard History Intelligent Management Engine</sub>
</p>

---

## 🎉 專案介紹

**ClipStack-CLI** 是一款專為開發者和進階使用者設計的強大終端剪貼簿歷史管理工具。它能夠自動擷取、分類和整理您的剪貼簿內容，並智慧偵測敏感資料。

### 為什麼選擇 ClipStack-CLI？

- 🔒 **再也不會遺失重要的剪貼簿內容** - 一切自動儲存
- 🧠 **智慧分類** - 程式碼、URL、電子郵件等自動歸類
- ⚠️ **敏感資料保護** - 自動偵測密碼、API金鑰和憑證
- 🎨 **美觀的TUI儀表板** - 豐富的終端介面，易於管理
- 📦 **零依賴核心** - 最小依賴，最大效能

### 靈感來源

靈感來自於對一款簡單而強大的剪貼簿管理器的需求，它完全在終端中執行，尊重開發者的工作流程和隱私。

---

## ✨ 核心特性

### 📋 剪貼簿管理
- **即時監控** - 自動擷取剪貼簿變更
- **持久化儲存** - SQLite資料庫確保歷史可靠
- **去重機制** - 智慧內容雜湊防止重複
- **存取追蹤** - 查看每項內容的使用頻率

### 🧠 智慧分類
- **內容類型偵測** - 自動識別：
  - 💻 程式碼（Python、JavaScript、Go、Rust等）
  - 🔗 URL連結
  - 📧 電子郵件地址
  - 📁 檔案路徑
  - ⚡ Shell命令
  - 📊 JSON資料
  - 🌐 IP位址

### 🔒 安全特性
- **敏感資料偵測** - 警告以下內容：
  - 🔑 密碼
  - 🔐 API金鑰（OpenAI、GitHub、AWS等）
  - 📜 私鑰
  - 💳 信用卡號
- **視覺化標記** - 清晰標記敏感內容

### 🎨 美觀介面
- **TUI儀表板** - 基於Rich的互動式終端介面
- **語法高亮** - 程式碼預覽支援語言偵測
- **顏色編碼分類** - 便於視覺識別
- **鍵盤導航** - 快速高效

### 📤 匯出選項
- **多種格式** - JSON、CSV、Markdown、HTML、純文字
- **搜尋與過濾** - 快速尋找內容
- **批次操作** - 管理多筆記錄

---

## 🚀 快速開始

### 環境需求

- Python 3.8 或更高版本
- 支援 Linux、macOS 和 Windows

### 安裝方法

```bash
# 從PyPI安裝
pip install clipstack-cli

# 或從原始碼安裝
git clone https://github.com/gitstq/ClipStack-CLI.git
cd ClipStack-CLI
pip install -e .
```

### 基本用法

```bash
# 啟動TUI儀表板
clipstack

# 列出最近記錄
clipstack list

# 搜尋剪貼簿歷史
clipstack search "python"

# 查看特定記錄
clipstack view 1

# 複製記錄到剪貼簿
clipstack copy 1

# 啟動監控模式
clipstack watch

# 匯出歷史
clipstack export --format json --output backup.json

# 顯示統計資訊
clipstack stats
```

---

## 📖 詳細使用指南

### TUI儀表板

啟動互動式儀表板：

```bash
clipstack
```

**鍵盤快速鍵：**
- `v` - 查看記錄詳情
- `c` - 複製記錄到剪貼簿
- `d` - 刪除記錄
- `s` - 搜尋
- `f` - 按分類過濾
- `e` - 匯出
- `q` - 離開

### 命令參考

#### 列出記錄

```bash
# 列出最近10筆記錄
clipstack list

# 列出最近20筆記錄
clipstack list --limit 20

# 按分類過濾
clipstack list --category code

# JSON格式輸出
clipstack list --json
```

#### 搜尋

```bash
# 互動式搜尋
clipstack search

# 直接搜尋
clipstack search "github.com"

# 帶過濾條件搜尋
clipstack search "api" --category credential
```

#### 監控模式

```bash
# 使用預設設定啟動監控
clipstack watch

# 自訂輪詢間隔（秒）
clipstack watch --interval 1.0

# 靜默模式（無輸出）
clipstack watch --quiet
```

#### 匯出

```bash
# 匯出為JSON
clipstack export --format json

# 匯出為CSV
clipstack export --format csv --output history.csv

# 匯出為Markdown
clipstack export --format markdown

# 匯出為HTML
clipstack export --format html
```

### 設定

ClipStack 資料儲存在 `~/.clipstack/`：

```
~/.clipstack/
├── history.db      # SQLite資料庫
└── config.json     # 設定檔（可選）
```

---

## 💡 設計思路

### 為什麼選擇終端優先？

- **速度** - 無GUI開銷，即時回應
- **整合** - 與現有終端工作流程無縫配合
- **可腳本化** - 易於自動化和擴充
- **隱私** - 一切都在本機

### 技術選型

- **Python** - 跨平台，易於擴充
- **Rich/Textual** - 無需複雜即可實現美觀的終端介面
- **SQLite** - 可靠、快速、零設定儲存
- **Click** - 直觀的CLI框架

### 後續規劃

- [ ] 雲端同步支援
- [ ] 外掛系統
- [ ] 敏感資料加密
- [ ] 團隊共享功能
- [ ] Web UI伴侶

---

## 📦 打包與部署

### 從原始碼建置

```bash
# 複製儲存庫
git clone https://github.com/gitstq/ClipStack-CLI.git
cd ClipStack-CLI

# 安裝開發相依性
pip install -e ".[dev]"

# 執行測試
pytest tests/

# 建置套件
python -m build
```

### 跨平台說明

- **Linux**: 需要安裝 `xclip` 或 `xsel`
  ```bash
  sudo apt install xclip  # Debian/Ubuntu
  sudo dnf install xclip  # Fedora
  ```

- **macOS**: 開箱即用，使用 `pbcopy`/`bpaste`

- **Windows**: 使用內建剪貼簿支援

---

## 🤝 貢獻指南

歡迎貢獻！以下是開始方式：

1. **Fork** 本儲存庫
2. **建立** 功能分支 (`git checkout -b feature/amazing-feature`)
3. **提交** 變更 (`git commit -m 'feat: add amazing feature'`)
4. **推送** 到分支 (`git push origin feature/amazing-feature`)
5. **提交** Pull Request

### 開發規範

- 遵循 PEP 8 程式碼風格
- 為新功能撰寫測試
- 更新文件
- 使用約定式提交

### 問題回報

發現Bug？有建議？

- 提交 [Issue](https://github.com/gitstq/ClipStack-CLI/issues)
- 包含您的作業系統、Python版本和重現步驟

---

## 📄 開源授權

本專案基於 **MIT授權條款** 開源 - 詳見 [LICENSE](LICENSE) 檔案。

---

<p align="center">
  由 <a href="https://github.com/gitstq">gitstq</a> 用 ❤️ 製作
</p>

<p align="center">
  <sub>⭐ 如果您覺得這個專案有用，請考慮給它一個星標！</sub>
</p>
