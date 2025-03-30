"""
Command-line interface for IITJP package
"""

import argparse
import sys

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description="IITJP - Interactive learning tool")
    
    # Command arguments
    parser.add_argument("--greet", action="store_true", help="Display greeting message")
    parser.add_argument("--quiz", action="store_true", help="Start the quiz")
    parser.add_argument("--thanks", action="store_true", help="Display thank you message")
    parser.add_argument("--silent", action="store_true", help="Run in silent mode (no audio)")
    parser.add_argument("--repair", action="store_true", help="Repair audio files")
    parser.add_argument("--fast-text", action="store_true", help="Disable typing effect for instant text display")
    
    args = parser.parse_args()
    
    # Import IITJP modules
    from .rajlaxmi import greetings, quiz, thanks, quitquiz, set_silent_mode, set_typing_effect
    
    # Apply settings
    if args.silent:
        set_silent_mode(True)
    
    if args.fast_text:
        set_typing_effect(False)
    
    # Run repair if requested
    if args.repair:
        from .iitjp_repair import repair_package
        repair_package()
        print("Repair completed.")
        return 0
    
    # Run requested command
    if args.greet:
        greetings()
    elif args.quiz:
        quiz()
    elif args.thanks:
        thanks()
    else:
        # Default to greeting if no command specified
        greetings()
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 