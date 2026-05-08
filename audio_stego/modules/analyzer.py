"""
Audio Analysis Module
Provides visualization and analysis of audio files
"""

import numpy as np
from pathlib import Path
from typing import Optional, Tuple, Dict
import wave


class AudioAnalyzer:
    """Analyze and visualize audio file properties"""
    
    def __init__(self):
        pass
    
    def get_wave_info(self, audio_path: str) -> dict:
        """Get basic information about a WAV file"""
        try:
            with wave.open(audio_path, 'rb') as wav_file:
                params = wav_file.getparams()
                
            return {
                'channels': params.nchannels,
                'sample_width': params.sampwidth,
                'frame_rate': params.framerate,
                'n_frames': params.nframes,
                'duration_seconds': params.nframes / params.framerate,
                'compression_type': params.comptype.decode('utf-8') if isinstance(params.comptype, bytes) else params.comptype,
                'compression_name': params.compname.decode('utf-8') if isinstance(params.compname, bytes) else params.compname,
            }
        except Exception as e:
            return {'error': str(e)}
    
    def read_audio_data(self, audio_path: str) -> Tuple[np.ndarray, dict]:
        """
        Read audio data from WAV file
        
        Returns:
            Tuple of (audio_data as numpy array, info dict)
        """
        with wave.open(audio_path, 'rb') as wav_file:
            params = wav_file.getparams()
            raw_data = wav_file.readframes(params.nframes)
        
        sampwidth = params.sampwidth
        if sampwidth == 1:
            dtype = np.uint8
            audio_data = np.frombuffer(raw_data, dtype=dtype).astype(np.float32)
            audio_data = (audio_data - 128) / 128.0  # Normalize to [-1, 1]
        elif sampwidth == 2:
            dtype = np.int16
            audio_data = np.frombuffer(raw_data, dtype=dtype).astype(np.float32)
            audio_data = audio_data / 32768.0  # Normalize to [-1, 1]
        elif sampwidth == 4:
            dtype = np.int32
            audio_data = np.frombuffer(raw_data, dtype=dtype).astype(np.float32)
            audio_data = audio_data / 2147483648.0  # Normalize to [-1, 1]
        else:
            raise ValueError(f"Unsupported sample width: {sampwidth}")
        
        info = {
            'channels': params.nchannels,
            'sample_rate': params.framerate,
            'duration': params.nframes / params.framerate,
            'dtype': str(dtype),
        }
        
        return audio_data, info
    
    def calculate_statistics(self, audio_data: np.ndarray) -> dict:
        """Calculate statistical properties of audio data"""
        return {
            'mean': float(np.mean(audio_data)),
            'std': float(np.std(audio_data)),
            'min': float(np.min(audio_data)),
            'max': float(np.max(audio_data)),
            'rms': float(np.sqrt(np.mean(audio_data ** 2))),
            'peak_to_peak': float(np.max(audio_data) - np.min(audio_data)),
            'zero_crossings': int(np.sum(np.diff(np.sign(audio_data)) != 0)),
        }
    
    def detect_silence(
        self,
        audio_data: np.ndarray,
        sample_rate: int,
        threshold: float = 0.01,
        min_duration: float = 0.5
    ) -> list:
        """
        Detect silent regions in audio
        
        Args:
            audio_data: Audio samples
            sample_rate: Sample rate in Hz
            threshold: Amplitude threshold for silence
            min_duration: Minimum silence duration in seconds
            
        Returns:
            List of (start_time, end_time) tuples for silent regions
        """
        # Calculate energy
        energy = np.abs(audio_data)
        
        # Find silent samples
        is_silent = energy < threshold
        
        # Find transitions
        diff = np.diff(is_silent.astype(int))
        starts = np.where(diff == 1)[0] + 1
        ends = np.where(diff == -1)[0] + 1
        
        # Handle edge cases
        if is_silent[0]:
            starts = np.r_[0, starts]
        if is_silent[-1]:
            ends = np.r_[ends, len(is_silent)]
        
        # Convert to time and filter by duration
        min_samples = int(min_duration * sample_rate)
        silent_regions = []
        
        for start, end in zip(starts, ends):
            if end - start >= min_samples:
                start_time = start / sample_rate
                end_time = end / sample_rate
                silent_regions.append((start_time, end_time))
        
        return silent_regions
    
    def estimate_capacity(self, audio_path: str, method: str = 'lsb') -> dict:
        """
        Estimate steganographic capacity of audio file
        
        Args:
            audio_path: Path to audio file
            method: Steganography method ('lsb', 'lsb2', etc.)
            
        Returns:
            Dictionary with capacity estimates
        """
        info = self.get_wave_info(audio_path)
        
        if 'error' in info:
            return info
        
        total_samples = info['n_frames'] * info['channels']
        
        capacities = {
            'lsb_1bit': {
                'bits': total_samples,
                'bytes': total_samples // 8,
                'chars': total_samples // 8,
                'description': '1 bit per sample (LSB)'
            },
            'lsb_2bit': {
                'bits': total_samples * 2,
                'bytes': total_samples // 4,
                'chars': total_samples // 4,
                'description': '2 bits per sample'
            },
            'lsb_4bit': {
                'bits': total_samples * 4,
                'bytes': total_samples // 2,
                'chars': total_samples // 2,
                'description': '4 bits per sample (lower quality)'
            }
        }
        
        return {
            'file_info': info,
            'total_samples': total_samples,
            'capacities': capacities
        }
    
    def compare_audio(self, original_path: str, modified_path: str) -> dict:
        """
        Compare two audio files to detect differences
        
        Args:
            original_path: Path to original audio
            modified_path: Path to modified audio
            
        Returns:
            Comparison statistics
        """
        orig_data, orig_info = self.read_audio_data(original_path)
        mod_data, mod_info = self.read_audio_data(modified_path)
        
        if len(orig_data) != len(mod_data):
            return {'error': 'Audio files have different lengths'}
        
        diff = orig_data - mod_data
        
        return {
            'max_difference': float(np.max(np.abs(diff))),
            'mean_difference': float(np.mean(np.abs(diff))),
            'rms_difference': float(np.sqrt(np.mean(diff ** 2))),
            'samples_changed': int(np.sum(diff != 0)),
            'percent_changed': float(np.sum(diff != 0) / len(diff) * 100),
            'snr_db': float(10 * np.log10(np.var(orig_data) / np.var(diff))) if np.var(diff) > 0 else float('inf')
        }
