"""
Content Classifier Module - Intelligent content classification and sensitive data detection.
内容分类模块 - 智能内容分类与敏感数据检测。
"""

import re
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple


class ContentType(Enum):
    """Content type enumeration."""
    TEXT = "text"
    CODE = "code"
    URL = "url"
    EMAIL = "email"
    PASSWORD = "password"
    API_KEY = "api_key"
    JSON = "json"
    COMMAND = "command"
    PATH = "path"
    IP_ADDRESS = "ip_address"
    PHONE = "phone"
    CREDIT_CARD = "credit_card"


@dataclass
class ClassificationResult:
    """Result of content classification."""
    content_type: ContentType
    is_sensitive: bool
    confidence: float
    tags: List[str]
    language: Optional[str] = None
    warnings: List[str] = None
    
    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []


class ContentClassifier:
    """
    Intelligent content classifier with sensitive data detection.
    
    Features:
    - Automatic content type detection
    - Sensitive data pattern matching
    - Programming language detection
    - Security warning generation
    """
    
    # Sensitive data patterns
    SENSITIVE_PATTERNS = {
        "api_key": [
            r"(?i)(api[_-]?key|apikey)\s*[=:]\s*['\"]?([a-zA-Z0-9_-]{20,})['\"]?",
            r"(?i)(secret[_-]?key|secretkey)\s*[=:]\s*['\"]?([a-zA-Z0-9_-]{20,})['\"]?",
            r"(?i)(access[_-]?token|accesstoken)\s*[=:]\s*['\"]?([a-zA-Z0-9_-]{20,})['\"]?",
            r"sk-[a-zA-Z0-9]{20,}",  # OpenAI style
            r"ghp_[a-zA-Z0-9]{36}",  # GitHub PAT
            r"xox[baprs]-[a-zA-Z0-9-]+",  # Slack tokens
        ],
        "password": [
            r"(?i)(password|passwd|pwd)\s*[=:]\s*['\"]?([^'\"\\s]{8,})['\"]?",
            r"(?i)(db[_-]?password)\s*[=:]\s*['\"]?([^'\"\\s]{8,})['\"]?",
        ],
        "private_key": [
            r"-----BEGIN (?:RSA |EC |DSA )?PRIVATE KEY-----",
            r"-----BEGIN PGP PRIVATE KEY BLOCK-----",
        ],
        "aws_credentials": [
            r"(?i)aws_access_key_id\s*[=:]\s*['\"]?([A-Z0-9]{20})['\"]?",
            r"(?i)aws_secret_access_key\s*[=:]\s*['\"]?([a-zA-Z0-9/+=]{40})['\"]?",
        ],
        "credit_card": [
            r"\b(?:\d{4}[-\s]?){3}\d{4}\b",  # Standard format
            r"\b\d{13,16}\b",  # Raw numbers
        ],
    }
    
    # Content type patterns
    CONTENT_PATTERNS = {
        ContentType.URL: [
            r"https?://[^\s<>\"{}|\\^`\[\]]+",
            r"www\.[a-zA-Z0-9][-a-zA-Z0-9]*\.[a-zA-Z]{2,}",
        ],
        ContentType.EMAIL: [
            r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        ],
        ContentType.IP_ADDRESS: [
            r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
            r"\b(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}\b",
        ],
        ContentType.JSON: [
            r"^\s*[\[{]",
            r"\"[a-zA-Z_][a-zA-Z0-9_]*\"\s*:",
        ],
        ContentType.COMMAND: [
            r"^\s*(?:sudo\s+)?(?:apt|yum|brew|pip|npm|git|docker|kubectl|aws)\s+",
            r"^\s*(?:cd|ls|cat|grep|find|chmod|chown)\s+",
        ],
        ContentType.PATH: [
            r"(?:^|[\"'\s])(?:/[\w.-]+)+/?",
            r"(?:^|[\"'\s])[A-Za-z]:\\[\w.-]+\\?",
            r"(?:^|[\"'\s])~/?[\w.-]*",
        ],
        ContentType.PHONE: [
            r"\+?1?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}",
            r"\+?[1-9]\d{1,14}",
        ],
    }
    
    # Programming language patterns
    LANGUAGE_PATTERNS = {
        "python": [
            r"\bdef\s+\w+\s*\(",
            r"\bclass\s+\w+.*:",
            r"\bimport\s+\w+",
            r"\bfrom\s+\w+\s+import",
            r"@\w+\s*\ndef\s+",  # Decorators
        ],
        "javascript": [
            r"\bfunction\s+\w+\s*\(",
            r"\bconst\s+\w+\s*=",
            r"\blet\s+\w+\s*=",
            r"\bvar\s+\w+\s*=",
            r"=>\s*\{",
            r"\.then\s*\(",
        ],
        "typescript": [
            r":\s*(?:string|number|boolean|any)\b",
            r"interface\s+\w+",
            r"type\s+\w+\s*=",
        ],
        "java": [
            r"\bpublic\s+class\s+\w+",
            r"\bprivate\s+\w+\s+\w+",
            r"\bSystem\.out\.println",
        ],
        "go": [
            r"\bfunc\s+\w+\s*\(",
            r"\bpackage\s+\w+",
            r"\bimport\s*\(",
            r":=\s*",
        ],
        "rust": [
            r"\bfn\s+\w+\s*\(",
            r"\blet\s+mut\s+",
            r"\bimpl\s+\w+",
            r"->\s*\w+",
        ],
        "sql": [
            r"\bSELECT\s+.+\s+FROM\b",
            r"\bINSERT\s+INTO\b",
            r"\bUPDATE\s+.+\s+SET\b",
            r"\bCREATE\s+TABLE\b",
        ],
        "shell": [
            r"#!/bin/(?:ba)?sh",
            r"\bif\s+\[\[",
            r"\bfor\s+\w+\s+in\s+",
            r"\$\{\w+\}",
        ],
        "html": [
            r"<!DOCTYPE\s+html",
            r"<html[>\s]",
            r"<(?:div|span|p|a|script|style)[>\s]",
        ],
        "css": [
            r"\{[^}]*:\s*[^;]+;",
            r"@media\s+",
            r"\.[a-zA-Z][\w-]*\s*\{",
        ],
        "yaml": [
            r"^\s*[\w-]+:\s*$",
            r"^\s*-?\s*[\w-]+:",
            r"^\s*-\s+\w+",
        ],
        "markdown": [
            r"^#+\s+\w+",
            r"\[.+\]\(.+\)",
            r"```",
            r"^\s*[-*+]\s+\w+",
        ],
    }
    
    def classify(self, content: str) -> ClassificationResult:
        """
        Classify clipboard content.
        
        Args:
            content: Clipboard content to classify
            
        Returns:
            ClassificationResult with type, sensitivity, and tags
        """
        if not content or not content.strip():
            return ClassificationResult(
                content_type=ContentType.TEXT,
                is_sensitive=False,
                confidence=1.0,
                tags=["empty"]
            )
        
        # Check for sensitive data first
        is_sensitive, sensitive_types = self._check_sensitive(content)
        
        # Determine content type
        content_type, confidence = self._detect_content_type(content)
        
        # Detect programming language if code
        language = None
        if content_type == ContentType.CODE:
            language = self._detect_language(content)
        
        # Generate tags
        tags = self._generate_tags(content, content_type, language, sensitive_types)
        
        # Generate warnings
        warnings = []
        if is_sensitive:
            warnings.append(f"⚠️ Contains sensitive data: {', '.join(sensitive_types)}")
        
        return ClassificationResult(
            content_type=content_type,
            is_sensitive=is_sensitive,
            confidence=confidence,
            tags=tags,
            language=language,
            warnings=warnings
        )
    
    def _check_sensitive(self, content: str) -> Tuple[bool, List[str]]:
        """
        Check if content contains sensitive data.
        
        Args:
            content: Content to check
            
        Returns:
            Tuple of (is_sensitive, list of sensitive types found)
        """
        found_types = []
        
        for sensitive_type, patterns in self.SENSITIVE_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
                    found_types.append(sensitive_type)
                    break
        
        return len(found_types) > 0, found_types
    
    def _detect_content_type(self, content: str) -> Tuple[ContentType, float]:
        """
        Detect the primary content type.
        
        Args:
            content: Content to analyze
            
        Returns:
            Tuple of (ContentType, confidence)
        """
        scores = {}
        
        # Check each content type
        for content_type, patterns in self.CONTENT_PATTERNS.items():
            score = 0
            for pattern in patterns:
                matches = re.findall(pattern, content, re.MULTILINE | re.IGNORECASE)
                score += len(matches)
            if score > 0:
                scores[content_type] = score
        
        # Check for code (multiple language patterns)
        code_score = 0
        for lang_patterns in self.LANGUAGE_PATTERNS.values():
            for pattern in lang_patterns:
                if re.search(pattern, content, re.MULTILINE):
                    code_score += 1
        
        if code_score >= 2:
            scores[ContentType.CODE] = code_score * 2
        
        # Check for JSON specifically
        content_stripped = content.strip()
        if content_stripped.startswith('{') or content_stripped.startswith('['):
            try:
                import json
                json.loads(content)
                scores[ContentType.JSON] = 10
            except (json.JSONDecodeError, ValueError):
                pass
        
        # Return highest scoring type
        if not scores:
            return ContentType.TEXT, 0.5
        
        best_type = max(scores, key=scores.get)
        total_score = sum(scores.values())
        confidence = scores[best_type] / max(total_score, 1)
        
        return best_type, min(confidence, 1.0)
    
    def _detect_language(self, content: str) -> Optional[str]:
        """
        Detect programming language.
        
        Args:
            content: Code content
            
        Returns:
            Detected language or None
        """
        language_scores = {}
        
        for language, patterns in self.LANGUAGE_PATTERNS.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, content, re.MULTILINE):
                    score += 1
            if score > 0:
                language_scores[language] = score
        
        if not language_scores:
            return None
        
        return max(language_scores, key=language_scores.get)
    
    def _generate_tags(
        self,
        content: str,
        content_type: ContentType,
        language: Optional[str],
        sensitive_types: List[str]
    ) -> List[str]:
        """
        Generate tags for content.
        
        Args:
            content: Content string
            content_type: Detected content type
            language: Detected programming language
            sensitive_types: List of sensitive data types found
            
        Returns:
            List of tags
        """
        tags = [content_type.value]
        
        if language:
            tags.append(language)
        
        if sensitive_types:
            tags.extend([f"sensitive:{t}" for t in sensitive_types])
        
        # Add length-based tags
        if len(content) < 100:
            tags.append("short")
        elif len(content) > 1000:
            tags.append("long")
        
        # Add line count tag
        lines = content.count('\n') + 1
        if lines > 10:
            tags.append("multiline")
        
        return list(set(tags))
    
    def get_category_for_type(self, content_type: ContentType) -> str:
        """
        Get display category for content type.
        
        Args:
            content_type: Content type enum
            
        Returns:
            Category string for storage
        """
        category_map = {
            ContentType.TEXT: "text",
            ContentType.CODE: "code",
            ContentType.URL: "url",
            ContentType.EMAIL: "contact",
            ContentType.PASSWORD: "credential",
            ContentType.API_KEY: "credential",
            ContentType.JSON: "data",
            ContentType.COMMAND: "command",
            ContentType.PATH: "path",
            ContentType.IP_ADDRESS: "network",
            ContentType.PHONE: "contact",
            ContentType.CREDIT_CARD: "credential",
        }
        return category_map.get(content_type, "text")
