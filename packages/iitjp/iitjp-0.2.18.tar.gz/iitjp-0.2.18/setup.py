from setuptools import setup, find_packages
import sys
import platform
import os

# Ensure data directories exist
if not os.path.exists('temp'):
    os.makedirs('temp', exist_ok=True)

# Make sure data directory exists 
data_dir = os.path.join('iitjp', 'data')
if not os.path.exists(data_dir):
    os.makedirs(data_dir, exist_ok=True)
    
# Copy WAV files to package directory for proper inclusion
import shutil
import glob
for wav_file in glob.glob(os.path.join('data', '*.wav')):
    dest_file = os.path.join('iitjp', 'data', os.path.basename(wav_file))
    try:
        shutil.copy2(wav_file, dest_file)
        print(f"Copied {wav_file} to {dest_file}")
    except Exception as e:
        print(f"Error copying {wav_file}: {e}")

# Copy JSON files to package directory
for json_file in glob.glob(os.path.join('data', '*.json')):
    dest_file = os.path.join('iitjp', 'data', os.path.basename(json_file))
    try:
        shutil.copy2(json_file, dest_file)
        print(f"Copied {json_file} to {dest_file}")
    except Exception as e:
        print(f"Error copying {json_file}: {e}")

# Get platform-specific dependencies
if sys.platform == 'darwin':  # macOS
    platform_requires = [
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "pyaudio>=0.2.11",
        "pyobjc-framework-Cocoa",  # Required for audio on macOS
    ]
elif sys.platform == 'win32':  # Windows
    platform_requires = [
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "pyaudio>=0.2.11",
        "pywin32",  # Windows-specific utilities
    ]
else:  # Linux and other systems
    platform_requires = [
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "pyaudio>=0.2.11",
        "python-dbus",  # Commonly needed for audio in Linux
    ]

setup(
    name="iitjp",  # Lowercase package name for consistency
    version="0.2.18",
    author="Utkarsh Yadav",
    author_email="utkarsh.brainstorm@gmail.com",
    description="A CLI tutor library for Statistics with audio-visual interactions.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yutkarsh.brainstorm/ourusername/IITJP",  
    license="Custom", 
    packages=find_packages(),
    install_requires=platform_requires,
    include_package_data=True,
    package_data={
        "iitjp": ["data/*.wav", "data/*.json"],
    },
    data_files=[
        ('data', [
            'data/questions.json',
            'data/greeting.wav',
            'data/start_quiz.wav', 
            'data/end_quiz.wav',
            'data/farewell.wav'
        ]),
        ('temp', []),  # Include empty temp directory
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Education",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires=">=3.7",
    entry_points={ 
        "console_scripts": [
            "iitjp=iitjp.__main__:main"
        ]
    }
)
