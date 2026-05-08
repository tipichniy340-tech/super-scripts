"""
Audio Steganography CLI Tool
Command-line interface for hiding and extracting messages from audio files
"""

import argparse
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress

# Import modules
from audio_stego import (
    AudioStegoCore,
    AudioConverter,
    CryptoModule,
    EncryptedStegoWrapper,
    AudioAnalyzer,
)

console = Console()


def print_banner():
    """Display application banner"""
    banner = """
[bold blue]╔═══════════════════════════════════════════╗[/bold blue]
[bold blue]║   🔒 Audio Steganography Tool v1.0        ║[/bold blue]
[bold blue]║   Hide secrets in your audio files!       ║[/bold blue]
[bold blue]╚═══════════════════════════════════════════╝[/bold blue]
    """
    console.print(Panel(banner, style="blue"))


def cmd_encode(args):
    """Encode a message into an audio file"""
    console.print("[green]📝 Encoding message...[/green]")
    
    stego = AudioStegoCore()
    
    # Check if encryption is requested
    if args.encrypt:
        crypto = CryptoModule()
        wrapper = EncryptedStegoWrapper(crypto, stego)
        
        if not args.password:
            args.password = crypto.generate_password(24)
            console.print(f"[yellow]⚠ Generated password: {args.password}[/yellow]")
            console.print("[yellow]⚠ Save this password! You'll need it to decode.[/yellow]")
        
        success = wrapper.encode_encrypted(
            args.input,
            args.message,
            args.password,
            args.output
        )
    else:
        success = stego.encode(args.input, args.message, args.output)
    
    if success:
        console.print(Panel(
            f"[bold green]✓ Success![/bold green]\n"
            f"Message hidden in: [cyan]{args.output}[/cyan]",
            title="Encoding Complete",
            border_style="green"
        ))
    else:
        console.print("[red]✗ Failed to encode message[/red]")
        sys.exit(1)


def cmd_decode(args):
    """Decode a message from an audio file"""
    console.print("[green]📖 Decoding message...[/green]")
    
    stego = AudioStegoCore()
    
    if args.decrypt:
        if not args.password:
            console.print("[red]✗ Password required for decryption![/red]")
            sys.exit(1)
        
        crypto = CryptoModule()
        wrapper = EncryptedStegoWrapper(crypto, stego)
        message = wrapper.decode_decrypted(args.input, args.password)
    else:
        message = stego.decode(args.input)
    
    if message:
        console.print(Panel(
            f"[bold cyan]Hidden Message:[/bold cyan]\n\n{message}",
            title="Decoded Successfully",
            border_style="cyan"
        ))
    else:
        console.print("[yellow]⚠ No hidden message found in audio file[/yellow]")


def cmd_convert(args):
    """Convert audio file format"""
    console.print(f"[green]🔄 Converting {args.input} to {args.format}...[/green]")
    
    converter = AudioConverter()
    
    if not converter.ffmpeg_available:
        console.print("[red]✗ ffmpeg is not installed. Please install ffmpeg first.[/red]")
        console.print("  Ubuntu/Debian: sudo apt install ffmpeg")
        console.print("  macOS: brew install ffmpeg")
        console.print("  Windows: Download from ffmpeg.org")
        sys.exit(1)
    
    success = converter.convert(
        args.input,
        args.format,
        args.output,
        bitrate=args.bitrate
    )
    
    if success:
        console.print("[bold green]✓ Conversion complete![/bold green]")
    else:
        console.print("[red]✗ Conversion failed[/red]")
        sys.exit(1)


def cmd_analyze(args):
    """Analyze audio file"""
    console.print(f"[green]📊 Analyzing {args.input}...[/green]")
    
    analyzer = AudioAnalyzer()
    
    # Get basic info
    info = analyzer.get_wave_info(args.input)
    
    if 'error' in info:
        console.print(f"[red]✗ Error: {info['error']}[/red]")
        sys.exit(1)
    
    # Display info table
    table = Table(title="Audio File Information", show_header=True, header_style="bold magenta")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")
    
    for key, value in info.items():
        table.add_row(key.replace('_', ' ').title(), str(value))
    
    console.print(table)
    
    # Capacity estimation
    if args.capacity:
        console.print("\n[bold]Steganographic Capacity:[/bold]")
        capacity = analyzer.estimate_capacity(args.input)
        
        cap_table = Table(show_header=True, header_style="bold blue")
        cap_table.add_column("Method", style="cyan")
        cap_table.add_column("Capacity", style="green")
        cap_table.add_column("Description", style="yellow")
        
        for method, data in capacity['capacities'].items():
            cap_table.add_row(
                method,
                f"{data['chars']} chars",
                data['description']
            )
        
        console.print(cap_table)
    
    # Compare mode
    if args.compare:
        console.print(f"\n[bold]Comparing with {args.compare}...[/bold]")
        comparison = analyzer.compare_audio(args.input, args.compare)
        
        if 'error' not in comparison:
            comp_table = Table(show_header=True, header_style="bold red")
            comp_table.add_column("Metric", style="cyan")
            comp_table.add_column("Value", style="red")
            
            for key, value in comparison.items():
                comp_table.add_row(key.replace('_', ' ').title(), str(round(value, 6) if isinstance(value, float) else value))
            
            console.print(comp_table)


