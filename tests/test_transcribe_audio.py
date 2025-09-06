import os
import pytest
from audio_transcribe_and_summarize.transcribe_audio import transcribe_audio


def test_transcribe_audio_success(tmp_path, mocker):
    """
    Tests that transcribe_audio correctly calls the whisper model,
    saves the transcript, and returns the text.
    """
    # Create a fake audio file to be "transcribed"
    audio_path = tmp_path / "test_audio.wav"
    audio_path.touch()

    # Create a path for the output transcript
    transcript_path = tmp_path / "transcript.txt"

    # Mock the whisper library
    mock_model = mocker.MagicMock()
    mock_model.transcribe.return_value = {"text": "This is a test transcript."}
    mocker.patch("whisper.load_model", return_value=mock_model)

    result_text = transcribe_audio(
        str(audio_path), str(transcript_path), model_size="base"
    )

    # Check that the function returned the correct text
    assert result_text == "This is a test transcript."

    # Check that the transcript file was created and contains the correct text
    assert os.path.exists(transcript_path)
    with open(transcript_path, "r") as f:
        content = f.read()
    assert content == "This is a test transcript."
