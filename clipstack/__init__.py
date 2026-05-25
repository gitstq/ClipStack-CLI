"""
ClipStack-CLI - Lightweight Terminal Clipboard History Intelligent Manager
轻量级终端剪贴板历史智能管理引擎

A zero-dependency, cross-platform clipboard history manager with intelligent
classification, full-text search, TUI dashboard, and encrypted storage.
"""

__version__ = "1.0.0"
__author__ = "SOLO Agent"
__description__ = "Lightweight Terminal Clipboard History Intelligent Manager"

from .database import ClipboardDatabase
from .classifier import ContentClassifier
from .monitor import ClipboardMonitor
from .tui import ClipboardTUI

__all__ = [
    "ClipboardDatabase",
    "ContentClassifier", 
    "ClipboardMonitor",
    "ClipboardTUI",
]
