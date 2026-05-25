"""
Clipboard Monitor Module - Cross-platform clipboard monitoring
"""

import threading
import time
import platform
import subprocess
from typing import Optional, Callable, Dict, Any
from datetime import datetime

from .database import ClipboardDatabase
from .classifier import ContentClassifier


class ClipboardMonitor:
    """Cross-platform clipboard monitor with intelligent classification."""
    
    def __init__(
        self,
        db: Optional[ClipboardDatabase] = None,
        on_new_content: Optional[Callable[[Dict[str, Any]], None]] = None,
        poll_interval: float = 0.5
    ):
        """Initialize the clipboard monitor.
        
        Args:
            db: ClipboardDatabase instance
            on_new_content: Callback for new content
            poll_interval: Polling interval in seconds
        """
        self.db = db or ClipboardDatabase()
        self.classifier = ContentClassifier()
        self.on_new_content = on_new_content
        self.poll_interval = poll_interval
        
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._last_content: Optional[str] = None
        self._lock = threading.Lock()
        
        # Detect platform
        self.platform = platform.system().lower()
        self._setup_clipboard_backend()
    
    def _setup_clipboard_backend(self) -> None:
        """Setup the appropriate clipboard backend for the platform."""
        self.backend = self._detect_backend()
    
    def _detect_backend(self) -> str:
        """Detect available clipboard backend."""
        if self.platform == 'windows':
            return 'win32'
        elif self.platform == 'darwin':
            # Check for pbcopy
            try:
                subprocess.run(['pbcopy', '-help'], capture_output=True)
                return 'pbcopy'
            except (subprocess.SubprocessError, FileNotFoundError):
                pass
        elif self.platform == 'linux':
            # Check for xclip, xsel, or wl-copy
            for cmd in ['xclip', 'xsel', 'wl-copy']:
                try:
                    subprocess.run([cmd, '-version'], capture_output=True)
                    return cmd
                except (subprocess.SubprocessError, FileNotFoundError):
                    continue
        
        return 'fallback'
    
    def get_clipboard_content(self) -> Optional[str]:
        """Get current clipboard content."""
        try:
            if self.backend == 'win32':
                return self._get_win32_clipboard()
            elif self.backend == 'pbcopy':
                return self._get_macos_clipboard()
            elif self.backend in ['xclip', 'xsel', 'wl-copy']:
                return self._get_linux_clipboard()
            else:
                return self._get_fallback_clipboard()
        except Exception as e:
            return None
    
    def _get_win32_clipboard(self) -> Optional[str]:
        """Get clipboard content on Windows."""
        try:
            import ctypes
            from ctypes import wintypes
            
            CF_UNICODETEXT = 13
            
            user32 = ctypes.windll.user32
            kernel32 = ctypes.windll.kernel32
            
            user32.OpenClipboard(0)
            try:
                if user32.IsClipboardFormatAvailable(CF_UNICODETEXT):
                    data = user32.GetClipboardData(CF_UNICODETEXT)
                    data_locked = kernel32.GlobalLock(data)
                    text = ctypes.wstring_at(data_locked)
                    kernel32.GlobalUnlock(data)
                    return text
            finally:
                user32.CloseClipboard()
        except Exception:
            pass
        
        return None
    
    def _get_macos_clipboard(self) -> Optional[str]:
        """Get clipboard content on macOS."""
        try:
            result = subprocess.run(
                ['pbpaste'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return result.stdout
        except Exception:
            pass
        
        return None
    
    def _get_linux_clipboard(self) -> Optional[str]:
        """Get clipboard content on Linux."""
        try:
            if self.backend == 'xclip':
                result = subprocess.run(
                    ['xclip', '-selection', 'clipboard', '-o'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
            elif self.backend == 'xsel':
                result = subprocess.run(
                    ['xsel', '--clipboard', '--output'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
            elif self.backend == 'wl-copy':
                result = subprocess.run(
                    ['wl-paste'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
            else:
                return None
            
            if result.returncode == 0:
                return result.stdout
        except Exception:
            pass
        
        return None
    
    def _get_fallback_clipboard(self) -> Optional[str]:
        """Fallback method to get clipboard content."""
        # Try pyperclip if available
        try:
            import pyperclip
            return pyperclip.paste()
        except ImportError:
            pass
        
        return None
    
    def set_clipboard_content(self, content: str) -> bool:
        """Set clipboard content."""
        try:
            if self.backend == 'win32':
                return self._set_win32_clipboard(content)
            elif self.backend == 'pbcopy':
                return self._set_macos_clipboard(content)
            elif self.backend in ['xclip', 'xsel', 'wl-copy']:
                return self._set_linux_clipboard(content)
            else:
                return self._set_fallback_clipboard(content)
        except Exception:
            return False
    
    def _set_win32_clipboard(self, content: str) -> bool:
        """Set clipboard content on Windows."""
        try:
            import ctypes
            
            CF_UNICODETEXT = 13
            GMEM_MOVEABLE = 0x0002
            
            user32 = ctypes.windll.user32
            kernel32 = ctypes.windll.kernel32
            
            user32.OpenClipboard(0)
            try:
                user32.EmptyClipboard()
                
                # Allocate memory
                text = content.encode('utf-16-le') + b'\x00\x00'
                size = len(text)
                
                h_mem = kernel32.GlobalAlloc(GMEM_MOVEABLE, size)
                p_mem = kernel32.GlobalLock(h_mem)
                
                ctypes.memmove(p_mem, text, size)
                kernel32.GlobalUnlock(h_mem)
                
                user32.SetClipboardData(CF_UNICODETEXT, h_mem)
                return True
            finally:
                user32.CloseClipboard()
        except Exception:
            pass
        
        return False
    
    def _set_macos_clipboard(self, content: str) -> bool:
        """Set clipboard content on macOS."""
        try:
            subprocess.run(
                ['pbcopy'],
                input=content,
                capture_output=True,
                text=True,
                timeout=5
            )
            return True
        except Exception:
            pass
        
        return False
    
    def _set_linux_clipboard(self, content: str) -> bool:
        """Set clipboard content on Linux."""
        try:
            if self.backend == 'xclip':
                subprocess.run(
                    ['xclip', '-selection', 'clipboard'],
                    input=content,
                    capture_output=True,
                    text=True,
                    timeout=5
                )
            elif self.backend == 'xsel':
                subprocess.run(
                    ['xsel', '--clipboard', '--input'],
                    input=content,
                    capture_output=True,
                    text=True,
                    timeout=5
                )
            elif self.backend == 'wl-copy':
                subprocess.run(
                    ['wl-copy'],
                    input=content,
                    capture_output=True,
                    text=True,
                    timeout=5
                )
            return True
        except Exception:
            pass
        
        return False
    
    def _set_fallback_clipboard(self, content: str) -> bool:
        """Fallback method to set clipboard content."""
        try:
            import pyperclip
            pyperclip.copy(content)
            return True
        except ImportError:
            pass
        
        return False
    
    def _monitor_loop(self) -> None:
        """Main monitoring loop."""
        while self._running:
            try:
                content = self.get_clipboard_content()
                
                if content and content != self._last_content:
                    with self._lock:
                        self._last_content = content
                    
                    # Classify content
                    content_type, category, tags = self.classifier.classify(content)
                    
                    # Add to database
                    entry_id = self.db.add_entry(
                        content=content,
                        content_type=content_type,
                        category=category,
                        tags=tags
                    )
                    
                    # Callback
                    if entry_id and self.on_new_content:
                        entry = {
                            'id': entry_id,
                            'content': content,
                            'content_type': content_type,
                            'category': category,
                            'tags': tags,
                            'timestamp': datetime.now().isoformat()
                        }
                        try:
                            self.on_new_content(entry)
                        except Exception:
                            pass
                
                time.sleep(self.poll_interval)
                
            except Exception:
                time.sleep(self.poll_interval)
    
    def start(self) -> None:
        """Start monitoring clipboard."""
        if self._running:
            return
        
        self._running = True
        self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._thread.start()
    
    def stop(self) -> None:
        """Stop monitoring clipboard."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=2)
            self._thread = None
    
    def is_running(self) -> bool:
        """Check if monitor is running."""
        return self._running
    
    def get_status(self) -> Dict[str, Any]:
        """Get monitor status."""
        return {
            'running': self._running,
            'platform': self.platform,
            'backend': self.backend,
            'poll_interval': self.poll_interval,
            'last_content_length': len(self._last_content) if self._last_content else 0
        }
