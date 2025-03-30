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
import importlib.util

# Disable warnings during import
import warnings
warnings.filterwarnings("ignore")

# Redirect stdout/stderr during import
import io
original_stdout = sys.stdout
original_stderr = sys.stderr
sys.stdout = io.StringIO()
sys.stderr = io.StringIO()

try:
    # Import the resource manager first to ensure it's initialized
    from .resource_manager import preload_resources

    # Import main components
    from .rajlaxmi import greetings, quiz, quitquiz, thanks, set_silent_mode, set_typing_effect
    from .rajlaxmi import load_platform_modules, get_audio_path

    # Version information
    __version__ = "0.2.7"

    # Platform detection
    PLATFORM = platform.system().lower()

    # First try to find and import the fix module
    try:
        # Check if fix_iitjp.py exists in the package directory
        from . import fix_iitjp
    except ImportError:
        # If not found, check for standalone fix script
        try:
            spec = importlib.util.find_spec("iitjp.fix_iitjp")
            if spec is None:
                # If not found as a module, try to find the script file
                pkg_dir = os.path.dirname(os.path.abspath(__file__))
                fix_script = os.path.join(pkg_dir, "fix_iitjp.py")
                if os.path.exists(fix_script):
                    # Load the script dynamically
                    spec = importlib.util.spec_from_file_location("iitjp.fix_iitjp", fix_script)
                    fix_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(fix_module)
        except Exception:
            pass

    # Verify data files during import (silently)
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
                            break
            except Exception:
                pass
        
        return (found_files, missing_files)

    # Install platform-specific dependencies if needed (silently)
    def ensure_platform_dependencies():
        """Install platform-specific dependencies if needed."""
        try:
            if PLATFORM == 'windows' or sys.platform == 'win32':
                try:
                    # pywin32 is not directly importable - check for win32api instead
                    import win32api
                except ImportError:
                    try:
                        subprocess.run([sys.executable, "-m", "pip", "install", "pywin32"],
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        try:
                            import win32api
                        except ImportError:
                            pass
                    except Exception:
                        pass
            
            elif PLATFORM == 'darwin':  # macOS
                try:
                    from AppKit import NSSound
                except ImportError:
                    try:
                        subprocess.run([sys.executable, "-m", "pip", "install", "pyobjc-framework-Cocoa"],
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        try:
                            from AppKit import NSSound
                        except ImportError:
                            pass
                    except Exception:
                        pass
            
            elif PLATFORM == 'linux':  # Linux
                try:
                    # Check for dbus by trying to import it
                    import dbus
                except ImportError:
                    try:
                        subprocess.run([sys.executable, "-m", "pip", "install", "python-dbus"],
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        try:
                            import dbus
                        except ImportError:
                            pass
                    except Exception:
                        pass
        except Exception:
            pass

    # Create a namespace for the main interface
    from .rajlaxmi import (
        greetings, 
        quiz, 
        thanks, 
        quitquiz, 
        set_silent_mode,
        set_typing_effect,
    )

    # Create 'mam' namespace like in version 0.2.1
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

    # Try to install platform-specific dependencies silently on import
    try:
        # Preload all resources to ensure they're available
        preload_resources()
        
        ensure_platform_dependencies()
        # Verify audio files are accessible
        verify_audio_files()
    except Exception:
        pass

finally:
    # Restore stdout/stderr
    sys.stdout = original_stdout
    sys.stderr = original_stderr
    # Re-enable warnings after import
    warnings.resetwarnings()
