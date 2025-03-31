from pydub import AudioSegment
from pydub.playback import play
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
import winsound  # Import winsound for Windows audio playback
import pkg_resources

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
    
    # First, try to find data within the package
    package_data_dir = os.path.join(package_dir, "data")
    if os.path.exists(package_data_dir):
        return package_dir
    
    # Next, check parent directory (for development)
    if os.path.exists(os.path.join(package_dir, "..", "data")):
        return os.path.abspath(os.path.join(package_dir, ".."))
    
    # For installed packages, use package resources to locate files
    try:
        # Check if we can access data files via package resources
        # Just check if one file exists to confirm this approach works
        data_file_path = pkg_resources.resource_filename("iitjp", "data/questions.json")
        if os.path.exists(data_file_path):
            return os.path.dirname(os.path.dirname(data_file_path))
    except Exception as e:
        print(f"[⚠️ Error locating package data: {e}]")
    
    # Fallback: Use current directory
    return os.getcwd()

# Ensure the data directory structure exists
def ensure_data_directory():
    # First try to create the directory structure if it doesn't exist
    try:
        os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data"), exist_ok=True)
    except Exception as e:
        print(f"[⚠️ Could not create package data directory: {e}]")
    
    # Copy data files from the source data directory to the package data directory
    # This handles the case when running from source
    try:
        src_data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
        dst_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
        
        if os.path.exists(src_data_dir) and os.path.exists(dst_data_dir):
            # Copy all mp3 and json files
            for filename in os.listdir(src_data_dir):
                if filename.endswith(".mp3") or filename.endswith(".json"):
                    src_file = os.path.join(src_data_dir, filename)
                    dst_file = os.path.join(dst_data_dir, filename)
                    if not os.path.exists(dst_file):
                        shutil.copy2(src_file, dst_file)
    except Exception as e:
        print(f"[⚠️ Error copying data files: {e}]")

# Initialize data directory
ensure_data_directory()

# Set up paths
PACKAGE_ROOT = get_package_root()
DATA_DIR = os.path.join(PACKAGE_ROOT, "data")

# For temporary files
TEMP_DIR = os.path.join(tempfile.gettempdir(), "iitjp")

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

# Load MCQs from JSON file
def load_questions():
    # First try to get the file using package resources
    try:
        question_file = pkg_resources.resource_filename("iitjp", "data/questions.json")
        if os.path.exists(question_file):
            with open(question_file, "r", encoding="utf-8") as file:
                questions = json.load(file)["questions"]
                # Shuffle the questions to get random order each time
                random.shuffle(questions)
                return questions
    except Exception as e:
        print(f"[⚠️ Error loading questions via package resources: {e}]")
    
    # Try standard file paths
    question_file = os.path.join(DATA_DIR, "questions.json")
    if not os.path.exists(question_file):
        print(f"[⚠️ Question file not found at {question_file}]")
        # Try to locate questions.json in various places
        for possible_dir in [
            os.path.dirname(os.path.abspath(__file__)),  # Package directory
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "data"),  # Package data directory
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
    # First try to get the file using package resources
    try:
        audio_file = pkg_resources.resource_filename("iitjp", f"data/{filename}")
        if os.path.exists(audio_file):
            return audio_file
    except Exception as e:
        print(f"[⚠️ Error locating audio via package resources: {e}]")
    
    # Check in the DATA_DIR
    file_path = os.path.join(DATA_DIR, filename)
    if os.path.exists(file_path):
        return file_path
    
    # Check in the package directory's data folder
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", filename)
    if os.path.exists(file_path):
        return file_path
    
    # Check in the parent directory's data folder
    file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", filename)
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

# Play an audio file in a separate thread
def play_audio_threaded(filename):
    thread = threading.Thread(target=play_audio, args=(filename,))
    thread.daemon = True
    thread.start()
    return thread

