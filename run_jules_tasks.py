import os
import subprocess

# --- Configuration ---

# The local filename to read tasks from.
TODO_FILENAME = "TODO.md"

# --- End Configuration ---

def create_jules_task_with_cli(prompt: str):
    """
    Calls the Jules CLI to create a new remote session.
    This is the most reliable method as it uses the official tool.

    Args:
        prompt: The task description to send to Jules.
    """
    print(f"  -> Creating task for prompt: '{prompt}'")
    try:
        # Construct the command: jules remote new --repo . --session "your prompt"
        command = ["jules", "remote", "new", "--repo", ".", "--session", prompt]

        # Execute the command
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True  # This will raise an error if the command fails
        )
        
        # Print the output from the jules command on success
        print(f"     ...Success! Response from Jules CLI:")
        print(result.stdout)

    except FileNotFoundError:
        print("\nError: The 'jules' command was not found.")
        print("Please ensure the Jules CLI is installed and in your system's PATH.")
    except subprocess.CalledProcessError as e:
        # This error happens if the command returns a non-zero exit code (i.e., it failed)
        print("     ...Failed to create task.")
        print("     Jules CLI returned an error:")
        print(e.stderr) # Print the error output from the CLI

def main():
    """Reads the TODO file and calls the CLI for each line."""
    
    # Check if the TODO file exists first
    if not os.path.exists(TODO_FILENAME):
        print(f"Error: '{TODO_FILENAME}' not found.")
        print("Please run this script from the same directory as your TODO.md file.")
        return

    print(f"Reading tasks from '{TODO_FILENAME}'...")
    with open(TODO_FILENAME, "r", encoding="utf-8") as f:
        # Read all lines, filter out empty ones
        lines = [line.strip() for line in f if line.strip()]

    print(f"Found {len(lines)} tasks. Processing...")

    for line in lines:
        create_jules_task_with_cli(line)
    
    print("\nScript finished.")

if __name__ == "__main__":
    main()