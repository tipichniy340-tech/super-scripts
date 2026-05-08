"""
Generate example WAV audio files for testing the steganography tool.
"""

import wave
import struct
import math


def generate_sine_wave(filename: str, duration: float = 3.0, frequency: float = 440.0, 
                       sample_rate: int = 44100, amplitude: int = 16000):
    """
    Generate a simple sine wave WAV file.
    
    Args:
        filename: Output WAV file path
        duration: Duration in seconds
        frequency: Frequency in Hz (default: A4 note)
        sample_rate: Sample rate in Hz
        amplitude: Amplitude (0-32767 for 16-bit)
    """
    n_samples = int(sample_rate * duration)
    
    with wave.open(filename, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        
        samples = []
        for i in range(n_samples):
            # Generate sine wave sample
            t = i / sample_rate
            sample = amplitude * math.sin(2 * math.pi * frequency * t)
            # Convert to 16-bit integer
            samples.append(struct.pack('<h', int(sample)))
        
        wav_file.writeframes(b''.join(samples))
    
    print(f"✓ Generated {filename} ({duration}s, {frequency}Hz)")


def generate_stereo_tone(filename: str, duration: float = 3.0, 
                         left_freq: float = 440.0, right_freq: float = 880.0,
                         sample_rate: int = 44100, amplitude: int = 16000):
    """
    Generate a stereo WAV file with different tones in each channel.
    
    Args:
        filename: Output WAV file path
        duration: Duration in seconds
        left_freq: Frequency for left channel
        right_freq: Frequency for right channel
        sample_rate: Sample rate in Hz
        amplitude: Amplitude (0-32767 for 16-bit)
    """
    n_samples = int(sample_rate * duration)
    
    with wave.open(filename, 'wb') as wav_file:
        wav_file.setnchannels(2)
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        
        samples = []
        for i in range(n_samples):
            t = i / sample_rate
            # Left channel
            left_sample = amplitude * math.sin(2 * math.pi * left_freq * t)
            # Right channel
            right_sample = amplitude * math.sin(2 * math.pi * right_freq * t)
            # Interleave channels
            samples.append(struct.pack('<hh', int(left_sample), int(right_sample)))
        
        wav_file.writeframes(b''.join(samples))
    
    print(f"✓ Generated {filename} (stereo: {left_freq}Hz/{right_freq}Hz)")


def generate_white_noise(filename: str, duration: float = 2.0, 
                         sample_rate: int = 44100, amplitude: int = 8000):
    """
    Generate white noise WAV file.
    
    Args:
        filename: Output WAV file path
        duration: Duration in seconds
        sample_rate: Sample rate in Hz
        amplitude: Amplitude (0-32767 for 16-bit)
    """
    import random
    n_samples = int(sample_rate * duration)
    
    with wave.open(filename, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        
        samples = []
        for _ in range(n_samples):
            sample = random.randint(-amplitude, amplitude)
            samples.append(struct.pack('<h', sample))
        
        wav_file.writeframes(b''.join(samples))
    
    print(f"✓ Generated {filename} ({duration}s white noise)")


if __name__ == '__main__':
    print("🎵 Generating example audio files...\n")
    
    # Generate test files
    generate_sine_wave('examples/test_tone.wav', duration=3.0, frequency=440.0)
    generate_sine_wave('examples/test_tone_880.wav', duration=2.0, frequency=880.0)
    generate_stereo_tone('examples/stereo_test.wav', duration=3.0)
    generate_white_noise('examples/white_noise.wav', duration=2.0)
    
    print("\n✅ All example files generated successfully!")
    print("\nUsage examples:")
    print("  python main.py encode -i examples/test_tone.wav -o output.wav -m \"Secret message\"")
    print("  python main.py decode -i output.wav")
