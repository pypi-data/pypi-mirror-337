from .audio import AudioPlayer, play_audio_threaded
import os
import json
import time
import random
import tempfile
import sys
import threading
import importlib.resources as pkg_resources
import importlib.util
import shutil
import platform
import subprocess
import warnings

# Global flag to enable/disable audio playback
SILENT_MODE = False

# Global variables to track quiz progress
QUIZ_SCORE = 0
QUIZ_ATTEMPTED = 0

# Global settings
TYPING_EFFECT_ENABLED = True  # Can be disabled for immediate text display

# Get platform information
PLATFORM = platform.system().lower()  # 'darwin', 'windows', 'linux'

# Get package base directory - works both in development and installed mode
def get_package_root():
    package_dir = os.path.dirname(os.path.abspath(__file__))
    if os.path.exists(os.path.join(package_dir, "..", "data")):
        # Running in development mode
        return os.path.abspath(os.path.join(package_dir, ".."))
    else:
        # Running as installed package
        try:
            # Get site-packages location
            spec = importlib.util.find_spec("iitjp")
            if spec is not None:
                site_packages_dir = os.path.dirname(os.path.dirname(spec.origin))
                # Look for data directory in site-packages
                data_dir = os.path.join(site_packages_dir, "data")
                if os.path.exists(data_dir):
                    return site_packages_dir
        except Exception as e:
            print(f"[⚠️ Error finding package root: {e}]")
    
    # Fallback: Use current directory
    return os.getcwd()

# Set up paths
PACKAGE_ROOT = get_package_root()
DATA_DIR = os.path.join(PACKAGE_ROOT, "data")
TEMP_DIR = os.path.join(PACKAGE_ROOT, "temp")

# Ensure temp directory exists
def ensure_temp_dir():
    global TEMP_DIR
    if not os.path.exists(TEMP_DIR):
        try:
            os.makedirs(TEMP_DIR, exist_ok=True)
            return True
        except Exception as e:
            print(f"[⚠️ Could not create temp directory: {e}]")
            # Fallback to system temp directory
            TEMP_DIR = tempfile.gettempdir()
            return os.path.exists(TEMP_DIR)
    return True

