"""
AutoDiag Pro - Main Entry Point
Professional Automotive Diagnostic Tool
"""
import sys
import argparse


def main():
    """Main entry point for AutoDiag Pro."""
    parser = argparse.ArgumentParser(
        description="AutoDiag Pro - Professional Automotive Diagnostic Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --cli              Run CLI interface
  python main.py --gui              Run GUI interface
  python main.py --lang ru          Set default language to Russian
  python main.py                    Interactive mode selection
        """
    )
    
    parser.add_argument(
        '--cli', 
        action='store_true',
        help='Run command-line interface'
    )
    
    parser.add_argument(
        '--gui',
        action='store_true', 
        help='Run graphical user interface'
    )
    
    parser.add_argument(
        '--lang',
        choices=['en', 'ru'],
        default='en',
        help='Set default language (default: en)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='AutoDiag Pro v1.0.0'
    )
    
    args = parser.parse_args()
    
    # If no interface specified, ask user
    if not args.cli and not args.gui:
        print("╔══════════════════════════════════════════════════════════╗")
        print("║       AutoDiag Pro - Professional Diagnostic Tool        ║")
        print("╠══════════════════════════════════════════════════════════╣")
        print("║  Select interface:                                       ║")
        print("║    1. CLI (Command Line Interface)                       ║")
        print("║    2. GUI (Graphical User Interface)                     ║")
        print("║    3. Exit                                               ║")
        print("╚══════════════════════════════════════════════════════════╝")
        
        choice = input("\nEnter choice [1-3]: ").strip()
        
        if choice == '1':
            args.cli = True
        elif choice == '2':
            args.gui = True
        else:
            print("Goodbye!")
            sys.exit(0)
    
    # Set language
    from core.diagnostic import Language
    language = Language.RU if args.lang == 'ru' else Language.EN
    
    try:
        if args.cli:
            print(f"Starting CLI interface (Language: {args.lang.upper()})...")
            from interfaces.cli import CLIInterface
            cli = CLIInterface(language=language)
            cli.run()
        elif args.gui:
            print(f"Starting GUI interface (Language: {args.lang.upper()})...")
            from interfaces.gui import GUIInterface
            gui = GUIInterface()
            gui.run()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
