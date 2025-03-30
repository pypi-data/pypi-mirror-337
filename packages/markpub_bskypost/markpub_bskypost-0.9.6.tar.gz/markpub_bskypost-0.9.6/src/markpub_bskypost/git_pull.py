#!/usr/bin/env python3
import subprocess

def git_pull():
    try:
        result = subprocess.run(["git", "pull"], capture_output=True, text=True, check=True)
        print(result.stdout)
        return 0
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return 1
