"""
Windows-optimized audio playback module for IITJP

This module provides simplified audio playback functionality
that works reliably across Windows, macOS, and Linux without
complex dependencies like ffmpeg.
"""

import os
import sys
import platform
import subprocess
import threading
import time
import tempfile
import importlib.util
import base64
from pathlib import Path

# Silent flag - set to True to disable all output
SILENT = False

# Platform detection
WINDOWS = platform.system().lower() == 'windows' or sys.platform == 'win32'

# Internal resource cache
_RESOURCE_CACHE = {}

# Audio resource cache to avoid repeated lookups
_audio_path_cache = {}

def silent_print(*args, **kwargs):
    """Print only if not in silent mode"""
    if not SILENT:
        print(*args, **kwargs)

def get_package_dir():
    """Get the package directory without any debug output"""
    return os.path.dirname(os.path.abspath(__file__))

def find_audio_file(filename):
    """Find an audio file in various possible locations"""
    # Return from cache if available
    if filename in _audio_path_cache and os.path.exists(_audio_path_cache[filename]):
        return _audio_path_cache[filename]
    
    # Ensure the filename has the .mp3 extension
    if not filename.endswith('.mp3'):
        filename = f"{filename}.mp3"
    
    # First try embedded resources from the embedded_audio module
    try:
        from . import embedded_audio
        # Check if the file exists as an embedded resource
        base_filename = os.path.basename(filename)
        if hasattr(embedded_audio, base_filename.replace('.', '_')):
            # Get the embedded audio data
            audio_data = getattr(embedded_audio, base_filename.replace('.', '_'))
            # Create a temporary file
            temp_dir = os.path.join(tempfile.gettempdir(), "iitjp_audio")
            os.makedirs(temp_dir, exist_ok=True)
            temp_file = os.path.join(temp_dir, base_filename)
            
            # Write the audio data to the temporary file
            with open(temp_file, "wb") as f:
                f.write(base64.b64decode(audio_data))
            
            # Cache and return the path
            _audio_path_cache[filename] = temp_file
            return temp_file
    except Exception:
        pass
    
    # Define possible locations for the audio file
    pkg_dir = get_package_dir()
    search_paths = [
        # Direct path if already absolute
        filename if os.path.isabs(filename) else None,
        
        # Package directory paths
        os.path.join(pkg_dir, filename),
        os.path.join(pkg_dir, "data", filename),
        os.path.join(pkg_dir, "..", "data", filename),
        
        # User directory paths
        os.path.join(os.getcwd(), filename),
        os.path.join(os.getcwd(), "data", filename),
        
        # Site-packages paths
        os.path.join(sys.prefix, "Lib", "site-packages", "iitjp", "data", filename),
        os.path.join(sys.prefix, "Lib", "site-packages", "data", filename),
        
        # Home directory persistent cache
        os.path.join(os.path.expanduser("~"), ".iitjp", "audio", filename)
    ]
    
    # Check each path
    for path in [p for p in search_paths if p]:
        if os.path.exists(path):
            _audio_path_cache[filename] = path
            return path
    
    # No file found, return None
    return None

class AudioPlayer:
    """Audio playback class optimized for Windows"""
    
    @classmethod
    def play(cls, filename, block=True):
        """Play an audio file with fallbacks for different platforms"""
        # Find the audio file
        file_path = find_audio_file(filename)
        if not file_path:
            return False
        
        if block:
            # Blocking playback
            return cls._play_audio(file_path)
        else:
            # Non-blocking playback
            return cls._play_threaded(file_path)
    
    @classmethod
    def _play_threaded(cls, file_path):
        """Play audio in a separate thread"""
        thread = threading.Thread(target=cls._play_audio, args=(file_path,))
        thread.daemon = True
        thread.start()
        return thread
    
    @classmethod
    def _play_audio(cls, file_path):
        """Play audio with multiple fallbacks"""
        if WINDOWS:
            # Try winsound first (most reliable on Windows)
            success = cls._play_with_winsound(file_path)
            if success:
                return True
            
            # Try PowerShell next
            success = cls._play_with_powershell(file_path)
            if success:
                return True
        
        # Final fallback for all platforms
        return cls._play_with_subprocess(file_path)
    
    @classmethod
    def _play_with_winsound(cls, file_path):
        """Play using winsound (Windows only)"""
        if not WINDOWS:
            return False
        
        try:
            import winsound
            winsound.PlaySound(file_path, winsound.SND_FILENAME)
            return True
        except Exception:
            return False
    
    @classmethod
    def _play_with_powershell(cls, file_path):
        """Play using PowerShell (Windows only)"""
        if not WINDOWS:
            return False
        
        try:
            # PowerShell command to play audio
            ps_command = f'(New-Object Media.SoundPlayer "{file_path}").PlaySync();'
            
            # Run PowerShell with the command
            subprocess.run(
                ["powershell", "-Command", ps_command],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            return True
        except Exception:
            return False
    
    @classmethod
    def _play_with_subprocess(cls, file_path):
        """Cross-platform fallback using appropriate media player"""
        try:
            if WINDOWS:
                # Windows - use built-in media player
                subprocess.run(
                    ["cmd", "/c", "start", "/min", file_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
            else:
                # Linux/Mac fallback (nohup to run in background)
                try:
                    subprocess.run(
                        ["nohup", "play", file_path],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                except Exception:
                    pass
            return True
        except Exception:
            return False

# Play audio in a background thread
def play_audio_threaded(filename):
    """Play audio in a background thread"""
    thread = threading.Thread(target=AudioPlayer.play, args=(filename,))
    thread.daemon = True
    thread.start()
    return thread 