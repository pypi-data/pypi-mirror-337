from .audio import AudioPlayer, play_audio_threaded
import os
import json
import time
import random
import sys
import threading
import platform

# Global flag to enable/disable audio playback
SILENT_MODE = False

# Global variables to track quiz progress
QUIZ_SCORE = 0
QUIZ_ATTEMPTED = 0

# Global settings
TYPING_EFFECT_ENABLED = True  # Can be disabled for immediate text display

# Set silent mode
def set_silent_mode(silent=True):
    """Enable or disable silent mode (no audio)"""
    global SILENT_MODE
    SILENT_MODE = silent

# Play audio file
def play_audio(filename):
    """Play an audio file silently"""
    if SILENT_MODE:
        return
        
    # Direct playback with no output
    AudioPlayer.play(filename, block=False)

# Enable or disable typing effect
def set_typing_effect(enabled=True):
    """Enable or disable the typing effect"""
    global TYPING_EFFECT_ENABLED
    TYPING_EFFECT_ENABLED = enabled

# Type text with a typing effect
def type_text(text, speed=0.01):  # Reduced default speed for faster typing
    """Print text with a typing effect"""
    if not TYPING_EFFECT_ENABLED:
        # Just print instantly if typing effect is disabled
        print(text)
        return
        
    for char in text:
        print(char, end='', flush=True)
        time.sleep(speed)
    print()  # New line at the end

# Estimate audio duration
def estimate_audio_duration(text, words_per_minute=150):
    """Estimate audio duration based on text length and speaking speed"""
    word_count = len(text.split())
    minutes = word_count / words_per_minute
    return minutes * 60  # Convert to seconds

# Type text with audio
def type_text_with_audio(text, audio_file, speed=None, wait_for_audio=False):
    """Display text with a typing effect while playing audio"""
    # Play audio
    if not SILENT_MODE:
        audio_thread = play_audio_threaded(audio_file)
    
    # Calculate typing speed based on audio duration
    if speed is None and not SILENT_MODE:
        # Estimate audio duration
        duration = estimate_audio_duration(text)
        # Calculate typing delay
        char_count = len(text)
        if char_count > 0 and duration > 0:
            speed = duration / (char_count * 1.5)  # Slightly faster than audio
    
    # Default speed if estimation failed or in silent mode
    if speed is None:
        speed = 0.01
    
    # Type text
    if not TYPING_EFFECT_ENABLED:
        # Just print instantly if typing effect is disabled
        print(text)
    else:
        for char in text:
            print(char, end='', flush=True)
            time.sleep(speed)
        print()  # New line at the end
    
    # Wait for audio to finish
    if wait_for_audio and not SILENT_MODE and 'audio_thread' in locals():
        try:
            audio_thread.join()
        except Exception:
            pass

# Load MCQs from JSON file
def load_questions():
    """Load questions from the JSON file"""
    try:
        # Try multiple locations for questions.json
        possible_locations = [
            os.path.join(os.path.dirname(__file__), "questions.json"),
            os.path.join(os.path.dirname(__file__), "data", "questions.json"),
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "questions.json"),
            os.path.join(os.getcwd(), "questions.json"),
            os.path.join(os.getcwd(), "data", "questions.json")
        ]
        
        for location in possible_locations:
            if os.path.exists(location):
                with open(location, "r", encoding="utf-8") as file:
                    questions = json.load(file)["questions"]
                    # Shuffle the questions to get random order each time
                    random.shuffle(questions)
                    return questions
        
        # If no file found, use embedded questions
        return [
            {
                "question": "What is the measure of central tendency that is most affected by extreme values?",
                "options": ["Median", "Mode", "Mean", "Range"],
                "answer": "Mean",
                "explanation": "The mean is calculated by summing all values and dividing by the number of observations, so extreme values significantly impact the result."
            },
            {
                "question": "Which statistical measure represents the middle value in a dataset?",
                "options": ["Mean", "Median", "Mode", "Standard Deviation"],
                "answer": "Median",
                "explanation": "The median is the middle value when the data is arranged in order."
            }
        ]
    except Exception:
        # Return some default questions if loading fails
        return [
            {
                "question": "What is the measure of central tendency that is most affected by extreme values?",
                "options": ["Median", "Mode", "Mean", "Range"],
                "answer": "Mean",
                "explanation": "The mean is calculated by summing all values and dividing by the number of observations, so extreme values significantly impact the result."
            },
            {
                "question": "Which statistical measure represents the middle value in a dataset?",
                "options": ["Mean", "Median", "Mode", "Standard Deviation"],
                "answer": "Median",
                "explanation": "The median is the middle value when the data is arranged in order."
            }
        ]

