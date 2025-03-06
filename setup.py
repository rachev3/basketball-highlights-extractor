from setuptools import setup, find_packages

setup(
    name="basketball-highlights-extractor",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "yt-dlp>=2023.11.16",
        "numpy>=1.26.0",
        "pandas>=2.1.1",
        "librosa>=0.10.1",
        "scipy>=1.11.3",
        "matplotlib>=3.8.0",
        "pydub>=0.25.1",
        "ffmpeg-python>=0.2.0",
    ],
    entry_points={
        "console_scripts": [
            "extract-highlights=highlight_extractor:main",
            "test-extractor=test_highlight_extractor:main",
        ],
    },
    python_requires=">=3.8",
    author="Your Name",
    author_email="your.email@example.com",
    description="Tool to extract basketball highlights based on audio peaks",
    keywords="basketball, highlights, video, audio, extraction",
    url="https://github.com/yourusername/basketball-highlights-extractor",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
) 