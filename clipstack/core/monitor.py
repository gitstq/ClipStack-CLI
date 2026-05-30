"""
Clipboard Monitor Module - Real-time clipboard monitoring with cross-platform support.
剪贴板监控模块 - 实时剪贴板监控，支持跨平台。
"""

import threading
import time
from typing import Callable, Optional

from clipstack.core.classifier import ContentClassifier, ContentType
from clipstack.core.storage import ClipboardStorage


class ClipboardMonitor:
    """
    Real-time clipboard monitor with intelligent content processing.
    
    Features:
    - Cross-platform clipboard monitoring
    - Automatic content classification
    - Sensitive data detection
    - Configurable polling interval
    """
    
    def __init__(
        self,
        storage: Optional[ClipboardStorage] = None,
        classifier: Optional[ContentClassifier] = None,
        poll_interval: float = 0.5,
        on_new_content: Optional[Callable] = None
    ):
        """
        Initialize clipboard monitor.
        
        Args:
            storage: ClipboardStorage instance
            classifier: ContentClassifier instance
            poll_interval: Polling interval in seconds
            on_new_content: Callback for new content (content, classification)
        """
        self.storage = storage or ClipboardStorage()
        self.classifier = classifier or ContentClassifier()
        self.poll_interval = poll_interval
        self.on_new_content = on_new_content
        
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._last_content: str = ""
        self._clipboard = None
    
    def _init_clipboard(self):
        """Initialize clipboard library."""
        try:
            import pyperclip
            self._clipboard = pyperclip
        except ImportError:
            raise ImportError(
                "pyperclip is required for clipboard monitoring. "
                "Install it with: pip install pyperclip"
            )
    
    def start(self) -> None:
        """Start clipboard monitoring."""
        if self._running:
            return
        
        self._init_clipboard()
        self._running = True
        self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._thread.start()
    
    def stop(self) -> None:
        """Stop clipboard monitoring."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=2.0)
            self._thread = None
    
    def _monitor_loop(self) -> None:
        """Main monitoring loop."""
        while self._running:
            try:
                content = self._get_clipboard_content()
                
                if content and content != self._last_content:
                    self._process_content(content)
                    self._last_content = content
                
            except Exception as e:
                # Log error but continue monitoring
                pass
            
            time.sleep(self.poll_interval)
    
    def _get_clipboard_content(self) -> Optional[str]:
        """
        Get current clipboard content.
        
        Returns:
            Clipboard content or None
        """
        try:
            if self._clipboard:
                return self._clipboard.paste()
        except Exception:
            pass
        return None
    
    def _process_content(self, content: str) -> None:
        """
        Process new clipboard content.
        
        Args:
            content: New clipboard content
        """
        # Classify content
        result = self.classifier.classify(content)
        
        # Get category
        category = self.classifier.get_category_for_type(result.content_type)
        
        # Store entry
        self.storage.add_entry(
            content=content,
            category=category,
            tags=result.tags,
            is_sensitive=result.is_sensitive
        )
        
        # Call callback if provided
        if self.on_new_content:
            self.on_new_content(content, result)
    
    def copy_to_clipboard(self, content: str) -> bool:
        """
        Copy content to clipboard.
        
        Args:
            content: Content to copy
            
        Returns:
            True if successful
        """
        try:
            if not self._clipboard:
                self._init_clipboard()
            
            self._clipboard.copy(content)
            self._last_content = content
            return True
        except Exception:
            return False
    
    def get_recent(self, limit: int = 10) -> list:
        """
        Get recent clipboard entries.
        
        Args:
            limit: Maximum entries to return
            
        Returns:
            List of recent entries
        """
        return self.storage.get_all_entries(limit=limit)
    
    def search(self, query: str, limit: int = 20) -> list:
        """
        Search clipboard history.
        
        Args:
            query: Search query
            limit: Maximum results
            
        Returns:
            List of matching entries
        """
        return self.storage.get_all_entries(limit=limit, search=query)
    
    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()
        return False


def watch_clipboard(
    on_new_content: Optional[Callable] = None,
    poll_interval: float = 0.5
) -> ClipboardMonitor:
    """
    Convenience function to create and start a clipboard monitor.
    
    Args:
        on_new_content: Callback for new content
        poll_interval: Polling interval in seconds
        
    Returns:
        ClipboardMonitor instance
    """
    monitor = ClipboardMonitor(
        poll_interval=poll_interval,
        on_new_content=on_new_content
    )
    monitor.start()
    return monitor
