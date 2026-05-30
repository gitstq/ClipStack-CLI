"""
Export Utils Module - Multi-format export utilities.
导出工具模块 - 多格式导出工具。
"""

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class ExportManager:
    """
    Multi-format export manager for clipboard history.
    
    Supported formats:
    - JSON
    - CSV
    - Markdown
    - HTML
    - Plain text
    """
    
    @staticmethod
    def export_to_json(
        entries: List[Dict[str, Any]],
        output_path: str,
        pretty: bool = True
    ) -> int:
        """
        Export entries to JSON file.
        
        Args:
            entries: List of entry dictionaries
            output_path: Output file path
            pretty: Whether to pretty-print JSON
            
        Returns:
            Number of entries exported
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            if pretty:
                json.dump(entries, f, ensure_ascii=False, indent=2, default=str)
            else:
                json.dump(entries, f, ensure_ascii=False, default=str)
        
        return len(entries)
    
    @staticmethod
    def export_to_csv(
        entries: List[Dict[str, Any]],
        output_path: str
    ) -> int:
        """
        Export entries to CSV file.
        
        Args:
            entries: List of entry dictionaries
            output_path: Output file path
            
        Returns:
            Number of entries exported
        """
        if not entries:
            return 0
        
        fieldnames = ['id', 'content', 'category', 'tags', 'is_sensitive', 'created_at', 'access_count']
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            
            for entry in entries:
                # Truncate content for CSV
                row = entry.copy()
                if 'content' in row and len(str(row['content'])) > 500:
                    row['content'] = str(row['content'])[:497] + '...'
                
                if 'tags' in row and isinstance(row['tags'], list):
                    row['tags'] = ', '.join(row['tags'])
                
                writer.writerow(row)
        
        return len(entries)
    
    @staticmethod
    def export_to_markdown(
        entries: List[Dict[str, Any]],
        output_path: str,
        title: str = "ClipStack Export"
    ) -> int:
        """
        Export entries to Markdown file.
        
        Args:
            entries: List of entry dictionaries
            output_path: Output file path
            title: Document title
            
        Returns:
            Number of entries exported
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"# {title}\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**Total entries:** {len(entries)}\n\n")
            f.write("---\n\n")
            
            for entry in entries:
                entry_id = entry.get('id', 'N/A')
                category = entry.get('category', 'text')
                tags = entry.get('tags', [])
                created_at = entry.get('created_at', 'N/A')
                content = entry.get('content', '')
                is_sensitive = entry.get('is_sensitive', False)
                
                f.write(f"## Entry #{entry_id}\n\n")
                
                # Metadata table
                f.write("| Property | Value |\n")
                f.write("|----------|-------|\n")
                f.write(f"| Category | `{category}` |\n")
                f.write(f"| Tags | {', '.join(f'`{t}`' for t in tags) if tags else 'None'} |\n")
                f.write(f"| Created | {created_at} |\n")
                f.write(f"| Sensitive | {'🔒 Yes' if is_sensitive else 'No'} |\n\n")
                
                # Content
                lang = ""
                if category == "code":
                    code_langs = ['python', 'javascript', 'typescript', 'java', 'go', 'rust', 'sql', 'shell', 'yaml', 'json', 'html', 'css']
                    for tag in tags:
                        if tag in code_langs:
                            lang = tag
                            break
                
                f.write(f"```{lang}\n{content}\n```\n\n")
                f.write("---\n\n")
        
        return len(entries)
    
    @staticmethod
    def export_to_html(
        entries: List[Dict[str, Any]],
        output_path: str,
        title: str = "ClipStack Export"
    ) -> int:
        """
        Export entries to HTML file.
        
        Args:
            entries: List of entry dictionaries
            output_path: Output file path
            title: Document title
            
        Returns:
            Number of entries exported
        """
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #1a1a2e;
            color: #eee;
        }}
        h1 {{
            color: #00d4ff;
            border-bottom: 2px solid #00d4ff;
            padding-bottom: 10px;
        }}
        .entry {{
            background: #16213e;
            border-radius: 8px;
            padding: 15px;
            margin: 15px 0;
            border-left: 4px solid #00d4ff;
        }}
        .entry.sensitive {{
            border-left-color: #ff4757;
        }}
        .meta {{
            font-size: 0.9em;
            color: #888;
            margin-bottom: 10px;
        }}
        .category {{
            display: inline-block;
            background: #0f3460;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.85em;
        }}
        .tag {{
            display: inline-block;
            background: #1a1a2e;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 0.8em;
            margin: 0 2px;
        }}
        pre {{
            background: #0f0f23;
            padding: 15px;
            border-radius: 6px;
            overflow-x: auto;
            white-space: pre-wrap;
            word-wrap: break-word;
        }}
        code {{
            font-family: 'Fira Code', 'Consolas', monospace;
        }}
        .stats {{
            background: #16213e;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}
    </style>
</head>
<body>
    <h1>🦞 {title}</h1>
    <div class="stats">
        <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>Total entries:</strong> {len(entries)}</p>
    </div>
"""
        
        for entry in entries:
            entry_id = entry.get('id', 'N/A')
            category = entry.get('category', 'text')
            tags = entry.get('tags', [])
            created_at = entry.get('created_at', 'N/A')
            content = entry.get('content', '')
            is_sensitive = entry.get('is_sensitive', False)
            
            sensitive_class = " sensitive" if is_sensitive else ""
            tags_html = " ".join(f'<span class="tag">{t}</span>' for t in tags)
            
            html += f"""
    <div class="entry{sensitive_class}">
        <div class="meta">
            <strong>Entry #{entry_id}</strong> |
            <span class="category">{category}</span>
            {tags_html}
            {' 🔒' if is_sensitive else ''}
        </div>
        <pre><code>{content}</code></pre>
    </div>
"""
        
        html += """
</body>
</html>
"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return len(entries)
    
    @staticmethod
    def export_to_text(
        entries: List[Dict[str, Any]],
        output_path: str
    ) -> int:
        """
        Export entries to plain text file.
        
        Args:
            entries: List of entry dictionaries
            output_path: Output file path
            
        Returns:
            Number of entries exported
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"ClipStack Export - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total entries: {len(entries)}\n")
            f.write("=" * 60 + "\n\n")
            
            for entry in entries:
                entry_id = entry.get('id', 'N/A')
                category = entry.get('category', 'text')
                content = entry.get('content', '')
                
                f.write(f"[Entry #{entry_id}] Category: {category}\n")
                f.write("-" * 40 + "\n")
                f.write(content + "\n")
                f.write("-" * 40 + "\n\n")
        
        return len(entries)
    
    @staticmethod
    def get_supported_formats() -> List[str]:
        """
        Get list of supported export formats.
        
        Returns:
            List of format names
        """
        return ['json', 'csv', 'markdown', 'html', 'text']
