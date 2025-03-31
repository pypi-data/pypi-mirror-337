from setuptools import setup, find_packages
import sys
import platform
import os

# Ensure data directories exist
if not os.path.exists('temp'):
    os.makedirs('temp', exist_ok=True)

# Get platform-specific dependencies
if sys.platform == 'darwin':  # macOS
    platform_requires = [
        "pydub>=0.25.1",
        "pyobjc-framework-Cocoa",  # Required for audio on macOS
        "pyaudioop; python_version >= '3.13'",  # For Python 3.13+ where audioop was moved
    ]
elif sys.platform == 'win32':  # Windows
    platform_requires = [
        # winsound is part of the standard library, no need to install it
        "pydub>=0.25.1",  # Still needed for MP3 to WAV conversion
        "pyaudioop; python_version >= '3.13'",  # For Python 3.13+ where audioop was moved
    ]
else:  # Linux and other systems
    platform_requires = [
        "pydub>=0.25.1",
        "python-dbus",  # Commonly needed for audio in Linux
        "pyaudioop; python_version >= '3.13'",  # For Python 3.13+ where audioop was moved
    ]

setup(
    name="iitjp",  # Lowercase package name for consistency
    version="0.2.12",
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
        "iitjp": ["data/*.mp3", "data/*.json"],
    },
    # Use a simpler approach for data files with absolute paths
    # This is to ensure data files are properly accessible
    data_files=[],
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
