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
  <strong>輕量級終端剪貼簿歷史智慧管理引擎</strong>
</p>

<p align="center">
  零依賴 · 跨平台 · 智慧分類 · TUI儀表板 · 本地儲存
</p>

---

## 🎉 專案介紹

**ClipStack-CLI** 是一款專為開發者設計的終端剪貼簿歷史管理工具。它能夠自動監控並儲存您的剪貼簿內容，支援智慧分類、全文搜尋、標籤管理等功能，讓您再也不用擔心複製的內容遺失。

### 🎯 解決的痛點

- 🔥 **複製內容遺失**：複製新內容後舊內容被覆蓋，無法找回
- 🔥 **重複複製**：頻繁複製相同內容，效率低下
- 🔥 **內容混亂**：複製的連結、程式碼、文字混在一起，難以管理
- 🔥 **隱私擔憂**：雲端剪貼簿工具存在資料外洩風險

### ✨ 自研差異化亮點

| 特性 | ClipStack-CLI | 其他工具 |
|------|---------------|----------|
| 零依賴 | ✅ 純Python標準庫 | ❌ 需要安裝多個依賴 |
| 智慧分類 | ✅ 自動識別15+種類型 | ❌ 需手動分類 |
| TUI儀表板 | ✅ 美觀的終端介面 | ❌ 只有命令列 |
| 隱私優先 | ✅ 本地儲存 | ❌ 雲端同步 |
| 跨平台 | ✅ Win/Mac/Linux | ⚠️ 部分支援 |

---

## ✨ 核心特性

### 📋 智慧剪貼簿監控
- **自動捕獲**：即時監控剪貼簿變化，自動儲存新內容
- **去重機制**：智慧識別重複內容，更新存取計數而非重複儲存
- **靜默執行**：背景執行不干擾正常工作

### 🏷️ 智慧內容分類
自動識別 **15+ 種內容類型**：
- 🔗 URL連結
- 📧 電子郵件
- 📞 電話號碼
- 🌐 IP位址
- 📊 JSON資料
- 📄 XML/HTML
- 💻 程式碼（支援Python/JS/Java/Go/Rust等）
- 📝 Markdown
- 📁 檔案路徑
- ⚡ Shell命令
- 🔢 數字/日期
- 💳 敏感資訊（自動標記）

### 🔍 強大的搜尋功能
- **全文搜尋**：快速搜尋所有歷史記錄
- **類型過濾**：按內容類型篩選
- **標籤搜尋**：透過標籤快速定位

### 🎨 美觀的TUI儀表板
- 直觀的列表檢視
- 詳細的項目詳情
- 鍵盤快速鍵操作
- 彩色高亮顯示

### 🔐 隱私與安全
- **本地儲存**：所有資料儲存在本地SQLite資料庫
- **可選加密**：敏感內容可加密儲存
- **無網路請求**：完全離線執行

### 📊 資料管理
- **收藏功能**：標記常用內容
- **標籤管理**：自訂標籤分類
- **統計分析**：檢視使用頻率和類型分佈
- **多格式匯出**：支援JSON/CSV/Markdown匯出

---

## 🚀 快速開始

### 環境要求

- Python 3.8 或更高版本
- 無需安裝任何外部依賴

### 安裝

```bash
# 從PyPI安裝（推薦）
pip install clipstack-cli

# 或從原始碼安裝
git clone https://github.com/gitstq/ClipStack-CLI.git
cd ClipStack-CLI
pip install -e .
```

### 啟動TUI儀表板

```bash
clipstack
```

### 基本命令

```bash
# 列出最近20條記錄
clipstack list

# 搜尋包含"python"的記錄
clipstack search python

# 複製指定ID的項目到剪貼簿
clipstack copy 1

# 顯示統計資訊
clipstack stats

# 匯出歷史記錄
clipstack export json -o history.json

# 開始監控剪貼簿
clipstack monitor
```

---

## 📖 詳細使用指南

### TUI快速鍵

