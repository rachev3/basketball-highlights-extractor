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

The implementation requests the highest quality MP4 video available to ensure good visual quality in the final highlights.

### 2. Audio Extraction and Analysis

After downloading the video, we extract the audio track using FFmpeg via the `ffmpeg-python` library:

- The audio is converted to WAV format with PCM encoding at 22050Hz mono
- This standard format ensures compatibility with audio processing libraries

For audio analysis, we use the `librosa` library with the following approach:

1. **RMS Energy Calculation**: We calculate the root-mean-square (RMS) energy in decibels over short time windows (0.5-second windows with 0.1-second hops)
2. **Peak Detection**: We use SciPy's `find_peaks` function to identify local maxima in the audio energy
3. **Thresholding**: We use a percentile-based threshold (95th percentile) to focus on only the loudest moments
4. **Selection**: We sort the detected peaks by intensity and select the top N based on user configuration

This method effectively identifies moments of highest crowd noise and commentator excitement, which strongly correlate with highlight-worthy plays.

### 3. Timestamp Processing

For each identified peak:

- We add a configurable buffer before and after (default: 5 seconds each)
- We handle edge cases by clamping to video boundaries (0 and total duration)
- We store timestamps with their corresponding intensity values

This approach ensures we capture the full context of each exciting moment, including the build-up and aftermath.

### 4. Video Clip Extraction

For each identified timestamp range:

- We use FFmpeg to extract the corresponding video segment
- We optimize the extraction by using the `-c copy` flag to avoid re-encoding when possible
- We create unique filenames based on index and timestamp to prevent overwrites

### 5. Highlight Compilation

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

3. **Peak Detection with Constraints**:
   - Height threshold: 95th percentile of all energy values ensures we only select truly loud moments
   - Distance constraint: Prevents detecting multiple peaks too close to each other (minimum distance of 1 second)

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

Each component returns clear status indicators and logs detailed error information for debugging.

## Testing Strategy

The application includes a testing script (`test_highlight_extractor.py`) that:

- Downloads only a short segment of a video to test the pipeline
- Analyzes the audio and visualizes the results
- Reports potential highlight timestamps
- This allows for quick validation of the core audio analysis without requiring full video processing

## Future Enhancements

1. **Machine Learning Integration**:

   - Train models to distinguish between different types of crowd noise
   - Combine audio peaks with visual features (fast motion, player clustering)

2. **OCR for Score Detection**:

   - Detect on-screen score changes to correlate with audio peaks
   - Filter highlights based on game situation

3. **Advanced Audio Features**:

   - Use MFCC and spectral features to better differentiate between different audio events
   - Implement voice activity detection to separate commentator speech from crowd noise

4. **UI Improvements**:
   - Develop a web or desktop interface
   - Add preview capabilities
   - Allow manual adjustment of detected highlights

## Conclusion

The Basketball Highlights Extractor effectively utilizes audio peak detection to identify key moments in basketball games. The system is designed to be modular, configurable, and extensible, allowing for future enhancements while providing valuable functionality in its current form.
