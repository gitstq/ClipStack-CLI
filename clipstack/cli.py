"""
ClipStack-CLI - Main Command Line Interface
"""

import argparse
import sys
import os
from typing import Optional

from .database import ClipboardDatabase
from .classifier import ContentClassifier
from .monitor import ClipboardMonitor
from .tui import ClipboardTUI


def main():
    """Main entry point for ClipStack-CLI."""
    parser = argparse.ArgumentParser(
        prog='clipstack',
        description='📋 ClipStack-CLI - Lightweight Terminal Clipboard History Intelligent Manager',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  clipstack                  Launch TUI dashboard
  clipstack list             List recent clipboard entries
  clipstack search <query>   Search clipboard history
  clipstack copy <id>        Copy entry to clipboard
  clipstack stats            Show clipboard statistics
  clipstack export json      Export to JSON file
  clipstack monitor          Start clipboard monitoring daemon
'''
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List recent clipboard entries')
    list_parser.add_argument('-n', '--number', type=int, default=20, help='Number of entries to show')
    list_parser.add_argument('-t', '--type', type=str, help='Filter by content type')
    list_parser.add_argument('-f', '--favorites', action='store_true', help='Show only favorites')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search clipboard history')
    search_parser.add_argument('query', type=str, help='Search query')
    search_parser.add_argument('-t', '--type', type=str, help='Filter by content type')
    search_parser.add_argument('-n', '--number', type=int, default=20, help='Number of results')
    
    # Copy command
    copy_parser = subparsers.add_parser('copy', help='Copy entry to clipboard')
    copy_parser.add_argument('id', type=int, help='Entry ID to copy')
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete clipboard entry')
    delete_parser.add_argument('id', type=int, help='Entry ID to delete')
    
    # Favorite command
    fav_parser = subparsers.add_parser('favorite', help='Toggle favorite status')
    fav_parser.add_argument('id', type=int, help='Entry ID')
    
    # Stats command
    subparsers.add_parser('stats', help='Show clipboard statistics')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export clipboard history')
    export_parser.add_argument('format', choices=['json', 'csv', 'markdown'], help='Export format')
    export_parser.add_argument('-o', '--output', type=str, help='Output file path')
    
    # Import command
    import_parser = subparsers.add_parser('import', help='Import clipboard history')
    import_parser.add_argument('file', type=str, help='File to import')
    
    # Clear command
    subparsers.add_parser('clear', help='Clear all clipboard history')
    
    # Monitor command
    monitor_parser = subparsers.add_parser('monitor', help='Start clipboard monitoring')
    monitor_parser.add_argument('-d', '--daemon', action='store_true', help='Run as daemon')
    
    # Add command
    add_parser = subparsers.add_parser('add', help='Add content to clipboard history')
    add_parser.add_argument('content', type=str, help='Content to add')
    add_parser.add_argument('-t', '--type', type=str, help='Content type')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Initialize database
    db = ClipboardDatabase()
    classifier = ContentClassifier()
    
    # Handle commands
    if args.command is None:
        # Default: launch TUI
        run_tui(db)
    
    elif args.command == 'list':
        cmd_list(db, args)
    
    elif args.command == 'search':
        cmd_search(db, args)
    
    elif args.command == 'copy':
        cmd_copy(db, args)
    
    elif args.command == 'delete':
        cmd_delete(db, args)
    
    elif args.command == 'favorite':
        cmd_favorite(db, args)
    
    elif args.command == 'stats':
        cmd_stats(db)
    
    elif args.command == 'export':
        cmd_export(db, args)
    
    elif args.command == 'import':
        cmd_import(db, args)
    
    elif args.command == 'clear':
        cmd_clear(db)
    
    elif args.command == 'monitor':
        cmd_monitor(db, args)
    
    elif args.command == 'add':
        cmd_add(db, classifier, args)


def run_tui(db: ClipboardDatabase):
    """Launch the TUI dashboard."""
    try:
        monitor = ClipboardMonitor(db)
        tui = ClipboardTUI(db)
        tui.run(monitor)
    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"Error launching TUI: {e}")
        print("Make sure your terminal supports curses.")


def cmd_list(db: ClipboardDatabase, args):
    """List clipboard entries."""
    if args.favorites:
        entries = db.get_favorites(args.number)
    elif args.type:
        entries = db.get_by_type(args.type, args.number)
    else:
        entries = db.get_recent(args.number)
    
    if not entries:
        print("No entries found.")
        return
    
    print(f"\n📋 Recent Clipboard Entries ({len(entries)}):\n")
    print(f"{'ID':<6} {'Type':<12} {'Preview':<50}")
    print("─" * 70)
    
    for entry in entries:
        entry_id = entry['id']
        content_type = entry['content_type'][:10]
        preview = classifier.get_content_preview(entry['content'], 45)
        fav = '⭐' if entry.get('is_favorite') else '  '
        
        print(f"{fav} {entry_id:<4} {content_type:<12} {preview}")


def cmd_search(db: ClipboardDatabase, args):
    """Search clipboard entries."""
    entries = db.search(args.query, args.type, args.number)
    
    if not entries:
        print(f"No results for '{args.query}'.")
        return
    
    print(f"\n🔍 Search Results for '{args.query}' ({len(entries)}):\n")
    print(f"{'ID':<6} {'Type':<12} {'Preview':<50}")
    print("─" * 70)
    
    for entry in entries:
        entry_id = entry['id']
        content_type = entry['content_type'][:10]
        preview = classifier.get_content_preview(entry['content'], 45)
        fav = '⭐' if entry.get('is_favorite') else '  '
        
        print(f"{fav} {entry_id:<4} {content_type:<12} {preview}")


def cmd_copy(db: ClipboardDatabase, args):
    """Copy entry to clipboard."""
    entry = db.get_entry(args.id)
    
    if not entry:
        print(f"Entry #{args.id} not found.")
        return
    
    monitor = ClipboardMonitor(db)
    if monitor.set_clipboard_content(entry['content']):
        print(f"✓ Copied entry #{args.id} to clipboard.")
    else:
        print("Failed to copy to clipboard.")


def cmd_delete(db: ClipboardDatabase, args):
    """Delete clipboard entry."""
    if db.delete_entry(args.id):
        print(f"✓ Deleted entry #{args.id}.")
    else:
        print(f"Entry #{args.id} not found.")


def cmd_favorite(db: ClipboardDatabase, args):
    """Toggle favorite status."""
    if db.toggle_favorite(args.id):
        entry = db.get_entry(args.id)
        status = "favorited" if entry and entry.get('is_favorite') else "unfavorited"
        print(f"✓ Entry #{args.id} {status}.")
    else:
        print(f"Entry #{args.id} not found.")


def cmd_stats(db: ClipboardDatabase):
    """Show clipboard statistics."""
    stats = db.get_statistics()
    
    print("\n📊 Clipboard Statistics\n")
    print(f"  Total Entries: {stats['total_entries']}")
    print(f"  Favorites: {stats['favorites']}")
    
    print("\n  By Type:")
    for type_name, count in stats.get('by_type', {}).items():
        bar = '█' * min(count, 20)
        print(f"    {type_name:<12} {bar} {count}")
    
    print("\n  By Category:")
    for cat_name, count in stats.get('by_category', {}).items():
        bar = '█' * min(count, 20)
        print(f"    {cat_name:<12} {bar} {count}")
    
    print("\n  Most Accessed:")
    for i, item in enumerate(stats.get('most_accessed', []), 1):
        print(f"    {i}. {item['content']} ({item['count']} times)")


def cmd_export(db: ClipboardDatabase, args):
    """Export clipboard history."""
    if args.output:
        output_path = args.output
    else:
        output_path = f"clipstack_export.{args.format}"
    
    if args.format == 'json':
        if db.export_to_json(output_path):
            print(f"✓ Exported to {output_path}")
    elif args.format == 'csv':
        if db.export_to_csv(output_path):
            print(f"✓ Exported to {output_path}")
    elif args.format == 'markdown':
        if db.export_to_markdown(output_path):
            print(f"✓ Exported to {output_path}")


def cmd_import(db: ClipboardDatabase, args):
    """Import clipboard history."""
    import json
    
    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            entries = json.load(f)
        
        count = 0
        for entry in entries:
            if 'content' in entry:
                db.add_entry(
                    content=entry['content'],
                    content_type=entry.get('content_type', 'text'),
                    category=entry.get('category', 'general'),
                    tags=entry.get('tags', [])
                )
                count += 1
        
        print(f"✓ Imported {count} entries from {args.file}")
    except Exception as e:
        print(f"Failed to import: {e}")


def cmd_clear(db: ClipboardDatabase):
    """Clear all clipboard history."""
    confirm = input("Are you sure you want to clear all history? (y/N): ")
    if confirm.lower() == 'y':
        count = db.clear_all()
        print(f"✓ Cleared {count} entries.")
    else:
        print("Cancelled.")


def cmd_monitor(db: ClipboardDatabase, args):
    """Start clipboard monitoring."""
    print("📋 Starting clipboard monitor...")
    print("Press Ctrl+C to stop.\n")
    
    def on_new_content(entry):
        preview = classifier.get_content_preview(entry['content'], 50)
        print(f"  [{entry['content_type']}] {preview}")
    
    monitor = ClipboardMonitor(db, on_new_content=on_new_content)
    monitor.start()
    
    try:
        while monitor.is_running():
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nStopping monitor...")
        monitor.stop()
        print("✓ Monitor stopped.")


def cmd_add(db: ClipboardDatabase, classifier: ContentClassifier, args):
    """Add content to clipboard history."""
    content_type, category, tags = classifier.classify(args.content)
    
    if args.type:
        content_type = args.type
    
    entry_id = db.add_entry(
        content=args.content,
        content_type=content_type,
        category=category,
        tags=tags
    )
    
    if entry_id:
        print(f"✓ Added entry #{entry_id} (type: {content_type})")
    else:
        print("Content already exists in history.")


if __name__ == '__main__':
    main()