def cmd_info(args):
    """Show supported formats and capabilities"""
    console.print("[bold]Audio Steganography Tool - Capabilities[/bold]\n")
    
    # Supported formats
    converter = AudioConverter()
    formats = converter.get_supported_formats()
    
    table = Table(title="Supported Audio Formats", show_header=True, header_style="bold green")
    table.add_column("Format", style="cyan")
    table.add_column("Quality", style="green")
    table.add_column("Description", style="yellow")
    
    for fmt, info in formats.items():
        table.add_row(fmt.upper(), info['quality'], info['description'])
    
    console.print(table)
    
    # Features
    features = [
        "✓ LSB Steganography (hide messages in audio)",
        "✓ AES-256 Encryption (optional)",
        "✓ Multi-format Support (WAV, MP3, FLAC, OGG, M4A)",
        "✓ Audio Analysis & Statistics",
        "✓ Batch Conversion",
        "✓ Silence Detection",
        "✓ Capacity Estimation",
    ]
    
    console.print("\n[bold]Features:[/bold]")
    for feature in features:
        console.print(f"  {feature}")


def main():
    parser = argparse.ArgumentParser(
        description='🔒 Audio Steganography Tool - Hide secrets in audio files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s encode -i audio.wav -m "Secret message" -o output.wav
  %(prog)s decode -i output.wav
  %(prog)s encode -i audio.wav -m "Secret" -o out.wav --encrypt -p mypassword
  %(prog)s convert -i song.mp3 -f wav
  %(prog)s analyze -i audio.wav --capacity
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Encode command
    encode_parser = subparsers.add_parser('encode', help='Encode a message into audio')
    encode_parser.add_argument('-i', '--input', required=True, help='Input audio file (WAV)')
    encode_parser.add_argument('-m', '--message', required=True, help='Message to hide')
    encode_parser.add_argument('-o', '--output', required=True, help='Output audio file')
    encode_parser.add_argument('--encrypt', action='store_true', help='Encrypt message before hiding')
    encode_parser.add_argument('-p', '--password', help='Encryption password (auto-generated if not provided)')
    encode_parser.set_defaults(func=cmd_encode)
    
    # Decode command
    decode_parser = subparsers.add_parser('decode', help='Decode a message from audio')
    decode_parser.add_argument('-i', '--input', required=True, help='Input audio file')
    decode_parser.add_argument('--decrypt', action='store_true', help='Decrypt message after extraction')
    decode_parser.add_argument('-p', '--password', help='Decryption password')
    decode_parser.set_defaults(func=cmd_decode)
    
    # Convert command
    convert_parser = subparsers.add_parser('convert', help='Convert audio format')
    convert_parser.add_argument('-i', '--input', required=True, help='Input audio file')
    convert_parser.add_argument('-f', '--format', required=True, 
                               choices=['wav', 'mp3', 'flac', 'ogg', 'm4a', 'aac', 'wma'],
                               help='Target format')
    convert_parser.add_argument('-o', '--output', help='Output file path (optional)')
    convert_parser.add_argument('-b', '--bitrate', default='192k', help='Bitrate for lossy formats (default: 192k)')
    convert_parser.set_defaults(func=cmd_convert)
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze audio file')
    analyze_parser.add_argument('-i', '--input', required=True, help='Audio file to analyze')
    analyze_parser.add_argument('--capacity', action='store_true', help='Show steganographic capacity')
    analyze_parser.add_argument('--compare', help='Compare with another audio file')
    analyze_parser.set_defaults(func=cmd_analyze)
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Show tool information and capabilities')
    info_parser.set_defaults(func=cmd_info)
    
    args = parser.parse_args()
    
    print_banner()
    
    if args.command is None:
        parser.print_help()
        sys.exit(0)
    
    args.func(args)


if __name__ == '__main__':
    main()
