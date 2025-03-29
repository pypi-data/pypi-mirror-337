"""
cli.py
-------
Main CLI tool for generating commit messages.
Loads the configuration, gets the staged diff, and prints the generated commit message.
"""

from .core import get_staged_diff, generate_commit_message
from .setup_config import load_config
import subprocess

def main():
    print("[*] Loading configuration...")
    config = load_config()
    language = config.get("language", "English")
    print(f"[*] Preferred language: {language}")
    while True:
        print("[*] Getting staged changes...")
        diff = get_staged_diff()

        if not diff:
            print("[!] No staged changes found. Please run 'git add' first.")
            return

        print("[*] Generating commit message...")
        message = generate_commit_message(diff, language)
        print("\nSuggested Commit Message:")
        print(f"> {message}")

        choice = input("✅ Accept this? [y]es / [n]o / [r]egenerate: ").strip().lower()
        if choice == "y":
            subprocess.run(["git", "commit", "-m", message])
            print("✅ Commit created successfully.")
            break
        elif choice == "r":
            print("🔄 Regenerating...\n")
            continue
        else:
            print("❌ Cancelled. No commit made.")
            break


if __name__ == "__main__":
    main()
