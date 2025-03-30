#!/usr/bin/env python
"""
IITJP Simple Audio Fix

Just drop this file in your project and import it to fix audio issues in iitjp:

import fix_iitjp

That's it!
"""

import os
import sys
import importlib.util
import shutil
import tempfile
import site

print("🔧 Applying IITJP audio fix...")

# Define audio files
AUDIO_FILES = [
    "greeting.mp3",
    "start_quiz.mp3", 
    "end_quiz.mp3",
    "farewell.mp3"
]

# Create user cache directory
USER_HOME = os.path.expanduser("~")
USER_CACHE = os.path.join(USER_HOME, ".iitjp_audio")
TEMP_DIR = os.path.join(tempfile.gettempdir(), "iitjp_audio")

# Create directories
try:
    os.makedirs(USER_CACHE, exist_ok=True)
    os.makedirs(TEMP_DIR, exist_ok=True)
except Exception:
    pass

# Find all possible audio file locations
def find_audio_files():
    """Find all audio files in the system"""
    files_found = {}
    
    # Build list of possible directories
    search_dirs = [
        # User and temp directories
        USER_CACHE,
        TEMP_DIR,
        
        # Current directory
        os.getcwd(),
        os.path.join(os.getcwd(), "data"),
        
        # Site-packages
        *[os.path.join(path, "data") for path in site.getsitepackages()],
        *[os.path.join(path, "iitjp", "data") for path in site.getsitepackages()],
        
        # Virtual env
        os.path.join(sys.prefix, "Lib", "site-packages", "data"),
        os.path.join(sys.prefix, "Lib", "site-packages", "iitjp", "data"),
    ]
    
    # Try to find the package directory
    try:
        spec = importlib.util.find_spec("iitjp")
        if spec and spec.origin:
            package_dir = os.path.dirname(os.path.abspath(spec.origin))
            search_dirs.extend([
                package_dir,
                os.path.join(package_dir, "data"),
                os.path.join(os.path.dirname(package_dir), "data"),
            ])
    except Exception:
        pass
    
    # Search for each audio file
    for audio_file in AUDIO_FILES:
        found = False
        for directory in search_dirs:
            try:
                if os.path.exists(directory):
                    path = os.path.join(directory, audio_file)
                    if os.path.exists(path):
                        if audio_file not in files_found:
                            files_found[audio_file] = []
                        files_found[audio_file].append(path)
                        found = True
            except Exception:
                continue
                
        if not found:
            print(f"⚠️ Could not find audio file: {audio_file}")
        
    return files_found

# Copy files to user cache
def copy_to_cache(files_found):
    """Copy found audio files to user cache for reliable access"""
    for audio_file, paths in files_found.items():
        if not paths:
            continue
            
        # Source is first found file
        source = paths[0]
        
        # Copy to user cache
        try:
            dest = os.path.join(USER_CACHE, audio_file)
            shutil.copy2(source, dest)
            print(f"✅ Cached {audio_file} to {USER_CACHE}")
        except Exception:
            pass
            
        # Also copy to temp directory
        try:
            dest = os.path.join(TEMP_DIR, audio_file)
            shutil.copy2(source, dest)
        except Exception:
            pass

# Apply monkey patch to make audio work
def apply_patch():
    """Monkey patch iitjp.audio to always find audio files"""
    try:
        import iitjp.audio
        
        # Store the original play method
        original_play = iitjp.audio.AudioPlayer.play
        
        # Create file path cache
        cache = {}
        for audio_file in AUDIO_FILES:
            # Check in user cache first
            path = os.path.join(USER_CACHE, audio_file)
            if os.path.exists(path):
                cache[audio_file] = path
                continue
                
            # Check in temp dir
            path = os.path.join(TEMP_DIR, audio_file)
            if os.path.exists(path):
                cache[audio_file] = path
        
        # Create patched method
        def patched_play(file_path, block=False):
            """Patched version of AudioPlayer.play that always finds audio files"""
            # If file exists directly, use it
            if os.path.exists(file_path):
                return original_play(file_path, block)
                
            # Try to resolve by filename
            basename = os.path.basename(file_path)
            if basename in cache:
                return original_play(cache[basename], block)
                
            # Fallback to original behavior
            return original_play(file_path, block)
        
        # Apply the patch
        iitjp.audio.AudioPlayer.play = patched_play
        print("✅ Applied audio path fix")
        return True
    except ImportError:
        print("❌ Could not find iitjp module. Is it installed?")
        return False
    except Exception as e:
        print(f"❌ Error applying patch: {e}")
        return False

# Main fix procedure
def main():
    # Find audio files
    files = find_audio_files()
    
    # Copy to cache
    copy_to_cache(files)
    
    # Apply patch
    apply_patch()

# Apply the fix when imported
main()

# User-friendly functions for recovery
def locate_audio_files():
    """Find and print all audio file locations"""
    files = find_audio_files()
    print("\nAudio files found:")
    for audio_file, paths in files.items():
        if paths:
            print(f"  {audio_file}: {paths[0]}")
        else:
            print(f"  {audio_file}: Not found")
    return files

def manual_repair():
    """Manual repair function that users can call if issues persist"""
    print("\nPerforming manual repair...")
    
    # Find files
    files = find_audio_files()
    
    # Copy to multiple locations
    for audio_file, paths in files.items():
        if not paths:
            print(f"⚠️ Could not find {audio_file}")
            continue
            
        source = paths[0]
        # Try extra locations
        for target_dir in [
            os.getcwd(),
            os.path.join(os.getcwd(), "data"),
            os.path.join(tempfile.gettempdir(), "iitjp_resources"),
        ]:
            try:
                os.makedirs(target_dir, exist_ok=True)
                target = os.path.join(target_dir, audio_file)
                shutil.copy2(source, target)
                print(f"📦 Copied {audio_file} to {target_dir}")
            except Exception:
                pass
    
    # Re-apply patch
    apply_patch()
    
    print("✅ Manual repair completed")

# If run directly, do a more aggressive repair
if __name__ == "__main__":
    print("\nRunning IITJP audio repair...")
    locate_audio_files()
    manual_repair()
    print("\nRepair completed. Try importing and using iitjp now.") 