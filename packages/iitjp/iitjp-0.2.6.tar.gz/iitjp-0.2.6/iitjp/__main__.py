"""
IITJP CLI Entry Point

This module provides a command-line interface for the IITJP library.
"""

import sys
import os
import argparse
import shutil
import importlib.util
from . import mam, enable_silent_mode, enable_typing_effect, verify_audio_files
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

def auto_repair_audio():
    """Try to automatically repair audio files by copying them to the right locations"""
    # Get the package directory
    package_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Files to check
    files_to_check = [
        "greeting.mp3", 
        "start_quiz.mp3", 
        "end_quiz.mp3", 
        "farewell.mp3",
        "questions.json"
    ]
    
    # Destination directories
    dest_dirs = [
        os.path.join(package_dir, "data"),  # In the package data directory
        DATA_DIR,  # Main data directory 
    ]
    
    # Ensure directories exist
    for directory in dest_dirs:
        if not os.path.exists(directory):
            try:
                os.makedirs(directory, exist_ok=True)
            except Exception:
                pass
    
    # Find and copy files
    for filename in files_to_check:
        # Places to look for the file
        search_paths = [
            os.path.join(PACKAGE_ROOT, "data", filename),  # Main data directory
            os.path.join(os.getcwd(), "data", filename),  # Current directory data
            os.path.join(os.getcwd(), filename),  # Current directory
            os.path.join(package_dir, "data", filename),  # Package data directory
            os.path.join(package_dir, filename),  # Package directory
        ]
        
        # Try to find the file
        found_file = None
        for path in search_paths:
            if os.path.exists(path):
                found_file = path
                break
        
        # If not found, try a recursive search
        if not found_file:
            for search_dir in [PACKAGE_ROOT, os.getcwd(), os.path.dirname(package_dir)]:
                for root, _, files in os.walk(search_dir):
                    if filename in files:
                        found_file = os.path.join(root, filename)
                        break
                if found_file:
                    break
        
        # If file found, copy to destination directories
        if found_file:
            for dest_dir in dest_dirs:
                dest_path = os.path.join(dest_dir, filename)
                if not os.path.exists(dest_path):
                    try:
                        shutil.copy2(found_file, dest_path)
                        print(f"Copied {filename} to {dest_path}")
                    except Exception as e:
                        print(f"Could not copy {filename} to {dest_path}: {e}")

def repair_command():
    """Run the audio file repair tool"""
    print("Running audio file repair...")
    
    # Create required directories
    create_required_dirs()
    
    # Try automatic repair
    auto_repair_audio()
    
    # Verify files
    found_files, missing_files = verify_audio_files()
    
    if not missing_files:
        print("All audio files were found and verified!")
    else:
        print(f"Some files are still missing: {', '.join(missing_files)}")
        print("You may need to download these files manually from the repository.")
    
    return 0

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
    
    parser.add_argument('--fast-text', action='store_true',
                        help='Disable typing effect for immediate text display')
    
    parser.add_argument('--version', action='store_true',
                        help='Display version information')
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Greetings command
    greetings_parser = subparsers.add_parser('greetings', help='Display welcome message')
    
    # Quiz command
    quiz_parser = subparsers.add_parser('quiz', help='Start an interactive quiz')
    
    # Thanks command
    thanks_parser = subparsers.add_parser('thanks', help='Display thank you message')
    
    # Repair command
    repair_parser = subparsers.add_parser('repair', help='Repair audio files')
    
    args = parser.parse_args()
    
    # Try auto-repair during initialization
    try:
        auto_repair_audio()
    except Exception as e:
        print(f"Auto-repair failed: {e}")
    
    # Handle version display
    if args.version:
        from . import __version__
        print(f"IITJP version {__version__}")
        print("A Python library for interactive learning with RajLaxmi")
        return
    
    # Handle silent mode
    if args.silent:
        enable_silent_mode(True)
    
    # Handle typing effect
    if args.fast_text:
        enable_typing_effect(False)
    
    # Execute command
    if args.command == 'greetings':
        mam.greetings()
    elif args.command == 'quiz':
        mam.quiz()
    elif args.command == 'thanks':
        mam.thanks()
    elif args.command == 'repair':
        return repair_command()
    else:
        # Default behavior - show help
        parser.print_help()

if __name__ == '__main__':
    main() 