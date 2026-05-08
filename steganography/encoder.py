"""
Audio Steganography Encoder Module

Encodes secret messages into audio files using LSB (Least Significant Bit) steganography.
"""

import wave
import struct
from typing import Optional


def text_to_bits(text: str) -> list:
    """Convert text string to list of bits."""
    bits = []
    for char in text:
        byte = ord(char)
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    return bits


def encode_message(audio_path: str, message: str, output_path: str) -> bool:
    """
    Encode a secret message into an audio file using LSB steganography.
    
    Args:
        audio_path: Path to the input WAV audio file
        message: Secret message to encode
        output_path: Path to save the output audio file with embedded message
        
    Returns:
        True if encoding was successful, False otherwise
        
    Raises:
        FileNotFoundError: If the input audio file doesn't exist
        ValueError: If the audio format is not supported or message is too large
        wave.Error: If the audio file is corrupted
    """
    try:
        # Validate inputs
        if not message:
            raise ValueError("Message cannot be empty")
        
        # Open the audio file
        with wave.open(audio_path, 'rb') as audio_file:
            # Get audio parameters
            params = audio_file.getparams()
            n_channels = params.nchannels
            sampwidth = params.sampwidth
            framerate = params.framerate
            n_frames = params.nframes
            
            # Check if format is supported (mono or stereo, 8 or 16 bit)
            if n_channels not in [1, 2]:
                raise ValueError(f"Unsupported number of channels: {n_channels}")
            if sampwidth not in [1, 2]:
                raise ValueError(f"Unsupported sample width: {sampwidth} bytes")
            
            # Read all frames
            frames = bytearray(audio_file.readframes(n_frames))
            
            # Calculate maximum message size
            max_bytes = (len(frames) // 8) - 4  # Reserve 4 bytes for length
            if len(message) > max_bytes:
                raise ValueError(
                    f"Message too large. Maximum size: {max_bytes} bytes, "
                    f"provided: {len(message)} bytes"
                )
            
            # Convert message to bits with length prefix
            message_length = len(message)
            length_bits = []
            for i in range(31, -1, -1):
                length_bits.append((message_length >> i) & 1)
            
            message_bits = text_to_bits(message)
            all_bits = length_bits + message_bits
            
            # Encode bits into LSB of audio frames
            for i, bit in enumerate(all_bits):
                if i >= len(frames):
                    raise ValueError("Not enough space in audio file")
                # Clear LSB and set it to our bit
                frames[i] = (frames[i] & 0xFE) | bit
            
            # Write output file
            with wave.open(output_path, 'wb') as output_file:
                output_file.setparams(params)
                output_file.writeframes(bytes(frames))
            
            return True
            
    except FileNotFoundError:
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    except wave.Error as e:
        raise wave.Error(f"Corrupted audio file: {e}")
    except Exception as e:
        raise ValueError(f"Encoding failed: {e}")
