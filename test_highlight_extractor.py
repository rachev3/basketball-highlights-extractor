#!/usr/bin/env python3
"""
Test script for the Basketball Highlights Extractor.
This script tests the audio analysis functionality without requiring a full video download.
"""

import os
import argparse
import tempfile
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import librosa
from scipy.signal import find_peaks
from highlight_extractor import HighlightExtractor


def download_test_video(url, output_path):
    """Download a small portion of the video for testing."""
    print(f"Downloading test segment from {url}...")
    
    # Download only the first 5 minutes of the video
    cmd = [
        "yt-dlp",
        "--output", output_path,
        "--format", "best[ext=mp4]",
        "--postprocessor-args", "ffmpeg:-t 300",  # Limit to 300 seconds (5 minutes)
        url
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("Test video segment downloaded successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error downloading test video: {e}")
        return False


def extract_test_audio(video_path, audio_path):
    """Extract audio from the test video file."""
    print("Extracting audio from test video...")
    
    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-vn",  # No video
        "-acodec", "pcm_s16le",  # PCM format
        "-ar", "22050",  # Sample rate
        "-ac", "1",  # Mono
        "-y",  # Overwrite output file
        audio_path
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("Test audio extracted successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error extracting test audio: {e}")
        return False


def analyze_test_audio(audio_path, output_dir):
    """Analyze the test audio file and plot the results."""
    print("Analyzing test audio...")
    
    try:
        # Load audio file
        y, sr = librosa.load(audio_path, sr=None)
        
        # Calculate RMS energy (volume envelope)
        frame_length = int(sr * 0.5)  # 0.5 second windows
        hop_length = int(sr * 0.1)    # 0.1 second hop
        
        # Calculate RMS energy in decibels (dB)
        S = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]
        S_db = librosa.amplitude_to_db(S, ref=np.max)
        
        # Find peaks (loudest moments)
        peaks, _ = find_peaks(S_db, height=np.percentile(S_db, 95), distance=sr)
        
        # Convert frame indices to time in seconds
        peak_times = librosa.frames_to_time(peaks, sr=sr, hop_length=hop_length)
        
        # Plot audio waveform and peaks for visualization
        plt.figure(figsize=(15, 5))
        times = librosa.frames_to_time(np.arange(len(S_db)), sr=sr, hop_length=hop_length)
        plt.plot(times, S_db)
        plt.scatter(peak_times, S_db[peaks], color='r')
        plt.xlabel('Time (s)')
        plt.ylabel('Energy (dB)')
        plt.title('Test Audio Energy and Detected Peaks')
        plt.tight_layout()
        
        # Save the plot
        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(os.path.join(output_dir, 'test_audio_analysis.png'))
        
        print(f"Found {len(peaks)} peak moments in the test audio.")
        print(f"Analysis plot saved to {os.path.join(output_dir, 'test_audio_analysis.png')}")
        
        return peak_times
    
    except Exception as e:
        print(f"Error analyzing test audio: {e}")
        return []


def main():
    """Run the test for the highlight extractor."""
    parser = argparse.ArgumentParser(description="Test the basketball highlights extractor.")
    parser.add_argument("--url", required=True, help="YouTube URL of the basketball game to test")
    parser.add_argument("--output", default="test_results", help="Output directory for test results")
    
    args = parser.parse_args()
    
    # Create temporary directory for test files
    temp_dir = tempfile.mkdtemp()
    video_path = os.path.join(temp_dir, "test_video.mp4")
    audio_path = os.path.join(temp_dir, "test_audio.wav")
    
    try:
        # Step 1: Download a small portion of the video
        if not download_test_video(args.url, video_path):
            return 1
        
        # Step 2: Extract audio from the test video
        if not extract_test_audio(video_path, audio_path):
            return 1
        
        # Step 3: Analyze the audio and visualize the results
        peak_times = analyze_test_audio(audio_path, args.output)
        
        if not peak_times:
            print("Test failed: No peaks detected in the audio.")
            return 1
        
        print("Test completed successfully!")
        print(f"Detected {len(peak_times)} potential highlights in the test segment.")
        
        # Print the timestamp of each potential highlight
        for i, time in enumerate(peak_times[:10]):  # Show top 10 at most
            minutes = int(time) // 60
            seconds = int(time) % 60
            print(f"Highlight {i+1}: {minutes}:{seconds:02d}")
        
        return 0
    
    finally:
        # Clean up temporary files
        try:
            import shutil
            shutil.rmtree(temp_dir)
            print("Test cleanup completed.")
        except Exception as e:
            print(f"Error during test cleanup: {e}")


if __name__ == "__main__":
    exit(main()) 