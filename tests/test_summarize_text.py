import os
from audio_transcribe_and_summarize.summarize_text import summarize_text


def test_summarize_text_success(tmp_path, mocker):
    """
    Tests that summarize_text correctly calls the ollama model,
    saves the summary, and returns the summary text.
    """
    input_text = "This is a long piece of text that needs to be summarized."
    summary_path = tmp_path / "summary.md"

    # Mock the ollama.chat function
    mock_response = {"message": {"content": "This is a summary."}}
    mocker.patch("ollama.chat", return_value=mock_response)

    result_summary = summarize_text(
        input_text, str(summary_path), model_name="test-model"
    )

    # Check that the function returned the correct summary
    assert result_summary == "This is a summary."

    # Check that the summary file was created and contains the correct text
    assert os.path.exists(summary_path)
    with open(summary_path, "r") as f:
        content = f.read()
    assert content == "This is a summary."
