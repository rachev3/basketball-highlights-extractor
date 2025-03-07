# Assignment: Automated Extraction of Basketball Highlights via Audio Peaks

## Objective

Develop an automated solution that extracts highlight segments from a full-match basketball video based on detecting the loudest moments in the audio track. These audio peaks should correlate with key, exciting moments such as crowd cheers and heightened commentator reactions.

## Scope

- **Input:** A YouTube video link for a full-match basketball game.
- **Output:** A set of video clips (or a single compiled highlight reel) extracted around the moments where the audio is at its loudest.
- **Constraints:** Use only free and open-source tools and libraries.

# Video link examples:

- https://www.youtube.com/watch?v=Jlv68sW4tLo&t=1997s
- https://www.youtube.com/watch?v=vEARGDMD_-4

## Proposed Approach

1. **Video Downloading:**

   - Accept a YouTube video link as input.
   - Use a tool such as **yt-dlp** or **youtube-dl** to download the full video in high quality. This ensures consistent access to every frame and avoids issues with streaming interruptions.

2. **Audio Extraction:**

   - Use FFmpeg to extract the audio track from the downloaded video.
   - Generate a high-quality audio file for subsequent analysis.

3. **Audio Analysis:**

   - Process the extracted audio using audio processing libraries (e.g., **librosa** or **PyDub**).
   - Compute the RMS (root-mean-square) energy or volume envelope over short, fixed-duration windows.
   - Identify the top N loudest segments (or segments above a dynamic threshold) which likely represent high-energy moments.
   - Add a configurable time buffer (e.g., 5 seconds before and after each peak) to capture the full context of the event.

4. **Timestamp Synchronization:**

   - Map the detected audio peak times to corresponding video timestamps.
   - Ensure synchronization accuracy so that the extracted clips precisely reflect the intended highlight moments.

5. **Video Clip Extraction:**
   - Use FFmpeg to extract video segments based on the computed timestamps.
   - Optionally, merge the clips into a single highlight reel.
   - Implement edge-case handling for peaks near the start or end of the video.

## Technical Requirements & Tools

- **Programming Language:** Python.
- **Video Downloading:**
  - **yt-dlp** or **youtube-dl** for downloading the YouTube video.
- **Audio/Video Processing Tools:**
  - **FFmpeg:** For audio extraction and video segment slicing.
  - **Librosa / PyDub:** For audio processing and analysis.
- **Data Processing Libraries:**
  - **NumPy & Pandas:** For handling time-series data and managing thresholds.
  - **SciPy (optional):** For advanced signal processing (e.g., peak detection).

## Additional Considerations

- **Error Handling & Logging:** Implement comprehensive logging for each step to handle and report errors.
- **Configuration:** Parameters such as buffer duration, threshold levels, and segment lengths should be configurable (via a configuration file or command-line arguments).
- **Documentation:** Provide clear instructions for installation, setup, usage, and any assumptions made.
- **Testing:** Develop test cases with sample videos to validate that the loudest audio segments correspond to actual game highlights.

## Deliverables

- A detailed technical document outlining the solution design.
- This assignment document to guide the development process.
- A project timeline with milestones for prototyping, testing, and final deployment.
- (Optional) Suggestions for future enhancements (e.g., integrating OCR for on-screen score detection or adding action recognition for refined highlight selection).

## Evaluation Criteria

- **Accuracy:** The extracted clips should correctly correspond to exciting moments in the game.
- **Performance:** The solution should process full-match videos within a reasonable time frame.
- **Scalability & Maintainability:** The code structure should be modular and easily extendable for future features.
- **User Documentation:** Clear instructions for both usage and ongoing maintenance.
