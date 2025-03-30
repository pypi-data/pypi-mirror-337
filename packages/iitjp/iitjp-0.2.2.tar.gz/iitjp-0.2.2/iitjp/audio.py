"""
Cross-platform audio playback module for IITJP

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
import warnings
from pathlib import Path

# Platform detection
PLATFORM = platform.system().lower()  # 'windows', 'darwin', or 'linux'

class AudioPlayer:
    """Simple cross-platform audio player that works without complex dependencies"""
    
    @staticmethod
    def play(file_path, block=False):
        """
        Play an audio file using the appropriate method for the current platform
        
        Args:
            file_path: Path to the audio file
            block: Whether to block until playback completes
        
        Returns:
            bool: True if playback started successfully, False otherwise
        """
        if not os.path.exists(file_path):
            print(f"[⚠️ Audio file not found: {file_path}]")
            return False
            
        # Platform-specific playback
        if PLATFORM == 'windows' or sys.platform == 'win32':
            return AudioPlayer._play_windows(file_path, block)
        elif PLATFORM == 'darwin':  # macOS
            return AudioPlayer._play_macos(file_path, block)
        else:  # Linux and other platforms
            return AudioPlayer._play_linux(file_path, block)
    
    @staticmethod
    def _play_windows(file_path, block=False):
        """Play audio on Windows using built-in methods"""
        try:
            # Try winsound first (built into Python standard library)
            import winsound
            if block:
                winsound.PlaySound(str(file_path), winsound.SND_FILENAME)
            else:
                # Start in a thread for non-blocking
                threading.Thread(
                    target=winsound.PlaySound,
                    args=(str(file_path), winsound.SND_FILENAME),
                    daemon=True
                ).start()
            return True
        except Exception as e:
            print(f"[⚠️ winsound playback failed: {e}]")
            
            # Try PowerShell as backup
            try:
                ps_cmd = f"(New-Object Media.SoundPlayer '{file_path}').{'PlaySync' if block else 'Play'}()"
                if block:
                    subprocess.run(["powershell", "-c", ps_cmd], 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE)
                else:
                    # Start in a thread for non-blocking
                    threading.Thread(
                        target=subprocess.run,
                        args=(["powershell", "-c", ps_cmd],),
                        kwargs={'stdout': subprocess.PIPE, 'stderr': subprocess.PIPE},
                        daemon=True
                    ).start()
                return True
            except Exception as e:
                print(f"[⚠️ PowerShell playback failed: {e}]")
                
            # Last resort: try with Windows Media Player
            try:
                cmd = f'(new-object -com wmplayer.ocx).cdromcollection.item(0).playitem(0)'
                subprocess.run(["cmd", "/c", f'start wmplayer "{file_path}"'], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE)
                return True
            except Exception as e:
                print(f"[⚠️ Windows Media Player failed: {e}]")
                
            return False
                
    @staticmethod
    def _play_macos(file_path, block=False):
        """Play audio on macOS"""
        try:
            # Try afplay (built into macOS)
            cmd = ["afplay", str(file_path)]
            if block:
                subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                # Start in a thread for non-blocking
                threading.Thread(
                    target=subprocess.run,
                    args=(cmd,),
                    kwargs={'stdout': subprocess.PIPE, 'stderr': subprocess.PIPE},
                    daemon=True
                ).start()
            return True
        except Exception as e:
            print(f"[⚠️ afplay failed: {e}]")
            
            # Try system open as backup
            try:
                cmd = ["open", str(file_path)]
                subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                return True
            except Exception as e:
                print(f"[⚠️ open command failed: {e}]")
                
            return False
    
    @staticmethod
    def _play_linux(file_path, block=False):
        """Play audio on Linux"""
        # Try various Linux audio players
        players = [
            ["aplay", str(file_path)],
            ["paplay", str(file_path)],
            ["mpg123", str(file_path)],
            ["mpg321", str(file_path)],
            ["mplayer", str(file_path)],
            ["cvlc", "--play-and-exit", str(file_path)],  # VLC command line
        ]
        
        for cmd in players:
            try:
                # Check if player exists
                player_name = cmd[0]
                which_cmd = "where" if PLATFORM == "windows" else "which"
                which_result = subprocess.run(
                    [which_cmd, player_name], 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE
                )
                
                if which_result.returncode == 0:
                    if block:
                        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    else:
                        # Start in a thread for non-blocking
                        threading.Thread(
                            target=subprocess.run,
                            args=(cmd,),
                            kwargs={'stdout': subprocess.PIPE, 'stderr': subprocess.PIPE},
                            daemon=True
                        ).start()
                    return True
            except Exception:
                continue
                
        print(f"[⚠️ No suitable audio player found on Linux]")
        return False

# Play audio in a background thread
def play_audio_threaded(file_path):
    """Play audio in a background thread"""
    thread = threading.Thread(
        target=AudioPlayer.play,
        args=(file_path, True),  # Use blocking mode in the thread
        daemon=True
    )
    thread.start()
    return thread 