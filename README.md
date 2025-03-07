# Basketball Highlights Extractor

This application automatically extracts highlight moments from full-length basketball games by analyzing audio peaks. It identifies the most exciting moments based on crowd noise and commentator reactions while filtering out referee whistles.

## Key Features

- **Automatic Highlight Detection**: Finds exciting moments in basketball games based on audio peaks
- **Referee Whistle Filtering**: Uses frequency analysis to differentiate between whistles and genuine excitement
- **Well-Distributed Highlights**: Ensures at least 1 minute between highlights for better game coverage
- **High-Quality Output**: Downloads videos at the best available quality (up to 1080p)
- **Customizable Parameters**: Adjust the number of highlights, buffer durations, and more
- **Highlight Compilation**: Automatically combines individual clips into a single highlight reel

## Prerequisites

- Python 3.8+
- FFmpeg installed and available in your system path
- Internet connection for downloading YouTube videos

## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/basketball-highlights-extractor.git
cd basketball-highlights-extractor
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Ensure FFmpeg is installed on your system:
   - Windows: Download from [FFmpeg website](https://ffmpeg.org/download.html) and add to PATH
   - Mac: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg` or equivalent for your distribution

## Usage

Run the main script with a YouTube URL of a basketball game:

```bash
python highlight_extractor.py --url "https://www.youtube.com/watch?v=YOUTUBE_VIDEO_ID" --num_highlights 10
```

### Parameters

- `--url`: YouTube URL of the basketball game (required)
- `--num_highlights`: Number of highlights to extract (default: 10)
- `--pre_buffer`: Seconds to include before the peak (default: 5)
- `--post_buffer`: Seconds to include after the peak (default: 5)
- `--output`: Output directory for highlights (default: "highlights")
- `--compile`: Whether to compile clips into a single video (default: True)

## Output

The script will:

1. Download the YouTube video at the highest available quality (up to 1080p)
2. Extract and analyze the audio track
3. Identify the loudest moments, filter out referee whistles, and ensure at least 1 minute between highlights
4. Extract video clips around those moments
5. Optionally compile them into a single highlight video

Results will be saved in the specified output directory, including:

- Individual highlight clips
- Optional compilation video
- Audio analysis visualizations showing detected peaks and whistle filtering

## How It Works

1. **Video Downloading**: Uses yt-dlp to download the YouTube video at high quality (up to 1080p)
2. **Audio Extraction**: Extracts audio using FFmpeg
3. **Audio Analysis**:
   - Calculates audio energy over time
   - Performs frequency analysis to detect and filter out referee whistles
   - Enforces a minimum 1-minute separation between highlights for better distribution
   - Finds and ranks the most significant non-whistle peaks
4. **Clip Extraction**: Extracts video clips around those peaks using FFmpeg
5. **Compilation**: Combines clips into a single highlight reel

## License

MIT
