"""
Audio Format Converter Module
Supports conversion between WAV, MP3, FLAC, OGG, and M4A formats
"""

import os
from pathlib import Path
from typing import Optional
import subprocess


class AudioConverter:
    """Convert audio files between different formats using ffmpeg"""
    
    SUPPORTED_FORMATS = {
        'wav': {'quality': 'lossless', 'description': 'Waveform Audio File'},
        'mp3': {'quality': 'lossy', 'description': 'MPEG Audio Layer III'},
        'flac': {'quality': 'lossless', 'description': 'Free Lossless Audio Codec'},
        'ogg': {'quality': 'lossy', 'description': 'Ogg Vorbis'},
        'm4a': {'quality': 'lossy', 'description': 'MPEG-4 Audio'},
        'aac': {'quality': 'lossy', 'description': 'Advanced Audio Coding'},
        'wma': {'quality': 'lossy', 'description': 'Windows Media Audio'},
    }
    
    def __init__(self):
        self.ffmpeg_available = self._check_ffmpeg()
    
    def _check_ffmpeg(self) -> bool:
        """Check if ffmpeg is installed"""
        try:
            result = subprocess.run(
                ['ffmpeg', '-version'],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def get_supported_formats(self) -> dict:
        """Return dictionary of supported formats"""
        return self.SUPPORTED_FORMATS.copy()
    
    def convert(
        self,
        input_path: str,
        output_format: str,
        output_path: Optional[str] = None,
        bitrate: str = '192k',
        quality: int = 2
    ) -> bool:
        """
        Convert audio file to different format
        
        Args:
            input_path: Path to input audio file
            output_format: Target format (wav, mp3, flac, ogg, m4a, aac, wma)
            output_path: Optional output path (auto-generated if not provided)
            bitrate: Bitrate for lossy formats (e.g., '128k', '192k', '320k')
            quality: Quality level for lossless (0-12, lower is better)
            
        Returns:
            True if conversion successful, False otherwise
        """
        if not self.ffmpeg_available:
            print("Error: ffmpeg is not installed. Please install ffmpeg first.")
            return False
        
        input_file = Path(input_path)
        if not input_file.exists():
            print(f"Error: Input file '{input_path}' not found")
            return False
        
        output_format = output_format.lower().lstrip('.')
        if output_format not in self.SUPPORTED_FORMATS:
            print(f"Error: Unsupported format '{output_format}'")
            print(f"Supported formats: {', '.join(self.SUPPORTED_FORMATS.keys())}")
            return False
        
        # Generate output path if not provided
        if output_path is None:
            output_path = str(input_file.with_suffix(f'.{output_format}'))
        
        # Build ffmpeg command based on format
        cmd = ['ffmpeg', '-y', '-i', str(input_file)]
        
        if output_format == 'mp3':
            cmd.extend(['-codec:a', 'libmp3lame', '-b:a', bitrate])
        elif output_format == 'ogg':
            cmd.extend(['-codec:a', 'libvorbis', '-b:a', bitrate])
        elif output_format == 'm4a' or output_format == 'aac':
            cmd.extend(['-codec:a', 'aac', '-b:a', bitrate])
        elif output_format == 'flac':
            cmd.extend(['-codec:a', 'flac', '-compression_level', str(quality)])
        elif output_format == 'wav':
            cmd.extend(['-codec:a', 'pcm_s16le'])
        elif output_format == 'wma':
            cmd.extend(['-codec:a', 'wmav2', '-b:a', bitrate])
        
        cmd.append(output_path)
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0:
                print(f"✓ Converted: {input_file.name} → {Path(output_path).name}")
                return True
            else:
                error_msg = result.stderr.decode('utf-8', errors='ignore')
                print(f"Conversion error: {error_msg}")
                return False
                
        except subprocess.TimeoutExpired:
            print("Error: Conversion timed out")
            return False
        except Exception as e:
            print(f"Conversion error: {e}")
            return False
    
    def batch_convert(
        self,
        input_files: list,
        output_format: str,
        output_dir: Optional[str] = None,
        **kwargs
    ) -> dict:
        """
        Convert multiple files to target format
        
        Args:
            input_files: List of input file paths
            output_format: Target format
            output_dir: Output directory (optional)
            **kwargs: Additional arguments passed to convert()
            
        Returns:
            Dictionary with success/failure counts
        """
        results = {'success': 0, 'failed': 0, 'files': []}
        
        for input_file in input_files:
            if output_dir:
                output_path = str(Path(output_dir) / Path(input_file).with_suffix(f'.{output_format.lstrip(".")}').name)
            else:
                output_path = None
            
            if self.convert(input_file, output_format, output_path, **kwargs):
                results['success'] += 1
                results['files'].append({'file': input_file, 'status': 'success'})
            else:
                results['failed'] += 1
                results['files'].append({'file': input_file, 'status': 'failed'})
        
        return results
    
    def get_audio_info(self, audio_path: str) -> dict:
        """Get detailed information about audio file"""
        if not self.ffmpeg_available:
            return {'error': 'ffmpeg not available'}
        
        try:
            cmd = [
                'ffprobe',
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                '-show_streams',
                audio_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                import json
                return json.loads(result.stdout)
            else:
                return {'error': 'Failed to get audio info'}
                
        except Exception as e:
            return {'error': str(e)}
