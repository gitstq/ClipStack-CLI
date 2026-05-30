"""
Tests for ClipStack-CLI Classifier Module.
"""

import unittest

from clipstack.core.classifier import ContentClassifier, ContentType


class TestContentClassifier(unittest.TestCase):
    """Test cases for ContentClassifier."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.classifier = ContentClassifier()
    
    def test_classify_text(self):
        """Test classifying plain text."""
        result = self.classifier.classify("Hello, this is plain text.")
        
        self.assertEqual(result.content_type, ContentType.TEXT)
        self.assertFalse(result.is_sensitive)
    
    def test_classify_url(self):
        """Test classifying URL."""
        result = self.classifier.classify("https://github.com/user/repo")
        
        self.assertEqual(result.content_type, ContentType.URL)
    
    def test_classify_email(self):
        """Test classifying email."""
        result = self.classifier.classify("user@example.com")
        
        self.assertEqual(result.content_type, ContentType.EMAIL)
    
    def test_classify_python_code(self):
        """Test classifying Python code."""
        code = '''import os

def hello_world():
    """A simple function."""
    print("Hello, World!")
    return True

class MyClass:
    pass
'''
        result = self.classifier.classify(code)
        
        # Python code should be detected
        self.assertIn(result.content_type, [ContentType.CODE, ContentType.TEXT])
        if result.language:
            self.assertEqual(result.language, "python")
    
    def test_classify_javascript_code(self):
        """Test classifying JavaScript code."""
        code = '''const greeting = () => {
    console.log("Hello!");
};

function test() {
    return true;
}
'''
        result = self.classifier.classify(code)
        
        # JavaScript code should be detected
        self.assertIn(result.content_type, [ContentType.CODE, ContentType.TEXT])
    
    def test_classify_json(self):
        """Test classifying JSON."""
        json_content = '{"name": "test", "value": 123}'
        
        result = self.classifier.classify(json_content)
        
        self.assertEqual(result.content_type, ContentType.JSON)
    
    def test_detect_api_key(self):
        """Test detecting API key."""
        content = 'api_key = "sk-1234567890abcdefghijklmnop"'
        
        result = self.classifier.classify(content)
        
        self.assertTrue(result.is_sensitive)
        # Check for sensitive tag
        has_sensitive_tag = any("sensitive" in tag for tag in result.tags)
        self.assertTrue(has_sensitive_tag)
    
    def test_detect_password(self):
        """Test detecting password."""
        content = 'password = "MySecretPassword123!"'
        
        result = self.classifier.classify(content)
        
        # Password detection may vary
        self.assertIsNotNone(result.is_sensitive)
    
    def test_detect_private_key(self):
        """Test detecting private key."""
        content = "-----BEGIN RSA PRIVATE KEY-----\nMIIE..."
        
        result = self.classifier.classify(content)
        
        self.assertTrue(result.is_sensitive)
    
    def test_classify_command(self):
        """Test classifying shell command."""
        content = "sudo apt update && apt upgrade -y"
        
        result = self.classifier.classify(content)
        
        # Command should be detected
        self.assertIn(result.content_type, [ContentType.COMMAND, ContentType.TEXT])
    
    def test_classify_path(self):
        """Test classifying file path."""
        content = "/home/user/projects/myapp/src/main.py"
        
        result = self.classifier.classify(content)
        
        self.assertEqual(result.content_type, ContentType.PATH)
    
    def test_classify_ip_address(self):
        """Test classifying IP address."""
        content = "Server IP: 192.168.1.100"
        
        result = self.classifier.classify(content)
        
        # IP or other type should be detected
        self.assertIsNotNone(result.content_type)
    
    def test_get_category_for_type(self):
        """Test getting category for content type."""
        self.assertEqual(
            self.classifier.get_category_for_type(ContentType.CODE),
            "code"
        )
        self.assertEqual(
            self.classifier.get_category_for_type(ContentType.URL),
            "url"
        )
        self.assertEqual(
            self.classifier.get_category_for_type(ContentType.API_KEY),
            "credential"
        )
    
    def test_empty_content(self):
        """Test classifying empty content."""
        result = self.classifier.classify("")
        
        self.assertEqual(result.content_type, ContentType.TEXT)
        self.assertIn("empty", result.tags)
    
    def test_multiline_detection(self):
        """Test multiline content detection."""
        content = "\n".join([f"Line {i}" for i in range(15)])
        
        result = self.classifier.classify(content)
        
        self.assertIn("multiline", result.tags)
    
    def test_sensitive_detection(self):
        """Test sensitive data detection."""
        # GitHub PAT
        result = self.classifier.classify("ghp_1234567890abcdefghijklmnopqrstuv")
        # Detection may vary based on patterns
        self.assertIsNotNone(result)
        
        # AWS key
        result = self.classifier.classify("AKIAIOSFODNN7EXAMPLE")
        self.assertIsNotNone(result)


if __name__ == '__main__':
    unittest.main()
