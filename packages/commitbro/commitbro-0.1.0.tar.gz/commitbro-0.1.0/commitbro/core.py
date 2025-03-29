"""
core.py
--------
Contains core functionality:
- Getting the staged git diff
- Generating a commit message by calling the local LLM API (e.g., Ollama)
"""

import subprocess
import requests

def get_staged_diff():
    """
    Runs 'git diff --cached' to get staged changes.
    Returns the diff as a string.
    """
    result = subprocess.run(["git", "diff", "--cached"], capture_output=True, text=True)
    return result.stdout.strip()

def generate_commit_message(diff, language="English"):
    """
    Calls the local LLM API to generate a commit message.
    
    Parameters:
      diff (str): The git diff.
      language (str): Preferred language for the commit message.
      
    Returns:
      str: The generated commit message.
    """
    if not diff:
        return "No staged changes found."

    prompt = (
        f"You are a helpful assistant that writes Git commit messages in {language}.\n\n"
        f"Here is a code diff:\n\n{diff}\n\n"
        f"Write a commit message in {language}, short and to the point."
    )    # Replace the URL and model name as needed for your LLM setup.

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "starling-lm", "prompt": prompt, "stream": False, "options": {"num_predict": 40}}
    )
    return response.json().get("response", "").strip()
