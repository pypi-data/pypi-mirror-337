#!/usr/bin/env python
"""
IITJP Ultra-Repair Script

This standalone script will ensure all audio files in the IITJP package are properly configured,
even in the most problematic installations.

Simply run this script after installing IITJP:

python iitjp_repair.py

It will fix audio file paths, create necessary copies, and validate everything works.
"""

import os
import sys
import shutil
import tempfile
import importlib.util
import site
import platform
import time
import subprocess
import glob
import base64

print("🔧 IITJP Ultra-Repair Script 🔧")
print("==============================")
print("Diagnosing your installation...")

# Audio files to repair
AUDIO_FILES = [
    "greeting.mp3",
    "start_quiz.mp3", 
    "end_quiz.mp3",
    "farewell.mp3"
]

# Get platform info
PLATFORM = platform.system().lower()

# Define key locations
USER_HOME = os.path.expanduser("~")
TEMP_DIR = tempfile.gettempdir()
USER_IITJP_DIR = os.path.join(USER_HOME, ".iitjp")
SITE_PACKAGES = []
VENV_PATH = None
PACKAGE_DIR = None

# Find site packages
try:
    SITE_PACKAGES = site.getsitepackages()
    print(f"✅ Found {len(SITE_PACKAGES)} Python site-packages directories")
except Exception:
    print("⚠️ Could not find site-packages directories")

# Find virtual environment 
VENV_PATH = sys.prefix
print(f"✅ Python environment: {VENV_PATH}")

# Find iitjp package location
try:
    spec = importlib.util.find_spec("iitjp")
    if spec and spec.origin:
        PACKAGE_DIR = os.path.dirname(os.path.abspath(spec.origin))
        print(f"✅ Found iitjp package at: {PACKAGE_DIR}")
except Exception:
    print("⚠️ Could not locate iitjp package. Is it installed?")
    if not SITE_PACKAGES:
        print("❌ Cannot continue without knowing where iitjp is installed.")
        sys.exit(1)
    
    # Try to find it manually
    for site_dir in SITE_PACKAGES:
        potential_dir = os.path.join(site_dir, "iitjp")
        if os.path.exists(potential_dir):
            PACKAGE_DIR = potential_dir
            print(f"✅ Found iitjp package at: {PACKAGE_DIR}")
            break

if not PACKAGE_DIR:
    print("❌ Could not find iitjp package location. Please ensure it's installed.")
    print("   Try running: pip install --upgrade iitjp")
    sys.exit(1)

# Identify all potential audio file locations
def get_all_possible_locations():
    """Get all locations where audio files might be stored"""
    locations = []
    
    # Package locations
    locations.extend([
        PACKAGE_DIR,
        os.path.join(PACKAGE_DIR, "data"),
    ])
    
    # Site-packages locations
    for site_dir in SITE_PACKAGES:
        locations.extend([
            os.path.join(site_dir, "data"),
            os.path.join(site_dir, "iitjp", "data"),
        ])
    
    # User locations
    locations.extend([
        os.path.join(VENV_PATH, "Lib", "site-packages", "data"),
        os.path.join(VENV_PATH, "Lib", "site-packages", "iitjp", "data"),
        os.path.join(USER_HOME, ".iitjp"),
        os.path.join(USER_HOME, ".iitjp", "data"),
        os.path.join(TEMP_DIR, "iitjp_resources"),
    ])
    
    # Current directory
    locations.extend([
        os.getcwd(),
        os.path.join(os.getcwd(), "data"),
    ])
    
    return locations

# Get all actual source directories
def find_source_directories():
    """Find all directories that contain audio files"""
    locations = get_all_possible_locations()
    source_dirs = []
    
    for location in locations:
        try:
            if os.path.exists(location) and os.path.isdir(location):
                has_files = False
                for audio_file in AUDIO_FILES:
                    if os.path.exists(os.path.join(location, audio_file)):
                        has_files = True
                        break
                
                if has_files:
                    source_dirs.append(location)
        except Exception:
            continue
    
    return source_dirs

# Get all target directories
def get_target_directories():
    """Get all directories where audio files should be copied"""
    targets = []
    
    # Create and add user directory
    try:
        os.makedirs(USER_IITJP_DIR, exist_ok=True)
        targets.append(USER_IITJP_DIR)
    except Exception:
        pass
    
    # Add temp directory
    temp_resources = os.path.join(TEMP_DIR, "iitjp_resources")
    try:
        os.makedirs(temp_resources, exist_ok=True)
        targets.append(temp_resources)
    except Exception:
        pass
    
    # Add data directory in package
    package_data = os.path.join(PACKAGE_DIR, "data")
    try:
        os.makedirs(package_data, exist_ok=True)
        targets.append(package_data)
    except Exception:
        pass
    
    # Add package directory itself
    targets.append(PACKAGE_DIR)
    
    # Try site-packages/data
    for site_dir in SITE_PACKAGES:
        try:
            data_dir = os.path.join(site_dir, "data")
            os.makedirs(data_dir, exist_ok=True)
            targets.append(data_dir)
        except Exception:
            pass
    
    return targets

