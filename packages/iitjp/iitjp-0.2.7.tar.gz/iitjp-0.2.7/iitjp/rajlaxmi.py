from .audio import AudioPlayer, play_audio_threaded
import os
import json
import time
import random
import tempfile
import sys
import threading
import importlib.util
import shutil
import platform

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
        except Exception:
            pass
    
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
        except Exception:
            # Fallback to system temp directory
            TEMP_DIR = tempfile.gettempdir()
            return os.path.exists(TEMP_DIR)
    return True

# Load platform-specific modules (silently)
def load_platform_modules():
    """Load platform-specific modules when needed."""
    if PLATFORM == 'windows' or sys.platform == 'win32':
        try:
            import win32api
            return True
        except ImportError:
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "pywin32"],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                try:
                    import win32api
                    return True
                except ImportError:
                    return False
            except Exception:
                return False
    return False

# Load MCQs from JSON file
def load_questions():
    question_file = os.path.join(DATA_DIR, "questions.json")
    if not os.path.exists(question_file):
        # Try to locate questions.json in various places silently
        for possible_dir in [
            os.path.dirname(os.path.abspath(__file__)),  # Package directory
            os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."),  # Parent directory
            os.getcwd(),  # Current working directory
            os.path.join(os.getcwd(), "data")  # data subdirectory of current working directory
        ]:
            test_path = os.path.join(possible_dir, "questions.json")
            if os.path.exists(test_path):
                question_file = test_path
                break
            
            test_path = os.path.join(possible_dir, "data", "questions.json")
            if os.path.exists(test_path):
                question_file = test_path
                break
    
    try:
        if os.path.exists(question_file):
            with open(question_file, "r", encoding="utf-8") as file:
                questions = json.load(file)["questions"]
                # Shuffle the questions to get random order each time
                random.shuffle(questions)
                return questions
        else:
            return []
    except Exception:
        return []

questions = load_questions()

# Get audio file path (delegates to AudioPlayer)
def get_audio_path(filename):
    """Get the full path to an audio file"""
    from .audio import find_audio_file
    return find_audio_file(filename)

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

# Print a title with separator
def print_title(title):
    """Print a title with a separator line"""
    print("\n" + "=" * 50)
    print(f" {title} ".center(50, "="))
    print("=" * 50)

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
            choice = int(choice)
            if 1 <= choice <= len(options):
                return choice
            else:
                print(f"Please enter a number between 1 and {len(options)}.")
        except ValueError:
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
    """Start the interactive quiz with audio"""
    global QUIZ_SCORE, QUIZ_ATTEMPTED
    
    # Reset quiz stats
    QUIZ_SCORE = 0
    QUIZ_ATTEMPTED = 0
    
    # Welcome message
    print_title("Statistical Quiz")
    type_text_with_audio(
        "Welcome to our statistical quiz! Let's test your knowledge with a few questions.",
        "start_quiz.mp3"
    )
    
    if not questions:
        type_text("Sorry, I couldn't load the questions. Please make sure the data files are properly installed.")
        return
    
    # Use up to 5 random questions
    quiz_questions = questions[:5]
    total_questions = len(quiz_questions)
    
    for i, question in enumerate(quiz_questions, 1):
        # Shuffle options
        options = question["options"].copy()
        random.shuffle(options)
        
        # Display question and get answer
        user_choice = display_question(question, options, i, total_questions)
        QUIZ_ATTEMPTED += 1
        
        # Check answer
        user_answer = options[user_choice - 1]
        correct_answer = question["answer"]
        
        if user_answer == correct_answer:
            print("✓ Correct!")
            QUIZ_SCORE += 1
        else:
            print(f"✗ Incorrect. The correct answer is: {correct_answer}")
        
        # Provide explanation if available
        if "explanation" in question and question["explanation"]:
            print(f"Explanation: {question['explanation']}")
        
        if i < total_questions:
            print("\nMoving to the next question...")
            time.sleep(1)  # Short pause between questions
    
    # Quiz completed
    play_audio("end_quiz.mp3")
    show_quiz_results()
    
    # Return to main menu prompt
    print("\nType 'iitjp.mam.greetings()' to return to the main menu.")

# Quit quiz function
def quitquiz():
    """End the quiz with a farewell message"""
    play_audio("end_quiz.mp3")
    print_title("Quiz Ended")
    type_text("Thank you for participating in the quiz. See you next time!")

# Thanks function
def thanks():
    """Display a thank you message"""
    play_audio("farewell.mp3")
    type_text_with_audio(
        "Thank you for using this interactive learning tool! I hope it helped in your statistical journey. "
        "Remember, practice makes perfect. Keep exploring the wonderful world of statistics!",
        "farewell.mp3"
    )

# Set silent mode
def set_silent_mode(silent=True):
    """Enable or disable audio playback"""
    global SILENT_MODE
    SILENT_MODE = silent
