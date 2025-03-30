# IITJP Python Library

A Python library for an interactive quiz assistant named RajLaxmi, featuring audio-visual interactions for learning Statistics.

## Getting Started

### Installation

The IITJP library can be installed directly from PyPI:

```bash
pip install iitjp
```

This will automatically install the base library and all platform-specific dependencies required for your operating system.

### External Dependencies

> **Note**: Version 0.2.2 and newer no longer require ffmpeg!

The library now uses native audio playback methods for each platform, which means:

- No need to install ffmpeg
- No dependency on pydub
- Better cross-platform compatibility
- Fewer installation issues

### Basic Usage

```python
import iitjp

# Start with a greeting
iitjp.mam.greetings()

# Start a quiz
iitjp.mam.quiz()

# Exit with a thank you message
iitjp.mam.thanks()
```

### Silent Mode

If you want to disable audio playback:

```python
import iitjp

# Enable silent mode
iitjp.enable_silent_mode(True)

# Now commands will run without audio
iitjp.mam.greetings()
```

### Text Synchronization Options

If you experience delays between voiceover and text printing, you have two options:

1. **Disable typing effect** - Shows all text instantly without the typing animation:

```python
import iitjp

# Disable typing effect for instant text display
iitjp.enable_typing_effect(False)

# Text will appear instantly while audio plays
iitjp.mam.greetings()
```

2. **Use built-in synchronization** - The library automatically adjusts typing speed to match audio duration (default behavior).

### Command Line Interface

IITJP also provides a command-line interface:

```bash
# Show welcome message
iitjp greetings

# Start a quiz
iitjp quiz

# Show thank you message
iitjp thanks

# Run in silent mode (no audio)
iitjp --silent greetings
```

## Installation

### Quick Install from PyPI

```bash
# Install from PyPI (when available)
pip install iitjp

# Or install directly from GitHub
pip install git+https://github.com/yutkarsh.brainstorm/ourusername/IITJP.git
```

### Install from Source

```bash
# Clone the repository
git clone https://github.com/yutkarsh.brainstorm/ourusername/IITJP.git
cd IITJP

# Install in development mode
pip install -e .
```

## Requirements

- Python 3.7+
- pydub (automatically installed)
- Platform-specific dependencies (automatically installed):
  - **Windows**: pywin32
  - **macOS**: pyobjc-framework-Cocoa
  - **Linux**: python-dbus

## Usage

### Python API

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

### Command Line Interface

The library also provides a command-line interface:

```bash
# Show welcome message
iitjp greetings

# Start an interactive quiz
iitjp quiz

# Display thank you message
iitjp thanks

# Show version information
iitjp version

# Enable silent mode (no audio)
iitjp --silent quiz
```

### Silent Mode

If you experience audio playback issues, you can enable silent mode:

```python
import iitjp
iitjp.enable_silent_mode(True)
```

## Cross-Platform Support

The library is designed to work across Windows, macOS, and Linux with appropriate audio playback methods for each platform:

- **Windows**: Uses PowerShell and winsound for audio playback
- **macOS**: Uses afplay and native macOS audio capabilities 
- **Linux**: Tries multiple common audio players (aplay, paplay, ffplay)

## Troubleshooting

### Audio Issues

If you're experiencing audio playback issues, there are several solutions:

#### Instant Fix (Recommended)

The package includes a simple fix script. Just add this one line at the top of your program:

```python
import iitjp.fix_iitjp  # This will automatically fix audio paths
import iitjp
```

This will automatically locate and fix all audio file paths.

#### Automatic Repair

You can also run the included repair utility:

```bash
# Download and run the repair script
python -c "import iitjp.iitjp_repair as fix; fix.manual_repair()"
```

#### Silent Mode

If you prefer to use the package without audio:

```python
import iitjp
iitjp.enable_silent_mode(True)  # Turn off all audio
```

### Audio File Not Found Errors

If you see errors like `[⚠️ Audio file not found: greeting.mp3]`, it means the package can't locate the audio files. Use one of the above solutions to fix this.

### Missing Audio Files

If you see errors like `[⚠️ Audio file not found: greeting.mp3]`, use the repair command to fix the issue:

```bash
# From the command line
iitjp repair
```

Or in Python:

```python
import iitjp
from iitjp.__main__ import repair_command

# Run the repair function
repair_command()
```

### Fast Text Display

For instant text display without typing effect:

```python
# Disable the typing effect for instant text display
import iitjp
iitjp.enable_typing_effect(False)
```

Or from the command line:

```bash
# Use --fast-text flag with any command
iitjp --fast-text greetings
```

### pywin32 Warning on Windows

If you see warnings about pywin32 not being installed:

```
[⚠️ Warning: pywin32 installed but win32api module not found. Some features may not work properly.]
```

Try manually installing pywin32 with the following commands:

```bash
# First install the package
pip install pywin32

# For Python 3.7+ you might need to run the post-install script
python -m pip install --upgrade pywin32
python -c "import win32com.client"
```

### Audio Synchronization Issues

If there's a delay between the voiceover and text display:

```python
# Disable the typing effect for instant text display
import iitjp
iitjp.enable_typing_effect(False)
```

### Update to Latest Version

For the best experience, make sure you're using the latest version, which has removed dependencies on pydub and ffmpeg:

```bash
pip install --upgrade iitjp
```

This update significantly improves cross-platform compatibility and reduces installation issues.

## Project Structure

- `iitjp/`: Main package directory
  - `__init__.py`: Package initialization with exposed functions
  - `rajlaxmi.py`: Core functionality for the virtual teacher
  - `__main__.py`: Command-line interface
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

## Changelog

### Version 0.2.6
- Added bulletproof audio file handling that works in any environment
- Included automatic fix scripts (fix_iitjp.py and iitjp_repair.py) to resolve path issues
- Improved audio path resolution across all platforms and installation methods
- Enhanced package with self-healing capabilities
- Fixed package structure to ensure all required files are included

### Version 0.2.5
- Embedded audio files directly in the package for guaranteed availability
- Added robust resource manager for fail-proof audio playback
- Improved path detection system to find resources in any installation method
- Enhanced audio file availability across all platforms and installation methods

### Version 0.2.4
- Fixed audio file path resolution for different installation environments
- Added standalone fix_audio_paths.py utility for resolving audio path issues
- Improved multi-platform compatibility with better path detection
- Enhanced recognition of audio files in site-packages locations

### Version 0.2.3
- Fixed audio file path resolution issues
- Added automatic audio file repair functionality
- Added `repair` command to fix missing audio files
- Added `--fast-text` flag for instant text display
- Improved package data file handling

### Version 0.2.2
- Completely removed dependency on pydub and ffmpeg for better compatibility
- Added native audio playback that works across all platforms without external dependencies
- Fixed synchronization between text display and audio playback
- Added option to disable typing effect for instant text display

### Version 0.2.1
- Improved cross-platform compatibility
- Added automatic installation of platform-specific dependencies
- Fixed timing issues between voiceover and text display

### Version 0.2.0
- Initial public release