# Find all audio files
def find_audio_files():
    """Find all audio files in the system"""
    files_found = {}
    source_dirs = find_source_directories()
    
    print(f"\nSearching for audio files in {len(source_dirs)} locations...")
    
    for source_dir in source_dirs:
        for audio_file in AUDIO_FILES:
            file_path = os.path.join(source_dir, audio_file)
            if os.path.exists(file_path):
                if audio_file not in files_found:
                    files_found[audio_file] = []
                files_found[audio_file].append(file_path)
                print(f"  Found {audio_file} at {file_path}")
    
    return files_found

# Distribute audio files to all target locations
def distribute_audio_files(files_found):
    """Copy audio files to all target locations"""
    targets = get_target_directories()
    print(f"\nCopying audio files to {len(targets)} locations...")
    
    for audio_file, sources in files_found.items():
        if not sources:
            print(f"❌ No source found for {audio_file}. Cannot distribute.")
            continue
            
        source = sources[0]  # Use the first source found
        
        for target_dir in targets:
            target_path = os.path.join(target_dir, audio_file)
            
            # Skip if source and target are the same
            if os.path.normpath(os.path.dirname(source)) == os.path.normpath(target_dir):
                continue
                
            try:
                shutil.copy2(source, target_path)
                print(f"  Copied {audio_file} to {target_dir}")
            except Exception as e:
                print(f"  ⚠️ Failed to copy to {target_dir}: {e}")

# Generate iitjp_resource_patch.py for custom imports
def create_resource_patch():
    """Create a patch file that users can import to fix resource access"""
    patch_file = "iitjp_resource_patch.py"
    
    content = """
# IITJP Resource Patch
# Import this file to fix resource loading issues

import os
import sys
import shutil
import tempfile

# Audio files we need to locate
AUDIO_FILES = [
    "greeting.mp3",
    "start_quiz.mp3", 
    "end_quiz.mp3",
    "farewell.mp3"
]

# Find all possible locations of audio files
def find_audio_files():
    # Check common locations
    locations = [
        os.path.expanduser(os.path.join("~", ".iitjp")),
        os.path.join(tempfile.gettempdir(), "iitjp_resources"),
        os.path.join(os.getcwd(), "data"),
        os.getcwd()
    ]
    
    # Try to find the package directory
    try:
        import importlib.util
        spec = importlib.util.find_spec("iitjp")
        if spec and spec.origin:
            package_dir = os.path.dirname(os.path.abspath(spec.origin))
            locations.extend([
                package_dir,
                os.path.join(package_dir, "data"),
            ])
    except:
        pass
        
    # Try to find site-packages
    try:
        import site
        for site_dir in site.getsitepackages():
            locations.extend([
                os.path.join(site_dir, "data"),
                os.path.join(site_dir, "iitjp", "data"),
            ])
    except:
        pass
    
    # Check all locations for each file
    files_found = {}
    for audio_file in AUDIO_FILES:
        for location in locations:
            if os.path.exists(location):
                path = os.path.join(location, audio_file)
                if os.path.exists(path):
                    if audio_file not in files_found:
                        files_found[audio_file] = []
                    files_found[audio_file].append(path)
    
    return files_found

# Monkey patch the AudioPlayer class to always find resources
def apply_monkey_patch():
    import iitjp.audio
    
    # Store the original play method
    original_play = iitjp.audio.AudioPlayer.play
    
    # Create a list of file locations
    file_locations = find_audio_files()
    
    # Override the play method
    def patched_play(file_path, block=False):
        # If path exists directly, use it
        if os.path.exists(file_path):
            return original_play(file_path, block)
            
        # Try to find the file by name
        basename = os.path.basename(file_path)
        if basename in file_locations and file_locations[basename]:
            # Use the first found location
            actual_path = file_locations[basename][0]
            return original_play(actual_path, block)
            
        # Fallback to original behavior
        return original_play(file_path, block)
    
    # Apply the patch
    iitjp.audio.AudioPlayer.play = patched_play
    print("[✓] Applied IITJP audio resource patch")

# Apply the patch when this module is imported
apply_monkey_patch()
"""
    
    try:
        with open(patch_file, "w") as f:
            f.write(content)
        print(f"\n✅ Created {patch_file}")
        print(f"   Users can fix issues by adding: import {os.path.splitext(patch_file)[0]}")
    except Exception as e:
        print(f"❌ Failed to create patch file: {e}")

