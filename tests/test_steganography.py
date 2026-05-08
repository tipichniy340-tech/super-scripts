"""
Tests for Audio Steganography Module
"""

import pytest
import wave
import os
import tempfile
from pathlib import Path

from steganography.encoder import encode_message, text_to_bits
from steganography.decoder import decode_message, bits_to_text


# Test fixtures
@pytest.fixture
def sample_audio_file():
    """Create a temporary WAV file for testing."""
    # Create a temporary WAV file
    temp_dir = tempfile.mkdtemp()
    audio_path = os.path.join(temp_dir, 'test_audio.wav')
    
    # Generate a simple WAV file with silence
    with wave.open(audio_path, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(44100)
        # Write 10 seconds of silence (enough for testing)
        frames = b'\x00\x00' * 44100 * 10
        wav_file.writeframes(frames)
    
    yield audio_path
    
    # Cleanup
    if os.path.exists(audio_path):
        os.remove(audio_path)
    os.rmdir(temp_dir)


@pytest.fixture
def output_audio_file():
    """Create a temporary output path."""
    temp_dir = tempfile.mkdtemp()
    output_path = os.path.join(temp_dir, 'output.wav')
    yield output_path
    
    # Cleanup
    if os.path.exists(output_path):
        os.remove(output_path)
    os.rmdir(temp_dir)


# Unit tests for utility functions
class TestUtilityFunctions:
    """Test helper functions."""
    
    def test_text_to_bits(self):
        """Test text to bits conversion."""
        assert text_to_bits('A') == [0, 1, 0, 0, 0, 0, 0, 1]
        assert text_to_bits('AB') == [0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0]
        assert text_to_bits('') == []
    
    def test_bits_to_text(self):
        """Test bits to text conversion."""
        assert bits_to_text([0, 1, 0, 0, 0, 0, 0, 1]) == 'A'
        assert bits_to_text([0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0]) == 'AB'
        assert bits_to_text([]) == ''


# Integration tests for encode/decode
class TestEncodeDecode:
    """Test encoding and decoding functionality."""
    
    def test_encode_and_decode_simple_message(self, sample_audio_file, output_audio_file):
        """Test encoding and decoding a simple message."""
        message = "Hello, World!"
        
        # Encode
        result = encode_message(sample_audio_file, message, output_audio_file)
        assert result is True
        
        # Decode
        decoded = decode_message(output_audio_file)
        assert decoded == message
    
    def test_encode_and_decode_empty_message_fails(self, sample_audio_file, output_audio_file):
        """Test that empty message raises an error."""
        with pytest.raises(ValueError, match="Message cannot be empty"):
            encode_message(sample_audio_file, "", output_audio_file)
    
    def test_encode_and_decode_long_message(self, sample_audio_file, output_audio_file):
        """Test encoding and decoding a longer message."""
        message = "This is a much longer secret message that contains multiple sentences. " \
                  "It should still work correctly with the LSB steganography algorithm."
        
        # Encode
        result = encode_message(sample_audio_file, message, output_audio_file)
        assert result is True
        
        # Decode
        decoded = decode_message(output_audio_file)
        assert decoded == message
    
    def test_encode_and_decode_special_characters(self, sample_audio_file, output_audio_file):
        """Test encoding and decoding special characters."""
        message = "Special chars: !@#$%^&*()_+-=[]{}|;':\",./<>?"
        
        # Encode
        result = encode_message(sample_audio_file, message, output_audio_file)
        assert result is True
        
        # Decode
        decoded = decode_message(output_audio_file)
        assert decoded == message
    
    def test_encode_nonexistent_file(self, output_audio_file):
        """Test encoding with non-existent input file."""
        with pytest.raises(FileNotFoundError):
            encode_message("nonexistent.wav", "test", output_audio_file)
    
    def test_decode_nonexistent_file(self):
        """Test decoding with non-existent input file."""
        with pytest.raises(FileNotFoundError):
            decode_message("nonexistent.wav")
    
    def test_message_too_large(self, output_audio_file):
        """Test that oversized messages raise an error."""
        # Create a very small audio file
        temp_dir = tempfile.mkdtemp()
        small_audio = os.path.join(temp_dir, 'small.wav')
        
        with wave.open(small_audio, 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(44100)
            # Write only 100 bytes (very small)
            wav_file.writeframes(b'\x00\x00' * 50)
        
        # Try to encode a message that's too large
        large_message = "A" * 1000
        with pytest.raises(ValueError, match="Message too large|Not enough space"):
            encode_message(small_audio, large_message, output_audio_file)
        
        # Cleanup
        os.remove(small_audio)
        os.rmdir(temp_dir)


# Edge case tests
class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_single_character(self, sample_audio_file, output_audio_file):
        """Test encoding and decoding a single character."""
        message = "X"
        
        encode_message(sample_audio_file, message, output_audio_file)
        decoded = decode_message(output_audio_file)
        assert decoded == message
    
    def test_numeric_message(self, sample_audio_file, output_audio_file):
        """Test encoding and decoding numeric message."""
        message = "1234567890"
        
        encode_message(sample_audio_file, message, output_audio_file)
        decoded = decode_message(output_audio_file)
        assert decoded == message
    
    def test_whitespace_message(self, sample_audio_file, output_audio_file):
        """Test encoding and decoding message with whitespace."""
        message = "   spaces   everywhere   "
        
        encode_message(sample_audio_file, message, output_audio_file)
        decoded = decode_message(output_audio_file)
        assert decoded == message
    
    def test_newline_characters(self, sample_audio_file, output_audio_file):
        """Test encoding and decoding message with newlines."""
        message = "Line 1\nLine 2\nLine 3"
        
        encode_message(sample_audio_file, message, output_audio_file)
        decoded = decode_message(output_audio_file)
        assert decoded == message


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
