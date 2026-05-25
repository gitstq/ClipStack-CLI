"""
Tests for ClipboardDatabase
"""

import pytest
import tempfile
import os
from clipstack.database import ClipboardDatabase


class TestClipboardDatabase:
    """Test cases for ClipboardDatabase."""
    
    def setup_method(self):
        """Setup test fixtures."""
        # Use a temporary database for each test
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_clipstack.db")
        self.db = ClipboardDatabase(self.db_path)
    
    def teardown_method(self):
        """Cleanup test fixtures."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_add_entry(self):
        """Test adding a new entry."""
        entry_id = self.db.add_entry(
            content="Test content",
            content_type="text",
            category="test"
        )
        assert entry_id is not None
        assert isinstance(entry_id, int)
    
    def test_add_duplicate_entry(self):
        """Test adding duplicate content updates access count."""
        self.db.add_entry(content="Duplicate content")
        entry_id2 = self.db.add_entry(content="Duplicate content")
        
        # Should return same ID for duplicate
        entries = self.db.get_recent()
        assert len(entries) == 1
        assert entries[0]['access_count'] == 2
    
    def test_get_entry(self):
        """Test retrieving an entry."""
        entry_id = self.db.add_entry(content="Test entry")
        entry = self.db.get_entry(entry_id)
        
        assert entry is not None
        assert entry['content'] == "Test entry"
    
    def test_get_entry_not_found(self):
        """Test retrieving non-existent entry."""
        entry = self.db.get_entry(99999)
        assert entry is None
    
    def test_get_recent(self):
        """Test retrieving recent entries."""
        for i in range(10):
            self.db.add_entry(content=f"Entry {i}")
        
        entries = self.db.get_recent(limit=5)
        assert len(entries) == 5
    
    def test_search(self):
        """Test searching entries."""
        self.db.add_entry(content="Python programming")
        self.db.add_entry(content="JavaScript code")
        self.db.add_entry(content="Python testing")
        
        results = self.db.search("Python")
        assert len(results) == 2
    
    def test_get_by_type(self):
        """Test filtering by content type."""
        self.db.add_entry(content="https://example.com", content_type="url")
        self.db.add_entry(content="user@test.com", content_type="email")
        self.db.add_entry(content="https://github.com", content_type="url")
        
        entries = self.db.get_by_type("url")
        assert len(entries) == 2
    
    def test_toggle_favorite(self):
        """Test toggling favorite status."""
        entry_id = self.db.add_entry(content="Favorite test")
        
        # Toggle to favorite
        self.db.toggle_favorite(entry_id)
        entry = self.db.get_entry(entry_id)
        assert entry['is_favorite'] == 1
        
        # Toggle back
        self.db.toggle_favorite(entry_id)
        entry = self.db.get_entry(entry_id)
        assert entry['is_favorite'] == 0
    
    def test_get_favorites(self):
        """Test retrieving favorites."""
        entry_id = self.db.add_entry(content="Favorite entry")
        self.db.add_entry(content="Regular entry")
        self.db.toggle_favorite(entry_id)
        
        favorites = self.db.get_favorites()
        assert len(favorites) == 1
        assert favorites[0]['content'] == "Favorite entry"
    
    def test_add_tag(self):
        """Test adding tags."""
        entry_id = self.db.add_entry(content="Tagged content")
        self.db.add_tag(entry_id, "important")
        
        entry = self.db.get_entry(entry_id)
        import json
        tags = json.loads(entry['tags'])
        assert "important" in tags
    
    def test_remove_tag(self):
        """Test removing tags."""
        entry_id = self.db.add_entry(content="Tagged content", tags=["tag1", "tag2"])
        self.db.remove_tag(entry_id, "tag1")
        
        entry = self.db.get_entry(entry_id)
        import json
        tags = json.loads(entry['tags'])
        assert "tag1" not in tags
        assert "tag2" in tags
    
    def test_delete_entry(self):
        """Test deleting an entry."""
        entry_id = self.db.add_entry(content="To be deleted")
        
        result = self.db.delete_entry(entry_id)
        assert result is True
        
        entry = self.db.get_entry(entry_id)
        assert entry is None
    
    def test_clear_all(self):
        """Test clearing all entries."""
        for i in range(5):
            self.db.add_entry(content=f"Entry {i}")
        
        count = self.db.clear_all()
        assert count == 5
        
        entries = self.db.get_recent()
        assert len(entries) == 0
    
    def test_get_statistics(self):
        """Test getting statistics."""
        self.db.add_entry(content="https://example.com", content_type="url")
        self.db.add_entry(content="user@test.com", content_type="email")
        self.db.add_entry(content="Some text", content_type="text")
        
        stats = self.db.get_statistics()
        
        assert stats['total_entries'] == 3
        assert 'url' in stats['by_type']
        assert 'email' in stats['by_type']
    
    def test_export_to_json(self):
        """Test exporting to JSON."""
        self.db.add_entry(content="Export test")
        
        export_path = os.path.join(self.temp_dir, "export.json")
        result = self.db.export_to_json(export_path)
        
        assert result is True
        assert os.path.exists(export_path)
    
    def test_export_to_csv(self):
        """Test exporting to CSV."""
        self.db.add_entry(content="Export test")
        
        export_path = os.path.join(self.temp_dir, "export.csv")
        result = self.db.export_to_csv(export_path)
        
        assert result is True
        assert os.path.exists(export_path)
    
    def test_export_to_markdown(self):
        """Test exporting to Markdown."""
        self.db.add_entry(content="Export test")
        
        export_path = os.path.join(self.temp_dir, "export.md")
        result = self.db.export_to_markdown(export_path)
        
        assert result is True
        assert os.path.exists(export_path)
