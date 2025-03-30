"""
IITJP CLI Entry Point

This module provides a command-line interface for the IITJP library.
"""

import sys
import os
import argparse
from . import mam, enable_silent_mode
from .rajlaxmi import PACKAGE_ROOT, DATA_DIR, TEMP_DIR, ensure_temp_dir

def create_required_dirs():
    """Ensure all required directories exist."""
    # Ensure temp directory exists
    if not os.path.exists(TEMP_DIR):
        try:
            os.makedirs(TEMP_DIR, exist_ok=True)
            print(f"Created temp directory at {TEMP_DIR}")
        except Exception as e:
            print(f"Could not create temp directory: {e}")
    
    # Ensure data directory exists
    if not os.path.exists(DATA_DIR):
        try:
            os.makedirs(DATA_DIR, exist_ok=True)
            print(f"Created data directory at {DATA_DIR}")
        except Exception as e:
            print(f"Could not create data directory: {e}")

def main():
    """Main entry point for the CLI."""
    # Ensure all directories are created
    create_required_dirs()
    
    parser = argparse.ArgumentParser(
        description="IITJP - Interactive Teacher for Statistics",
        epilog="Example: iitjp greetings"
    )
    
    parser.add_argument('--silent', action='store_true', 
                        help='Enable silent mode (no audio)')
    
    parser.add_argument('--version', action='store_true',
                        help='Display version information')
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Greetings command
    greetings_parser = subparsers.add_parser('greetings', help='Display welcome message')
    
    # Quiz command
    quiz_parser = subparsers.add_parser('quiz', help='Start an interactive quiz')
    
    # Thanks command
    thanks_parser = subparsers.add_parser('thanks', help='Display thank you message')
    
    args = parser.parse_args()
    
    # Handle version display
    if args.version:
        print("IITJP version 0.2.1")
        print("A Python library for interactive learning with RajLaxmi")
        return
    
    # Handle silent mode
    if args.silent:
        enable_silent_mode(True)
    
    # Execute command
    if args.command == 'greetings':
        mam.greetings()
    elif args.command == 'quiz':
        mam.quiz()
    elif args.command == 'thanks':
        mam.thanks()
    else:
        # Default behavior - show help
        parser.print_help()

if __name__ == '__main__':
    main() 