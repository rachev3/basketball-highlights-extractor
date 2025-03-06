#!/usr/bin/env python3
"""
Basketball Highlights Extractor

This script extracts highlight moments from basketball games based on audio peak detection.
"""

import os
import argparse
import subprocess
import tempfile
import shutil
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import ffmpeg
import wave  # Standard library module for reading WAV files


class HighlightExtractor:
    """Class to extract highlights from basketball games based on audio peaks."""

    def __init__(self, url, num_highlights=10, pre_buffer=5, post_buffer=5, output_dir="highlights"):
        """
        Initialize the highlight extractor.
        
        Args:
            url (str): YouTube URL of the basketball game
            num_highlights (int): Number of highlights to extract
            pre_buffer (int): Seconds to include before the peak
            post_buffer (int): Seconds to include after the peak
            output_dir (str): Output directory for highlights
        """
        self.url = url
        self.num_highlights = num_highlights
        self.pre_buffer = pre_buffer
        self.post_buffer = post_buffer
        self.output_dir = output_dir
        self.temp_dir = tempfile.mkdtemp()
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Set file paths
        self.video_path = os.path.join(self.temp_dir, "video.mp4")
        self.audio_path = os.path.join(self.temp_dir, "audio.wav")
        
        # Store extracted timestamps
        self.highlight_timestamps = []

    def download_video(self):
        """Download the YouTube video using yt-dlp."""
        print(f"Downloading video from {self.url}...")
        
        # Command to download the video with yt-dlp
        cmd = [
            "yt-dlp",
            "--output", self.video_path,
            "--format", "best[ext=mp4]",
            self.url
        ]
        
        try:
            subprocess.run(cmd, check=True)
            print("Video downloaded successfully!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error downloading video: {e}")
            return False

    def extract_audio(self):
        """Extract audio from the video using FFmpeg."""
        print("Extracting audio from video...")
        
        try:
            # Command to extract audio using ffmpeg
            ffmpeg.input(self.video_path).output(
                self.audio_path, 
                acodec='pcm_s16le', 
                ac=1, 
                ar=22050
            ).run(quiet=True, overwrite_output=True)
            
            print("Audio extracted successfully!")
            return True
        except ffmpeg.Error as e:
            print(f"Error extracting audio: {e}")
            return False

    def analyze_audio(self):
        """
        Analyze the audio to find peak moments using direct WAV file reading.
        Returns true if analysis was successful.
        """
        print("Analyzing audio for peak moments...")
        
        try:
            # Open the WAV file
            with wave.open(self.audio_path, 'rb') as wav_file:
                # Get basic information
                n_channels = wav_file.getnchannels()
                sample_width = wav_file.getsampwidth()
                frame_rate = wav_file.getframerate()
                n_frames = wav_file.getnframes()
                
                # Read all frames at once
                binary_data = wav_file.readframes(n_frames)
            
            # Convert binary data to numpy array (assuming 16-bit PCM, which is common)
            if sample_width == 2:  # 16-bit audio
                dtype = np.int16
            elif sample_width == 4:  # 32-bit audio
                dtype = np.int32
            else:
                raise ValueError(f"Unsupported sample width: {sample_width}")
            
            # Convert binary data to numpy array
            samples = np.frombuffer(binary_data, dtype=dtype)
            
            # If stereo, convert to mono by averaging channels
            if n_channels == 2:
                samples = samples.reshape(-1, 2).mean(axis=1)
            
            # Normalize to -1.0 to 1.0
            samples = samples / np.iinfo(dtype).max
            
            # Calculate RMS energy in windows
            frame_length = int(frame_rate * 0.5)  # 0.5 second windows
            hop_length = int(frame_rate * 0.1)    # 0.1 second hop
            
            # Calculate energy
            energy = []
            times = []
            
            for i in range(0, len(samples) - frame_length, hop_length):
                chunk = samples[i:i + frame_length]
                rms = np.sqrt(np.mean(chunk**2))
                energy.append(rms)
                times.append(i / frame_rate)
            
            energy = np.array(energy)
            times = np.array(times)
            
            # Convert to dB scale
            eps = 1e-10  # to avoid log(0)
            energy_db = 20.0 * np.log10(energy + eps)
            
            # Find peaks (loudest moments)
            peaks, _ = find_peaks(energy_db, height=np.percentile(energy_db, 95), distance=int(frame_rate / hop_length))
            
            # Create dataframe with peaks and their intensities
            peak_df = pd.DataFrame({
                'time': times[peaks],
                'intensity': energy_db[peaks]
            })
            
            # Sort by intensity (loudest first) and take top N
            peak_df = peak_df.sort_values('intensity', ascending=False).reset_index(drop=True)
            self.highlight_timestamps = peak_df.head(self.num_highlights)[['time', 'intensity']]
            
            # Plot audio waveform and peaks for visualization
            plt.figure(figsize=(15, 5))
            plt.plot(times, energy_db)
            plt.scatter(self.highlight_timestamps['time'], self.highlight_timestamps['intensity'], color='r')
            plt.xlabel('Time (s)')
            plt.ylabel('Energy (dB)')
            plt.title('Audio Energy and Detected Peaks')
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, 'audio_analysis.png'))
            
            print(f"Found {len(self.highlight_timestamps)} peak moments.")
            return True
        
        except Exception as e:
            print(f"Error analyzing audio: {e}")
            return False

    def extract_highlights(self):
        """Extract video clips around the peak moments."""
        print("Extracting highlight clips...")
        
        clip_paths = []
        video_info = ffmpeg.probe(self.video_path)
        video_duration = float(video_info['format']['duration'])
        
        for idx, row in self.highlight_timestamps.iterrows():
            peak_time = row['time']
            
            # Calculate start and end time with buffer
            start_time = max(0, peak_time - self.pre_buffer)
            end_time = min(video_duration, peak_time + self.post_buffer)
            duration = end_time - start_time
            
            # Format timestamp for filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(self.output_dir, f"highlight_{idx+1}_{timestamp}.mp4")
            clip_paths.append(output_path)
            
            try:
                # Extract clip using ffmpeg
                ffmpeg.input(self.video_path, ss=start_time, t=duration).output(
                    output_path, 
                    c='copy'
                ).run(quiet=True, overwrite_output=True)
                
                print(f"Extracted highlight {idx+1}/{len(self.highlight_timestamps)}")
            
            except ffmpeg.Error as e:
                print(f"Error extracting highlight {idx+1}: {e}")
        
        return clip_paths

    def compile_highlights(self, clip_paths):
        """Compile all highlight clips into a single video."""
        print("Compiling highlights into a single video...")
        
        # Create a text file listing all clips
        concat_file = os.path.join(self.temp_dir, "concat_list.txt")
        with open(concat_file, 'w') as f:
            for clip_path in clip_paths:
                f.write(f"file '{os.path.abspath(clip_path)}'\n")
        
        # Output path for the compiled video
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.output_dir, f"highlights_compilation_{timestamp}.mp4")
        
        try:
            # Concatenate clips using ffmpeg
            subprocess.run([
                "ffmpeg", 
                "-f", "concat", 
                "-safe", "0", 
                "-i", concat_file, 
                "-c", "copy", 
                output_path
            ], check=True)
            
            print(f"Compilation completed: {output_path}")
            return output_path
        
        except subprocess.CalledProcessError as e:
            print(f"Error compiling highlights: {e}")
            return None

    def cleanup(self):
        """Clean up temporary files."""
        print("Cleaning up temporary files...")
        try:
            shutil.rmtree(self.temp_dir)
            print("Cleanup completed.")
        except Exception as e:
            print(f"Error during cleanup: {e}")

    def run(self, compile_clips=True):
        """Run the entire highlight extraction pipeline."""
        success = True
        clip_paths = []
        
        try:
            # Step 1: Download the video
            if not self.download_video():
                return False
            
            # Step 2: Extract audio
            if not self.extract_audio():
                return False
            
            # Step 3: Analyze audio
            if not self.analyze_audio():
                return False
            
            # Step 4: Extract highlight clips
            clip_paths = self.extract_highlights()
            
            # Step 5: Compile highlights if requested
            if compile_clips and clip_paths:
                self.compile_highlights(clip_paths)
            
        except Exception as e:
            print(f"Error during highlight extraction: {e}")
            success = False
        
        finally:
            # Clean up temporary files
            self.cleanup()
            
        return success


def main():
    """Parse command line arguments and run the highlight extractor."""
    parser = argparse.ArgumentParser(description="Extract highlights from basketball games based on audio peaks.")
    parser.add_argument("--url", required=True, help="YouTube URL of the basketball game")
    parser.add_argument("--num_highlights", type=int, default=10, help="Number of highlights to extract")
    parser.add_argument("--pre_buffer", type=int, default=5, help="Seconds to include before the peak")
    parser.add_argument("--post_buffer", type=int, default=5, help="Seconds to include after the peak")
    parser.add_argument("--output", default="highlights", help="Output directory for highlights")
    parser.add_argument("--compile", action="store_true", default=True, help="Compile clips into a single video")
    
    args = parser.parse_args()
    
    # Create and run the highlight extractor
    extractor = HighlightExtractor(
        url=args.url,
        num_highlights=args.num_highlights,
        pre_buffer=args.pre_buffer,
        post_buffer=args.post_buffer,
        output_dir=args.output
    )
    
    success = extractor.run(compile_clips=args.compile)
    
    if success:
        print("Highlight extraction completed successfully!")
    else:
        print("Highlight extraction failed.")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main()) 