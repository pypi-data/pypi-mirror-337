"""
Enhanced UI Demo for IITJP Library

This script demonstrates:
1. Border-less text for voiceovers and questions
2. Table borders retained only in instructions section
3. Randomized quiz questions
4. Ability to quit quiz with "mam.quitquiz()" command
5. Matching text to audio files
"""
import iitjp
import time

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                        ENHANCED IITJP LIBRARY DEMO                         ║
╚════════════════════════════════════════════════════════════════════════════╝
""")

print("This demo shows the new enhanced features of the library:")
print("• Border-less text for voiceovers and questions")
print("• Table borders retained only in instructions section")
print("• Randomized quiz questions each time")
print("• Ability to quit the quiz at any time")
print("• Text content matching the voiceovers")

input("\nPress Enter to start the demo with a greeting...\n")

# Run the greeting function - shows border-less text for voiceover but bordered command table
iitjp.mam.greetings()

time.sleep(2)

print("\n\n>>> QUIZ WITH RANDOMIZED QUESTIONS")
print("Each time you run the quiz, questions appear in random order.")
print("During the quiz, you can type 'mam.quitquiz()' to exit early.")
input("Press Enter to start the quiz demo...\n")

# Since this is a demo, we'll use silent mode to avoid waiting for audio
iitjp.enable_silent_mode(True)

# Run the quiz with limited questions for the demo
import iitjp.rajlaxmi
original_questions = iitjp.rajlaxmi.questions
# Use just 2 questions for the demo
iitjp.rajlaxmi.questions = iitjp.rajlaxmi.questions[:2]

try:
    # Simulate user input to demonstrate functionality
    import builtins
    original_input = builtins.input
    
    # A simple counter to track number of inputs requested
    input_count = 0
    
    # Override input function for demo
    def demo_input(prompt):
        global input_count
        print(prompt)
        
        # First question: answer correctly
        if input_count == 0:
            input_count += 1
            print("(Automatically entering 'C' for first question)")
            return "C"
        
        # Second question: exit quiz
        elif input_count == 1:
            input_count += 1
            print("(Automatically entering 'mam.quitquiz()' to demonstrate quiz exit)")
            return "mam.quitquiz()"
        
        # Default
        else:
            return ""
    
    # Replace input function
    builtins.input = demo_input
    
    # Start the quiz
    try:
        iitjp.mam.quiz()
    except Exception as e:
        print(f"Error during quiz: {e}")
    
except Exception as e:
    print(f"Error: {e}")
finally:
    # Restore original input and questions
    if 'original_input' in locals():
        builtins.input = original_input
    iitjp.rajlaxmi.questions = original_questions
    # Disable silent mode
    iitjp.enable_silent_mode(False)

time.sleep(2)

print("\n\n>>> THANKS MESSAGE")
print("This demonstrates the farewell message:")
input("Press Enter to continue...\n")

# Show the thanks message
iitjp.mam.thanks()

print("\n\nDemo completed!")
print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                         LIBRARY IMPROVEMENTS SUMMARY                        ║
╠════════════════════════════════════════════════════════════════════════════╣
║ ✓ Border-less text for voiceovers and questions                           ║
║ ✓ Table borders retained only in instructions section                     ║
║ ✓ Quiz questions now appear in random order each time                     ║
║ ✓ Ability to exit quiz by typing 'mam.quitquiz()'                         ║
║ ✓ Text content matching the corresponding audio files                     ║
║ ✓ Improved visual feedback for quiz answers and scores                    ║
╚════════════════════════════════════════════════════════════════════════════╝
""") 