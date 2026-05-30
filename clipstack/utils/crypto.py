"""
Crypto Utils Module - Encryption utilities for sensitive clipboard data.
加密工具模块 - 敏感剪贴板数据的加密工具。
"""

import base64
import hashlib
import os
from typing import Optional, Tuple


class CryptoUtils:
    """
    Encryption utilities for sensitive clipboard data.
    
    Features:
    - AES-256-GCM encryption (requires cryptography package)
    - Fallback to simple encoding if cryptography unavailable
    - Secure key derivation
    """
    
    @staticmethod
    def is_encryption_available() -> bool:
        """
        Check if cryptography package is available.
        
        Returns:
            True if encryption is available
        """
        try:
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM
            return True
        except ImportError:
            return False
    
    @staticmethod
    def generate_key(password: str, salt: Optional[bytes] = None) -> Tuple[bytes, bytes]:
        """
        Generate encryption key from password.
        
        Args:
            password: User password
            salt: Optional salt (generated if not provided)
            
        Returns:
            Tuple of (key, salt)
        """
        if salt is None:
            salt = os.urandom(16)
        
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000,
            dklen=32
        )
        
        return key, salt
    
    @staticmethod
    def encrypt(content: str, password: str) -> str:
        """
        Encrypt content with password.
        
        Args:
            content: Content to encrypt
            password: Encryption password
            
        Returns:
            Encrypted content (base64 encoded)
        """
        if CryptoUtils.is_encryption_available():
            return CryptoUtils._encrypt_aes_gcm(content, password)
        else:
            return CryptoUtils._encode_simple(content)
    
    @staticmethod
    def decrypt(encrypted_content: str, password: str) -> str:
        """
        Decrypt content with password.
        
        Args:
            encrypted_content: Encrypted content (base64 encoded)
            password: Decryption password
            
        Returns:
            Decrypted content
        """
        if CryptoUtils.is_encryption_available():
            return CryptoUtils._decrypt_aes_gcm(encrypted_content, password)
        else:
            return CryptoUtils._decode_simple(encrypted_content)
    
    @staticmethod
    def _encrypt_aes_gcm(content: str, password: str) -> str:
        """
        Encrypt using AES-256-GCM.
        
        Args:
            content: Content to encrypt
            password: Encryption password
            
        Returns:
            Base64 encoded encrypted content
        """
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        
        key, salt = CryptoUtils.generate_key(password)
        nonce = os.urandom(12)
        
        aesgcm = AESGCM(key)
        ciphertext = aesgcm.encrypt(nonce, content.encode('utf-8'), None)
        
        # Combine salt + nonce + ciphertext
        combined = salt + nonce + ciphertext
        return base64.b64encode(combined).decode('utf-8')
    
    @staticmethod
    def _decrypt_aes_gcm(encrypted_content: str, password: str) -> str:
        """
        Decrypt using AES-256-GCM.
        
        Args:
            encrypted_content: Base64 encoded encrypted content
            password: Decryption password
            
        Returns:
            Decrypted content
        """
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        from cryptography.exceptions import InvalidTag
        
        combined = base64.b64decode(encrypted_content.encode('utf-8'))
        
        salt = combined[:16]
        nonce = combined[16:28]
        ciphertext = combined[28:]
        
        key, _ = CryptoUtils.generate_key(password, salt)
        
        aesgcm = AESGCM(key)
        
        try:
            plaintext = aesgcm.decrypt(nonce, ciphertext, None)
            return plaintext.decode('utf-8')
        except InvalidTag:
            raise ValueError("Decryption failed - invalid password or corrupted data")
    
    @staticmethod
    def _encode_simple(content: str) -> str:
        """
        Simple base64 encoding (fallback when cryptography unavailable).
        
        Args:
            content: Content to encode
            
        Returns:
            Base64 encoded content
        """
        return base64.b64encode(content.encode('utf-8')).decode('utf-8')
    
    @staticmethod
    def _decode_simple(encoded_content: str) -> str:
        """
        Simple base64 decoding (fallback when cryptography unavailable).
        
        Args:
            encoded_content: Base64 encoded content
            
        Returns:
            Decoded content
        """
        return base64.b64decode(encoded_content.encode('utf-8')).decode('utf-8')


def mask_sensitive_content(content: str, visible_chars: int = 4) -> str:
    """
    Mask sensitive content for display.
    
    Args:
        content: Content to mask
        visible_chars: Number of characters to show at start and end
        
    Returns:
        Masked content
    """
    if len(content) <= visible_chars * 2:
        return "*" * len(content)
    
    return f"{content[:visible_chars]}{'*' * (len(content) - visible_chars * 2)}{content[-visible_chars:]}"


def is_likely_sensitive(content: str) -> bool:
    """
    Quick check if content is likely sensitive.
    
    Args:
        content: Content to check
        
    Returns:
        True if likely sensitive
    """
    sensitive_keywords = [
        "password", "passwd", "pwd", "secret", "token", "api_key", "apikey",
        "private_key", "access_key", "secret_key", "credential", "auth"
    ]
    
    content_lower = content.lower()
    
    for keyword in sensitive_keywords:
        if keyword in content_lower:
            return True
    
    return False
