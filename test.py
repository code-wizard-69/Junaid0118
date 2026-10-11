
import subprocess
import sys
from datetime import datetime


def run(command):
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False
    )


def contribute():
    status = run(["git", "status", "--short"])

    if status.returncode != 0:
        print("Error: Run this script inside a Git repository.")
        sys.exit(1)

    if not status.stdout.strip():
        print("No actual changes found. Nothing to commit.")
        return

    print("Changes found:")
    print(status.stdout)

    confirm = input("Commit and push these changes? (y/n): ")

    if confirm.lower() != "y":
        print("Cancelled.")
        return

    # Stage actual changes
    if run(["git", "add", "-A"]).returncode != 0:
        print("Failed to stage changes.")
        return

    # Commit using the current date and time
    message = f"chore: project updates {datetime.now():%Y-%m-%d}"

    result = run(["git", "commit", "-m", message])

    if result.returncode != 0:
        print(result.stderr)
        return

    print(result.stdout)

    # Push to the configured upstream branch
    result = run(["git", "push"])

    if result.returncode != 0:
        print("Push failed:", result.stderr)
        return

    print("Successfully pushed genuine project changes.")


if __name__ == "__main__":
    contribute()
