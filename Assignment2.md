# Assignment: Refining Highlight Extraction Pipeline

## Objective

Enhance our current automated highlight extraction solution by addressing two key issues:

1. **Filtering Out Referee Whistles:** Reduce false-positive highlights caused by the loud referee whistles, ensuring that only actual game highlights (crowd reactions, commentator excitement, etc.) are extracted.
2. **Improving Video Quality:** Ensure the downloaded video is of the highest available quality from YouTube (up to 1080p) for better visual clarity in the extracted clips.

## Issues Encountered

- **False Positives:** The current audio-based method identifies referee whistles as high-intensity segments. These are not indicative of a highlight play and should be filtered out.
- **Video Quality:** The program is currently not downloading the highest quality version of the video. YouTube’s maximum is 1080p, and we want to utilize that to improve clip quality.

## Proposed Solutions

### 1. Filtering Out Referee Whistles

- **Frequency Analysis:** Implement a frequency domain analysis of the audio segments. Referee whistles typically occupy a specific high-frequency range. Use libraries like `librosa` or `SciPy` to analyze the spectral content of detected peaks and discard those whose frequency characteristics match a typical whistle pattern.
- **Audio Pattern Recognition:** Train a small classifier (or rule-based filter) to distinguish between referee whistles and other exciting sounds (crowd noise, commentator shouts, etc.). This could involve:
  - Creating a labeled dataset of whistle vs. non-whistle audio segments.
  - Using machine learning techniques to classify peaks.
- **Threshold Adjustment:** Reevaluate and adjust the detection threshold or consider additional features (e.g., duration, amplitude modulation) that may help differentiate a whistle from a true highlight.

### 2. Improving Video Quality

- **Download Parameter Tuning:** Modify the video downloading script to always request the highest quality available. Update the parameters for **yt-dlp** (or **youtube-dl**) to ensure that the 1080p version is selected.
- **Validation:** After downloading, add a validation step to check the resolution of the video file. Log a warning or error if the resolution is below 1080p.
- **Fallback Mechanism:** If a 1080p version is not available, consider selecting the highest quality alternative and documenting this behavior.

## Technical Requirements & Tools

- **Programming Language:** Python
- **Audio Processing:**
  - Use `librosa` and/or `SciPy` for spectral analysis and feature extraction.
- **Video Downloading:**
  - Configure **yt-dlp** or **youtube-dl** to select the best quality stream (e.g., using `-f bestvideo[height<=1080]+bestaudio/best`).
- **Logging & Validation:**
  - Enhance the logging to capture audio filtering decisions and video quality checks.
- **Testing:**
  - Develop test cases using sample videos containing referee whistles and high-quality video downloads to validate the filtering and quality improvements.

## Deliverables

- **Updated Codebase:** Modified scripts incorporating:
  - Audio filtering for referee whistles.
  - Enhanced video download settings to target 1080p quality.
- **Documentation:** Detailed explanation of the new filtering algorithm and the changes made to the download process.
- **Test Cases:** A suite of tests demonstrating the effectiveness of the whistle filtering and confirming that the video is downloaded at the highest quality.
- **Project Timeline:** Updated timeline with milestones for development, testing, and integration of these enhancements.

## Evaluation Criteria

- **Accuracy of Filtering:** The system should effectively reduce false positives by ignoring referee whistles without omitting genuine highlight moments.
- **Video Quality:** The downloaded video should be of 1080p resolution whenever available.
- **Robustness & Logging:** Clear logging of decisions made by the filtering algorithm and video quality checks.
- **Maintainability:** Code modifications should be clean, well-documented, and modular for future enhancements.
