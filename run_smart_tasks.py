import os
import subprocess

# --- Configuration ---

TODO_FILENAME = "TODO.md"

# IMPORTANT: You MUST replace the placeholder path below with the
# full path to your 'jules.cmd' file.
#
# To find the path, run this command in your terminal:
#   npm config get prefix
#
# Then, take the output (e.g., C:\Users\power\AppData\Roaming\npm)
# and add "\jules.cmd" to the end.
#
# Remember to use forward slashes (/) or double-backslashes (\\).
JULES_EXECUTABLE_PATH = "C:/Users/power/AppData/Roaming/npm/jules.cmd"

# --- End Configuration ---


def parse_structured_todo(filename: str) -> list[str]:
    """
    Parses a structured TODO.md file to extract detailed, multi-line task prompts.
    It only looks for tasks under a '## **Pending Tasks**' heading.
    """
    prompts = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: '{filename}' not found in the current directory.")
        return []

    in_pending_section = False
    is_capturing_task = False
    current_task_lines = []

    for line in lines:
        stripped_line = line.strip()

        # Check for section boundaries
        if stripped_line.startswith('## **Pending Tasks**'):
            in_pending_section = True
            continue
        elif stripped_line.startswith('## **Completed Tasks**'):
            in_pending_section = False
            continue

        # If we are not in the pending section, skip to the next line
        if not in_pending_section:
            continue
        
        # '---' is a hard separator between tasks. When we see it, we save
        # the task we've been building and reset.
        if stripped_line == '---':
            if current_task_lines:
                prompts.append("\n".join(current_task_lines))
                current_task_lines = []
            is_capturing_task = False
            continue

        # '- **Task:**' is the trigger to start capturing lines for a prompt
        if stripped_line == '- **Task:**':
            is_capturing_task = True
            continue # Don't include the literal "- Task:" line in the prompt

        # If we are in "capture mode", add any non-empty line to our current task
        if is_capturing_task and stripped_line:
            current_task_lines.append(stripped_line)

    # This handles the very last task in the file, which might not have a '---' after it
    if current_task_lines:
        prompts.append("\n".join(current_task_lines))

    return prompts


def create_jules_task_with_cli(prompt: str):
    """
    Calls the Jules CLI using its full path to create a new remote session.
    """
    print("---")
    print(f"-> Creating task for the following prompt:\n{prompt}\n")
    try:
        # This command uses the full path to the executable, bypassing the PATH issue
        command = [JULES_EXECUTABLE_PATH, "remote", "new", "--repo", ".", "--session", prompt]
        
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True  # This will raise an error if the command fails
        )
        print(f"--> Success! Response from Jules CLI:\n{result.stdout}")

    except FileNotFoundError:
        print(f"\nError: The executable was not found at the specified path: {JULES_EXECUTABLE_PATH}")
        print("Please verify the path in the JULES_EXECUTABLE_PATH variable in the script.")
    except subprocess.CalledProcessError as e:
        # This error happens if the command returns a non-zero exit code (i.e., it failed)
        print(f"--> Failed to create task. Jules CLI returned an error:\n{e.stderr}")


def main():
    """Main function to parse the file and execute the tasks."""
    if "YourUsername" in JULES_EXECUTABLE_PATH:
        print("ERROR: You have not configured the script yet.")
        print("Please open the script and edit the 'JULES_EXECUTABLE_PATH' variable.")
        return
        
    print(f"Parsing structured tasks from '{TODO_FILENAME}'...")
    prompts = parse_structured_todo(TODO_FILENAME)

    if not prompts:
        print("No pending tasks were found in the TODO.md file.")
        return

    print(f"\nFound {len(prompts)} pending tasks. Starting creation process...")
    for prompt in prompts:
        create_jules_task_with_cli(prompt)
    
    print("\n---")
    print("Script finished.")


if __name__ == "__main__":
    main()