| 快速鍵 | 功能 |
|--------|------|
| `↑/↓` | 上下移動 |
| `Enter` | 檢視詳情 |
| `s` | 搜尋 |
| `f` | 過濾類型 |
| `Space` | 收藏/取消收藏 |
| `c` | 複製到剪貼簿 |
| `d` | 刪除項目 |
| `e` | 匯出 |
| `h` | 說明 |
| `q` | 離開 |

### 命令列參數詳解

#### 列表命令
```bash
# 顯示最近50條記錄
clipstack list -n 50

# 只顯示URL類型
clipstack list -t url

# 只顯示收藏
clipstack list -f
```

#### 搜尋命令
```bash
# 搜尋內容
clipstack search "關鍵字"

# 搜尋並過濾類型
clipstack search "api" -t url
```

#### 匯出命令
```bash
# 匯出為JSON
clipstack export json -o clipboard.json

# 匯出為CSV
clipstack export csv -o clipboard.csv

# 匯出為Markdown
clipstack export markdown -o clipboard.md
```

### 資料儲存位置

- **Linux/macOS**: `~/.clipstack/history.db`
- **Windows**: `%USERPROFILE%\.clipstack\history.db`

### 典型使用場景

1. **開發者日常**
   - 複製程式碼片段，自動識別語言
   - 複製API URL，自動分類
   - 快速搜尋歷史命令

2. **內容創作**
   - 收集素材連結
   - 管理引用文字
   - 標籤分類整理

3. **系統管理**
   - 儲存常用命令
   - 記錄IP位址和設定
   - 快速存取伺服器資訊

---

## 💡 設計思路與迭代規劃

### 設計理念

ClipStack-CLI 的設計遵循以下原則：

1. **零依賴優先**：使用Python標準庫，避免依賴地獄
2. **隱私優先**：本地儲存，無網路請求
3. **效率優先**：鍵盤操作為主，減少滑鼠依賴
4. **跨平台優先**：支援主流作業系統

### 技術選型

| 元件 | 技術選擇 | 原因 |
|------|----------|------|
| 儲存 | SQLite | 輕量、無服務、跨平台 |
| 介面 | curses | 標準庫、跨平台終端 |
| 分類 | 正則表達式 | 無依賴、速度快 |
| 監控 | 多後端適配 | 相容不同平台 |

### 後續迭代計劃

- [ ] 支援圖片剪貼簿
- [ ] 新增雲端同步選項（可選）
- [ ] 支援外掛擴展
- [ ] 新增AI智慧標籤
- [ ] 支援多語言介面

---

## 📦 打包與部署指南

### 開發環境設定

```bash
# 複製儲存庫
git clone https://github.com/gitstq/ClipStack-CLI.git
cd ClipStack-CLI

# 建立虛擬環境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows

# 安裝開發依賴
pip install -e ".[dev]"

# 執行測試
pytest

# 程式碼格式化
black clipstack tests
isort clipstack tests

# 類型檢查
mypy clipstack
```

### 建構發布套件

```bash
# 安裝建構工具
pip install build twine

# 建構
python -m build

# 檢查
twine check dist/*

# 上傳到PyPI
twine upload dist/*
```

---

## 🤝 貢獻指南

歡迎貢獻程式碼、報告問題或提出建議！

### 如何貢獻

1. Fork 本儲存庫
2. 建立特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交變更 (`git commit -m 'feat: Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

### 提交規範

使用 [Conventional Commits](https://www.conventionalcommits.org/) 規範：

- `feat:` 新功能
- `fix:` 修復問題
- `docs:` 文檔更新
- `refactor:` 程式碼重構
- `test:` 測試相關
- `chore:` 建構/工具相關

### 問題回報

請使用 [GitHub Issues](https://github.com/gitstq/ClipStack-CLI/issues) 報告問題。

---

## 📄 開源協議

本專案採用 [MIT License](LICENSE) 開源協議。

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/gitstq">SOLO Agent</a>
</p>

<p align="center">
  如果這個專案對你有幫助，請給一個 ⭐ Star 支持一下！
</p>
