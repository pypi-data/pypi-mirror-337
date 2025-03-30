from setuptools import setup, find_packages

setup(
    name="IITJP",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pydub",
        "ffmpeg"
    ],
    include_package_data=True,
    package_data={
        "iitjp": ["../data/*.mp3", "../data/*.json"]
    }
)
