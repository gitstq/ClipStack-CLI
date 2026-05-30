"""
ClipStack-CLI - Main CLI Entry Point
轻量级终端剪贴板历史智能管理引擎

A powerful CLI tool for managing clipboard history with intelligent classification,
sensitive data detection, and beautiful TUI dashboard.

Author: gitstq
License: MIT
"""

import sys
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from clipstack import __version__, __description__
from clipstack.core.storage import ClipboardStorage
from clipstack.core.classifier import ContentClassifier
from clipstack.core.monitor import ClipboardMonitor, watch_clipboard
from clipstack.tui.dashboard import run_dashboard
from clipstack.utils.export import ExportManager


console = Console()


def print_version(ctx, param, value):
    """Print version and exit."""
    if not value or ctx.resilient_parsing:
        return
    console.print(f"[bold cyan]ClipStack-CLI[/bold cyan] version {__version__}")
    sys.exit(0)


def print_help(ctx, param, value):
    """Print help and exit."""
    if not value or ctx.resilient_parsing:
        return
    console.print(ctx.get_help())
    sys.exit(0)


@click.group(invoke_without_command=True)
@click.option('--version', '-v', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True, help='Show version and exit.')
@click.option('--help', '-h', is_flag=True, callback=print_help,
              expose_value=False, is_eager=True, help='Show this help message.')
@click.pass_context
def cli(ctx):
    """
    🦞 ClipStack-CLI - Lightweight Terminal Clipboard History Intelligent Management Engine
    
    轻量级终端剪贴板历史智能管理引擎
    
    Features:
    - Real-time clipboard monitoring
    - Intelligent content classification
    - Sensitive data detection
    - Beautiful TUI dashboard
    - Multi-format export
    
    Examples:
        clipstack              Launch TUI dashboard
        clipstack list         List recent clipboard entries
        clipstack search       Search clipboard history
        clipstack watch        Start clipboard monitoring
        clipstack export       Export clipboard history
    """
    if ctx.invoked_subcommand is None:
        # Default: launch TUI dashboard
        run_dashboard()


@cli.command()
@click.option('--limit', '-l', default=10, help='Number of entries to show.')
@click.option('--category', '-c', default=None, help='Filter by category.')
@click.option('--json', 'as_json', is_flag=True, help='Output as JSON.')
def list(limit: int, category: Optional[str], as_json: bool):
    """
    List recent clipboard entries.
    
    列出最近的剪贴板条目
    """
    storage = ClipboardStorage()
    entries = storage.get_all_entries(limit=limit, category=category)
    
    if not entries:
        console.print("[yellow]No clipboard entries found.[/yellow]")
        return
    
    if as_json:
        import json
        console.print(json.dumps(entries, indent=2, default=str))
        return
    
    table = Table(title=f"📋 Recent Clipboard Entries ({len(entries)})")
    table.add_column("#", style="dim", width=4)
    table.add_column("Content", width=50)
    table.add_column("Category", width=10)
    table.add_column("Time", width=10)
    
    for entry in entries:
        content = entry["content"][:47] + "..." if len(entry["content"]) > 50 else entry["content"]
        content = content.replace("\n", "\\n")
        
        table.add_row(
            str(entry["id"]),
            content,
            entry["category"],
            str(entry.get("created_at", ""))[:10]
        )
    
    console.print(table)


@cli.command()
@click.argument('query', required=False)
@click.option('--limit', '-l', default=20, help='Maximum results.')
@click.option('--category', '-c', default=None, help='Filter by category.')
def search(query: Optional[str], limit: int, category: Optional[str]):
    """
    Search clipboard history.
    
    搜索剪贴板历史
    
    QUERY: Search term (optional, will prompt if not provided)
    """
    storage = ClipboardStorage()
    
    if not query:
        query = click.prompt('Search query', type=str)
    
    entries = storage.get_all_entries(limit=limit, category=category, search=query)
    
    if not entries:
        console.print(f"[yellow]No results found for '{query}'[/yellow]")
        return
    
    console.print(f"\n[green]Found {len(entries)} results for '{query}':[/green]\n")
    
    for entry in entries:
        content = entry["content"][:100]
        if len(entry["content"]) > 100:
            content += "..."
        
        console.print(f"[bold cyan]#{entry['id']}[/bold cyan] [{entry['category']}]")
        console.print(f"  {content}")
        console.print()


