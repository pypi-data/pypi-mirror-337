"""
Simple Demo of Enhanced IITJP Library

This script demonstrates the key features of the enhanced library without requiring user interaction.
It now shows the border-less text for voiceovers and questions with table borders only in instruction sections.
"""
import iitjp
import time

print("\n=== IITJP LIBRARY ENHANCED DEMO ===\n")

# Enable silent mode for faster demo
iitjp.enable_silent_mode(True)
print("Silent mode enabled for demo purposes\n")

print("1. Showing greeting with border-less text...")
iitjp.mam.greetings()
time.sleep(1)

print("\n2. Demonstrating randomized questions with border-less display...")
# Patch quiz function to only show the display without waiting for input
import iitjp.rajlaxmi
import builtins

original_input = builtins.input
original_questions = iitjp.rajlaxmi.questions

# Limit to just one question for demo
iitjp.rajlaxmi.questions = iitjp.rajlaxmi.questions[:1]

try:
    # Override input to auto-answer
    builtins.input = lambda _: "C"
    
    # Only show one question
    original_display = iitjp.rajlaxmi.display_question
    
    def demo_display(*args, **kwargs):
        original_display(*args, **kwargs)
        # Auto-exit after showing one question's display
        raise KeyboardInterrupt()
    
    # Replace display function
    iitjp.rajlaxmi.display_question = demo_display
    
    try:
        iitjp.mam.quiz()
    except KeyboardInterrupt:
        print("\nQuiz display demonstration completed")
    except Exception as e:
        print(f"Error in quiz: {e}")
    
finally:
    # Restore original functions and data
    builtins.input = original_input
    iitjp.rajlaxmi.questions = original_questions
    iitjp.rajlaxmi.display_question = original_display

time.sleep(1)

print("\n3. Demonstrating thanks message with border-less text...")
iitjp.mam.thanks()

print("\n=== Demo Completed ===")
print("The updated library now features:")
print("✓ Border-less text for voiceovers and questions")
print("✓ Table borders retained only in the instructions section")
print("✓ Randomized questions order")
print("✓ Ability to quit the quiz with 'mam.quitquiz()'")
print("✓ Text matching the audio content")
print("✓ Better feedback for correct/incorrect answers")
print("\nTo use the library with audio, disable silent mode:"
      "\n    import iitjp"
      "\n    iitjp.enable_silent_mode(False)"
      "\n    iitjp.mam.greetings()") 

# Build the package
python setup.py sdist bdist_wheel