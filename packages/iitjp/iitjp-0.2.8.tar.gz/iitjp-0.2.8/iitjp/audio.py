"""
Optimized audio playback module for IITJP version 0.2.8

This module provides robust audio playback functionality
that works reliably across Windows, macOS, and Linux.
"""

import os
import sys
import platform
import subprocess
import threading
import tempfile
import base64
from pathlib import Path

# Silent flag - always set to True to disable all output
SILENT = True

# Platform detection
WINDOWS = platform.system().lower() == 'windows' or sys.platform == 'win32'
MACOS = platform.system().lower() == 'darwin'
LINUX = platform.system().lower() == 'linux'

# Audio resource cache
_audio_path_cache = {}

def find_audio_file(filename):
    """Find an audio file in various possible locations"""
    # Return from cache if available
    if filename in _audio_path_cache and os.path.exists(_audio_path_cache[filename]):
        return _audio_path_cache[filename]
    
    # Ensure the filename has the .mp3 extension
    if not filename.endswith('.mp3'):
        filename = f"{filename}.mp3"
    
    # Get package directory
    pkg_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define possible locations for the audio file in order of preference
    search_paths = []
    
    # First check locations most likely to exist
    
    # 1. Direct path if already absolute
    if os.path.isabs(filename):
        search_paths.append(filename)
    
    # 2. User's persistent cache directory (most reliable after first run)
    cache_dir = os.path.join(os.path.expanduser("~"), ".iitjp_audio")
    search_paths.append(os.path.join(cache_dir, os.path.basename(filename)))
    
    # 3. Package directory paths
    search_paths.extend([
        os.path.join(pkg_dir, filename),
        os.path.join(pkg_dir, "data", filename),
        os.path.join(os.path.dirname(pkg_dir), "data", filename),
    ])
    
    # 4. Current working directory paths
    search_paths.extend([
        os.path.join(os.getcwd(), filename),
        os.path.join(os.getcwd(), "data", filename),
    ])
    
    # 5. Site-packages paths
    site_pkg_paths = [
        os.path.join(sys.prefix, "Lib", "site-packages", "iitjp", "data", filename),
        os.path.join(sys.prefix, "Lib", "site-packages", "data", filename),
        os.path.join(sys.prefix, "lib", "python*", "site-packages", "iitjp", "data", filename),
    ]
    
    # Expand any glob patterns in site_pkg_paths
    for pattern in site_pkg_paths:
        if '*' in pattern:
            import glob
            for match in glob.glob(pattern):
                search_paths.append(match)
        else:
            search_paths.append(pattern)
    
    # Check each path
    for path in [p for p in search_paths if p]:
        if os.path.exists(path):
            _audio_path_cache[filename] = path
            return path
    
    # Try embedded resources if file not found in filesystem
    try:
        from . import embedded_audio
        # Check if the file exists as an embedded resource
        base_filename = os.path.basename(filename)
        var_name = base_filename.replace('.', '_')
        if hasattr(embedded_audio, var_name):
            # Get the embedded audio data
            audio_data = getattr(embedded_audio, var_name)
            
            # Create user cache directory for persistent storage
            cache_dir = os.path.join(os.path.expanduser("~"), ".iitjp_audio")
            os.makedirs(cache_dir, exist_ok=True)
            cache_file = os.path.join(cache_dir, base_filename)
            
            # Write the audio data to the cache file if it doesn't exist
            if not os.path.exists(cache_file):
                with open(cache_file, "wb") as f:
                    f.write(base64.b64decode(audio_data))
            
            # Cache and return the path
            _audio_path_cache[filename] = cache_file
            return cache_file
    except Exception:
        pass
    
    # No file found, return None
    return None

class AudioPlayer:
    """Optimized audio playback class for all platforms"""
    
    @classmethod
    def play(cls, filename, block=True):
        """Play an audio file with platform-specific optimizations"""
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
        """Play audio with multiple fallbacks for maximum reliability"""
        # Windows-specific methods (most reliable on Windows)
        if WINDOWS:
            # Try winsound first - most compatible on all Windows versions
            try:
                import winsound
                winsound.PlaySound(file_path, winsound.SND_FILENAME)
                return True
            except Exception:
                pass
            
            # Try PowerShell method for newer Windows
            try:
                ps_command = f'(New-Object Media.SoundPlayer "{file_path}").PlaySync();'
                subprocess.run(
                    ["powershell", "-Command", ps_command],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                return True
            except Exception:
                pass
            
            # Try Windows Media Player command-line
            try:
                subprocess.run(
                    ["cmd", "/c", "start", "/min", file_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                return True
            except Exception:
                pass
                
        # macOS optimized playback
        elif MACOS:
            try:
                subprocess.run(
                    ["afplay", file_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                return True
            except Exception:
                pass
                
        # Linux optimized playback - try common players
        elif LINUX:
            for player in ["aplay", "paplay", "ffplay", "mplayer", "mpg123", "mpg321"]:
                try:
                    subprocess.run(
                        [player, file_path],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    return True
                except Exception:
                    continue
                    
        # Final fallback - should work on most systems as a last resort
        try:
            # Use Python's built-in module capabilities if available
            if WINDOWS:
                os.startfile(file_path)
            else:
                # Generic "open" commands as last resort
                if MACOS:
                    subprocess.run(["open", file_path], 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE)
                else:
                    subprocess.run(["xdg-open", file_path], 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE)
            return True
        except Exception:
            # Return failure if nothing worked
            return False

# Play audio in a background thread
def play_audio_threaded(filename):
    """Play audio in a background thread"""
    thread = threading.Thread(target=AudioPlayer.play, args=(filename,))
    thread.daemon = True
    thread.start()
    return thread 