"""
IITJP - Interactive Teacher Module

This module provides an interactive teacher named RajLaxmi 
with audio-visual interaction capabilities.
"""

import sys
import platform
import os

# Version information
__version__ = "0.2.8"

# Import main components
from .rajlaxmi import greetings, quiz, quitquiz, thanks, set_silent_mode, set_typing_effect
from .rajlaxmi import get_audio_path

# Create a namespace for the main interface
class Mam:
    def __init__(self):
        self.greetings = greetings
        self.quiz = quiz
        self.thanks = thanks
        self.quitquiz = quitquiz

mam = Mam()

# Expose main functions
__all__ = ['mam', 'greetings', 'quiz', 'thanks', 'quitquiz', 'set_silent_mode', 'set_typing_effect']

# Export enable_silent_mode for convenience
def enable_silent_mode(silent=True):
    set_silent_mode(silent)

# Export enable_typing_effect for convenience
def enable_typing_effect(enabled=True):
    set_typing_effect(enabled)
