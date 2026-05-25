"""
TUI Module - Terminal User Interface for ClipStack
"""

import curses
import curses.panel
from curses import wrapper
from typing import Optional, List, Dict, Any, Callable
from datetime import datetime
import threading
import time

from .database import ClipboardDatabase
from .classifier import ContentClassifier
from .monitor import ClipboardMonitor


class ClipboardTUI:
    """Terminal User Interface for ClipStack."""
    
    # Color pairs
    COLOR_HEADER = 1
    COLOR_FOOTER = 2
    COLOR_SELECTED = 3
    COLOR_TYPE_URL = 4
    COLOR_TYPE_EMAIL = 5
    COLOR_TYPE_CODE = 6
    COLOR_TYPE_JSON = 7
    COLOR_TYPE_TEXT = 8
    COLOR_FAVORITE = 9
    COLOR_HELP = 10
    
    def __init__(self, db: Optional[ClipboardDatabase] = None):
        """Initialize TUI.
        
        Args:
            db: ClipboardDatabase instance
        """
        self.db = db or ClipboardDatabase()
        self.classifier = ContentClassifier()
        self.monitor: Optional[ClipboardMonitor] = None
        
        # State
        self.entries: List[Dict[str, Any]] = []
        self.selected_index = 0
        self.offset = 0
        self.mode = 'list'  # list, search, detail, help
        self.search_query = ""
        self.filter_type = None
        self.message = ""
        self.message_time = 0
        self.running = True
        
        # UI dimensions
        self.height = 0
        self.width = 0
        self.content_height = 0
    
    def _init_colors(self) -> None:
        """Initialize color pairs."""
        curses.start_color()
        curses.use_default_colors()
        
        # Define color pairs
        curses.init_pair(self.COLOR_HEADER, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(self.COLOR_FOOTER, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(self.COLOR_SELECTED, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(self.COLOR_TYPE_URL, curses.COLOR_CYAN, -1)
        curses.init_pair(self.COLOR_TYPE_EMAIL, curses.COLOR_YELLOW, -1)
        curses.init_pair(self.COLOR_TYPE_CODE, curses.COLOR_GREEN, -1)
        curses.init_pair(self.COLOR_TYPE_JSON, curses.COLOR_MAGENTA, -1)
        curses.init_pair(self.COLOR_TYPE_TEXT, curses.COLOR_WHITE, -1)
        curses.init_pair(self.COLOR_FAVORITE, curses.COLOR_RED, -1)
        curses.init_pair(self.COLOR_HELP, curses.COLOR_CYAN, -1)
    
    def _get_type_color(self, content_type: str) -> int:
        """Get color pair for content type."""
        colors = {
            'url': self.COLOR_TYPE_URL,
            'email': self.COLOR_TYPE_EMAIL,
            'code': self.COLOR_TYPE_CODE,
            'json': self.COLOR_TYPE_JSON,
        }
        return colors.get(content_type, self.COLOR_TYPE_TEXT)
    
    def _draw_header(self, stdscr) -> None:
        """Draw the header."""
        header = f"  📋 ClipStack-CLI v1.0.0  │  Mode: {self.mode.upper()}  │  Entries: {len(self.entries)}  "
        if self.filter_type:
            header += f"│  Filter: {self.filter_type}  "
        if self.search_query:
            header += f"│  Search: {self.search_query}  "
        
        header = header.ljust(self.width)
        stdscr.addstr(0, 0, header, curses.color_pair(self.COLOR_HEADER) | curses.A_BOLD)
    
    def _draw_footer(self, stdscr) -> None:
        """Draw the footer with keybindings."""
        if self.mode == 'list':
            footer = " ↑/↓:Navigate │ Enter:View │ s:Search │ f:Filter │ Space:Favorite │ c:Copy │ d:Delete │ h:Help │ q:Quit "
        elif self.mode == 'search':
            footer = " Type to search │ Enter:Apply │ Esc:Cancel "
        elif self.mode == 'detail':
            footer = " ↑/↓:Scroll │ c:Copy │ f:Favorite │ d:Delete │ Esc:Back "
        elif self.mode == 'help':
            footer = " Press any key to close "
        else:
            footer = " Press Esc to go back "
        
        footer = footer.center(self.width)[:self.width]
        stdscr.addstr(self.height - 1, 0, footer, curses.color_pair(self.COLOR_FOOTER) | curses.A_REVERSE)
    
    def _draw_entry_line(self, stdscr, y: int, entry: Dict[str, Any], is_selected: bool) -> None:
        """Draw a single entry line."""
        # Prepare content preview
        content = entry.get('content', '')
        preview = self.classifier.get_content_preview(content, self.width - 30)
        
        # Format line
        content_type = entry.get('content_type', 'text')
        is_favorite = entry.get('is_favorite', 0)
        timestamp = entry.get('created_at', '')[:16] if entry.get('created_at') else ''
        
        # Type indicator
        type_icons = {
            'url': '🔗',
            'email': '📧',
            'code': '💻',
            'json': '📊',
            'text': '📝',
            'path': '📁',
            'command': '⚡',
            'ip_address': '🌐',
            'phone': '📞',
        }
        type_icon = type_icons.get(content_type, '📄')
        
        # Favorite indicator
        fav_icon = '⭐' if is_favorite else '  '
        
        # Build line
        line = f" {fav_icon} {type_icon} {timestamp} {preview}"
        line = line[:self.width - 2].ljust(self.width - 2)
        
        # Draw with appropriate color
        if is_selected:
            stdscr.addstr(y, 0, line, curses.color_pair(self.COLOR_SELECTED))
        else:
            color = self._get_type_color(content_type)
            stdscr.addstr(y, 0, line, curses.color_pair(color))
    
    def _draw_list(self, stdscr) -> None:
        """Draw the entry list."""
        if not self.entries:
            stdscr.addstr(self.height // 2, (self.width - 30) // 2, 
                         "No clipboard entries yet", curses.A_DIM)
            stdscr.addstr(self.height // 2 + 1, (self.width - 40) // 2,
                         "Copy something to get started!", curses.A_DIM)
            return
        
        # Calculate visible range
        visible_count = self.content_height - 2
        start_idx = self.offset
        end_idx = min(start_idx + visible_count, len(self.entries))
        
        for i, idx in enumerate(range(start_idx, end_idx)):
            y = 2 + i
            entry = self.entries[idx]
            is_selected = (idx == self.selected_index)
            self._draw_entry_line(stdscr, y, entry, is_selected)
        
        # Draw scrollbar if needed
        if len(self.entries) > visible_count:
            scrollbar_height = max(1, int(visible_count * visible_count / len(self.entries)))
            scrollbar_pos = int(self.offset * visible_count / len(self.entries))
            
            for i in range(visible_count):
                char = '│'
                if scrollbar_pos <= i < scrollbar_pos + scrollbar_height:
                    char = '█'
                stdscr.addch(2 + i, self.width - 1, char, curses.A_DIM)
    
    def _draw_detail(self, stdscr) -> None:
        """Draw entry detail view."""
        if not self.entries or self.selected_index >= len(self.entries):
            return
        
        entry = self.entries[self.selected_index]
        
        # Header info
        y = 2
        stdscr.addstr(y, 2, f"Entry #{entry.get('id', 'N/A')}", curses.A_BOLD)
        y += 1
        
        # Metadata
        metadata = [
            f"Type: {entry.get('content_type', 'text')}",
            f"Category: {entry.get('category', 'general')}",
            f"Created: {entry.get('created_at', 'N/A')}",
            f"Access: {entry.get('access_count', 0)} times",
            f"Favorite: {'Yes ⭐' if entry.get('is_favorite') else 'No'}",
        ]
        
        for item in metadata:
            stdscr.addstr(y, 2, item)
            y += 1
        
        y += 1
        stdscr.addstr(y, 2, "─" * (self.width - 4), curses.A_DIM)
        y += 2
        
        # Content
        content = entry.get('content', '')
        lines = content.split('\n')
        
        for line in lines[:self.content_height - y - 2]:
            # Truncate long lines
            display_line = line[:self.width - 4]
            try:
                stdscr.addstr(y, 2, display_line)
            except curses.error:
                pass
            y += 1
        
        if len(lines) > self.content_height - y - 2:
            stdscr.addstr(y, 2, f"... ({len(lines) - (self.content_height - y - 2)} more lines)", curses.A_DIM)
    
    def _draw_search(self, stdscr) -> None:
        """Draw search input."""
        y = self.height // 2
        prompt = "Search: "
        stdscr.addstr(y, (self.width - 40) // 2, prompt)
        stdscr.addstr(y, (self.width - 40) // 2 + len(prompt), self.search_query + "_", curses.A_REVERSE)
    
    def _draw_help(self, stdscr) -> None:
        """Draw help screen."""
        help_text = [
            "╔══════════════════════════════════════════════════════════════╗",
            "║                    📋 ClipStack-CLI Help                      ║",
            "╠══════════════════════════════════════════════════════════════╣",
            "║  Navigation                                                   ║",
            "║    ↑/↓     - Move up/down in list                            ║",
            "║    PgUp/PgDn - Page up/down                                  ║",
            "║    Home/End - Go to first/last entry                         ║",
            "║    Enter   - View entry details                              ║",
            "║    Esc     - Go back / Cancel                                ║",
            "╠══════════════════════════════════════════════════════════════╣",
            "║  Actions                                                      ║",
            "║    s       - Search entries                                  ║",
            "║    f       - Filter by type                                  ║",
            "║    Space   - Toggle favorite                                 ║",
            "║    c       - Copy to clipboard                               ║",
            "║    d       - Delete entry                                    ║",
            "║    e       - Export all entries                              ║",
            "║    r       - Refresh list                                    ║",
            "╠══════════════════════════════════════════════════════════════╣",
            "║  General                                                      ║",
            "║    h       - Show this help                                  ║",
            "║    q       - Quit                                            ║",
            "╚══════════════════════════════════════════════════════════════╝",
        ]
        
        start_y = (self.height - len(help_text)) // 2
        for i, line in enumerate(help_text):
            x = (self.width - len(line)) // 2
            stdscr.addstr(start_y + i, max(0, x), line[:self.width], curses.color_pair(self.COLOR_HELP))
    
    def _draw_message(self, stdscr) -> None:
        """Draw status message."""
        if self.message and time.time() - self.message_time < 3:
            y = self.height - 2
            stdscr.addstr(y, 2, self.message[:self.width - 4], curses.A_BOLD)
    
    def _refresh_entries(self) -> None:
        """Refresh entry list."""
        if self.search_query:
            self.entries = self.db.search(self.search_query, self.filter_type)
        elif self.filter_type:
            self.entries = self.db.get_by_type(self.filter_type)
        else:
            self.entries = self.db.get_recent(100)
        
        # Ensure selected index is valid
        if self.selected_index >= len(self.entries):
            self.selected_index = max(0, len(self.entries) - 1)
    
    def _show_message(self, msg: str) -> None:
        """Show a status message."""
        self.message = msg
        self.message_time = time.time()
    
    def _handle_list_key(self, key: int, stdscr) -> None:
        """Handle key press in list mode."""
        if key == curses.KEY_UP:
            if self.selected_index > 0:
                self.selected_index -= 1
                if self.selected_index < self.offset:
                    self.offset = self.selected_index
        
        elif key == curses.KEY_DOWN:
            if self.selected_index < len(self.entries) - 1:
                self.selected_index += 1
                visible = self.content_height - 2
                if self.selected_index >= self.offset + visible:
                    self.offset = self.selected_index - visible + 1
        
        elif key == curses.KEY_PPAGE:
            self.selected_index = max(0, self.selected_index - 10)
            self.offset = max(0, self.offset - 10)
        
        elif key == curses.KEY_NPAGE:
            self.selected_index = min(len(self.entries) - 1, self.selected_index + 10)
            visible = self.content_height - 2
            self.offset = min(len(self.entries) - visible, self.offset + 10)
        
        elif key == curses.KEY_HOME:
            self.selected_index = 0
            self.offset = 0
        
        elif key == curses.KEY_END:
            self.selected_index = len(self.entries) - 1
            visible = self.content_height - 2
            self.offset = max(0, len(self.entries) - visible)
        
        elif key == ord('\n') or key == curses.KEY_ENTER:
            if self.entries:
                self.mode = 'detail'
        
        elif key == ord('s'):
            self.mode = 'search'
            self.search_query = ""
        
        elif key == ord('f'):
            # Cycle through filters
            types = [None, 'url', 'email', 'code', 'json', 'text']
            current_idx = types.index(self.filter_type) if self.filter_type in types else 0
            self.filter_type = types[(current_idx + 1) % len(types)]
            self._refresh_entries()
            self._show_message(f"Filter: {self.filter_type or 'All'}")
        
        elif key == ord(' '):
            if self.entries and self.selected_index < len(self.entries):
                entry = self.entries[self.selected_index]
                self.db.toggle_favorite(entry['id'])
                self._refresh_entries()
                self._show_message("Favorite toggled")
        
        elif key == ord('c'):
            if self.entries and self.selected_index < len(self.entries):
                entry = self.entries[self.selected_index]
                if self.monitor:
                    self.monitor.set_clipboard_content(entry['content'])
                self._show_message("Copied to clipboard")
        
        elif key == ord('d'):
            if self.entries and self.selected_index < len(self.entries):
                entry = self.entries[self.selected_index]
                self.db.delete_entry(entry['id'])
                self._refresh_entries()
                self._show_message("Entry deleted")
        
        elif key == ord('e'):
            # Export
            import os
            export_path = os.path.expanduser("~/clipstack_export.json")
            self.db.export_to_json(export_path)
            self._show_message(f"Exported to {export_path}")
        
        elif key == ord('r'):
            self._refresh_entries()
            self._show_message("Refreshed")
        
        elif key == ord('h'):
            self.mode = 'help'
        
        elif key == ord('q'):
            self.running = False
    
    def _handle_search_key(self, key: int, stdscr) -> None:
        """Handle key press in search mode."""
        if key == 27:  # ESC
            self.mode = 'list'
            self.search_query = ""
        
        elif key == ord('\n') or key == curses.KEY_ENTER:
            self._refresh_entries()
            self.mode = 'list'
            self._show_message(f"Found {len(self.entries)} entries")
        
        elif key == curses.KEY_BACKSPACE or key == 127:
            self.search_query = self.search_query[:-1]
        
        elif 32 <= key <= 126:  # Printable characters
            self.search_query += chr(key)
    
    def _handle_detail_key(self, key: int, stdscr) -> None:
        """Handle key press in detail mode."""
        if key == 27:  # ESC
            self.mode = 'list'
        
        elif key == ord('c'):
            if self.entries and self.selected_index < len(self.entries):
                entry = self.entries[self.selected_index]
                if self.monitor:
                    self.monitor.set_clipboard_content(entry['content'])
                self._show_message("Copied to clipboard")
        
        elif key == ord('f'):
            if self.entries and self.selected_index < len(self.entries):
                entry = self.entries[self.selected_index]
                self.db.toggle_favorite(entry['id'])
                self._refresh_entries()
                self._show_message("Favorite toggled")
        
        elif key == ord('d'):
            if self.entries and self.selected_index < len(self.entries):
                entry = self.entries[self.selected_index]
                self.db.delete_entry(entry['id'])
                self._refresh_entries()
                self.mode = 'list'
                self._show_message("Entry deleted")
    
    def _handle_help_key(self, key: int, stdscr) -> None:
        """Handle key press in help mode."""
        self.mode = 'list'
    
    def _main_loop(self, stdscr) -> None:
        """Main TUI loop."""
        # Setup
        curses.curs_set(0)  # Hide cursor
        stdscr.keypad(True)
        stdscr.timeout(100)  # Non-blocking input with 100ms timeout
        
        self._init_colors()
        
        # Get dimensions
        self.height, self.width = stdscr.getmaxyx()
        self.content_height = self.height - 2
        
        # Initial load
        self._refresh_entries()
        
        # Main loop
        while self.running:
            # Clear screen
            stdscr.clear()
            
            # Update dimensions
            self.height, self.width = stdscr.getmaxyx()
            self.content_height = self.height - 2
            
            # Draw UI
            self._draw_header(stdscr)
            self._draw_footer(stdscr)
            
            if self.mode == 'list':
                self._draw_list(stdscr)
            elif self.mode == 'search':
                self._draw_list(stdscr)
                self._draw_search(stdscr)
            elif self.mode == 'detail':
                self._draw_detail(stdscr)
            elif self.mode == 'help':
                self._draw_help(stdscr)
            
            self._draw_message(stdscr)
            
            # Refresh
            stdscr.refresh()
            
            # Handle input
            try:
                key = stdscr.getch()
                
                if key != -1:
                    if self.mode == 'list':
                        self._handle_list_key(key, stdscr)
                    elif self.mode == 'search':
                        self._handle_search_key(key, stdscr)
                    elif self.mode == 'detail':
                        self._handle_detail_key(key, stdscr)
                    elif self.mode == 'help':
                        self._handle_help_key(key, stdscr)
            except Exception:
                pass
        
        # Cleanup
        curses.curs_set(1)
    
    def run(self, monitor: Optional[ClipboardMonitor] = None) -> None:
        """Run the TUI.
        
        Args:
            monitor: Optional ClipboardMonitor instance
        """
        self.monitor = monitor
        wrapper(self._main_loop)
