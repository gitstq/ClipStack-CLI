"""
Content Classifier Module - Intelligent content type detection
"""

import re
from typing import Tuple, List, Optional
from enum import Enum


class ContentType(Enum):
    """Supported content types for classification."""
    TEXT = "text"
    URL = "url"
    EMAIL = "email"
    PHONE = "phone"
    IP_ADDRESS = "ip_address"
    JSON = "json"
    XML = "xml"
    HTML = "html"
    CODE = "code"
    MARKDOWN = "markdown"
    PATH = "path"
    COMMAND = "command"
    NUMBER = "number"
    DATE = "date"
    CREDIT_CARD = "credit_card"
    BASE64 = "base64"
    HASH = "hash"
    UUID = "uuid"


class ContentClassifier:
    """Intelligent content type classifier for clipboard content."""
    
    # Regex patterns for different content types
    PATTERNS = {
        ContentType.URL: [
            re.compile(r'^https?://[^\s]+$'),
            re.compile(r'^ftp://[^\s]+$'),
            re.compile(r'^www\.[^\s]+\.[a-z]{2,}', re.IGNORECASE),
        ],
        ContentType.EMAIL: [
            re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'),
        ],
        ContentType.PHONE: [
            re.compile(r'^\+?[\d\s\-\(\)]{7,20}$'),
            re.compile(r'^\d{3}[-.\s]?\d{3}[-.\s]?\d{4}$'),
        ],
        ContentType.IP_ADDRESS: [
            re.compile(r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'),
            re.compile(r'^[0-9a-fA-F:]+$'),  # IPv6 simplified
        ],
        ContentType.JSON: [
            re.compile(r'^\s*[\[{]', re.DOTALL),
        ],
        ContentType.XML: [
            re.compile(r'^\s*<\?xml', re.IGNORECASE),
            re.compile(r'^\s*<[a-zA-Z][^>]*>.*</[a-zA-Z][^>]*>\s*$', re.DOTALL),
        ],
        ContentType.HTML: [
            re.compile(r'<(!DOCTYPE|html|head|body|div|span|p|a|table|form)', re.IGNORECASE),
        ],
        ContentType.MARKDOWN: [
            re.compile(r'^#{1,6}\s'),
            re.compile(r'\[.+\]\(.+\)'),
            re.compile(r'^\s*[-*+]\s'),
            re.compile(r'^\s*\d+\.\s'),
            re.compile(r'`[^`]+`'),
            re.compile(r'\*\*[^*]+\*\*'),
        ],
        ContentType.PATH: [
            re.compile(r'^[A-Za-z]:\\'),  # Windows
            re.compile(r'^/(?:usr|home|etc|var|opt|tmp)/'),  # Linux
            re.compile(r'^~/'),  # Home directory
            re.compile(r'^\./'),  # Relative path
        ],
        ContentType.COMMAND: [
            re.compile(r'^(sudo|apt|yum|brew|pip|npm|git|docker|kubectl|python|node)\s'),
            re.compile(r'\|\s*(grep|awk|sed|sort|uniq|head|tail)'),
            re.compile(r'&&\s*'),
        ],
        ContentType.NUMBER: [
            re.compile(r'^-?\d+\.?\d*$'),
            re.compile(r'^\$?\d{1,3}(,\d{3})*(\.\d{2})?$'),
        ],
        ContentType.DATE: [
            re.compile(r'^\d{4}[-/]\d{1,2}[-/]\d{1,2}$'),
            re.compile(r'^\d{1,2}[-/]\d{1,2}[-/]\d{4}$'),
            re.compile(r'^\d{1,2}\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)', re.IGNORECASE),
        ],
        ContentType.CREDIT_CARD: [
            re.compile(r'^(?:\d{4}[-\s]?){3}\d{4}$'),
            re.compile(r'^(?:3[47]\d{2}|4\d{3}|5[1-5]\d{2}|6(?:011|5\d{2}))\d{12,15}$'),
        ],
        ContentType.BASE64: [
            re.compile(r'^[A-Za-z0-9+/]+=*$'),
        ],
        ContentType.HASH: [
            re.compile(r'^[a-fA-F0-9]{32}$'),  # MD5
            re.compile(r'^[a-fA-F0-9]{40}$'),  # SHA1
            re.compile(r'^[a-fA-F0-9]{64}$'),  # SHA256
        ],
        ContentType.UUID: [
            re.compile(r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'),
        ],
    }
    
    # Code language indicators
    CODE_INDICATORS = [
        ('python', [r'def\s+\w+\s*\(', r'import\s+\w+', r'from\s+\w+\s+import', r'if\s+__name__\s*==\s*[\'"]__main__[\'"]']),
        ('javascript', [r'function\s+\w+\s*\(', r'const\s+\w+\s*=', r'let\s+\w+\s*=', r'=>\s*\{', r'async\s+function']),
        ('java', [r'public\s+class', r'private\s+\w+', r'System\.out\.println', r'import\s+java\.']),
        ('c', [r'#include\s*<', r'int\s+main\s*\(', r'printf\s*\(', r'struct\s+\w+']),
        ('cpp', [r'#include\s*<', r'std::', r'cout\s*<<', r'class\s+\w+\s*\{']),
        ('go', [r'package\s+\w+', r'func\s+\w+\s*\(', r'import\s*\(', r'fmt\.Print']),
        ('rust', [r'fn\s+\w+\s*\(', r'let\s+mut', r'impl\s+\w+', r'use\s+std::']),
        ('sql', [r'SELECT\s+', r'INSERT\s+INTO', r'UPDATE\s+\w+\s+SET', r'CREATE\s+TABLE', r'FROM\s+\w+']),
        ('shell', [r'#!/bin/', r'echo\s+', r'export\s+\w+=', r'if\s+\[\[', r'for\s+\w+\s+in']),
    ]
    
    def __init__(self):
        """Initialize the classifier."""
        pass
    
    def classify(self, content: str) -> Tuple[str, str, List[str]]:
        """Classify the content type.
        
        Args:
            content: The content to classify
            
        Returns:
            Tuple of (content_type, category, tags)
        """
        if not content or not content.strip():
            return "text", "empty", []
        
        content = content.strip()
        tags = []
        
        # Check for specific patterns
        for content_type, patterns in self.PATTERNS.items():
            for pattern in patterns:
                if pattern.match(content):
                    return content_type.value, self._get_category(content_type), [content_type.value]
        
        # Check for JSON
        if self._is_json(content):
            return "json", "data", ["json", "structured"]
        
        # Check for code
        code_lang = self._detect_code_language(content)
        if code_lang:
            return "code", "programming", [code_lang, "code"]
        
        # Check for markdown
        if self._is_markdown(content):
            return "markdown", "document", ["markdown", "formatted"]
        
        # Default to text
        word_count = len(content.split())
        if word_count < 10:
            return "text", "snippet", ["short"]
        elif word_count < 100:
            return "text", "paragraph", ["medium"]
        else:
            return "text", "document", ["long"]
    
    def _get_category(self, content_type: ContentType) -> str:
        """Get category for a content type."""
        categories = {
            ContentType.URL: "web",
            ContentType.EMAIL: "contact",
            ContentType.PHONE: "contact",
            ContentType.IP_ADDRESS: "network",
            ContentType.JSON: "data",
            ContentType.XML: "data",
            ContentType.HTML: "web",
            ContentType.CODE: "programming",
            ContentType.MARKDOWN: "document",
            ContentType.PATH: "filesystem",
            ContentType.COMMAND: "system",
            ContentType.NUMBER: "numeric",
            ContentType.DATE: "temporal",
            ContentType.CREDIT_CARD: "sensitive",
            ContentType.BASE64: "encoded",
            ContentType.HASH: "security",
            ContentType.UUID: "identifier",
        }
        return categories.get(content_type, "general")
    
    def _is_json(self, content: str) -> bool:
        """Check if content is valid JSON."""
        try:
            import json
            json.loads(content)
            return True
        except (json.JSONDecodeError, ValueError):
            return False
    
    def _is_markdown(self, content: str) -> bool:
        """Check if content contains markdown."""
        markdown_count = 0
        for pattern in self.PATTERNS[ContentType.MARKDOWN]:
            if pattern.search(content):
                markdown_count += 1
        return markdown_count >= 2
    
    def _detect_code_language(self, content: str) -> Optional[str]:
        """Detect programming language from code content."""
        max_matches = 0
        detected_lang = None
        
        for lang, patterns in self.CODE_INDICATORS:
            matches = 0
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    matches += 1
            if matches > max_matches:
                max_matches = matches
                detected_lang = lang
        
        # Require at least 2 matches to be confident
        if max_matches >= 2:
            return detected_lang
        
        return None
    
    def get_content_preview(self, content: str, max_length: int = 100) -> str:
        """Get a preview of the content."""
        if not content:
            return ""
        
        # Remove extra whitespace
        preview = ' '.join(content.split())
        
        if len(preview) <= max_length:
            return preview
        
        return preview[:max_length - 3] + "..."
    
    def is_sensitive(self, content: str, content_type: str) -> bool:
        """Check if content might be sensitive."""
        sensitive_types = {
            'credit_card', 'email', 'phone', 'ip_address', 'hash', 'base64'
        }
        return content_type in sensitive_types
    
    def suggest_tags(self, content: str, content_type: str) -> List[str]:
        """Suggest tags based on content analysis."""
        tags = [content_type]
        
        # Add length-based tags
        length = len(content)
        if length < 50:
            tags.append("short")
        elif length < 500:
            tags.append("medium")
        else:
            tags.append("long")
        
        # Add language tag for code
        if content_type == "code":
            lang = self._detect_code_language(content)
            if lang:
                tags.append(lang)
        
        # Add sensitive tag
        if self.is_sensitive(content, content_type):
            tags.append("sensitive")
        
        return list(set(tags))
