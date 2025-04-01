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
import wave
import pyaudio
import numpy as np
import pkg_resources as pkg_res
from pathlib import Path

# Global flag to enable/disable audio playback
SILENT_MODE = False

# Global variables to track quiz progress
QUIZ_SCORE = 0
QUIZ_ATTEMPTED = 0

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
    global TEMP_DIR  # Moved global declaration to the top of the function
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
                
        # Try to find file in installed package
        try:
            resource_path = pkg_res.resource_filename('iitjp', 'data/questions.json')
            if os.path.exists(resource_path):
                question_file = resource_path
                print(f"[✓] Found questions file in package resources at {question_file}")
        except Exception:
            pass
    
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
    # Make sure we have the .wav extension
    if not filename.endswith('.wav'):
        filename = filename.replace('.mp3', '.wav')
        if not filename.endswith('.wav'):
            filename += '.wav'
    
    # Try to find the file in different locations
    possible_locations = [
        # Check in DATA_DIR
        os.path.join(DATA_DIR, filename),
        
        # Check in the package directory's data folder
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", filename),
        
        # Check in the current directory
        os.path.join(os.getcwd(), filename),
        
        # Check in the current directory's data subfolder
        os.path.join(os.getcwd(), "data", filename),
        
        # Try to find in installed package data directory
        os.path.join(sys.prefix, "data", filename),
    ]
    
    # Check all possible locations
    for file_path in possible_locations:
        if os.path.exists(file_path):
            return file_path
    
    # If not found in filesystem, try to find in package resources
    try:
        resource_path = pkg_res.resource_filename('iitjp', f'data/{filename}')
        if os.path.exists(resource_path):
            return resource_path
    except Exception:
        pass
            
    try:
        # Try to look in the package's data directory specifically
        if pkg_res.resource_exists('iitjp', f'../data/{filename}'):
            return pkg_res.resource_filename('iitjp', f'../data/{filename}')
    except Exception:
        pass
    
    # If all else fails, check installed package data
    try:
        for dist in pkg_res.working_set:
            if dist.key == 'iitjp':
                for path in dist._get_metadata('installed-files.txt'):
                    if filename in path:
                        return os.path.join(dist.location, path)
    except Exception:
        pass

    # Couldn't find the file
    print(f"[⚠️ Audio file '{filename}' not found in any expected location]")
    return None

# Play an audio file in a separate thread
def play_audio_threaded(filename):
    thread = threading.Thread(target=play_audio, args=(filename,))
    thread.daemon = True
    thread.start()
    return thread

# Play a WAV file using PyAudio (cross-platform)
def play_audio(filename):
    global SILENT_MODE
    if SILENT_MODE:
        print(f"[🔇 Silent Mode: Audio '{filename}' would play here]")
        return
    
    # Get the audio file path
    file_path = get_audio_path(filename)
    if not file_path:
        print(f"[⚠️ Audio file '{filename}' not found]")
        return
    
    # Validate the WAV file before attempting to play it
    try:
        # Check if the file exists and is readable
        if not os.path.isfile(file_path):
            print(f"[⚠️ Audio file '{file_path}' does not exist]")
            return
            
        # Open the WAV file for validation
        try:
            wf = wave.open(file_path, 'rb')
            # Get basic parameters to verify it's a valid WAV file
            channels = wf.getnchannels()
            rate = wf.getframerate()
            frames = wf.getnframes()
            width = wf.getsampwidth()
            
            # Log the WAV file parameters
            print(f"[🔊 Playing audio: {filename}, Format: {channels} channels, {rate} Hz, {width} bytes/sample]")
            
            # Close and reopen the file to ensure clean state
            wf.close()
            wf = wave.open(file_path, 'rb')
        except Exception as e:
            print(f"[⚠️ Invalid WAV file format: {e}]")
            # Try system default player as a fallback
            _play_with_system_player(file_path)
            return
        
        # Platform-specific audio playback methods
        try:
            # Initialize PyAudio
            p = pyaudio.PyAudio()
            
            # Open a stream to play the audio
            stream = p.open(format=p.get_format_from_width(width),
                            channels=channels,
                            rate=rate,
                            output=True)
            
            # Read data in chunks and play
            chunk_size = 1024
            data = wf.readframes(chunk_size)
            
            while data:
                stream.write(data)
                data = wf.readframes(chunk_size)
                
            # Cleanup
            stream.stop_stream()
            stream.close()
            p.terminate()
            wf.close()
            
        except Exception as e:
            print(f"[⚠️ PyAudio playback failed: {e}]")
            # Try system default player as a fallback
            _play_with_system_player(file_path)
    
    except Exception as e:
        print(f"[⚠️ All audio playback methods failed: {e}]")
        SILENT_MODE = True
        print("[🔇 Switching to silent mode due to persistent errors]")

# Helper function to play audio with system player
def _play_with_system_player(file_path):
    try:
        print("[🔊 Trying system default player...]")
        if PLATFORM == 'windows' or sys.platform == 'win32':
            os.system(f'start "" "{file_path}"')
        elif PLATFORM == 'darwin':
            os.system(f'open "{file_path}"')
        else:  # Linux
            os.system(f'xdg-open "{file_path}" > /dev/null 2>&1')
    except Exception as e:
        print(f"[⚠️ System player failed: {e}]")
        SILENT_MODE = True
        print("[🔇 Switching to silent mode due to playback errors]")

# Simple typing effect for text display (without table borders)
def type_text(text, speed=0.05):
    print("\n")
    for line in text.split('\n'):
        # Print line by line with typing effect
        for char in line:
            print(char, end="", flush=True)
            time.sleep(speed)
        print()  # New line after each line of text
    print()  # Extra line at the end

# Typing text with simultaneous audio playback
def type_text_with_audio(text, audio_file, speed=0.05):
    # Make sure the audio file has .wav extension
    if not audio_file.endswith('.wav'):
        audio_file = audio_file.replace('.mp3', '.wav')
        if not audio_file.endswith('.wav'):
            audio_file += '.wav'
    
    # Start audio playback in a background thread
    audio_thread = play_audio_threaded(audio_file)
    
    # Display the text with typing effect
    type_text(text)
    
    # Optional: Wait for audio to complete if needed
    # audio_thread.join()

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
    type_text_with_audio(greeting_text, "greeting.wav")
    
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
    type_text_with_audio(quiz_text, "start_quiz.wav")

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
    play_audio("end_quiz.wav")

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
    play_audio("end_quiz.wav")

# Command: mam(thanks)
def thanks():
    thanks_text = "I hope you enjoyed this learning experience!\nThis program is still in its early stages, so there might be a few issues—but don't worry, I'm always open to feedback.\nUntil next time—bye! See you again!"
    type_text_with_audio(thanks_text, "farewell.wav")

# Set silent mode function for external use
def set_silent_mode(silent=True):
    global SILENT_MODE
    SILENT_MODE = silent
    print(f"[🔧 Silent mode {'enabled' if silent else 'disabled'}]") 