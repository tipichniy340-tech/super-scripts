"""
Encryption Module for Audio Steganography
Provides AES encryption for messages before hiding them in audio files
"""

import base64
import hashlib
from typing import Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class CryptoModule:
    """Encrypt and decrypt messages using AES-256 via Fernet"""
    
    def __init__(self):
        self.salt_length = 16
    
    def _derive_key(self, password: str, salt: bytes) -> bytes:
        """Derive a 32-byte key from password using PBKDF2"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100_000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))
    
    def encrypt(self, message: str, password: str) -> str:
        """
        Encrypt a message with a password
        
        Args:
            message: Plain text message to encrypt
            password: Password for encryption
            
        Returns:
            Encrypted message (base64 encoded, includes salt)
        """
        import os
        salt = os.urandom(self.salt_length)
        key = self._derive_key(password, salt)
        fernet = Fernet(key)
        
        encrypted_bytes = fernet.encrypt(message.encode('utf-8'))
        
        # Prepend salt to encrypted data and encode as base64
        combined = salt + encrypted_bytes
        return base64.b64encode(combined).decode('utf-8')
    
    def decrypt(self, encrypted_message: str, password: str) -> Optional[str]:
        """
        Decrypt a message with a password
        
        Args:
            encrypted_message: Encrypted message (base64 encoded)
            password: Password for decryption
            
        Returns:
            Decrypted message or None if decryption fails
        """
        try:
            combined = base64.b64decode(encrypted_message.encode('utf-8'))
            
            # Extract salt and encrypted data
            salt = combined[:self.salt_length]
            encrypted_bytes = combined[self.salt_length:]
            
            # Derive key from password
            key = self._derive_key(password, salt)
            fernet = Fernet(key)
            
            decrypted_bytes = fernet.decrypt(encrypted_bytes)
            return decrypted_bytes.decode('utf-8')
            
        except Exception as e:
            print(f"Decryption error: {e}")
            return None
    
    def generate_password(self, length: int = 32) -> str:
        """Generate a random secure password"""
        import secrets
        alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    
    def hash_password(self, password: str) -> str:
        """Create a SHA-256 hash of a password"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify a password against its hash"""
        return self.hash_password(password) == hashed


class EncryptedStegoWrapper:
    """Wrapper that combines encryption with steganography"""
    
    def __init__(self, crypto_module: CryptoModule, stego_core):
        self.crypto = crypto_module
        self.stego = stego_core
    
    def encode_encrypted(
        self,
        audio_path: str,
        message: str,
        password: str,
        output_path: str
    ) -> bool:
        """
        Encrypt a message and hide it in an audio file
        
        Args:
            audio_path: Path to input audio file
            message: Message to encrypt and hide
            password: Password for encryption
            output_path: Path for output audio file
            
        Returns:
            True if successful
        """
        # First encrypt the message
        encrypted_message = self.crypto.encrypt(message, password)
        
        # Then hide it in the audio file
        return self.stego.encode(audio_path, encrypted_message, output_path)
    
    def decode_decrypted(
        self,
        audio_path: str,
        password: str
    ) -> Optional[str]:
        """
        Extract and decrypt a message from an audio file
        
        Args:
            audio_path: Path to audio file with hidden message
            password: Password for decryption
            
        Returns:
            Decrypted message or None
        """
        # First extract the encrypted message
        encrypted_message = self.stego.decode(audio_path)
        
        if encrypted_message is None:
            return None
        
        # Then decrypt it
        return self.crypto.decrypt(encrypted_message, password)
