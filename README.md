# Audio Transcribe and Summarize

A powerful command-line tool to automate the process of converting video content into concise, text-based notes. This project uses a pipeline of best-in-class open-source tools to extract audio, generate a highly accurate transcription, and produce an AI-generated summary in Markdown format.

The primary goal is to create an efficient workflow for processing video lectures, webinars, and meetings, turning them into easily searchable notes for knowledge bases like Obsidian, Notion, or any other note-taking app.

## Core Features

- **Audio Extraction**: Uses FFmpeg to efficiently extract high-quality audio (.wav) from various video formats (.mp4, .mkv, etc.).
- **Accurate Transcription**: Leverages OpenAI's Whisper model to generate a detailed and precise text transcription from the audio file.
- **AI-Powered Summarization**: Utilizes a local Large Language Model (e.g., Llama 3.1) via Ollama to create a concise, coherent summary of the transcribed text.
- **Markdown Output**: Formats the final summary in clean Markdown, perfect for copying and pasting into your notes.
- **Modular and Standalone Scripts**: Each step (extract, transcribe, summarize) can be run as part of the main pipeline or as a standalone script for manual control and testing.
- **Organized File Structure**: Designed to work with a simple, scalable directory structure to keep your raw files and processed outputs organized by category.

## Workflow

The process follows a simple, three-step pipeline:

`[Video File (MP4)] -> [1. Extract Audio (WAV)] -> [2. Transcribe Text] -> [3. Summarize (Markdown)]`

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python (version 3.12 or higher)
- Poetry for Python package management.
- FFmpeg: A command-line tool for handling multimedia files.
  - On macOS (via Homebrew): `brew install ffmpeg`
  - On Debian/Ubuntu: `sudo apt update && sudo apt install ffmpeg`
- Ollama: To run the local LLM for summarization.
  - Follow the installation instructions at https://ollama.com.
  - After installing, pull the model you wish to use (Llama 3.1 is recommended):
  ```bash
  ollama pull llama3.1
  ```
  **Note**: This project is developed using the Llama 3.1 70B model, which is approximately 40GB in size. Ensure you have sufficient disk space before downloading large language models, especially those larger than 10 billion parameters.

### Installation

Clone the repository:

```bash
git clone [https://github.com/dqfan2012/audio-transcribe-and-summarize.git](https://github.com/dqfan2012/audio-transcribe-and-summarize.git)
cd audio-transcribe-and-summarize
```

#### A Note on Hardware (CUDA vs. CPU)

This project is developed on a system with an NVIDIA GPU and is configured by default to use CUDA for accelerated performance.

The openai-whisper[cuda] dependency in the pyproject.toml file is for GPU-powered transcription. If you do not have an NVIDIA GPU, or wish to use your CPU, you must make a small change before installing.

1. Open the pyproject.toml file.
2. Find the line: openai-whisper[cuda] = "..."
3. Remove [cuda] so the line reads: openai-whisper = "..."

This will install the CPU-only version of Whisper, which is compatible with all systems but will be slower.

#### Install Dependencies

Install the dependencies using Poetry:

```bash
poetry install
```

This will create a virtual environment and install all the necessary Python libraries.

### Recommended Directory Setup

This tool is designed to work with the following directory structure in your home directory (`~/`):

```bash
~/media_workbench/
└── Your_Project_Name/
    ├── 01_raw_videos/
    ├── 02_extracted_audio/
    └── 03_summaries/
```

You may have more than one project in the `media_workbench` folder. You may edit the code to change folder and file locations as you see fit.

### Usage

The primary way to use this tool is to run the full pipeline with the main script. However, each step can also be run individually.

#### Running the Full Pipeline

```bash
poetry run python src/audio_transcribe_and_summarize/main.py <PROJECT_NAME> <PATH_TO_VIDEO>
```

**Example:**

```bash
# Define the path to your video
VIDEO_SOURCE="$HOME/media_workbench/SNHU/01_raw_videos/lecture_01.mp4"

# Run the full pipeline
poetry run python src/audio_transcribe_and_summarize/main.py SNHU "$VIDEO_SOURCE"
```

The script will then:

1. Save the extracted audio to `~/media_workbench/SNHU/02_extracted_audio/`.
2. Save the full transcript and the final summary to `~/media_workbench/SNHU/03_summaries/`.

#### Running Individual Steps

- **To extract audio only:**
  ```bash
  poetry run python src/audio_transcribe_and_summarize/extract_audio.py <PROJECT_NAME> <PATH_TO_VIDEO>
  ```
- **To transcribe an existing audio file:**
  ```bash
  poetry run python src/audio_transcribe_and_summarize/transcribe_audio.py <PROJECT_NAME> <PATH_TO_AUDIO_FILE>
  ```

## Technology Stack

- **Core Logic**: Python
- **Dependency Management**: Poetry
- **Audio Extraction**: FFmpeg
- **Transcription**: OpenAI Whisper
- **Summarization**: Ollama with a Large Language Model (e.g., Llama 3.1)

## Contributing

Contributions are welcome! If you have ideas for new features, improvements, or bug fixes, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
