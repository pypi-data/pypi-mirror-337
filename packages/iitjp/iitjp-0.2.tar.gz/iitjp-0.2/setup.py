from setuptools import setup, find_packages
import sys
import platform
import os

# Platform-specific dependencies
if sys.platform == 'darwin':  # macOS
    platform_requires = [
        "pydub",
        "pyobjc-framework-Cocoa",  # Required for audio on macOS
    ]
elif sys.platform == 'win32':  # Windows
    platform_requires = [
        "pydub",
        "pywin32",  # Windows-specific utilities
    ]
else:  # Linux and other systems
    platform_requires = [
        "pydub",
        "python-dbus",  # Commonly needed for audio in Linux
    ]

# Ensure data directories exist
if not os.path.exists('temp'):
    os.makedirs('temp')

setup(
    name="iitjp",  # Lowercase package name for consistency
    version="0.2",
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
    data_files=[
        ('data', ['data/questions.json',
                 'data/greeting.mp3',
                 'data/start_quiz.mp3', 
                 'data/end_quiz.mp3',
                 'data/farewell.mp3']),
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
