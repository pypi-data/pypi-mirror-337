from setuptools import setup, find_packages
import sys
import platform
import os
import shutil
import subprocess

# Run embed_resources.py to embed audio files in resource_manager.py
print("Embedding audio resources...")
try:
    if os.path.exists("embed_resources.py"):
        subprocess.run([sys.executable, "embed_resources.py"], check=True)
except Exception as e:
    print(f"Warning: Could not embed resources: {e}")

# Ensure data directories exist
if not os.path.exists('temp'):
    os.makedirs('temp', exist_ok=True)

# Make sure package data directory exists
if not os.path.exists('iitjp/data'):
    os.makedirs('iitjp/data', exist_ok=True)

# Copy data files to the package directory to ensure they're included
data_files = [
    'questions.json',
    'greeting.mp3',
    'start_quiz.mp3', 
    'end_quiz.mp3',
    'farewell.mp3'
]
for file in data_files:
    src = os.path.join('data', file) 
    dst = os.path.join('iitjp', 'data', file)
    if os.path.exists(src) and not os.path.exists(dst):
        try:
            shutil.copy2(src, dst)
            print(f"Copied {src} to {dst}")
        except Exception as e:
            print(f"Could not copy {src} to {dst}: {e}")

# Copy our fix scripts to the package
for file in ['fix_iitjp.py', 'iitjp_repair.py']:
    if os.path.exists(file):
        try:
            shutil.copy2(file, 'iitjp')
            print(f"Copied {file} to iitjp/")
        except Exception as e:
            print(f"Could not copy {file}: {e}")

# Get platform-specific dependencies
if sys.platform == 'darwin':  # macOS
    platform_requires = [
        # "pydub>=0.25.1",  # Removed pydub dependency
        "pyobjc-framework-Cocoa",  # Required for audio on macOS
    ]
elif sys.platform == 'win32':  # Windows
    platform_requires = [
        # "pydub>=0.25.1",  # Removed pydub dependency
        "pywin32",  # Windows-specific utilities
    ]
else:  # Linux and other systems
    platform_requires = [
        # "pydub>=0.25.1",  # Removed pydub dependency
        "python-dbus",  # Commonly needed for audio in Linux
    ]

# Common dependencies for all platforms
common_requires = [
    "setuptools>=44.0.0",
]

# Combine dependencies
all_requires = common_requires + platform_requires

setup(
    name="iitjp",  # Lowercase package name for consistency
    version="0.2.6",  # Increment version for comprehensive audio fixes
    author="Utkarsh Yadav",
    author_email="utkarsh.brainstorm@gmail.com",
    description="A CLI tutor library for Statistics with audio-visual interactions.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yutkarsh.brainstorm/ourusername/IITJP",  
    license="Custom", 
    packages=find_packages(),
    install_requires=all_requires,
    include_package_data=True,
    package_data={
        "iitjp": ["data/*.mp3", "data/*.json", "*.mp3", "*.json"],
    },
    data_files=[
        ('data', [
            'data/questions.json',
            'data/greeting.mp3',
            'data/start_quiz.mp3', 
            'data/end_quiz.mp3',
            'data/farewell.mp3'
        ]),
        ('iitjp', [
            'data/questions.json',
            'data/greeting.mp3',
            'data/start_quiz.mp3', 
            'data/end_quiz.mp3',
            'data/farewell.mp3'
        ]),
        ('temp', []),  # Include empty temp directory
    ],
    zip_safe=False,  # Ensure the package is not installed as a zip file
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
    },
    # Not needed anymore since we don't use ffmpeg
    # options={
    #     'metadata': {
    #         'requires_external': [
    #             'ffmpeg - For audio processing (install manually if not available)'
    #         ]
    #     }
    # }
)
