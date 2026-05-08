"""
Audio Steganography Core Module
Provides LSB (Least Significant Bit) encoding/decoding for WAV files
"""

import wave
import struct
import numpy as np
from typing import Optional, Tuple
from pathlib import Path


class AudioStegoCore:
    """Core steganography engine using LSB method"""
    
    def __init__(self):
        self.delimiter = "###STEGO_END###"
    
    def _encode_bits(self, data: bytes) -> list:
        """Convert bytes to list of bits"""
        bits = []
        for byte in data:
            for i in range(7, -1, -1):
                bits.append((byte >> i) & 1)
        return bits
    
    def _decode_bits(self, bits: list) -> bytes:
        """Convert list of bits back to bytes"""
        result = bytearray()
        for i in range(0, len(bits), 8):
            byte = 0
            for j in range(8):
                if i + j < len(bits):
                    byte = (byte << 1) | bits[i + j]
            result.append(byte)
        return bytes(result)
    
    def encode(self, audio_path: str, message: str, output_path: str) -> bool:
        """
        Encode a secret message into an audio file
        
        Args:
            audio_path: Path to input WAV file
            message: Secret message to hide
            output_path: Path for output file with hidden message
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Prepare message with delimiter
            full_message = message + self.delimiter
            message_bytes = full_message.encode('utf-8')
            message_bits = self._encode_bits(message_bytes)
            
            # Read audio file
            with wave.open(audio_path, 'rb') as wav_file:
                params = wav_file.getparams()
                n_channels = params.nchannels
                sampwidth = params.sampwidth
                framerate = params.framerate
                n_frames = params.nframes
                
                # Read all frames
                raw_data = wav_file.readframes(n_frames)
                
            # Convert to numpy array based on sample width
            if sampwidth == 1:
                dtype = np.uint8
                audio_data = np.frombuffer(raw_data, dtype=dtype)
            elif sampwidth == 2:
                dtype = np.int16
                audio_data = np.frombuffer(raw_data, dtype=dtype).astype(np.int32)
            else:
                raise ValueError(f"Unsupported sample width: {sampwidth}")
            
            # Check capacity
            max_bits = len(audio_data)
            if len(message_bits) > max_bits:
                raise ValueError(f"Message too large! Max capacity: {max_bits // 8} bytes")
            
            # Encode bits into LSB
            for i, bit in enumerate(message_bits):
                if dtype == np.uint8:
                    audio_data[i] = (audio_data[i] & 0xFE) | bit
                else:
                    # For signed integers, preserve sign
                    if audio_data[i] >= 0:
                        audio_data[i] = (audio_data[i] & 0xFFFE) | bit
                    else:
                        audio_data[i] = (audio_data[i] | 0x0001) if bit else (audio_data[i] & 0xFFFE)
            
            # Write modified audio
            with wave.open(output_path, 'wb') as wav_out:
                wav_out.setparams(params)
                if dtype == np.uint8:
                    wav_out.writeframes(audio_data.tobytes())
                else:
                    wav_out.writeframes(audio_data.astype(np.int16).tobytes())
            
            return True
            
        except Exception as e:
            print(f"Encoding error: {e}")
            return False
    
    def decode(self, audio_path: str) -> Optional[str]:
        """
        Decode a secret message from an audio file
        
        Args:
            audio_path: Path to WAV file with hidden message
            
        Returns:
            Decoded message or None if no message found
        """
        try:
            with wave.open(audio_path, 'rb') as wav_file:
                params = wav_file.getparams()
                sampwidth = params.sampwidth
                n_frames = params.nframes
                
                raw_data = wav_file.readframes(n_frames)
            
            # Convert to numpy array
            if sampwidth == 1:
                dtype = np.uint8
                audio_data = np.frombuffer(raw_data, dtype=dtype)
            elif sampwidth == 2:
                dtype = np.int16
                audio_data = np.frombuffer(raw_data, dtype=dtype).astype(np.int32)
            else:
                raise ValueError(f"Unsupported sample width: {sampwidth}")
            
            # Extract LSBs
            bits = []
            for sample in audio_data:
                if dtype == np.uint8:
                    bits.append(sample & 1)
                else:
                    bits.append(abs(sample) & 1)
            
            # Convert bits to bytes
            decoded_bytes = self._decode_bits(bits)
            decoded_str = decoded_bytes.decode('utf-8', errors='ignore')
            
            # Check for delimiter
            if self.delimiter in decoded_str:
                return decoded_str.split(self.delimiter)[0]
            
            return None
            
        except Exception as e:
            print(f"Decoding error: {e}")
            return None
    
    def get_capacity(self, audio_path: str) -> dict:
        """Get information about audio file and its steganographic capacity"""
        try:
            with wave.open(audio_path, 'rb') as wav_file:
                params = wav_file.getparams()
                n_samples = params.nframes * params.nchannels
                
            return {
                'channels': params.nchannels,
                'sample_width': params.sampwidth,
                'frame_rate': params.framerate,
                'duration': params.nframes / params.framerate,
                'total_samples': n_samples,
                'max_capacity_bytes': n_samples // 8,
                'max_capacity_chars': n_samples // 8
            }
        except Exception as e:
            return {'error': str(e)}
