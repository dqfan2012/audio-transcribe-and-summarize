import argparse
import os
import subprocess
import sys


def extract_audio(video_path: str, audio_output_dir: str) -> str:
    """
    Extracts audio from a video file using ffmpeg and returns the output path.

    Args:
        video_path (str): The full path to the input video file.
        audio_output_dir (str): The directory where the audio file will be saved.

    Returns:
        str: The full path to the newly created audio file.
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    # Ensure the output directory exists
    os.makedirs(audio_output_dir, exist_ok=True)

    # Dynamically create the output audio filename from the video filename
    # e.g., "lecture_04.mp4" -> "lecture_04.wav"
    base_filename = os.path.basename(video_path)
    filename_without_ext = os.path.splitext(base_filename)[0]
    # The output path is now created inside the function
    audio_path = os.path.join(audio_output_dir, f"{filename_without_ext}.wav")

    print(f"Extracting audio to: {audio_path}")

    command = ["ffmpeg", "-i", video_path, "-q:a", "0", "-map", "a", "-y", audio_path]

    try:
        subprocess.run(
            command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE
        )
        print("Audio extraction completed successfully.")
        # Return the path to the file we just created
        return audio_path
    except subprocess.CalledProcessError as e:
        print("Ffmpeg failed to execute.")
        print(f"Error: {e.stderr.decode()}")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: 'ffmpeg' command not found. Is it installed and in your PATH?")
        sys.exit(1)


# This block makes the script runnable on its own for testing or individual use.
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract audio from a video file.")
    parser.add_argument(
        "project", help="The name of the project directory (e.g., SNHU)."
    )
    parser.add_argument("video_file", help="The full path to the input video file.")

    args = parser.parse_args()

    home_dir = os.getenv("HOME")
    if not home_dir:
        raise OSError("HOME environment variable is not set.")

    # Correctly build the path to the audio output directory for this project
    audio_dir = os.path.join(
        home_dir, "media_workbench", args.project, "02_extracted_audio"
    )

    # Run the function
    extract_audio(args.video_file, audio_dir)
