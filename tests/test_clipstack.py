"""
Tests for ContentClassifier
"""

import pytest
from clipstack.classifier import ContentClassifier, ContentType


class TestContentClassifier:
    """Test cases for ContentClassifier."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.classifier = ContentClassifier()
    
    def test_classify_url(self):
        """Test URL classification."""
        content = "https://github.com/example/repo"
        content_type, category, tags = self.classifier.classify(content)
        assert content_type == "url"
        assert category == "web"
        assert "url" in tags
    
    def test_classify_email(self):
        """Test email classification."""
        content = "user@example.com"
        content_type, category, tags = self.classifier.classify(content)
        assert content_type == "email"
        assert category == "contact"
    
    def test_classify_json(self):
        """Test JSON classification."""
        content = '{"name": "test", "value": 123}'
        content_type, category, tags = self.classifier.classify(content)
        assert content_type == "json"
        assert category == "data"
    
    def test_classify_python_code(self):
        """Test Python code classification."""
        content = '''
def hello_world():
    print("Hello, World!")
    return True

if __name__ == "__main__":
    hello_world()
'''
        content_type, category, tags = self.classifier.classify(content)
        assert content_type == "code"
        assert category == "programming"
        assert "python" in tags or "code" in tags
    
    def test_classify_path(self):
        """Test path classification."""
        content = "/home/user/documents/file.txt"
        content_type, category, tags = self.classifier.classify(content)
        assert content_type == "path"
        assert category == "filesystem"
    
    def test_classify_ip_address(self):
        """Test IP address classification."""
        content = "192.168.1.1"
        content_type, category, tags = self.classifier.classify(content)
        assert content_type == "ip_address"
        assert category == "network"
    
    def test_classify_plain_text(self):
        """Test plain text classification."""
        content = "This is just some plain text content."
        content_type, category, tags = self.classifier.classify(content)
        assert content_type == "text"
    
    def test_classify_empty_content(self):
        """Test empty content classification."""
        content = ""
        content_type, category, tags = self.classifier.classify(content)
        assert content_type == "text"
        assert category == "empty"
    
    def test_get_content_preview(self):
        """Test content preview generation."""
        content = "This is a long piece of content that should be truncated for preview purposes."
        preview = self.classifier.get_content_preview(content, 30)
        assert len(preview) <= 33  # 30 + "..."
        assert preview.endswith("...")
    
    def test_is_sensitive(self):
        """Test sensitive content detection."""
        assert self.classifier.is_sensitive("test@email.com", "email") is True
        assert self.classifier.is_sensitive("some text", "text") is False
    
    def test_suggest_tags(self):
        """Test tag suggestion."""
        tags = self.classifier.suggest_tags("https://example.com", "url")
        assert "url" in tags
        assert "short" in tags or "medium" in tags