@cli.command()
@click.option('--interval', '-i', default=0.5, help='Polling interval in seconds.')
@click.option('--quiet', '-q', is_flag=True, help='Quiet mode (no output).')
def watch(interval: float, quiet: bool):
    """
    Start clipboard monitoring.
    
    启动剪贴板监控
    """
    def on_new_content(content, classification):
        if not quiet:
            category = classification.content_type.value
            sensitive = " 🔒" if classification.is_sensitive else ""
            console.print(f"[green]✓[/green] Captured: [{category}]{sensitive}")
    
    console.print("[cyan]🦞 ClipStack Monitor started...[/cyan]")
    console.print("[dim]Press Ctrl+C to stop.[/dim]\n")
    
    try:
        monitor = watch_clipboard(
            on_new_content=on_new_content,
            poll_interval=interval
        )
        
        # Keep running until interrupted
        import time
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Monitor stopped.[/yellow]")


@cli.command()
@click.argument('entry_id', type=int)
def view(entry_id: int):
    """
    View a specific clipboard entry.
    
    查看特定剪贴板条目
    """
    storage = ClipboardStorage()
    entry = storage.get_entry(entry_id)
    
    if not entry:
        console.print(f"[red]Entry #{entry_id} not found.[/red]")
        return
    
    # Display entry details
    console.print(Panel(f"[bold]Entry #{entry_id}[/bold]", border_style="cyan"))
    
    meta_table = Table(show_header=False, box=None)
    meta_table.add_column("Key", style="bold cyan")
    meta_table.add_column("Value")
    
    meta_table.add_row("Category", entry["category"])
    meta_table.add_row("Tags", ", ".join(entry.get("tags", [])))
    meta_table.add_row("Created", str(entry.get("created_at", "N/A")))
    meta_table.add_row("Access Count", str(entry.get("access_count", 1)))
    
    if entry.get("is_sensitive"):
        meta_table.add_row("Sensitive", "[red]🔒 Yes[/red]")
    
    console.print(meta_table)
    console.print()
    console.print(Panel(entry["content"], title="Content", border_style="green"))


@cli.command()
@click.argument('entry_id', type=int)
def copy(entry_id: int):
    """
    Copy entry to clipboard.
    
    复制条目到剪贴板
    """
    storage = ClipboardStorage()
    entry = storage.get_entry(entry_id)
    
    if not entry:
        console.print(f"[red]Entry #{entry_id} not found.[/red]")
        return
    
    try:
        import pyperclip
        pyperclip.copy(entry["content"])
        console.print(f"[green]✓ Copied entry #{entry_id} to clipboard[/green]")
    except ImportError:
        console.print("[yellow]pyperclip not installed. Content:[/yellow]")
        console.print(entry["content"])


@cli.command()
@click.argument('entry_id', type=int)
@click.option('--force', '-f', is_flag=True, help='Skip confirmation.')
def delete(entry_id: int, force: bool):
    """
    Delete a clipboard entry.
    
    删除剪贴板条目
    """
    storage = ClipboardStorage()
    
    if not force:
        if not click.confirm(f"Delete entry #{entry_id}?"):
            return
    
    if storage.delete_entry(entry_id):
        console.print(f"[green]✓ Deleted entry #{entry_id}[/green]")
    else:
        console.print(f"[red]Entry #{entry_id} not found.[/red]")


@cli.command()
@click.option('--format', '-f', 'export_format', 
              type=click.Choice(['json', 'csv', 'markdown', 'html', 'text']),
              default='json', help='Export format.')
