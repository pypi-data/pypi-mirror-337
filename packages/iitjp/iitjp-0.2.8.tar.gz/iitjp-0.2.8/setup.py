"""
Setup script for IITJP package
Ensures all necessary files are included in the package
"""

import os
import sys
import base64
import glob
import shutil
import subprocess
from setuptools import setup, find_packages

# Embed audio files
def embed_audio_files():
    """Embed audio files as base64 strings in a Python module"""
    print("Embedding audio resources...")
    
    # Template for the output file
    template = """\"\"\"
Embedded audio files as base64 strings
This module is auto-generated - do not edit directly.
\"\"\"

"""
    
    # Audio files to embed
    audio_files = [
        "data/end_quiz.mp3",
        "data/farewell.mp3",
        "data/greeting.mp3",
        "data/start_quiz.mp3"
    ]
    
    # Process each audio file
    for audio_file in audio_files:
        try:
            print(f"Embedding {audio_file}")
            if os.path.exists(audio_file):
                with open(audio_file, "rb") as f:
                    audio_data = f.read()
                    base64_data = base64.b64encode(audio_data).decode('utf-8')
                    
                    # Create variable name from filename
                    var_name = os.path.basename(audio_file).replace(".", "_")
                    
                    # Add to template
                    template += f"{var_name} = \"{base64_data}\"\n"
        except Exception as e:
            print(f"Error embedding {audio_file}: {e}")
    
    # Write the output file
    try:
        output_file = "iitjp/embedded_audio.py"
        with open(output_file, "w") as f:
            f.write(template)
        print("Audio files embedded successfully")
    except Exception as e:
        print(f"Error writing embedded_audio.py: {e}")

# Copy repair scripts
def copy_repair_scripts():
    """Copy repair scripts to package directory"""
    print("Copying repair scripts...")
    try:
        scripts = [
            "fix_iitjp.py",
            "iitjp_repair.py"
        ]
        
        for script in scripts:
            if os.path.exists(script):
                with open(script, "r") as src:
                    content = src.read()
                    
                with open(f"iitjp/{script}", "w") as dst:
                    dst.write(content)
                print(f"Copied {script}")
    except Exception as e:
        print(f"Error copying repair scripts: {e}")

# Embed audio files and copy repair scripts
embed_audio_files()
copy_repair_scripts()

# Read the README for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Define package metadata
setup(
    name="iitjp",
    version="0.2.8",
    author="IIT Jodhpur Team",
    author_email="info@iitjp.ac.in",
    description="Interactive Teacher for Statistics featuring RajLaxmi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://iitj.ac.in",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Topic :: Education",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: Other/Proprietary License",
    ],
    python_requires=">=3.6",
    install_requires=[
        "setuptools>=44.0.0",
    ],
    entry_points={
        "console_scripts": [
            "iitjp=iitjp.__main__:main",
        ],
    },
    data_files=[
        ("data", [
            "data/questions.json",
            "data/greeting.mp3",
            "data/start_quiz.mp3",
            "data/end_quiz.mp3", 
            "data/farewell.mp3"
        ]),
        ("iitjp/data", [
            "data/questions.json",
            "data/greeting.mp3",
            "data/start_quiz.mp3",
            "data/end_quiz.mp3", 
            "data/farewell.mp3"
        ]),
    ],
    zip_safe=False,
)