# Load platform-specific modules
def load_platform_modules():
    """Load platform-specific modules when needed."""
    if PLATFORM == 'windows' or sys.platform == 'win32':
        try:
            # pywin32 is not directly importable - check for win32api instead
            import win32api
            return True
        except ImportError:
            try:
                # Try to install pywin32 if missing
                print("[ℹ️ Installing Windows-specific dependencies...]")
                subprocess.run([sys.executable, "-m", "pip", "install", "pywin32"],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                # Need to check the actual module we'll use
                import win32api
                return True
            except ImportError:
                print("[⚠️ Warning: pywin32 installed but win32api module not found. Some features may not work properly.]")
                return False
            except Exception as e:
                print(f"[⚠️ Warning: Could not install or use pywin32: {e}. Some features may not work properly.]")
                return False
    elif PLATFORM == 'darwin':
        try:
            from AppKit import NSSound
            return True
        except ImportError:
            try:
                # Try to install pyobjc-framework-Cocoa if missing
                print("[ℹ️ Installing macOS-specific dependencies...]")
                subprocess.run([sys.executable, "-m", "pip", "install", "pyobjc-framework-Cocoa"],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                from AppKit import NSSound
                return True
            except Exception as e:
                print(f"[⚠️ Warning: Could not install or use pyobjc-framework-Cocoa: {e}. Some features may not work properly.]")
                return False
    return False

# Load MCQs from JSON file
def load_questions():
    question_file = os.path.join(DATA_DIR, "questions.json")
    if not os.path.exists(question_file):
        print(f"[⚠️ Question file not found at {question_file}]")
        # Try to locate questions.json in various places
        for possible_dir in [
            os.path.dirname(os.path.abspath(__file__)),  # Package directory
            os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."),  # Parent directory
            os.getcwd(),  # Current working directory
            os.path.join(os.getcwd(), "data")  # data subdirectory of current working directory
        ]:
            test_path = os.path.join(possible_dir, "questions.json")
            if os.path.exists(test_path):
                question_file = test_path
                print(f"[✓] Found questions file at {question_file}")
                break
            
            test_path = os.path.join(possible_dir, "data", "questions.json")
            if os.path.exists(test_path):
                question_file = test_path
                print(f"[✓] Found questions file at {question_file}")
                break
    
    try:
        if os.path.exists(question_file):
            with open(question_file, "r", encoding="utf-8") as file:
                questions = json.load(file)["questions"]
                # Shuffle the questions to get random order each time
                random.shuffle(questions)
                return questions
        else:
            print(f"[⚠️ Questions file not found! Looked in {question_file}]")
            return []
    except Exception as e:
        print(f"[⚠️ Error loading questions: {e}]")
        return []

questions = load_questions()

# Get audio file path
def get_audio_path(filename):
    """Get the full path to an audio file, checking multiple locations."""
    # First check in the DATA_DIR
    file_path = os.path.join(DATA_DIR, filename)
    if os.path.exists(file_path):
        return file_path
    
    # Check in the package directory's data folder
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", filename)
    if os.path.exists(file_path):
        return file_path
    
    # Check in the current directory
    file_path = os.path.join(os.getcwd(), filename)
    if os.path.exists(file_path):
        return file_path
    
    # Check in the current directory's data subfolder
    file_path = os.path.join(os.getcwd(), "data", filename)
    if os.path.exists(file_path):
        return file_path
    
    # Couldn't find the file
    print(f"[⚠️ Audio file '{filename}' not found in any expected location]")
    return None

# Play an audio file using the appropriate method for each platform
def play_audio(filename):
    """Play an audio file using platform-specific methods"""
    global SILENT_MODE
    if SILENT_MODE:
        print(f"[🔇 Silent Mode: Audio '{filename}' would play here]")
        return
    
    # Get the audio file path
    file_path = get_audio_path(filename)
    if not file_path:
        print(f"[⚠️ Audio file '{filename}' not found]")
        return
    
    # Use our new AudioPlayer (much more compatible)
    try:
        success = AudioPlayer.play(file_path, block=True)
        if not success:
            print("[⚠️ Audio playback failed. Running in silent mode.]")
            SILENT_MODE = True
    except Exception as e:
        print(f"[⚠️ Audio playback error: {e}]")
        print("[ℹ️ Running in silent mode due to errors]")
        SILENT_MODE = True

# Enable or disable typing effect
def set_typing_effect(enabled=True):
    global TYPING_EFFECT_ENABLED
    TYPING_EFFECT_ENABLED = enabled
    print(f"[ℹ️ Typing effect {'enabled' if enabled else 'disabled'}]")

# Simple typing effect for text display (without table borders)
def type_text(text, speed=0.01):  # Reduced default speed for faster typing
    """Display text with a typing effect"""
    global TYPING_EFFECT_ENABLED
    
    print("\n")
    
    # If typing effect is disabled, just print the text immediately
    if not TYPING_EFFECT_ENABLED:
        print(text)
        print()  # Extra line at the end
        return
        
    for line in text.split('\n'):
        # Print line by line with typing effect
        for char in line:
            print(char, end="", flush=True)
            time.sleep(speed)
        print()  # New line after each line of text
    
    print()  # Extra line at the end

# Calculate approximate audio duration from text length for better synchronization
def estimate_audio_duration(text, words_per_minute=150):
    """Estimate audio duration in seconds based on text length"""
    # Approximate words by counting spaces and adding 1
    word_count = len(text.split()) 
    # Convert words per minute to seconds
    return (word_count / words_per_minute) * 60

# Typing text with simultaneous audio playback
def type_text_with_audio(text, audio_file, speed=None, wait_for_audio=False):
    """
    Display text with a typing effect while playing audio.
    Automatically adjusts typing speed to match audio duration.
    
    Args:
        text: The text to display with typing effect
        audio_file: Filename of the audio to play
        speed: If provided, uses fixed typing speed instead of auto-adjustment
        wait_for_audio: Whether to wait for audio to complete before returning
    """
    # Start audio playback in a background thread
    audio_thread = play_audio_threaded(audio_file)
    
    if speed is None:
        # Auto-adjust typing speed based on text length to match audio
        estimated_duration = estimate_audio_duration(text)
        # Calculate total characters in text
        total_chars = sum(len(line) for line in text.split('\n'))
        if total_chars > 0 and estimated_duration > 0:
            # Calculate delay per character to match audio duration
            # Using 80% of the estimated duration to finish typing before audio ends
            speed = (estimated_duration * 0.8) / total_chars
        else:
            # Fallback to a moderate typing speed
            speed = 0.01
            
    # Display the text with typing effect
    type_text(text, speed)
    
    # Wait for audio to complete if requested
    if wait_for_audio and audio_thread.is_alive():
        # Wait with a timeout to prevent hanging
        audio_thread.join(timeout=10)  # 10 second timeout

# Pretty print a title with borders (keep this styled for command section)
def print_title(title):
    width = 80
    print("\n" + "╔" + "═" * (width-2) + "╗")
    padding = (width - len(title) - 4) // 2
    print("║" + " " * padding + f"● {title} ●" + " " * (width - padding - len(title) - 4 - 2) + "║")
    print("╚" + "═" * (width-2) + "╝\n")

# Display a question without borders
def display_question(question, options, qnum, total):
    # Print question number and total
    print(f"\nQuestion {qnum} of {total}")
    print("-" * 50)
    
    # Print the question
    print(f"{question}\n")
    
    # Print options in a single column
    for i, option in enumerate(options):
        print(f"{chr(65+i)}. {option}")
    
    print("\nEnter your answer (A/B/C/D) or type 'mam.quitquiz()' to exit:")

# Show quiz results based on attempted questions
def show_quiz_results():
    global QUIZ_SCORE, QUIZ_ATTEMPTED
    
    if QUIZ_ATTEMPTED == 0:
        print("\nNo questions were attempted!")
        return
    
    print("\n" + "-" * 50)
    print(f"Quiz results: {QUIZ_SCORE}/{QUIZ_ATTEMPTED}")
    
    percentage = (QUIZ_SCORE / QUIZ_ATTEMPTED) * 100
    print(f"Percentage: {percentage:.1f}%")
    
    if percentage >= 90:
        print("Excellent! Outstanding performance!")
    elif percentage >= 70:
        print("Good job! Well done!") 
    elif percentage >= 50:
        print("Not bad! Keep practicing.")
    else:
        print("You can do better! Keep studying.")
    
    print("-" * 50)

# Command: mam(greetings)
def greetings():
    greeting_text = "Hello, students! I'm your virtual teacher, RajLaxmi, and I warmly welcome you to this new Python-powered world of learning Foundations of Statistics.\nFirst of all, a big thanks to RajLaxmi Mam for lending her voice to make this possible.\nNow, let's get started! What's on your mind today?"
    type_text_with_audio(greeting_text, "greeting.mp3")
    
    # Display available commands after greeting (keep this styled)
    print_title("Available Commands")
    
    commands = [
        ("mam.greetings()", "Get a welcome message from your teacher"),
        ("mam.quiz()", "Start an interactive statistics quiz"),
        ("mam.quitquiz()", "Exit from the current quiz"),
        ("mam.thanks()", "Thank your teacher and say goodbye")
    ]
    
    width = 80
    print("┌" + "─" * 25 + "┬" + "─" * (width-27) + "┐")
    print("│ " + "Command".ljust(23) + "│ " + "Description".ljust(width-29) + "│")
    print("├" + "─" * 25 + "┼" + "─" * (width-27) + "┤")
    
    for cmd, desc in commands:
        print("│ " + cmd.ljust(23) + "│ " + desc.ljust(width-29) + "│")
    
    print("└" + "─" * 25 + "┴" + "─" * (width-27) + "┘")
    print("\nUse these commands to interact with your virtual teacher Rajlaxmi!")

# Command: mam(quiz)
def quiz():
    global QUIZ_SCORE, QUIZ_ATTEMPTED
    
    # Reset quiz tracking variables
    QUIZ_SCORE = 0
    QUIZ_ATTEMPTED = 0
    
    if not questions:
        type_text("No questions found! Make sure your data file exists.")
        return

    quiz_text = "Alright! As you requested, let's begin the quiz.\nI won't disturb you until you submit your answers—so take your time. Good luck!"
    type_text_with_audio(quiz_text, "start_quiz.mp3")

    total = len(questions)
    
    # Get a fresh randomized set of questions
    quiz_questions = load_questions()
    
    for qnum, q in enumerate(quiz_questions, 1):
        display_question(q["question"], q["options"], qnum, total)
        
        answer = input("> ").strip()
        
        # Check if user wants to quit
        if answer.lower() in ["mam.quitquiz()", "quit", "exit"]:
            print("\nQuitting quiz...")
            quitquiz()
            return
        
        # Count this as an attempted question
        QUIZ_ATTEMPTED += 1
        
        # Convert to uppercase for comparison (case-insensitive)
        answer = answer.upper()
        
        # Check if the answer is valid (A/B/C/D)
        if len(answer) == 1 and answer in "ABCD":
            # Convert letter to index (A=0, B=1, etc.) and get the option text
            answer_idx = ord(answer) - ord('A')
            if 0 <= answer_idx < len(q["options"]):
                # Get selected answer text and correct answer text
                selected_answer_text = q["options"][answer_idx].strip()
                correct_answer_text = q["answer"].strip()
                
                # Case-insensitive comparison
                is_correct = selected_answer_text.upper() == correct_answer_text.upper()
            else:
                is_correct = False  # Invalid option index
        else:
            # If not A/B/C/D format, check if text matches directly (case-insensitive)
            is_correct = answer.upper() == q["answer"].strip().upper()
        
        if is_correct:
            print("\n✅ Correct!\n")
            QUIZ_SCORE += 1
        else:
            print(f"\n❌ Wrong! The correct answer was: {q['answer']}\n")
        
    # All questions completed, show final score
    show_quiz_results()
    
    # Play end quiz audio
    play_audio("end_quiz.mp3")

# Command: mam(quitquiz)
def quitquiz():
    quit_text = "I hope you did well! Thanks for learning with me."
    type_text(quit_text)
    
    # Show results for attempted questions
    show_quiz_results()
    
    # Continue with the farewell message
    continue_text = "If you'd like to try the quiz again, just let me know!"
    type_text(continue_text)
    
    # Play end quiz audio
    play_audio("end_quiz.mp3")

# Command: mam(thanks)
def thanks():
    thanks_text = "I hope you enjoyed this learning experience!\nThis program is still in its early stages, so there might be a few issues—but don't worry, I'm always open to feedback.\nUntil next time—bye! See you again!"
    type_text_with_audio(thanks_text, "farewell.mp3")

# Set silent mode function for external use
def set_silent_mode(silent=True):
    global SILENT_MODE
    SILENT_MODE = silent
    print(f"[🔧 Silent mode {'enabled' if silent else 'disabled'}]")
