"""
Audio Steganography Package
"""

from .modules.core import AudioStegoCore
from .modules.converter import AudioConverter
from .modules.encryption import CryptoModule, EncryptedStegoWrapper
from .modules.analyzer import AudioAnalyzer

__version__ = '1.0.0'
__author__ = 'tipichniy340-tech'

__all__ = [
    'AudioStegoCore',
    'AudioConverter',
    'CryptoModule',
    'EncryptedStegoWrapper',
    'AudioAnalyzer',
]