@click.option('--output', '-o', default=None, help='Output file path.')
def export(export_format: str, output: Optional[str]):
    """
    Export clipboard history.
    
    导出剪贴板历史
    """
    storage = ClipboardStorage()
    entries = storage.get_all_entries(limit=10000)
    
    if not entries:
        console.print("[yellow]No entries to export.[/yellow]")
        return
    
    # Generate default output path
    if not output:
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        ext = {'json': 'json', 'csv': 'csv', 'markdown': 'md', 'html': 'html', 'text': 'txt'}[export_format]
        output = f"clipstack_export_{timestamp}.{ext}"
    
    # Export based on format
    count = 0
    if export_format == 'json':
        count = ExportManager.export_to_json(entries, output)
    elif export_format == 'csv':
        count = ExportManager.export_to_csv(entries, output)
    elif export_format == 'markdown':
        count = ExportManager.export_to_markdown(entries, output)
    elif export_format == 'html':
        count = ExportManager.export_to_html(entries, output)
    elif export_format == 'text':
        count = ExportManager.export_to_text(entries, output)
    
    console.print(f"[green]✓ Exported {count} entries to {output}[/green]")


@cli.command()
@click.option('--force', '-f', is_flag=True, help='Skip confirmation.')
def clear(force: bool):
    """
    Clear all clipboard history.
    
    清空所有剪贴板历史
    """
    storage = ClipboardStorage()
    
    if not force:
        if not click.confirm("Clear ALL clipboard history? This cannot be undone!"):
            return
    
    count = storage.clear_all()
    console.print(f"[green]✓ Cleared {count} entries[/green]")


@cli.command()
def stats():
    """
    Show clipboard statistics.
    
    显示剪贴板统计信息
    """
    storage = ClipboardStorage()
    stats = storage.get_stats()
    
    console.print(Panel("[bold]📊 ClipStack Statistics[/bold]", border_style="cyan"))
    
    table = Table(show_header=False, box=None)
    table.add_column("Metric", style="bold cyan")
    table.add_column("Value")
    
    table.add_row("Total Entries", str(stats["total_entries"]))
    table.add_row("Sensitive Entries", f"[red]{stats['sensitive_entries']}[/red]")
    
    console.print(table)
    
    if stats["by_category"]:
        console.print("\n[bold]By Category:[/bold]")
        cat_table = Table(show_header=False, box=None)
        cat_table.add_column("Category", style="cyan")
        cat_table.add_column("Count", justify="right")
        
        for category, count in stats["by_category"].items():
            cat_table.add_row(category, str(count))
        
        console.print(cat_table)


@cli.command()
def classify():
    """
    Classify clipboard content interactively.
    
    交互式分类剪贴板内容
    """
    try:
        import pyperclip
        content = pyperclip.paste()
    except ImportError:
        content = click.prompt('Enter content to classify', type=str)
    
    if not content:
        console.print("[yellow]Clipboard is empty.[/yellow]")
        return
    
    classifier = ContentClassifier()
    result = classifier.classify(content)
    
    console.print(Panel("[bold]Classification Result[/bold]", border_style="cyan"))
    
    table = Table(show_header=False, box=None)
    table.add_column("Property", style="bold cyan")
    table.add_column("Value")
    
    table.add_row("Content Type", result.content_type.value)
    table.add_row("Confidence", f"{result.confidence:.2%}")
    table.add_row("Is Sensitive", "[red]Yes[/red]" if result.is_sensitive else "[green]No[/green]")
    
    if result.language:
        table.add_row("Language", result.language)
    
    table.add_row("Tags", ", ".join(result.tags))
    
    console.print(table)
    
    if result.warnings:
        console.print()
        for warning in result.warnings:
            console.print(f"[yellow]{warning}[/yellow]")


def main():
    """Main entry point."""
    try:
        cli()
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted.[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


if __name__ == '__main__':
    main()
