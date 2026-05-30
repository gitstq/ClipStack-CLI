"""
TUI Dashboard Module - Beautiful terminal interface for clipboard management.
TUI仪表盘模块 - 美观的终端剪贴板管理界面。
"""

from datetime import datetime
from typing import List, Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.layout import Layout
from rich.live import Live
from rich.prompt import Prompt, Confirm
from rich.syntax import Syntax

from clipstack.core.storage import ClipboardStorage
from clipstack.core.classifier import ContentClassifier, ContentType


class ClipStackDashboard:
    """
    Interactive TUI dashboard for clipboard management.
    
    Features:
    - Beautiful Rich-based interface
    - Real-time clipboard history view
    - Search and filter capabilities
    - Entry preview and actions
    - Statistics display
    """
    
    # Category colors
    CATEGORY_COLORS = {
        "text": "white",
        "code": "cyan",
        "url": "blue",
        "contact": "green",
        "credential": "red",
        "data": "yellow",
        "command": "magenta",
        "path": "blue",
        "network": "cyan",
    }
    
    # Content type icons
    TYPE_ICONS = {
        ContentType.TEXT: "📝",
        ContentType.CODE: "💻",
        ContentType.URL: "🔗",
        ContentType.EMAIL: "📧",
        ContentType.PASSWORD: "🔑",
        ContentType.API_KEY: "🔐",
        ContentType.JSON: "📊",
        ContentType.COMMAND: "⚡",
        ContentType.PATH: "📁",
        ContentType.IP_ADDRESS: "🌐",
        ContentType.PHONE: "📞",
        ContentType.CREDIT_CARD: "💳",
    }
    
    def __init__(self, storage: Optional[ClipboardStorage] = None):
        """
        Initialize dashboard.
        
        Args:
            storage: ClipboardStorage instance
        """
        self.storage = storage or ClipboardStorage()
        self.classifier = ContentClassifier()
        self.console = Console()
        self.current_filter: Optional[str] = None
        self.search_query: Optional[str] = None
    
    def run(self) -> None:
        """Run the interactive dashboard."""
        while True:
            self._clear_screen()
            self._show_header()
            
            entries = self._get_entries()
            self._show_entries(entries)
            
            self._show_stats()
            self._show_actions()
            
            action = self._get_action()
            
            if not self._handle_action(action):
                break
    
    def _clear_screen(self) -> None:
        """Clear the terminal screen."""
        self.console.clear()
    
    def _show_header(self) -> None:
        """Show dashboard header."""
        filter_text = f" [dim]Filter: {self.current_filter}[/dim]" if self.current_filter else ""
        search_text = f" [dim]Search: {self.search_query}[/dim]" if self.search_query else ""
        
        header = Panel(
            f"[bold cyan]🦞 ClipStack-CLI[/bold cyan] - Clipboard History Manager{filter_text}{search_text}",
            style="bold white on blue",
            padding=(0, 2)
        )
        self.console.print(header)
        self.console.print()
    
    def _get_entries(self, limit: int = 15) -> List[dict]:
        """
        Get clipboard entries with current filters.
        
        Args:
            limit: Maximum entries to return
            
        Returns:
            List of entries
        """
        return self.storage.get_all_entries(
            limit=limit,
            category=self.current_filter,
            search=self.search_query
        )
    
    def _show_entries(self, entries: List[dict]) -> None:
        """
        Display clipboard entries in a table.
        
        Args:
            entries: List of entry dictionaries
        """
        if not entries:
            self.console.print("\n[yellow]No clipboard entries found.[/yellow]")
            self.console.print("[dim]Copy some content to get started![/dim]\n")
            return
        
        table = Table(
            show_header=True,
            header_style="bold cyan",
            border_style="blue",
            padding=(0, 1),
            expand=True
        )
        
        table.add_column("#", style="dim", width=3, justify="right")
        table.add_column("Content", width=50)
        table.add_column("Category", width=10)
        table.add_column("Time", width=12)
        table.add_column("Count", width=5, justify="right")
        
        for entry in entries:
            # Truncate content for display
            content = entry["content"]
            if len(content) > 45:
                content = content[:42] + "..."
            
            # Replace newlines for display
            content = content.replace("\n", "\\n").replace("\r", "")
            
            # Get category color
            category = entry["category"]
            color = self.CATEGORY_COLORS.get(category, "white")
            
            # Format time
            created_at = entry["created_at"]
            if isinstance(created_at, str):
                try:
                    dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                    time_str = dt.strftime("%H:%M:%S")
                except (ValueError, TypeError):
                    time_str = created_at[:8] if len(created_at) >= 8 else created_at
            else:
                time_str = str(created_at)[:8]
            
            # Sensitive indicator
            sensitive = " 🔒" if entry.get("is_sensitive") else ""
            
            table.add_row(
                str(entry["id"]),
                Text(content, style=color) if not entry.get("is_sensitive") else Text(f"🔒 {content}", style="red"),
                f"[{color}]{category}[/{color}]{sensitive}",
                time_str,
                str(entry.get("access_count", 1))
            )
        
        self.console.print(table)
        self.console.print()
    
    def _show_stats(self) -> None:
        """Show storage statistics."""
        stats = self.storage.get_stats()
        
        stats_text = (
            f"[bold]Total:[/bold] {stats['total_entries']} | "
            f"[bold]Sensitive:[/bold] [red]{stats['sensitive_entries']}[/red]"
        )
        
        if stats['by_category']:
            categories = " | ".join(
                f"[{self.CATEGORY_COLORS.get(k, 'white')}]{k}:[/{self.CATEGORY_COLORS.get(k, 'white')}] {v}"
                for k, v in list(stats['by_category'].items())[:5]
            )
            stats_text += f"\n{categories}"
        
        self.console.print(Panel(stats_text, title="📊 Statistics", border_style="dim blue"))
    
    def _show_actions(self) -> None:
        """Show available actions."""
        actions = (
            "[bold]Actions:[/bold] "
            "[cyan]v[/cyan]=view | "
            "[cyan]c[/cyan]=copy | "
            "[cyan]d[/cyan]=delete | "
            "[cyan]s[/cyan]=search | "
            "[cyan]f[/cyan]=filter | "
            "[cyan]e[/cyan]=export | "
            "[cyan]q[/cyan]=quit"
        )
        self.console.print(f"\n{actions}")
    
    def _get_action(self) -> str:
        """
        Get user action input.
        
        Returns:
            Action string
        """
        return Prompt.ask("\n[action]", default="v").lower().strip()
    
    def _handle_action(self, action: str) -> bool:
        """
        Handle user action.
        
        Args:
            action: Action string
            
        Returns:
            True to continue, False to exit
        """
        if action in ("q", "quit", "exit"):
            return False
        
        elif action in ("v", "view"):
            self._action_view()
        
        elif action in ("c", "copy"):
            self._action_copy()
        
        elif action in ("d", "delete"):
            self._action_delete()
        
        elif action in ("s", "search"):
            self._action_search()
        
        elif action in ("f", "filter"):
            self._action_filter()
        
        elif action in ("e", "export"):
            self._action_export()
        
        elif action in ("clear", "clr"):
            self._action_clear()
        
        return True
    
    def _action_view(self) -> None:
        """View entry details."""
        try:
            entry_id = int(Prompt.ask("Entry ID"))
            entry = self.storage.get_entry(entry_id)
            
            if not entry:
                self.console.print("[red]Entry not found.[/red]")
                return
            
            self._show_entry_detail(entry)
            Prompt.ask("\nPress Enter to continue")
            
        except (ValueError, KeyboardInterrupt):
            pass
    
    def _show_entry_detail(self, entry: dict) -> None:
        """
        Show detailed entry view.
        
        Args:
            entry: Entry dictionary
        """
        # Header
        header = f"[bold]Entry #{entry['id']}[/bold]"
        if entry.get("is_sensitive"):
            header += " [red]🔒 SENSITIVE[/red]"
        
        self.console.print(Panel(header, border_style="cyan"))
        
        # Metadata
        meta = Table(show_header=False, box=None)
        meta.add_column("Key", style="bold cyan")
        meta.add_column("Value")
        
        meta.add_row("Category", entry["category"])
        meta.add_row("Tags", ", ".join(entry.get("tags", [])))
        meta.add_row("Created", str(entry.get("created_at", "N/A")))
        meta.add_row("Access Count", str(entry.get("access_count", 1)))
        
        self.console.print(meta)
        self.console.print()
        
        # Content
        content = entry["content"]
        
        # Try to syntax highlight if code
        if entry["category"] == "code":
            # Detect language from tags
            lang = None
            for tag in entry.get("tags", []):
                if tag in ("python", "javascript", "typescript", "java", "go", "rust", "sql", "shell", "html", "css", "yaml", "markdown"):
                    lang = tag
                    break
            
            if lang:
                try:
                    syntax = Syntax(content, lang, theme="monokai", line_numbers=True)
                    self.console.print(Panel(syntax, title="Content", border_style="green"))
                    return
                except Exception:
                    pass
        
        # Plain text content
        self.console.print(Panel(content, title="Content", border_style="green"))
    
    def _action_copy(self) -> None:
        """Copy entry to clipboard."""
        try:
            entry_id = int(Prompt.ask("Entry ID to copy"))
            entry = self.storage.get_entry(entry_id)
            
            if not entry:
                self.console.print("[red]Entry not found.[/red]")
                return
            
            try:
                import pyperclip
                pyperclip.copy(entry["content"])
                self.console.print(f"[green]✓ Copied entry #{entry_id} to clipboard[/green]")
            except ImportError:
                self.console.print("[yellow]pyperclip not installed. Content displayed below:[/yellow]")
                self.console.print(entry["content"])
            
            Prompt.ask("\nPress Enter to continue")
            
        except (ValueError, KeyboardInterrupt):
            pass
    
    def _action_delete(self) -> None:
        """Delete an entry."""
        try:
            entry_id = int(Prompt.ask("Entry ID to delete"))
            
            if Confirm.ask(f"Delete entry #{entry_id}?"):
                if self.storage.delete_entry(entry_id):
                    self.console.print(f"[green]✓ Deleted entry #{entry_id}[/green]")
                else:
                    self.console.print("[red]Entry not found.[/red]")
            
            Prompt.ask("\nPress Enter to continue")
            
        except (ValueError, KeyboardInterrupt):
            pass
    
    def _action_search(self) -> None:
        """Search clipboard history."""
        query = Prompt.ask("Search query (empty to clear)")
        
        if query.strip():
            self.search_query = query.strip()
        else:
            self.search_query = None
    
    def _action_filter(self) -> None:
        """Filter by category."""
        categories = ["text", "code", "url", "contact", "credential", "data", "command", "path", "network"]
        
        self.console.print("\n[cyan]Available categories:[/cyan]")
        for i, cat in enumerate(categories, 1):
            color = self.CATEGORY_COLORS.get(cat, "white")
            self.console.print(f"  {i}. [{color}]{cat}[/{color}]")
        self.console.print("  0. Clear filter")
        
        try:
            choice = int(Prompt.ask("Select category"))
            
            if choice == 0:
                self.current_filter = None
            elif 1 <= choice <= len(categories):
                self.current_filter = categories[choice - 1]
            
        except (ValueError, KeyboardInterrupt):
            pass
    
    def _action_export(self) -> None:
        """Export clipboard history."""
        self.console.print("\n[cyan]Export format:[/cyan]")
        self.console.print("  1. JSON")
        self.console.print("  2. CSV")
        self.console.print("  3. Markdown")
        
        try:
            choice = int(Prompt.ask("Select format"))
            
            if choice == 1:
                path = Prompt.ask("Output path", default="clipstack_export.json")
                count = self.storage.export_to_json(path)
                self.console.print(f"[green]✓ Exported {count} entries to {path}[/green]")
            
            elif choice == 2:
                path = Prompt.ask("Output path", default="clipstack_export.csv")
                count = self.storage.export_to_csv(path)
                self.console.print(f"[green]✓ Exported {count} entries to {path}[/green]")
            
            elif choice == 3:
                path = Prompt.ask("Output path", default="clipstack_export.md")
                count = self._export_to_markdown(path)
                self.console.print(f"[green]✓ Exported {count} entries to {path}[/green]")
            
            Prompt.ask("\nPress Enter to continue")
            
        except (ValueError, KeyboardInterrupt):
            pass
    
    def _export_to_markdown(self, path: str) -> int:
        """
        Export entries to Markdown format.
        
        Args:
            path: Output file path
            
        Returns:
            Number of entries exported
        """
        entries = self.storage.get_all_entries(limit=1000)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write("# ClipStack Export\n\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n\n")
            f.write(f"Total entries: {len(entries)}\n\n")
            f.write("---\n\n")
            
            for entry in entries:
                f.write(f"## Entry #{entry['id']}\n\n")
                f.write(f"- **Category:** {entry['category']}\n")
                f.write(f"- **Tags:** {', '.join(entry.get('tags', []))}\n")
                f.write(f"- **Created:** {entry.get('created_at', 'N/A')}\n")
                f.write(f"- **Access Count:** {entry.get('access_count', 1)}\n\n")
                
                # Content in code block
                lang = ""
                if entry["category"] == "code":
                    for tag in entry.get("tags", []):
                        if tag in ("python", "javascript", "typescript", "java", "go", "rust", "sql", "shell", "yaml", "json"):
                            lang = tag
                            break
                
                f.write(f"```{lang}\n{entry['content']}\n```\n\n")
                f.write("---\n\n")
        
        return len(entries)
    
    def _action_clear(self) -> None:
        """Clear all clipboard history."""
        if Confirm.ask("Clear ALL clipboard history? This cannot be undone!"):
            count = self.storage.clear_all()
            self.console.print(f"[green]✓ Cleared {count} entries[/green]")
            Prompt.ask("\nPress Enter to continue")


def run_dashboard() -> None:
    """Run the ClipStack dashboard."""
    dashboard = ClipStackDashboard()
    dashboard.run()
