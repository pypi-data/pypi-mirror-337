#!/usr/bin/env python3
"""
Command Line Interface for the IITJP package.
"""

import sys
import argparse
from . import mam, enable_silent_mode

def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="IITJP - Interactive Statistics Teacher with audio-visual interaction"
    )
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Add greetings command
    greetings_parser = subparsers.add_parser("greetings", help="Display welcome message from the teacher")
    
    # Add quiz command
    quiz_parser = subparsers.add_parser("quiz", help="Start an interactive statistics quiz")
    
    # Add thanks command
    thanks_parser = subparsers.add_parser("thanks", help="Display goodbye message from the teacher")
    
    # Add version command
    version_parser = subparsers.add_parser("version", help="Display package version information")
    
    # Add global option for silent mode
    parser.add_argument("--silent", action="store_true", help="Enable silent mode (no audio)")
    
    # Parse arguments
    args = parser.parse_args()
    
    # If no command provided, show help
    if not args.command:
        parser.print_help()
        return
    
    # Enable silent mode if requested
    if args.silent:
        enable_silent_mode(True)
    
    # Execute the specified command
    if args.command == "greetings":
        mam.greetings()
    elif args.command == "quiz":
        mam.quiz()
    elif args.command == "thanks":
        mam.thanks()
    elif args.command == "version":
        from . import __version__
        print(f"IITJP version {__version__}")

if __name__ == "__main__":
    main() 