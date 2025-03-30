"""
IITJP - Interactive Teacher Module

This module provides an interactive teacher named RajLaxmi 
with audio-visual interaction capabilities.
"""

import sys
import platform
import subprocess
import warnings
import os

from .rajlaxmi import greetings, quiz, quitquiz, thanks, set_silent_mode, set_typing_effect
from .rajlaxmi import load_platform_modules

# Version information
__version__ = "0.2.2"

# Platform detection
PLATFORM = platform.system().lower()

# Install platform-specific dependencies if needed
def ensure_platform_dependencies():
    """Install platform-specific dependencies if needed."""
    if PLATFORM == 'windows' or sys.platform == 'win32':
        try:
            # pywin32 is not directly importable - check for win32api instead
            import win32api
        except ImportError:
            try:
                print("[ℹ️ Installing Windows-specific dependencies...]")
                subprocess.run([sys.executable, "-m", "pip", "install", "pywin32"],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                # Try to import again after installation
                try:
                    import win32api
                except ImportError:
                    warnings.warn("pywin32 installed but win32api module not found. Some features may not work properly.")
            except Exception as e:
                warnings.warn(f"Could not install pywin32: {e}. Some features may not work properly.")
    
    elif PLATFORM == 'darwin':  # macOS
        try:
            from AppKit import NSSound
        except ImportError:
            try:
                print("[ℹ️ Installing macOS-specific dependencies...]")
                subprocess.run([sys.executable, "-m", "pip", "install", "pyobjc-framework-Cocoa"],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                # Try to import again after installation
                try:
                    from AppKit import NSSound
                except ImportError:
                    warnings.warn("pyobjc-framework-Cocoa installed but AppKit.NSSound not found. Some features may not work properly.")
            except Exception as e:
                warnings.warn(f"Could not install pyobjc-framework-Cocoa: {e}. Some features may not work properly.")
    
    elif PLATFORM == 'linux':  # Linux
        try:
            # Check for dbus by trying to import it
            import dbus
        except ImportError:
            try:
                print("[ℹ️ Installing Linux-specific dependencies...]")
                subprocess.run([sys.executable, "-m", "pip", "install", "python-dbus"],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                # Try to import again after installation
                try:
                    import dbus
                except ImportError:
                    warnings.warn("python-dbus installed but dbus module not found. Some features may not work properly.")
            except Exception as e:
                warnings.warn(f"Could not install python-dbus: {e}. Some features may not work properly.")

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

# Export enable_typing_effect for convenience
def enable_typing_effect(enabled=True):
    set_typing_effect(enabled)

# Try to install platform-specific dependencies silently on import
try:
    ensure_platform_dependencies()
    # We don't need to check for ffmpeg anymore
    # check_ffmpeg()
except Exception:
    # Don't fail on import if dependencies can't be installed
    pass
