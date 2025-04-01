# IITJP

A Python package for virtual teaching assistant with voice capabilities.

## Features

- Virtual teacher RajLaxmi who can speak to students
- Interactive statistics quiz
- Voice greetings and feedback

## Installation

```bash
pip install iitjp
```

## Usage

```python
import iitjp

# Get a greeting from your virtual teacher
iitjp.mam.greetings()

# Start an interactive quiz
iitjp.mam.quiz()

# Exit from a quiz
iitjp.mam.quitquiz()

# Say goodbye to your teacher
iitjp.mam.thanks()

# Enable or disable silent mode (no audio)
iitjp.enable_silent_mode(True)  # Enable silent mode
iitjp.enable_silent_mode(False)  # Disable silent mode (default)
```

## Requirements

- Python 3.6+
- NumPy
- SciPy
- PyAudio

## License

MIT
