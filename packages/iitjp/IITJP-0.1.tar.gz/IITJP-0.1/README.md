# IITJP Python Library

A Python library for an interactive quiz assistant named RajLaxmi.

## Installation

```bash
pip install -e .
```

## Requirements

- Python 3.6+
- pydub
- ffmpeg (must be installed and accessible in your PATH)

## Usage

```python
import iitjp

# Basic usage with audio
from iitjp import mam

# Greet the user
mam.greetings()

# Start a quiz
mam.quiz()

# End the quiz with a farewell
mam.thanks()
```

### Silent Mode

If you experience audio playback issues, you can enable silent mode:

```python
import iitjp

# Enable silent mode to avoid audio playback
iitjp.enable_silent_mode(True)

# Now use the library as normal
iitjp.mam.greetings()  # This will not play audio
```

## Troubleshooting

If you encounter issues with audio playback, it could be due to:

1. Missing ffmpeg - Make sure ffmpeg is installed and in your PATH
2. Permission issues - The library now uses multiple fallback methods to play audio
3. Audio device problems - You can manually enable silent mode to avoid audio playback issues

### Audio Playback Solutions

The library now includes several fallback methods to handle audio playback:

1. **Custom temp directory method**: Creates WAV files in a project-local temp directory
2. **Winsound method** (Windows only): Uses the built-in winsound module which doesn't require temp files
3. **System player method**: Opens the audio file with your system's default media player

To run a comprehensive audio troubleshooter:
```bash
python multi_method_audio_test.py
```

### If You're Still Having Issues

- Run your script or the troubleshooter with administrator privileges
- Make sure your Windows user account has sufficient permissions
- Check that your audio device is properly configured and not muted
- Use silent mode as a last resort if audio playback doesn't work

## Project Structure

- `iitjp/`: Main package directory
  - `__init__.py`: Package initialization with exposed functions
  - `rajlaxmi.py`: Core functionality for the virtual teacher
- `data/`: Contains audio files and quiz questions
  - `greeting.mp3`: Welcome message
  - `start_quiz.mp3`: Quiz introduction
  - `end_quiz.mp3`: Quiz conclusion
  - `farewell.mp3`: Goodbye message
  - `questions.json`: Quiz questions and answers
- `temp/`: Temporary directory for audio processing

## Development

```bash
# Clone the repository
git clone https://your-repo-url.git
cd iitjp

# Create temp directory if it doesn't exist
mkdir -p temp

# Install in development mode
pip install -e .

# Run the audio troubleshooter
python multi_method_audio_test.py

# Run the demo
python audio_demo.py
```
