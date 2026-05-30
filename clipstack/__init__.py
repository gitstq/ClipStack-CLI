"""
ClipStack-CLI - Lightweight Terminal Clipboard History Intelligent Management Engine
轻量级终端剪贴板历史智能管理引擎

A powerful CLI tool for managing clipboard history with intelligent classification,
sensitive data detection, and beautiful TUI dashboard.

Author: gitstq
License: MIT
"""

__version__ = "1.0.0"
__author__ = "gitstq"
__description__ = "Lightweight Terminal Clipboard History Intelligent Management Engine"

from clipstack.core.storage import ClipboardStorage
from clipstack.core.monitor import ClipboardMonitor
from clipstack.core.classifier import ContentClassifier

__all__ = [
    "ClipboardStorage",
    "ClipboardMonitor", 
    "ContentClassifier",
    "__version__",
    "__author__",
    "__description__",
]