# Test if iitjp works now
def test_iitjp_import():
    """Test if iitjp can be imported correctly"""
    print("\nTesting IITJP import...")
    try:
        import iitjp
        print("✅ Successfully imported iitjp")
        return True
    except Exception as e:
        print(f"❌ Failed to import iitjp: {e}")
        return False

# Test audio file access 
def test_audio_access():
    """Test if audio files can be accessed"""
    print("\nTesting audio file access...")
    try:
        import iitjp
        from iitjp.rajlaxmi import get_audio_path
        
        all_found = True
        for audio_file in AUDIO_FILES:
            path = get_audio_path(audio_file)
            if path:
                print(f"✅ Found {audio_file} at {path}")
            else:
                print(f"❌ Could not find {audio_file}")
                all_found = False
        
        return all_found
    except Exception as e:
        print(f"❌ Error testing audio access: {e}")
        return False

# Create fixed launcher script
def create_launcher():
    """Create a fixed launcher script for iitjp"""
    launcher_file = "launch_iitjp.py"
    
    content = """
# Fixed IITJP Launcher
# Run this script to use IITJP with guaranteed working audio

import os
import sys
import importlib.util

# Find all audio files first
audio_files = {
    "greeting.mp3": None,
    "start_quiz.mp3": None,
    "end_quiz.mp3": None,
    "farewell.mp3": None
}

# Search in common locations
locations = [
    os.path.expanduser(os.path.join("~", ".iitjp")),
    os.path.join(os.path.expanduser("~"), ".local", "share", "iitjp_resources"),
    os.path.join(os.environ.get("LOCALAPPDATA", ""), "iitjp_resources"),
    os.path.join(os.getcwd(), "data"),
    os.getcwd()
]

# Find files
for audio_file in audio_files:
    for location in locations:
        path = os.path.join(location, audio_file)
        if os.path.exists(path):
            audio_files[audio_file] = path
            break

# Import iitjp with fixed paths
import iitjp

# Monkey patch the audio playback
original_play = iitjp.audio.AudioPlayer.play

def fixed_play(file_path, block=False):
    # Check if it's a filename we know
    basename = os.path.basename(file_path)
    if basename in audio_files and audio_files[basename]:
        return original_play(audio_files[basename], block)
    return original_play(file_path, block)

# Apply the patch
iitjp.audio.AudioPlayer.play = fixed_play

# Now use iitjp as normal
if __name__ == "__main__":
    print("IITJP Launcher - Audio Paths Fixed")
    print("==================================")
    print("1. Run greeting")
    print("2. Start quiz")
    print("3. Exit")
    
    choice = input("Enter choice (1-3): ")
    
    if choice == "1":
        iitjp.mam.greetings()
    elif choice == "2":
        iitjp.mam.quiz()
    else:
        print("Goodbye!")
"""
    
    try:
        with open(launcher_file, "w") as f:
            f.write(content)
        print(f"\n✅ Created {launcher_file}")
        print(f"   Users can run IITJP with guaranteed working audio by running: python {launcher_file}")
    except Exception as e:
        print(f"❌ Failed to create launcher file: {e}")

# Main repair procedure
def main():
    # Find audio files
    files_found = find_audio_files()
    
    # Check if we found all files
    missing_files = [f for f in AUDIO_FILES if f not in files_found or not files_found[f]]
    
    if missing_files:
        print(f"\n⚠️ Could not find these audio files: {', '.join(missing_files)}")
        print("   The repair may be incomplete.")
    
    # Distribute audio files
    distribute_audio_files(files_found)
    
    # Create helper files
    create_resource_patch()
    create_launcher()
    
    # Test if it works now
    import_ok = test_iitjp_import()
    if import_ok:
        audio_ok = test_audio_access()
    else:
        audio_ok = False
    
    # Final status
    print("\n🔧 Repair Completed 🔧")
    print("====================")
    
    if import_ok and audio_ok:
        print("✅ IITJP should now work correctly!")
        print("   You can use it normally with 'import iitjp'")
    else:
        print("⚠️ Some issues could not be fixed automatically.")
        print("   Please try using the launch_iitjp.py script instead.")
    
    print("\nUseful files created:")
    print("1. iitjp_resource_patch.py - Import this to fix resource loading")
    print("2. launch_iitjp.py - Run this to use IITJP with working audio")
    
    print("\nIf you still have issues, try reinstalling:")
    print("pip uninstall -y iitjp")
    print("pip install --upgrade iitjp")

if __name__ == "__main__":
    main() 