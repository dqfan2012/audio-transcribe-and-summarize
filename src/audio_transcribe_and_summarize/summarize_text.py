import argparse
import os
import sys


try:
    import ollama
except ImportError:
    print("Error: The 'ollama' library is not installed.")
    print("Please install it by running: pip install ollama")
    sys.exit(1)


def summarize_text(
    text_to_summarize: str, summary_output_path: str, model_name: str = "llama3.1:70b"
) -> str:
    """
    Summarizes a block of text using a local Ollama model and saves the summary.

    Args:
        text_to_summarize (str): The text content to summarize.
        summary_output_path (str): The full path to save the output summary file (.md).
        model_name (str): The name of the Ollama model to use.

    Returns:
        str: The generated summary.
    """
    if not text_to_summarize.strip():
        raise ValueError("Input text for summarization cannot be empty.")

    print(f"Summarizing text with model: {model_name}...")

    # A structured prompt for better results
    prompt = f"""Please provide a concise, well-structured summary of the following text.
The summary should capture the key points and main arguments.
Format the output in Markdown.

---
TEXT:
{text_to_summarize}
---

SUMMARY:
"""

    try:
        response = ollama.chat(
            model=model_name, messages=[{"role": "user", "content": prompt}]
        )
        summary = response["message"]["content"]
        print("Summarization complete.")

        # Save the summary to the specified output path
        output_dir = os.path.dirname(summary_output_path)
        os.makedirs(output_dir, exist_ok=True)
        with open(summary_output_path, "w", encoding="utf-8") as f:
            f.write(summary)
        print(f"Summary saved to: {summary_output_path}")

        return summary
    except Exception as e:
        print(f"An error occurred while communicating with Ollama: {e}")
        sys.exit(1)


# This block makes the script runnable on its own for testing or individual use.
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Summarize a text file using an Ollama LLM."
    )
    parser.add_argument(
        "project", help="The name of the project directory (e.g., SNHU)."
    )
    parser.add_argument(
        "transcript_file", help="The full path to the input transcript file (.txt)."
    )
    parser.add_argument(
        "--model",
        default="llama3.1",
        help="The Ollama model to use for summarization (default: llama3.1).",
    )
    args = parser.parse_args()

    home_dir = os.getenv("HOME")
    if not home_dir:
        raise OSError("HOME environment variable is not set.")

    # Read the content from the transcript file
    try:
        with open(args.transcript_file, "r", encoding="utf-8") as f:
            transcript_content = f.read()
    except FileNotFoundError:
        print(f"Error: Transcript file not found at {args.transcript_file}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading transcript file: {e}")
        sys.exit(1)

    # Build the output path for the summary file
    summary_dir = os.path.join(
        home_dir, "media_workbench", args.project, "03_summaries"
    )
    base_filename = os.path.splitext(os.path.basename(args.transcript_file))[0].replace(
        "_transcript", ""
    )
    summary_path = os.path.join(summary_dir, f"{base_filename}_summary.md")

    # Run the summarization function
    summarize_text(transcript_content, summary_path, model_name=args.model)
