import argparse
import os
import sys
import torch
from .extract_audio import extract_audio
from .transcribe_audio import transcribe_audio
from .summarize_text import summarize_text


def main():
    """
    Main function to orchestrate the audio extraction, transcription, and summarization pipeline.
    """
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Extract, transcribe, and summarize audio from a video file."
    )
    parser.add_argument(
        "project", help="The name of the project directory (e.g., SNHU)."
    )
    parser.add_argument("video_file", help="The full path to the input video file.")
    parser.add_argument(
        "--model",
        default="llama3.1",
        help="The Ollama model to use for summarization (default: llama3.1).",
    )
    parser.add_argument(
        "--whisper_model",
        default="large-v2",
        help="The Whisper model size to use (default: large-v2).",
    )
    args = parser.parse_args()

    # Clear GPU cache if using CUDA
    torch.cuda.empty_cache()

    # Build the directory paths
    home_dir = os.getenv("HOME")
    if not home_dir:
        print("Error: HOME environment variable not set.")
        sys.exit(1)

    base_path = os.path.join(home_dir, "media_workbench", args.project)
    video_path = args.video_file

    audio_dir = os.path.join(base_path, "02_extracted_audio")
    summary_dir = os.path.join(base_path, "03_summaries")

    # Execute the pipeline
    try:
        print(f"--- Starting pipeline for {os.path.basename(video_path)} ---")

        # Step 1: Extract Audio
        # The function now returns the exact path of the created audio file.
        audio_path = extract_audio(video_path, audio_dir)

        # Step 2: Transcribe Audio
        # Dynamically create the transcript path and pass it to the function.
        base_filename = os.path.splitext(os.path.basename(audio_path))[0]
        transcript_path = os.path.join(summary_dir, f"{base_filename}_transcript.txt")
        transcribed_text = transcribe_audio(
            audio_path, transcript_path, model_size=args.whisper_model
        )

        # Step 3: Summarize Text
        # The summarize_text function now handles saving the file itself.
        summary_path = os.path.join(summary_dir, f"{base_filename}_summary.md")
        summarize_text(transcribed_text, summary_path, model_name=args.model)

        print("--- Pipeline completed successfully! ---")

    except FileNotFoundError as e:
        print(f"\nError: A file was not found.")
        print(e)
        sys.exit(1)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
