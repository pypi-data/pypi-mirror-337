"""
IITJP - Interactive Teacher Module

This module provides an interactive teacher named RajLaxmi 
with audio-visual interaction capabilities.
"""

__version__ = "0.2.13"

from .rajlaxmi import greetings, quiz, quitquiz, thanks, set_silent_mode

# Create mam namespace for user-friendly access
class Teacher:
    def __init__(self):
        self.greetings = greetings
        self.quiz = quiz
        self.quitquiz = quitquiz
        self.thanks = thanks

# Create instance
mam = Teacher()

# Export enable_silent_mode for convenience
def enable_silent_mode(silent=True):
    set_silent_mode(silent)
