# whisper-gui
 Basic GUI for openai-whisper

A simple graphical user interface for OpenAI's Whisper speech recognition system.

## Features
- Convert video files to audio
- Transcribe audio files using Whisper
- Support for multiple languages
- Drag & drop support
- Save transcription settings

## Installation

1. Install ffmpeg (required for audio conversion):
   ```bash
   # Ubuntu/Debian
   sudo apt install ffmpeg

   # macOS
   brew install ffmpeg

   # Windows
   # Download from https://ffmpeg.org/download.html or use winget / choco
   winget install ffmpeg
   ```

2. Install whisper-gui:
   ```bash
   pip install openai-whisper 
   # or pip install git+https://github.com/openai/whisper.git 
   pip install PySide6
   pip install whisper-gui
   ```

## Usage

1. Launch the application:
   ```bash
   whisper-gui
   ```

2. Either:
   - Open a video file and convert it to audio
   - Open an audio file directly
   
3. Select language and model size
4. Click "Transcribe" to generate text from speech
