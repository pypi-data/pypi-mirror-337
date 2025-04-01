"""
IITJP - Main module.

This module provides the entry point for the package when it's run as a script.
Example: python -m iitjp
"""

import sys
import os
import time
from .rajlaxmi import greetings, quiz, thanks, set_silent_mode

def show_intro():
    """Display an introduction when the package is run directly"""
    print("\n========================================")
    print("IITJP - Interactive Teacher for Statistics")
    print("Version 0.2.16")
    print("========================================")
    print("\nThis package provides an interactive teaching experience")
    print("with RajLaxmi mam as your virtual teacher.\n")
    print("Running in demo mode...\n")

def main():
    """Main entry point when running the package as a script"""
    
    # Show intro information
    show_intro()
    
    # Run a short demo
    # Set to silent mode for faster demo
    set_silent_mode(True)
    
    print("1. First, greeting students...")
    greetings()
    time.sleep(1)  # Short pause between steps
    
    print("\n2. Now, showing how a quiz would start...")
    # Just start the quiz, but don't actually run it in demo mode
    print("Quiz would start here. Use 'import iitjp' and call 'iitjp.mam.quiz()' to try it.")
    time.sleep(1)  # Short pause between steps
    
    print("\n3. Finally, saying goodbye...")
    thanks()
    
    print("\nTo use this package in your code:")
    print("  import iitjp")
    print("  iitjp.enable_silent_mode(False)  # Enable audio")
    print("  iitjp.mam.greetings()")
    print("  iitjp.mam.quiz()")
    print("  iitjp.mam.thanks()")

if __name__ == "__main__":
    main() 