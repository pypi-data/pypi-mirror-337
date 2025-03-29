"""
setup_config.py
----------------
Handles first-time user setup:
- Prompts for language selection and training mode.
- Writes configuration to ~/.commitgen/config.json.
"""

import os
import json
from pathlib import Path

# Path to store user configuration.
CONFIG_PATH = Path.home() / ".commitgen" / "config.json"

SUPPORTED_LANGUAGES = ["English", "Spanish", "French", "German", "Hindi", "Chinese"]

def setup():
    print("Welcome to CommitGen setup!")
    print("Select your preferred language for commit messages:")

    # Display language options.
    for i, lang in enumerate(SUPPORTED_LANGUAGES, 1):
        print(f"{i}. {lang}")
    
    choice = input("Enter the number of your preferred language: ")
    try:
        selected_language = SUPPORTED_LANGUAGES[int(choice) - 1]
    except (IndexError, ValueError):
        selected_language = "English"
        print("Invalid choice, defaulting to English.")

    print("\nDo you want to train the model with your commits?")
    print("1. Local")
    print("2. Remote")
    print("3. Both")
    print("4. None")
    training_choice = input("Choice: ")
    training_modes = {"1": "local", "2": "remote", "3": "both", "4": "none"}
    training = training_modes.get(training_choice, "none")

    remote_url = ""
    if training in ("remote", "both"):
        remote_url = input("Enter remote training API URL (e.g., https://your-domain.com/train): ")

    config = {
        "language": selected_language,
        "training": training,
        "remote_training_url": remote_url
    }

    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)
    
    print(f"\nConfiguration saved at {CONFIG_PATH}")

def load_config():
    """
    Loads the configuration from ~/.commitgen/config.json.
    Returns an empty dictionary if config does not exist.
    """
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    return {}

if __name__ == "__main__":
    setup()
