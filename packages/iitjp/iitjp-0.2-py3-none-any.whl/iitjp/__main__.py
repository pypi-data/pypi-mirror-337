"""
IITJP CLI Entry Point

This module provides a command-line interface for the IITJP library.
"""

import sys
import os
import argparse
from . import mam, enable_silent_mode

def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="IITJP - Interactive Teacher for Statistics",
        epilog="Example: iitjp greetings"
    )
    
    parser.add_argument('--silent', action='store_true', 
                        help='Enable silent mode (no audio)')
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Greetings command
    greetings_parser = subparsers.add_parser('greetings', help='Display welcome message')
    
    # Quiz command
    quiz_parser = subparsers.add_parser('quiz', help='Start an interactive quiz')
    
    # Thanks command
    thanks_parser = subparsers.add_parser('thanks', help='Display thank you message')
    
    # Version command
    version_parser = subparsers.add_parser('version', help='Display version information')
    
    args = parser.parse_args()
    
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
    elif args.command == 'version':
        print("IITJP version 0.2")
        print("A Python library for interactive learning with RajLaxmi")
    else:
        # Default behavior - show help
        parser.print_help()

if __name__ == '__main__':
    main() 