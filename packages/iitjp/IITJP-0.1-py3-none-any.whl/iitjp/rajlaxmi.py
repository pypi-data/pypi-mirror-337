from pydub import AudioSegment
from pydub.playback import play
import os
import json
import time
import random
import tempfile
import sys
import threading

# Global flag to enable/disable audio playback
SILENT_MODE = False

# Global variables to track quiz progress
QUIZ_SCORE = 0
QUIZ_ATTEMPTED = 0

# Custom temporary directory path for audio playback
TEMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../temp")

# Load MCQs from JSON file
def load_questions():
    data_file = os.path.join(os.path.dirname(__file__), "../data/questions.json")
    if os.path.exists(data_file):
        with open(data_file, "r", encoding="utf-8") as file:
            questions = json.load(file)["questions"]
            # Shuffle the questions to get random order each time
            random.shuffle(questions)
            return questions
    return []

questions = load_questions()

# Ensure temp directory exists
def ensure_temp_dir():
    if not os.path.exists(TEMP_DIR):
        try:
            os.makedirs(TEMP_DIR)
            return True
        except Exception as e:
            print(f"[⚠️ Could not create temp directory: {e}]")
            return False
    return True

# Play an audio file in a separate thread
def play_audio_threaded(filename):
    thread = threading.Thread(target=play_audio, args=(filename,))
    thread.daemon = True
    thread.start()
    return thread

# Play an audio file
def play_audio(filename):
    global SILENT_MODE
    if SILENT_MODE:
        print(f"[🔇 Silent Mode: Audio '{filename}' would play here]")
        return
        
    file_path = os.path.join(os.path.dirname(__file__), f"../data/{filename}")
    if os.path.exists(file_path):
        try:
            # Method 1: Try with pydub and custom temp files
            try:
                audio = AudioSegment.from_file(file_path)
                # Create a custom temporary file with permissions
                if ensure_temp_dir():
                    # Set a custom temp directory for pydub
                    temp_file = os.path.join(TEMP_DIR, f"temp_{int(time.time())}.wav")
                    
                    # Export the audio to our temp location instead of letting pydub handle it
                    audio.export(temp_file, format="wav")
                    
                    # Play the exported file directly instead of using pydub's play
                    if sys.platform == 'win32':
                        # Windows specific approach
                        from subprocess import call
                        call(["powershell", "-c", f"(New-Object Media.SoundPlayer '{temp_file}').PlaySync()"])
                    else:
                        # Fall back to pydub's play for other platforms
                        audio_to_play = AudioSegment.from_file(temp_file)
                        play(audio_to_play)
                        
                    # Clean up the temp file
                    try:
                        os.remove(temp_file)
                    except:
                        pass
                else:
                    # Try direct playback
                    play(audio)
            except Exception as e:
                print(f"[⚠️ First playback method failed: {e}]")
                
                # Method 2: Try with direct winsound (Windows only, no temp files needed)
                if sys.platform == 'win32':
                    try:
                        print("[🔊 Trying direct winsound playback...]")
                        import winsound
                        winsound.PlaySound(file_path, winsound.SND_FILENAME)
                        return  # Success!
                    except Exception as e:
                        print(f"[⚠️ Winsound playback failed: {e}]")
                
                # Method 3: Last resort - try with system default player
                try:
                    print("[🔊 Trying system default player...]")
                    if sys.platform == 'win32':
                        os.system(f'start "" "{file_path}"')
                    elif sys.platform == 'darwin':  # macOS
                        os.system(f'open "{file_path}"')
                    else:  # Linux
                        os.system(f'xdg-open "{file_path}"')
                    return  # Success!
                except Exception as e:
                    print(f"[⚠️ System player failed: {e}]")
                    
                # If all methods fail, switch to silent mode
                SILENT_MODE = True
                print("[🔇 Switching to silent mode due to playback errors]")
        except Exception as e:
            print(f"[⚠️ Error loading audio file: {e}]")
    else:
        print(f"[⚠️ Audio file '{filename}' not found.]")

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