# Play an audio file using the appropriate method for each platform
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
    
    # Platform-specific audio playback methods
    try:
        # Windows-specific playback using winsound (preferred for Windows)
        if PLATFORM == 'windows' or sys.platform == 'win32':
            try:
                # For MP3 files, convert to WAV first (winsound only supports WAV)
                if file_path.lower().endswith('.mp3'):
                    if ensure_temp_dir():
                        # Create a temporary WAV file
                        audio = AudioSegment.from_file(file_path)
                        temp_file = os.path.join(TEMP_DIR, f"temp_{int(time.time())}.wav")
                        audio.export(temp_file, format="wav")
                        
                        # Play using winsound
                        winsound.PlaySound(temp_file, winsound.SND_FILENAME)
                        
                        # Clean up the temp file
                        try:
                            os.remove(temp_file)
                        except:
                            pass
                else:
                    # If already a WAV file
                    winsound.PlaySound(file_path, winsound.SND_FILENAME)
            except Exception as e:
                print(f"[⚠️ Winsound playback failed: {e}]")
                # Fallback to alternative Windows methods
                try_windows_fallback_methods(file_path)
        else:
            # For non-Windows platforms use the existing methods
            try_cross_platform_playback(file_path)
    except Exception as e:
        print(f"[⚠️ All audio playback methods failed: {e}]")
        SILENT_MODE = True
        print("[🔇 Switching to silent mode due to persistent errors]")

# Windows fallback methods in case winsound fails
def try_windows_fallback_methods(file_path):
    try:
        # Try PowerShell playback
        from subprocess import call
        
        # Create a wav file if it's not already
        if not file_path.lower().endswith('.wav'):
            audio = AudioSegment.from_file(file_path)
            temp_file = os.path.join(TEMP_DIR, f"temp_{int(time.time())}.wav")
            audio.export(temp_file, format="wav")
            file_path = temp_file
        
        call(["powershell", "-c", f"(New-Object Media.SoundPlayer '{file_path}').PlaySync()"])
    except Exception as e:
        print(f"[⚠️ PowerShell playback failed: {e}]")
        # Try system default player
        try:
            os.system(f'start "" "{file_path}"')
        except Exception as e:
            print(f"[⚠️ System player failed: {e}]")
            # Last resort - use pydub's play
            try:
                audio = AudioSegment.from_file(file_path)
                play(audio)
            except Exception as e:
                print(f"[⚠️ Pydub playback failed: {e}]")
                SILENT_MODE = True
                print("[🔇 Switching to silent mode due to playback errors]")

# Cross-platform playback for non-Windows systems
def try_cross_platform_playback(file_path):
    try:
        audio = AudioSegment.from_file(file_path)
        if ensure_temp_dir():
            # Create a temporary file for playback
            temp_file = os.path.join(TEMP_DIR, f"temp_{int(time.time())}.wav")
            audio.export(temp_file, format="wav")
            
            if PLATFORM == 'darwin':
                # macOS-specific playback
                try:
                    from subprocess import call
                    call(["afplay", temp_file])
                except Exception as e:
                    print(f"[⚠️ afplay failed: {e}]")
                    os.system(f'open "{temp_file}"')
            else:
                # Linux and other platforms
                try:
                    from subprocess import call
                    # Try multiple players that might be available
                    for player_cmd in ["aplay", "paplay", "ffplay -nodisp -autoexit"]:
                        try:
                            cmd = f"{player_cmd.split()[0]} --version"
                            ret = os.system(cmd + " > /dev/null 2>&1")
                            if ret == 0:  # Player exists
                                os.system(f"{player_cmd} '{temp_file}' > /dev/null 2>&1")
                                break
                        except:
                            continue
                except Exception as e:
                    print(f"[⚠️ System audio players failed: {e}]")
                    audio_to_play = AudioSegment.from_file(temp_file)
                    play(audio_to_play)
            
            # Clean up the temp file
            try:
                os.remove(temp_file)
            except:
                pass
        else:
            # Fallback to direct pydub playback
            play(audio)
    except Exception as e:
        print(f"[⚠️ Cross-platform playback failed: {e}]")
        
        # Try system default player as a last resort
        try:
            if PLATFORM == 'darwin':
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
