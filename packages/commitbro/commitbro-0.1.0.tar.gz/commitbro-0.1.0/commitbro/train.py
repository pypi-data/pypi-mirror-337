"""
train.py
---------
Handles training initiation:
- Extracts commit history from git log.
- Sends the commit data to a remote training API if configured.
"""

import subprocess
import requests
import json
from pathlib import Path
from .setup_config import load_config

def extract_commit_history(limit=50):
    """
    Extracts commit history (subject, commit hash, and body) from the last `limit` commits.
    Returns a list of structured commit dictionaries.
    """
    result = subprocess.run(
        ["git", "log", f"-n {limit}", "--pretty=format:%s%n---%n%H%n---%n%b%n---%n", "-p"],
        capture_output=True,
        text=True
    )
    raw_logs = result.stdout.strip()
    commits = raw_logs.split("\n---\n")

    structured_commits = []
    # Process in groups of 3: subject, hash, and body.
    for i in range(0, len(commits) - 1, 3):
        message = commits[i].strip()
        commit_hash = commits[i + 1].strip()
        body = commits[i + 2].strip()
        structured_commits.append({
            "hash": commit_hash,
            "message": message,
            "body": body
        })
    return structured_commits

def send_to_remote_training(api_url, commits):
    """
    Sends commit data to the remote training API.
    
    Parameters:
      api_url (str): The URL of the training API.
      commits (list): The list of commit data dictionaries.
    """
    try:
        response = requests.post(api_url, json={"commits": commits})
        if response.status_code == 200:
            print("[*] Remote training started successfully.")
            print("Response:", response.json())
        else:
            print("[!] Remote training failed with status code:", response.status_code)
            print("Response:", response.text)
    except Exception as e:
        print("[!] Error while sending data:", e)

def main():
    config = load_config()
    training_mode = config.get("training", "none")
    remote_url = config.get("remote_training_url", "")

    if training_mode not in ("remote", "both"):
        print("[*] Remote training is not enabled in config.")
        return

    commits = extract_commit_history(limit=50)
    print(f"[*] Extracted {len(commits)} commits from local repository.")

    if training_mode in ("remote", "both") and remote_url:
        print(f"[*] Sending commits to remote training server: {remote_url}")
        send_to_remote_training(remote_url, commits)
    else:
        print("[!] Remote training URL is not set in configuration.")

if __name__ == "__main__":
    main()
