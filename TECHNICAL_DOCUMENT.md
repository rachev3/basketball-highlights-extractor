# Basketball Highlights Extractor: Technical Document

## Overview

This document provides a detailed explanation of the design and implementation of the Basketball Highlights Extractor application. The system automatically extracts highlight segments from full-length basketball games by detecting audio peaks that correspond to exciting moments.

## Solution Architecture

The solution is implemented as a Python-based command-line application with the following components:

1. **Input Handler**: Accepts a YouTube URL and downloads the video using yt-dlp.
2. **Audio Processor**: Extracts and analyzes the audio track to identify peak moments.
3. **Video Extractor**: Cuts video segments around the identified peaks.
4. **Highlight Compiler**: Optionally combines extracted clips into a single highlight reel.

## Implementation Details

### 1. Video Acquisition

We use `yt-dlp` (a fork of youtube-dl with better performance and more features) to download the full basketball game video. This approach provides several advantages:

- Reliable downloading with auto-retry capabilities
- Support for various video qualities and formats
- Ability to resume interrupted downloads
- Better performance compared to streaming-based approaches

The implementation requests the highest quality video available (up to 1080p) to ensure excellent visual quality in the final highlights. We use the format specification `bestvideo[height<=1080]+bestaudio/best` to select:

- The best video stream with height up to 1080p
- Combined with the best audio stream
- With a fallback to the best combined stream if separate streams aren't available

After downloading, we validate the video resolution using FFmpeg probe and provide feedback on the quality level that was obtained.

### 2. Audio Extraction and Analysis

After downloading the video, we extract the audio track using FFmpeg via the `ffmpeg-python` library:

- The audio is converted to WAV format with PCM encoding at 22050Hz mono
- This standard format ensures compatibility with audio processing libraries

For audio analysis, we use the following approach:

1. **RMS Energy Calculation**: We calculate the root-mean-square (RMS) energy in decibels over short time windows (0.5-second windows with 0.1-second hops)
2. **Peak Detection**: We use SciPy's `find_peaks` function to identify local maxima in the audio energy
3. **Frequency Analysis**: We analyze the frequency content of each peak to identify and filter out referee whistles
4. **Time Separation Enforcement**: We ensure a minimum of 1 minute between detected peaks to avoid clustered highlights
5. **Thresholding**: We use a percentile-based threshold (95th percentile) to focus on only the loudest moments
6. **Selection**: We sort the detected peaks by intensity and select the top N based on user configuration

### 3. Referee Whistle Filtering

To address the issue of referee whistles creating false positive highlights, we implemented spectral analysis:

1. **Frequency Domain Transformation**: For each audio segment, we compute the Fast Fourier Transform (FFT) to analyze its frequency content
2. **Whistle Feature Extraction**: We calculate the energy ratio in the 2000-4000 Hz frequency range, which is characteristic of referee whistles
3. **Classification**: Audio peaks with high energy concentration in the whistle frequency range (energy ratio > 0.4) are classified as whistles and filtered out
4. **Visualization**: We generate plots showing the detected peaks, whistles, and selected highlights for verification

This approach effectively reduces false positives while preserving genuine highlight moments from crowd reactions and commentator excitement.

### 4. Highlight Spacing

To ensure a good distribution of highlights throughout the game and avoid clustering:

1. **Minimum Time Separation**: We enforce a minimum separation of 1 minute between any two highlights
2. **Peak Detection Configuration**: This is implemented by setting the `distance` parameter in SciPy's `find_peaks` function
3. **Prioritization**: When multiple peaks occur within a 1-minute window, only the loudest one is retained
4. **Game Coverage**: This approach improves coverage of the entire game rather than focusing on short intense sequences

### 5. Timestamp Processing

For each identified peak:

- We add a configurable buffer before and after (default: 5 seconds each)
- We handle edge cases by clamping to video boundaries (0 and total duration)
- We store timestamps with their corresponding intensity values

This approach ensures we capture the full context of each exciting moment, including the build-up and aftermath.

### 6. Video Clip Extraction

For each identified timestamp range:

- We use FFmpeg to extract the corresponding video segment
- We optimize the extraction by using the `-c copy` flag to avoid re-encoding when possible
- We create unique filenames based on index and timestamp to prevent overwrites

### 7. Highlight Compilation

If requested, we compile all highlights into a single video:

- We create a concat file listing all clips
- We use FFmpeg's concat demuxer to join the clips
- We preserve the original video quality by using `-c copy`

## Signal Processing Details

The audio analysis uses the following signal processing techniques:

1. **Frame-based RMS Energy**:

   - For a signal `x` in a frame, RMS = sqrt(mean(x²))
   - This measures the power of the audio signal in each time window

2. **Decibel Conversion**:

   - S_db = 20 \* log10(S / ref)
   - This converts linear amplitude to logarithmic scale, which better matches human perception

3. **Spectral Analysis for Whistle Detection**:

   - Fast Fourier Transform (FFT) to convert time-domain signals to frequency domain
   - Hamming window applied to reduce spectral leakage
   - Energy ratio calculation in the 2000-4000 Hz range characteristic of whistles
   - Threshold-based classification to separate whistles from other sounds

4. **Peak Detection with Constraints**:
   - Height threshold: 95th percentile of all energy values ensures we only select truly loud moments
   - Distance constraint: At least 1 minute (600 frames at 0.1s hop length) between peaks ensures good game coverage
   - This prevents detecting multiple peaks too close to each other and avoids clustered highlights

## Performance Considerations

- **Memory Efficiency**: The system processes audio in manageable chunks to avoid loading entire long videos into memory
- **Processing Time**: For a typical 2-hour basketball game:
  - Download: 2-5 minutes (depends on internet speed and video quality)
  - Audio extraction and analysis: 1-2 minutes
  - Highlight extraction: 1-3 minutes
  - Total processing time: 4-10 minutes

## Error Handling

The application implements comprehensive error handling:

- Network errors during download
- File access issues
- Audio processing failures
- FFmpeg execution errors
- Video quality validation

Each component returns clear status indicators and logs detailed error information for debugging.

## Testing Strategy

The application includes a testing script (`test_highlight_extractor.py`) that:

- Downloads only a short segment of a video to test the pipeline
- Analyzes the audio and visualizes the results
- Reports potential highlight timestamps
- This allows for quick validation of the core audio analysis without requiring full video processing

## Future Enhancements

1. **Machine Learning Integration**:

   - Train more sophisticated models to distinguish between different types of game sounds
   - Combine audio peaks with visual features (fast motion, player clustering)

2. **OCR for Score Detection**:

   - Detect on-screen score changes to correlate with audio peaks
   - Filter highlights based on game situation

3. **Advanced Audio Features**:

   - Use MFCC and additional spectral features for better audio event classification
   - Implement voice activity detection to separate commentator speech from crowd noise

4. **UI Improvements**:
   - Develop a web or desktop interface
   - Add preview capabilities
   - Allow manual adjustment of detected highlights

## Conclusion

The Basketball Highlights Extractor effectively utilizes audio peak detection with frequency analysis to identify key moments in basketball games while filtering out referee whistles. The system ensures high-quality video output with well-distributed highlights spaced at least 1 minute apart. It is designed to be modular, configurable, and extensible, allowing for future enhancements while providing valuable functionality in its current form.
