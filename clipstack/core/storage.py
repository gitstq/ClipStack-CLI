"""
Clipboard Storage Module - SQLite-based clipboard history storage with encryption support.
剪贴板存储模块 - 基于SQLite的剪贴板历史存储，支持加密。
"""

import hashlib
import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class ClipboardStorage:
    """
    SQLite-based clipboard history storage with encryption support.
    
    Features:
    - Persistent storage with SQLite
    - Content hashing for deduplication
    - Metadata tracking (timestamp, category, tags)
    - Search and filter capabilities
    """
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize clipboard storage.
        
        Args:
            db_path: Path to SQLite database file. Defaults to ~/.clipstack/history.db
        """
        if db_path is None:
            config_dir = Path.home() / ".clipstack"
            config_dir.mkdir(parents=True, exist_ok=True)
            db_path = str(config_dir / "history.db")
        
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self) -> None:
        """Initialize database schema."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clipboard_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    content_hash TEXT UNIQUE NOT NULL,
                    category TEXT DEFAULT 'text',
                    tags TEXT DEFAULT '[]',
                    is_sensitive INTEGER DEFAULT 0,
                    is_encrypted INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    access_count INTEGER DEFAULT 1
                )
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_content_hash 
                ON clipboard_history(content_hash)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_category 
                ON clipboard_history(category)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_created_at 
                ON clipboard_history(created_at DESC)
            """)
            conn.commit()
    
    def _compute_hash(self, content: str) -> str:
        """Compute SHA-256 hash of content."""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()[:16]
    
    def add_entry(
        self,
        content: str,
        category: str = "text",
        tags: Optional[List[str]] = None,
        is_sensitive: bool = False,
        is_encrypted: bool = False
    ) -> int:
        """
        Add a new clipboard entry.
        
        Args:
            content: Clipboard content
            category: Content category (text, code, url, email, password, etc.)
            tags: List of tags for the entry
            is_sensitive: Whether content contains sensitive data
            is_encrypted: Whether content is encrypted
            
        Returns:
            Entry ID
        """
        content_hash = self._compute_hash(content)
        tags_json = json.dumps(tags or [], ensure_ascii=False)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Check if entry already exists (deduplication)
            cursor.execute(
                "SELECT id, access_count FROM clipboard_history WHERE content_hash = ?",
                (content_hash,)
            )
            existing = cursor.fetchone()
            
            if existing:
                # Update access count and timestamp
                entry_id, count = existing
                cursor.execute(
                    """
                    UPDATE clipboard_history 
                    SET access_count = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                    """,
                    (count + 1, entry_id)
                )
                conn.commit()
                return entry_id
            
            # Insert new entry
            cursor.execute(
                """
                INSERT INTO clipboard_history 
                (content, content_hash, category, tags, is_sensitive, is_encrypted)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (content, content_hash, category, tags_json, int(is_sensitive), int(is_encrypted))
            )
            conn.commit()
            return cursor.lastrowid
    
    def get_entry(self, entry_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific clipboard entry.
        
        Args:
            entry_id: Entry ID
            
        Returns:
            Entry dictionary or None if not found
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clipboard_history WHERE id = ?", (entry_id,))
            row = cursor.fetchone()
            
            if row:
                return self._row_to_dict(row)
            return None
    
    def get_all_entries(
        self,
        limit: int = 100,
        offset: int = 0,
        category: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get all clipboard entries with optional filtering.
        
        Args:
            limit: Maximum number of entries to return
            offset: Number of entries to skip
            category: Filter by category
            search: Search term for content
            
        Returns:
            List of entry dictionaries
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            query = "SELECT * FROM clipboard_history WHERE 1=1"
            params = []
            
            if category:
                query += " AND category = ?"
                params.append(category)
            
            if search:
                query += " AND content LIKE ?"
                params.append(f"%{search}%")
            
            query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
            params.extend([limit, offset])
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            return [self._row_to_dict(row) for row in rows]
    
    def delete_entry(self, entry_id: int) -> bool:
        """
        Delete a clipboard entry.
        
        Args:
            entry_id: Entry ID
            
        Returns:
            True if deleted, False if not found
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM clipboard_history WHERE id = ?", (entry_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def clear_all(self) -> int:
        """
        Clear all clipboard history.
        
        Returns:
            Number of entries deleted
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM clipboard_history")
            count = cursor.fetchone()[0]
            cursor.execute("DELETE FROM clipboard_history")
            conn.commit()
            return count
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get storage statistics.
        
        Returns:
            Dictionary with statistics
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Total entries
            cursor.execute("SELECT COUNT(*) FROM clipboard_history")
            total = cursor.fetchone()[0]
            
            # Entries by category
            cursor.execute("""
                SELECT category, COUNT(*) as count 
                FROM clipboard_history 
                GROUP BY category 
                ORDER BY count DESC
            """)
            by_category = dict(cursor.fetchall())
            
            # Sensitive entries
            cursor.execute("SELECT COUNT(*) FROM clipboard_history WHERE is_sensitive = 1")
            sensitive = cursor.fetchone()[0]
            
            # Most accessed
            cursor.execute("""
                SELECT content, access_count 
                FROM clipboard_history 
                ORDER BY access_count DESC 
                LIMIT 5
            """)
            most_accessed = cursor.fetchall()
            
            return {
                "total_entries": total,
                "by_category": by_category,
                "sensitive_entries": sensitive,
                "most_accessed": [
                    {"content": c[:50] + "..." if len(c) > 50 else c, "count": cnt}
                    for c, cnt in most_accessed
                ]
            }
    
    def export_to_json(self, output_path: str) -> int:
        """
        Export all entries to JSON file.
        
        Args:
            output_path: Path to output JSON file
            
        Returns:
            Number of entries exported
        """
        entries = self.get_all_entries(limit=10000)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(entries, f, ensure_ascii=False, indent=2, default=str)
        
        return len(entries)
    
    def export_to_csv(self, output_path: str) -> int:
        """
        Export all entries to CSV file.
        
        Args:
            output_path: Path to output CSV file
            
        Returns:
            Number of entries exported
        """
        import csv
        
        entries = self.get_all_entries(limit=10000)
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            if not entries:
                return 0
            
            fieldnames = ['id', 'content', 'category', 'tags', 'is_sensitive', 'created_at', 'access_count']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for entry in entries:
                writer.writerow({
                    'id': entry['id'],
                    'content': entry['content'][:200],  # Truncate for CSV
                    'category': entry['category'],
                    'tags': entry['tags'],
                    'is_sensitive': entry['is_sensitive'],
                    'created_at': entry['created_at'],
                    'access_count': entry['access_count']
                })
        
        return len(entries)
    
    def _row_to_dict(self, row: sqlite3.Row) -> Dict[str, Any]:
        """Convert database row to dictionary."""
        return {
            "id": row["id"],
            "content": row["content"],
            "content_hash": row["content_hash"],
            "category": row["category"],
            "tags": json.loads(row["tags"]),
            "is_sensitive": bool(row["is_sensitive"]),
            "is_encrypted": bool(row["is_encrypted"]),
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
            "access_count": row["access_count"]
        }
