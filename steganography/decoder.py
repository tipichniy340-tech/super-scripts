"""
Audio Steganography Decoder Module

Decodes secret messages from audio files using LSB (Least Significant Bit) steganography.
"""

import wave
from typing import Optional


def bits_to_text(bits: list) -> str:
    """Convert list of bits to text string."""
    chars = []
    for i in range(0, len(bits), 8):
        byte_bits = bits[i:i+8]
        if len(byte_bits) == 8:
            byte_val = 0
            for bit in byte_bits:
                byte_val = (byte_val << 1) | bit
            if byte_val == 0:  # Null terminator
                break
            chars.append(chr(byte_val))
    return ''.join(chars)


def decode_message(audio_path: str) -> str:
    """
    Decode a secret message from an audio file using LSB steganography.
    
    Args:
        audio_path: Path to the WAV audio file with embedded message
        
    Returns:
        The decoded secret message
        
    Raises:
        FileNotFoundError: If the audio file doesn't exist
        ValueError: If no message is found or audio format is not supported
        wave.Error: If the audio file is corrupted
    """
    try:
        # Open the audio file
        with wave.open(audio_path, 'rb') as audio_file:
            # Get audio parameters
            params = audio_file.getparams()
            n_channels = params.nchannels
            sampwidth = params.sampwidth
            
            # Check if format is supported
            if n_channels not in [1, 2]:
                raise ValueError(f"Unsupported number of channels: {n_channels}")
            if sampwidth not in [1, 2]:
                raise ValueError(f"Unsupported sample width: {sampwidth} bytes")
            
            # Read all frames
            frames = bytearray(audio_file.readframes(params.nframes))
            
            # Extract length (first 32 bits)
            if len(frames) < 32:
                raise ValueError("Audio file too small to contain a message")
            
            length_bits = []
            for i in range(32):
                length_bits.append(frames[i] & 1)
            
            # Convert length bits to integer
            message_length = 0
            for bit in length_bits:
                message_length = (message_length << 1) | bit
            
            # Validate message length
            if message_length <= 0:
                raise ValueError("No valid message found (invalid length)")
            
            max_possible_length = (len(frames) - 32) // 8
            if message_length > max_possible_length:
                raise ValueError(
                    f"Invalid message length: {message_length}. "
                    f"Maximum possible: {max_possible_length}"
                )
            
            # Extract message bits
            total_bits_needed = 32 + (message_length * 8)
            if len(frames) < total_bits_needed:
                raise ValueError("Audio file too small for declared message length")
            
            message_bits = []
            for i in range(32, total_bits_needed):
                message_bits.append(frames[i] & 1)
            
            # Convert bits to text
            message = bits_to_text(message_bits)
            
            # Validate that we got the expected length
            if len(message) != message_length:
                raise ValueError(
                    f"Message length mismatch: expected {message_length}, "
                    f"got {len(message)}"
                )
            
            return message
            
    except FileNotFoundError:
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    except wave.Error as e:
        raise wave.Error(f"Corrupted audio file: {e}")
    except Exception as e:
        raise ValueError(f"Decoding failed: {e}")
