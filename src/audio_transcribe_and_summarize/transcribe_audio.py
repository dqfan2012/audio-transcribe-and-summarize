import argparse
import os
import sys


try:
    import whisper
except ImportError:
    print("Error: The 'openai-whisper' library is not installed.")
    print("Please install it by running: pip install openai-whisper")
    sys.exit(1)


def transcribe_audio(
    audio_path: str, transcript_output_path: str, model_size: str = "base"
) -> str:
    """
    Transcribes an audio file using OpenAI's Whisper model and saves the transcript to a file.

    Args:
        audio_path (str): The path to the input audio file (.wav).
        transcript_output_path (str): The full path to save the output transcript file (.txt).
        model_size (str): The Whisper model to use (e.g., "tiny", "base", "small", "medium", "large").

    Returns:
        str: The transcribed text, which can be passed to the next step.
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found at: {audio_path}")

    print(f"Loading Whisper model '{model_size}'...")
    try:
        model = whisper.load_model(model_size)
    except Exception as e:
        print(f"Error loading Whisper model: {e}")
        sys.exit(1)

    print(f"Starting transcription for '{os.path.basename(audio_path)}'...")
    # fp16=False can improve compatibility on systems without NVIDIA GPUs
    result = model.transcribe(audio_path, fp16=False)

    transcribed_text = result["text"]
    print("Transcription complete.")

    try:
        output_dir = os.path.dirname(transcript_output_path)
        os.makedirs(output_dir, exist_ok=True)
        with open(transcript_output_path, "w", encoding="utf-8") as f:
            f.write(transcribed_text)
        print(f"Full transcript saved to: {transcript_output_path}")
    except IOError as e:
        print(f"Error saving transcript file: {e}")
        sys.exit(1)

    return transcribed_text


# This block makes the script runnable on its own for testing or individual use.
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Transcribe an audio file using OpenAI's Whisper."
    )
    parser.add_argument(
        "project", help="The name of the project directory (e.g., SNHU)."
    )
    parser.add_argument("audio_file", help="The full path to the input audio file.")
    parser.add_argument(
        "--model_size",
        default="large-v2",
        help="The Whisper model to use (default: large-v2).",
    )

    args = parser.parse_args()

    home_dir = os.getenv("HOME")
    if not home_dir:
        raise OSError("HOME environment variable is not set.")

    # Build the output path for the transcript file
    summary_dir = os.path.join(
        home_dir, "media_workbench", args.project, "03_summaries"
    )
    base_filename = os.path.splitext(os.path.basename(args.audio_file))[0]
    transcript_path = os.path.join(summary_dir, f"{base_filename}_transcript.txt")

    # Run the transcription function
    transcribe_audio(args.audio_file, transcript_path, model_size=args.model_size)
