import os
import subprocess
import pytest
from audio_transcribe_and_summarize.extract_audio import extract_audio


def test_extract_audio_success(tmp_path, mocker):
    """
    Tests that extract_audio calls ffmpeg with the correct command
    and returns the expected output path.
    """
    # Create a fake input video file in the temporary directory
    video_dir = tmp_path / "videos"
    video_dir.mkdir()
    video_path = video_dir / "test_video.mp4"
    video_path.touch()  # .touch() creates an empty file

    # Create the directory for the audio output
    audio_dir = tmp_path / "audio"

    # Mock the subprocess.run function so we don't actually run ffmpeg
    spy_subprocess = mocker.patch("subprocess.run")

    # Call the function we are testing
    output_path = extract_audio(str(video_path), str(audio_dir))

    # Check that the returned path is correct
    expected_path = os.path.join(audio_dir, "test_video.wav")
    assert output_path == expected_path

    # Check that subprocess.run was called exactly once with the right command
    expected_command = [
        "ffmpeg",
        "-i",
        str(video_path),
        "-q:a",
        "0",
        "-map",
        "a",
        "-y",
        expected_path,
    ]
    spy_subprocess.assert_called_once_with(
        expected_command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE
    )


def test_extract_audio_video_not_found(tmp_path):
    """
    Tests that the function raises a FileNotFoundError for a missing video.
    """
    with pytest.raises(FileNotFoundError):
        extract_audio("non_existent_video.mp4", str(tmp_path))
