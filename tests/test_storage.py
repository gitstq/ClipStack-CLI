"""
Tests for ClipStack-CLI Storage Module.
"""

import os
import shutil
import tempfile
import unittest

from clipstack.core.storage import ClipboardStorage


class TestClipboardStorage(unittest.TestCase):
    """Test cases for ClipboardStorage."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_clipstack.db")
        self.storage = ClipboardStorage(db_path=self.db_path)
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Close any open connections
        del self.storage
        
        # Remove entire temp directory
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_add_entry(self):
        """Test adding a clipboard entry."""
        entry_id = self.storage.add_entry(
            content="test content",
            category="text",
            tags=["test"]
        )
        
        self.assertIsInstance(entry_id, int)
        self.assertGreater(entry_id, 0)
    
    def test_get_entry(self):
        """Test retrieving a clipboard entry."""
        entry_id = self.storage.add_entry(
            content="test content",
            category="text"
        )
        
        entry = self.storage.get_entry(entry_id)
        
        self.assertIsNotNone(entry)
        self.assertEqual(entry["content"], "test content")
        self.assertEqual(entry["category"], "text")
    
    def test_get_all_entries(self):
        """Test retrieving all entries."""
        self.storage.add_entry(content="entry 1", category="text")
        self.storage.add_entry(content="entry 2", category="code")
        
        entries = self.storage.get_all_entries()
        
        self.assertEqual(len(entries), 2)
    
    def test_delete_entry(self):
        """Test deleting an entry."""
        entry_id = self.storage.add_entry(content="test content")
        
        result = self.storage.delete_entry(entry_id)
        self.assertTrue(result)
        
        entry = self.storage.get_entry(entry_id)
        self.assertIsNone(entry)
    
    def test_deduplication(self):
        """Test that duplicate content is deduplicated."""
        id1 = self.storage.add_entry(content="duplicate content")
        id2 = self.storage.add_entry(content="duplicate content")
        
        # Should return same ID for duplicate
        self.assertEqual(id1, id2)
        
        # Access count should be incremented
        entry = self.storage.get_entry(id1)
        self.assertEqual(entry["access_count"], 2)
    
    def test_search(self):
        """Test searching entries."""
        self.storage.add_entry(content="python code", category="code")
        self.storage.add_entry(content="javascript code", category="code")
        self.storage.add_entry(content="plain text", category="text")
        
        results = self.storage.get_all_entries(search="code")
        
        self.assertEqual(len(results), 2)
    
    def test_filter_by_category(self):
        """Test filtering by category."""
        self.storage.add_entry(content="code snippet", category="code")
        self.storage.add_entry(content="url link", category="url")
        
        results = self.storage.get_all_entries(category="code")
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["category"], "code")
    
    def test_get_stats(self):
        """Test getting statistics."""
        self.storage.add_entry(content="text", category="text")
        self.storage.add_entry(content="code", category="code", is_sensitive=True)
        
        stats = self.storage.get_stats()
        
        self.assertEqual(stats["total_entries"], 2)
        self.assertEqual(stats["sensitive_entries"], 1)
    
    def test_export_to_json(self):
        """Test exporting to JSON."""
        self.storage.add_entry(content="test content", category="text")
        
        output_path = os.path.join(self.temp_dir, "export.json")
        count = self.storage.export_to_json(output_path)
        
        self.assertEqual(count, 1)
        self.assertTrue(os.path.exists(output_path))
    
    def test_export_to_csv(self):
        """Test exporting to CSV."""
        self.storage.add_entry(content="test content", category="text")
        
        output_path = os.path.join(self.temp_dir, "export.csv")
        count = self.storage.export_to_csv(output_path)
        
        self.assertEqual(count, 1)
        self.assertTrue(os.path.exists(output_path))
    
    def test_clear_all(self):
        """Test clearing all entries."""
        self.storage.add_entry(content="entry 1")
        self.storage.add_entry(content="entry 2")
        
        count = self.storage.clear_all()
        
        self.assertEqual(count, 2)
        
        entries = self.storage.get_all_entries()
        self.assertEqual(len(entries), 0)


if __name__ == '__main__':
    unittest.main()