# Load questions at module import time
questions = load_questions()

# Function to get the path to an audio file
def get_audio_path(filename):
    """Get the full path to an audio file"""
    from .audio import find_audio_file
    return find_audio_file(filename)

# Display an MCQ
def display_question(question, options, qnum, total):
    # Print question number and total
    print(f"\nQuestion {qnum} of {total}:")
    type_text(question["question"])
    
    # Print options
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    
    # Get user input
    while True:
        try:
            choice = input("Your answer (number): ")
            
            # Check if the user is trying to exit
            if choice.lower() in ["q", "quit", "exit", "mam.quitquiz()"]:
                return -1
                
            choice = int(choice)
            if 1 <= choice <= len(options):
                return choice
            else:
                print(f"Please enter a number between 1 and {len(options)}.")
        except ValueError:
            # Check if the user entered a command to quit
            if choice.lower() in ["q", "quit", "exit"] or "quitquiz" in choice.lower():
                return -1
            print("Please enter a valid number.")

# Show quiz results
def show_quiz_results():
    global QUIZ_SCORE, QUIZ_ATTEMPTED
    if QUIZ_ATTEMPTED == 0:
        percentage = 0
    else:
        percentage = (QUIZ_SCORE / QUIZ_ATTEMPTED) * 100
    
    print("\n" + "=" * 50)
    print("Quiz Results".center(50, " "))
    print("=" * 50)
    print(f"Questions attempted: {QUIZ_ATTEMPTED}")
    print(f"Correct answers: {QUIZ_SCORE}")
    print(f"Score: {percentage:.1f}%")
    
    # Feedback based on score
    if percentage >= 80:
        type_text("Excellent work! You've done a fantastic job!")
    elif percentage >= 60:
        type_text("Good job! You're doing well.")
    elif percentage >= 40:
        type_text("Not bad, but there's room for improvement.")
    else:
        type_text("You might need to review the material again.")
    
    print("\n" + "=" * 50)

# Greeting function
def greetings():
    """Display greeting message with audio"""
    greeting_text = (
        "Hello, students! I'm your virtual teacher, RajLaxmi, and I warmly welcome you to this new "
        "Python-powered world of learning Foundations of Statistics.\n"
        "First of all, a big thanks to RajLaxmi Mam for lending her voice to make this possible.\n"
        "Now, let's get started with our journey into the fascinating world of statistics!"
    )
    
    type_text_with_audio(greeting_text, "greeting.mp3", wait_for_audio=True)
    print("\nType 'iitjp.mam.quiz()' to start the quiz.")

# Quiz function
def quiz():
    """Start an interactive quiz"""
    # Reset score
    global QUIZ_SCORE, QUIZ_ATTEMPTED
    QUIZ_SCORE = 0
    QUIZ_ATTEMPTED = 0
    
    # Check if questions are loaded
    if not questions:
        print("No questions available. Please check your installation.")
        return
    
    # Introduction
    type_text_with_audio(
        "Welcome to the quiz session! I'll ask you a series of questions about statistics. "
        "Let's see how well you understand the concepts. Good luck!",
        "start_quiz.mp3"
    )
    
    # Loop through questions
    total_questions = len(questions)
    for i, question in enumerate(questions, 1):
        # Get the question data
        q_text = question["question"]
        options = question["options"]
        correct_answer = question["answer"]
        explanation = question["explanation"]
        
        # Map the correct answer to an index
        correct_index = options.index(correct_answer) + 1
        
        # Display the question and get user's answer
        choice = display_question(question, options, i, total_questions)
        
        # Check if user wants to quit
        if choice == -1:
            quitquiz()
            return
        
        # Check the answer
        QUIZ_ATTEMPTED += 1
        if choice == correct_index:
            QUIZ_SCORE += 1
            print("✓ Correct! " + explanation)
        else:
            print(f"✗ Incorrect. The correct answer is: {correct_answer}")
            print(explanation)
    
    # End of quiz
    type_text_with_audio(
        "That concludes our quiz. Let's see how you performed!",
        "end_quiz.mp3"
    )
    
    # Show results
    show_quiz_results()

# Quit quiz function
def quitquiz():
    """Exit the quiz early"""
    print("\nQuiz terminated.")
    if QUIZ_ATTEMPTED > 0:
        show_quiz_results()
    else:
        print("No questions were attempted.")

# Thanks function
def thanks():
    """Display a thank you message"""
    play_audio("farewell.mp3")
    type_text_with_audio(
        "Thank you for using this interactive learning tool! I hope it helped in your statistical journey. "
        "Remember, practice makes perfect. Keep exploring the wonderful world of statistics!",
        "farewell.mp3"
    )
