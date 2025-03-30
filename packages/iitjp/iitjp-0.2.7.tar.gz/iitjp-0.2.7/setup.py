"""
Setup script for IITJP package
Ensures all necessary files are included in the package
"""

import os
import base64
import glob
import shutil
import subprocess
from setuptools import setup, find_packages

# First embed the audio files
def embed_audio_resources():
    """Embed audio files as base64 strings in embedded_audio.py"""
    audio_files = glob.glob("data/*.mp3")
    if not audio_files:
        print("Warning: No audio files found in data directory!")
        return False
    
    # Create content for embedded_audio.py
    file_content = [
        '"""',
        'Embedded audio files as base64 strings',
        'This ensures audio files are always available regardless of installation method',
        '"""',
        ''
    ]
    
    # Embed each audio file
    for audio_file in audio_files:
        var_name = os.path.basename(audio_file).replace('.', '_')
        print(f"Embedding {audio_file}")
        
        # Read audio file and convert to base64
        with open(audio_file, "rb") as f:
            audio_data = f.read()
        
        # Create variable with base64 data
        encoded_data = base64.b64encode(audio_data).decode('utf-8')
        file_content.append(f"{var_name} = \"\"\"{encoded_data}\"\"\"")
        file_content.append('')
    
    # Write to embedded_audio.py
    os.makedirs("iitjp", exist_ok=True)
    with open("iitjp/embedded_audio.py", "w") as f:
        f.write('\n'.join(file_content))
    
    print("Audio files embedded successfully")
    return True

# Copy repair scripts to package directory
def copy_repair_scripts():
    """Copy repair scripts to the package directory"""
    # List of scripts to copy
    scripts = ["fix_iitjp.py", "iitjp_repair.py"]
    
    for script in scripts:
        src = script if os.path.exists(script) else f"iitjp/{script}"
        dst = f"iitjp/{os.path.basename(script)}"
        
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Copied {script}")
    
    return True

# Embed audio resources
embed_audio_resources()

# Copy repair scripts
copy_repair_scripts()

# Read README with proper encoding
try:
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()
except UnicodeDecodeError:
    # Fallback to different encoding if utf-8 fails
    try:
        with open("README.md", "r", encoding="latin-1") as f:
            long_description = f.read()
    except Exception:
        long_description = "IITJP - Interactive learning tool with audio for Statistics"

# Setup configuration
setup(
    name="iitjp",
    version="0.2.7",
    description="Interactive learning tool with audio for Statistics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="IITJP",
    author_email="example@example.com",
    url="https://github.com/yourusername/iitjp",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "iitjp": ["data/*.mp3", "data/*.json", "*.py"],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.6",
    install_requires=[],  # No external dependencies needed!
    entry_points={
        "console_scripts": [
            "iitjp=iitjp.cli:main",
        ],
    },
)
