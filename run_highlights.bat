@echo off
echo Basketball Highlights Extractor
echo ============================

:: Check if Python is installed
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python 3.8 or later from https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Check if FFmpeg is installed
ffmpeg -version > nul 2>&1
if %errorlevel% neq 0 (
    echo Error: FFmpeg is not installed or not in PATH.
    echo Please install FFmpeg from https://ffmpeg.org/download.html
    pause
    exit /b 1
)

:: Create a virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate virtual environment and install dependencies
echo Activating virtual environment...
call venv\Scripts\activate

:: Install dependencies if requirements.txt exists
if exist requirements.txt (
    echo Installing dependencies...
    pip install -r requirements.txt
)

:: Ask for YouTube URL if not provided
set URL=%1
if "%URL%"=="" (
    echo.
    set /p URL="Enter YouTube URL of the basketball game: "
)

:: Ask for number of highlights
set /p NUM_HIGHLIGHTS="Enter number of highlights to extract [default: 10]: "
if "%NUM_HIGHLIGHTS%"=="" set NUM_HIGHLIGHTS=10

:: Ask for output directory
set /p OUTPUT_DIR="Enter output directory [default: highlights]: "
if "%OUTPUT_DIR%"=="" set OUTPUT_DIR=highlights

:: Run the highlight extractor
echo.
echo Running highlight extractor...
python highlight_extractor.py --url "%URL%" --num_highlights %NUM_HIGHLIGHTS% --output "%OUTPUT_DIR%"

:: Check if the extraction was successful
if %errorlevel% neq 0 (
    echo.
    echo Extraction failed with error code %errorlevel%.
    pause
    exit /b %errorlevel%
)

:: Open the output directory
echo.
echo Highlights extraction complete!
echo Opening output directory...
start explorer "%OUTPUT_DIR%"

pause 