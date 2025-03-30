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
import importlib.resources
import shutil

# Import the resource manager first to ensure it's initialized
from .resource_manager import preload_resources

from .rajlaxmi import greetings, quiz, quitquiz, thanks, set_silent_mode, set_typing_effect
from .rajlaxmi import load_platform_modules, get_audio_path

# Version information
__version__ = "0.2.5"

# Platform detection
PLATFORM = platform.system().lower()

# Verify data files during import
def verify_audio_files():
    """Verify audio files exist and are accessible"""
    audio_files = ["greeting.mp3", "start_quiz.mp3", "end_quiz.mp3", "farewell.mp3"]
    found_files = []
    missing_files = []
    
    for audio_file in audio_files:
        file_path = get_audio_path(audio_file)
        if file_path:
            found_files.append(audio_file)
        else:
            missing_files.append(audio_file)
    
    if missing_files:
        warnings.warn(f"Some audio files could not be found: {', '.join(missing_files)}")
        
        # Try to copy audio files from package data to the right location
        try:
            # Get the package directory
            package_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Get the correct data directory
            data_dir = os.path.join(package_dir, "data")
            if not os.path.exists(data_dir):
                os.makedirs(data_dir, exist_ok=True)
                
            # Try to find audio files in common locations
            for file in missing_files:
                for search_dir in [
                    os.path.join(os.path.dirname(package_dir), "data"),
                    os.path.join(os.getcwd(), "data")
                ]:
                    src = os.path.join(search_dir, file)
                    if os.path.exists(src):
                        dst = os.path.join(data_dir, file)
                        shutil.copy2(src, dst)
                        print(f"Copied audio file from {src} to {dst}")
                        break
        except Exception as e:
            warnings.warn(f"Could not copy audio files: {e}")
    
    return (found_files, missing_files)

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
    # Preload all resources to ensure they're available
    preload_resources()
    
    ensure_platform_dependencies()
    # Verify audio files are accessible
    verify_audio_files()
except Exception as e:
    # Don't fail on import if dependencies can't be installed
    warnings.warn(f"Error during initialization: {e}")
    pass
