"""
Clipboard Database Module - SQLite-based storage for clipboard history
"""

import sqlite3
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple
import threading


class ClipboardDatabase:
    """SQLite-based clipboard history storage with encryption support."""
    
    def __init__(self, db_path: Optional[str] = None):
        """Initialize the database.
        
        Args:
            db_path: Path to the database file. Defaults to ~/.clipstack/history.db
        """
        if db_path is None:
            home = Path.home()
            self.db_dir = home / ".clipstack"
            self.db_dir.mkdir(parents=True, exist_ok=True)
            db_path = str(self.db_dir / "history.db")
        
        self.db_path = db_path
        self._lock = threading.Lock()
        self._init_database()
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get a database connection with row factory."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def _init_database(self) -> None:
        """Initialize database tables."""
        with self._lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Main clipboard history table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS clipboard_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    content_hash TEXT UNIQUE,
                    content_type TEXT DEFAULT 'text',
                    category TEXT DEFAULT 'general',
                    tags TEXT DEFAULT '[]',
                    is_favorite INTEGER DEFAULT 0,
                    is_encrypted INTEGER DEFAULT 0,
                    char_count INTEGER DEFAULT 0,
                    word_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    access_count INTEGER DEFAULT 1
                )
            ''')
            
            # Index for faster searches
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_content_type 
                ON clipboard_history(content_type)
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_category 
                ON clipboard_history(category)
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_created_at 
                ON clipboard_history(created_at DESC)
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_access_count 
                ON clipboard_history(access_count DESC)
            ''')
            
            # Statistics table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS statistics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    stat_key TEXT UNIQUE,
                    stat_value TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
    
    def _compute_hash(self, content: str) -> str:
        """Compute SHA256 hash of content."""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    def add_entry(
        self,
        content: str,
        content_type: str = "text",
        category: str = "general",
        tags: Optional[List[str]] = None,
        is_encrypted: bool = False
    ) -> Optional[int]:
        """Add a new clipboard entry.
        
        Args:
            content: The clipboard content
            content_type: Type of content (text, url, email, code, json, etc.)
            category: Category for organization
            tags: List of tags
            is_encrypted: Whether the content is encrypted
            
        Returns:
            Entry ID if successful, None if duplicate
        """
        content_hash = self._compute_hash(content)
        
        with self._lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Check for duplicate
            cursor.execute(
                "SELECT id, access_count FROM clipboard_history WHERE content_hash = ?",
                (content_hash,)
            )
            existing = cursor.fetchone()
            
            if existing:
                # Update access count for existing entry
                cursor.execute(
                    "UPDATE clipboard_history SET access_count = ?, updated_at = ? WHERE id = ?",
                    (existing['access_count'] + 1, datetime.now().isoformat(), existing['id'])
                )
                conn.commit()
                conn.close()
                return existing['id']
            
            # Calculate word count
            word_count = len(content.split()) if content else 0
            char_count = len(content) if content else 0
            
            # Insert new entry
            cursor.execute('''
                INSERT INTO clipboard_history 
                (content, content_hash, content_type, category, tags, is_encrypted, char_count, word_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                content,
                content_hash,
                content_type,
                category,
                json.dumps(tags or []),
                1 if is_encrypted else 0,
                char_count,
                word_count
            ))
            
            entry_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return entry_id
    
    def get_entry(self, entry_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific entry by ID."""
        with self._lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM clipboard_history WHERE id = ?", (entry_id,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return dict(row)
            return None
    
    def get_recent(self, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """Get recent clipboard entries."""
        with self._lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM clipboard_history 
                ORDER BY created_at DESC 
                LIMIT ? OFFSET ?
            ''', (limit, offset))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in rows]
    
    def search(
        self,
        query: str,
        content_type: Optional[str] = None,
        category: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Search clipboard entries."""
        with self._lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            sql = "SELECT * FROM clipboard_history WHERE content LIKE ?"
            params = [f"%{query}%"]
            
            if content_type:
                sql += " AND content_type = ?"
                params.append(content_type)
            
            if category:
                sql += " AND category = ?"
                params.append(category)
            
            sql += " ORDER BY created_at DESC LIMIT ?"
            params.append(limit)
            
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in rows]
    
    def get_by_type(self, content_type: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get entries by content type."""
        with self._lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM clipboard_history 
                WHERE content_type = ?
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (content_type, limit))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in rows]
    
    def get_favorites(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get favorite entries."""
        with self._lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM clipboard_history 
                WHERE is_favorite = 1
                ORDER BY updated_at DESC 
                LIMIT ?
            ''', (limit,))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in rows]
    
    def toggle_favorite(self, entry_id: int) -> bool:
        """Toggle favorite status of an entry."""
        with self._lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE clipboard_history 
                SET is_favorite = NOT is_favorite, updated_at = ?
                WHERE id = ?
            ''', (datetime.now().isoformat(), entry_id))
            
            success = cursor.rowcount > 0
            conn.commit()
            conn.close()
            
            return success
    
    def add_tag(self, entry_id: int, tag: str) -> bool:
        """Add a tag to an entry."""
        with self._lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT tags FROM clipboard_history WHERE id = ?", (entry_id,))
            row = cursor.fetchone()
            
            if not row:
                conn.close()
                return False
            
            tags = json.loads(row['tags'])
            if tag not in tags:
                tags.append(tag)
                cursor.execute(
                    "UPDATE clipboard_history SET tags = ?, updated_at = ? WHERE id = ?",
                    (json.dumps(tags), datetime.now().isoformat(), entry_id)
                )
            
            conn.commit()
            conn.close()
            return True
    
    def remove_tag(self, entry_id: int, tag: str) -> bool:
        """Remove a tag from an entry."""
        with self._lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT tags FROM clipboard_history WHERE id = ?", (entry_id,))
            row = cursor.fetchone()
            
            if not row:
                conn.close()
                return False
            
            tags = json.loads(row['tags'])
            if tag in tags:
                tags.remove(tag)
                cursor.execute(
                    "UPDATE clipboard_history SET tags = ?, updated_at = ? WHERE id = ?",
                    (json.dumps(tags), datetime.now().isoformat(), entry_id)
                )
            
            conn.commit()
            conn.close()
            return True
    
    def delete_entry(self, entry_id: int) -> bool:
        """Delete an entry."""
        with self._lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM clipboard_history WHERE id = ?", (entry_id,))
            success = cursor.rowcount > 0
            
            conn.commit()
            conn.close()
            
            return success
    
    def clear_all(self) -> int:
        """Clear all entries."""
        with self._lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM clipboard_history")
            count = cursor.fetchone()[0]
            
            cursor.execute("DELETE FROM clipboard_history")
            conn.commit()
            conn.close()
            
            return count
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get clipboard statistics."""
        with self._lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            stats = {}
            
            # Total entries
            cursor.execute("SELECT COUNT(*) FROM clipboard_history")
            stats['total_entries'] = cursor.fetchone()[0]
            
            # Entries by type
            cursor.execute('''
                SELECT content_type, COUNT(*) as count 
                FROM clipboard_history 
                GROUP BY content_type
            ''')
            stats['by_type'] = {row['content_type']: row['count'] for row in cursor.fetchall()}
            
            # Entries by category
            cursor.execute('''
                SELECT category, COUNT(*) as count 
                FROM clipboard_history 
                GROUP BY category
            ''')
            stats['by_category'] = {row['category']: row['count'] for row in cursor.fetchall()}
            
            # Favorites count
            cursor.execute("SELECT COUNT(*) FROM clipboard_history WHERE is_favorite = 1")
            stats['favorites'] = cursor.fetchone()[0]
            
            # Most accessed
            cursor.execute('''
                SELECT content, access_count 
                FROM clipboard_history 
                ORDER BY access_count DESC 
                LIMIT 5
            ''')
            stats['most_accessed'] = [
                {'content': row['content'][:50] + '...' if len(row['content']) > 50 else row['content'],
                 'count': row['access_count']}
                for row in cursor.fetchall()
            ]
            
            conn.close()
            return stats
    
    def export_to_json(self, output_path: str) -> bool:
        """Export all entries to JSON file."""
        with self._lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM clipboard_history ORDER BY created_at DESC")
            rows = cursor.fetchall()
            conn.close()
            
            entries = [dict(row) for row in rows]
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(entries, f, indent=2, ensure_ascii=False, default=str)
            
            return True
    
    def export_to_csv(self, output_path: str) -> bool:
        """Export all entries to CSV file."""
        import csv
        
        with self._lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM clipboard_history ORDER BY created_at DESC")
            rows = cursor.fetchall()
            conn.close()
            
            if not rows:
                return False
            
            with open(output_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                for row in rows:
                    writer.writerow(dict(row))
            
            return True
    
    def export_to_markdown(self, output_path: str) -> bool:
        """Export all entries to Markdown file."""
        with self._lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM clipboard_history ORDER BY created_at DESC")
            rows = cursor.fetchall()
            conn.close()
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("# ClipStack History Export\n\n")
                f.write(f"Generated: {datetime.now().isoformat()}\n\n")
                
                for row in rows:
                    entry = dict(row)
                    f.write(f"## Entry #{entry['id']}\n\n")
                    f.write(f"- **Type**: {entry['content_type']}\n")
                    f.write(f"- **Category**: {entry['category']}\n")
                    f.write(f"- **Created**: {entry['created_at']}\n")
                    f.write(f"- **Access Count**: {entry['access_count']}\n")
                    if entry['is_favorite']:
                        f.write(f"- ⭐ **Favorite**\n")
                    f.write(f"\n```\n{entry['content']}\n```\n\n---\n\n")
            
            return True
