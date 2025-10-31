import os
import sys
import subprocess
import csv
import hashlib

# --- Configuration ---
TODO_FILENAME = "TODO.md"
TRACKING_FILE = "jules_tasks.csv"
GIT_REMOTE_NAME = "origin"
MAIN_BRANCH_NAME = "main"
JULES_EXECUTABLE_PATH = "C:/Users/power/AppData/Roaming/npm/jules.cmd"
# --- End Configuration ---

#==============================================================================
# SECTION 0: GIT SYNCHRONIZATION (Unchanged)
#==============================================================================
def sync_with_remote_and_prepare() -> bool:
    # ... (This function is unchanged)
    print("---")
    print("Step 0: Synchronizing with remote repository...")
    try:
        status_result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        if status_result.stdout:
            print("  - Found uncommitted changes. Stashing them...")
            subprocess.run(["git", "stash"], check=True)
        print(f"  - Checking out '{MAIN_BRANCH_NAME}' branch...")
        subprocess.run(["git", "checkout", MAIN_BRANCH_NAME], check=True, capture_output=True)
        print(f"  - Pulling latest changes from '{GIT_REMOTE_NAME}/{MAIN_BRANCH_NAME}'...")
        subprocess.run(["git", "pull", GIT_REMOTE_NAME, MAIN_BRANCH_NAME], check=True)
        print("  - Synchronization successful. Local repository is up-to-date.")
        print("---")
        return True
    except subprocess.CalledProcessError as e:
        print("\n  - FATAL ERROR: Git command failed during synchronization.")
        print(f"  - Error details: {e.stderr}")
        subprocess.run(["git", "stash", "pop"])
        return False

#==============================================================================
# SECTION 1: PARSING AND JULES INTERACTION (with one new function)
#==============================================================================
def parse_structured_todo(filename: str) -> dict[str, str]:
    # ... (This function is unchanged)
    prompts = {}
    try:
        with open(filename, "r", encoding="utf-8") as f: lines = f.readlines()
    except FileNotFoundError: return {}
    in_pending_section, is_capturing_task, current_task_lines = False, False, []
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith('## **Pending Tasks**'): in_pending_section = True; continue
        elif stripped_line.startswith('## **Completed Tasks**'): in_pending_section = False; continue
        if not in_pending_section: continue
        if stripped_line == '---':
            if current_task_lines:
                prompt = "\n".join(current_task_lines)
                prompt_hash = hashlib.sha256(prompt.encode()).hexdigest()
                prompts[prompt_hash] = prompt
                current_task_lines = []
            is_capturing_task = False; continue
        if stripped_line == '- **Task:**': is_capturing_task = True; continue
        if is_capturing_task and stripped_line: current_task_lines.append(stripped_line)
    if current_task_lines:
        prompt = "\n".join(current_task_lines)
        prompt_hash = hashlib.sha256(prompt.encode()).hexdigest()
        prompts[prompt_hash] = prompt
    return prompts

def get_existing_jules_sessions() -> dict[str, str]:
    """
    Calls 'jules remote list' and parses the output to get existing sessions.
    Returns a dictionary of {first_line_of_prompt: session_id}.
    NOTE: This parsing is based on an assumed output format.
    """
    print("  - Scanning for all existing remote Jules sessions...")
    sessions = {}
    try:
        command = [JULES_EXECUTABLE_PATH, "remote", "list"]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        # This parsing logic assumes an output format like:
        # ID: <id> | Status: <status> | Prompt: <prompt_text>
        for line in result.stdout.splitlines():
            if "ID:" in line and "Prompt:" in line:
                parts = line.split("|")
                session_id = parts[0].replace("ID:", "").strip()
                prompt_text = parts[2].replace("Prompt:", "").strip()
                # We use the first line of the prompt as a key, as the list view might truncate it
                sessions[prompt_text] = session_id
        print(f"  - Found {len(sessions)} existing sessions on the server.")
        return sessions
    except Exception as e:
        print(f"  - WARNING: Could not retrieve existing Jules sessions. Error: {e}")
        return {}

def create_jules_task_with_cli(prompt: str) -> str | None:
    # ... (This function is unchanged)
    print("---")
    print(f"-> Creating task for prompt:\n{prompt}\n")
    try:
        command = [JULES_EXECUTABLE_PATH, "remote", "new", "--repo", ".", "--session", prompt]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        session_id = None
        for line in result.stdout.splitlines():
            if "Session created:" in line: session_id = line.split(":")[-1].strip()
        if session_id: print(f"--> Success! Found Session ID: {session_id}"); return session_id
        else: print("--> Task created, but could not parse Session ID from output."); return None
    except Exception as e: print(f"--> Failed to create task. Error: {e}"); return None

def get_jules_task_status(session_id: str) -> str | None:
    # ... (This function is unchanged)
    try:
        command = [JULES_EXECUTABLE_PATH, "remote", "get", session_id]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        for line in result.stdout.splitlines():
            if line.lower().startswith("status:"): return line.split(":")[-1].strip().upper()
        return "UNKNOWN"
    except subprocess.CalledProcessError: return "ERROR"
    except FileNotFoundError: return "ERROR"

#==============================================================================
# SECTION 2: FILE AND GIT MANIPULATION (Unchanged)
#==============================================================================
def update_todo_for_completion(full_prompt_text: str) -> bool:
    # ... (This function is unchanged)
    print(f"  - Updating {TODO_FILENAME} to mark task as complete...")
    try:
        with open(TODO_FILENAME, 'r', encoding='utf-8') as f: lines = f.readlines()
        completed_block = f"---\n\n### **[AUTO-COMPLETED]**\n- **Status:** Complete\n- **Task:**\n{full_prompt_text}\n"
        completed_section_index = -1
        for i, line in enumerate(lines):
            if line.strip().startswith('## **Completed Tasks**'):
                completed_section_index = i
                break
        if completed_section_index != -1:
            lines.insert(completed_section_index + 1, completed_block)
            with open(TODO_FILENAME, 'w', encoding='utf-8') as f: f.writelines(lines)
            print("  - Successfully updated TODO.md.")
            return True
        else:
            print("  - ERROR: Could not find '## **Completed Tasks**' section in TODO.md.")
            return False
    except Exception as e:
        print(f"  - ERROR: Failed to write to {TODO_FILENAME}: {e}")
        return False

def create_pull_request(session_id: str, prompt_hash: str):
    # ... (This function is unchanged)
    print("  - Starting Git process to create a Pull Request...")
    branch_name = f"docs/complete-task-{session_id}"
    commit_message = f"docs: Mark task as complete\n\nAssociated Jules Session: {session_id}"
    try:
        subprocess.run(["git", "checkout", "-b", branch_name], check=True)
        subprocess.run(["git", "add", TODO_FILENAME], check=True)
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        print(f"  - Pushing branch '{branch_name}' to remote...")
        subprocess.run(["git", "push", GIT_REMOTE_NAME, branch_name], check=True)
        print("  - Creating Pull Request on GitHub...")
        pr_title = f"Docs: Mark task {session_id} as complete"
        pr_body = f"This PR automatically updates `TODO.md` after verifying that Jules session `{session_id}` is complete."
        subprocess.run(["gh", "pr", "create", "--title", pr_title, "--body", pr_body], check=True)
        print("  - Successfully created Pull Request!")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"  - GIT/GH ERROR: An error occurred: {e}")
        print("  - Cleaning up local branch...")
        subprocess.run(["git", "checkout", MAIN_BRANCH_NAME])
        subprocess.run(["git", "branch", "-D", branch_name])
    finally:
        subprocess.run(["git", "checkout", MAIN_BRANCH_NAME])

#==============================================================================
# SECTION 3: MAIN WORKFLOWS (with new 'sync' mode)
#==============================================================================

def run_sync_mode():
    """Scans for existing Jules sessions and adopts any that match untracked tasks in TODO.md."""
    print("Running in SYNC mode...")
    if not sync_with_remote_and_prepare(): return

    tasks_in_todo = parse_structured_todo(TODO_FILENAME)
    if not tasks_in_todo: print("No pending tasks found in TODO.md."); return

    tracked_tasks = {}
    if os.path.exists(TRACKING_FILE):
        with open(TRACKING_FILE, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader: tracked_tasks[row[0]] = row[1]

    untracked_tasks = {h: p for h, p in tasks_in_todo.items() if h not in tracked_tasks}
    if not untracked_tasks:
        print("All pending tasks in TODO.md are already being tracked.")
        return

    print(f"Found {len(untracked_tasks)} untracked tasks in TODO.md. Checking for existing sessions...")
    existing_sessions = get_existing_jules_sessions() # {prompt_first_line: session_id}
    if not existing_sessions:
        print("No existing remote sessions found to sync with.")
        return

    adopted_tasks = []
    for prompt_hash, full_prompt in untracked_tasks.items():
        # The prompt from 'jules remote list' might be truncated, so we check the first line
        first_line_of_prompt = full_prompt.splitlines()[0]
        
        if first_line_of_prompt in existing_sessions:
            session_id = existing_sessions[first_line_of_prompt]
            print(f"  - MATCH FOUND! Adopting session '{session_id}' for task: '{first_line_of_prompt}'")
            adopted_tasks.append([prompt_hash, session_id, full_prompt])

    if adopted_tasks:
        with open(TRACKING_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(adopted_tasks)
        print(f"\nSuccessfully adopted and tracked {len(adopted_tasks)} existing sessions.")
    else:
        print("\nFound no existing sessions that match untracked tasks.")

def run_create_mode():
    # ... (This function is unchanged)
    print("Running in CREATE mode...")
    if not sync_with_remote_and_prepare(): return
    tasks_in_todo = parse_structured_todo(TODO_FILENAME)
    if not tasks_in_todo: print("No pending tasks found in TODO.md."); return
    tracked_tasks = {}
    if os.path.exists(TRACKING_FILE):
        with open(TRACKING_FILE, 'r', newline='') as f:
            reader = csv.reader(f)
            for row in reader: tracked_tasks[row[0]] = row[1]
    new_tasks_to_create = {h: p for h, p in tasks_in_todo.items() if h not in tracked_tasks}
    if not new_tasks_to_create: print("All pending tasks in TODO.md are already being tracked."); return
    print(f"Found {len(new_tasks_to_create)} new tasks to create.")
    created_tasks_log = []
    for prompt_hash, prompt in new_tasks_to_create.items():
        session_id = create_jules_task_with_cli(prompt)
        if session_id: created_tasks_log.append([prompt_hash, session_id, prompt])
    if created_tasks_log:
        with open(TRACKING_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(created_tasks_log)
        print(f"\nSuccessfully tracked {len(created_tasks_log)} new tasks in {TRACKING_FILE}.")

def run_review_mode():
    # ... (This function is unchanged)
    print("Running in REVIEW mode...")
    if not sync_with_remote_and_prepare(): return
    if not os.path.exists(TRACKING_FILE): print(f"Tracking file '{TRACKING_FILE}' not found."); return
    with open(TRACKING_FILE, 'r', newline='', encoding='utf-8') as f: all_tasks = list(csv.reader(f))
    still_pending_tasks = []
    has_completed_a_task = False
    for prompt_hash, session_id, full_prompt in all_tasks:
        print(f"- Checking task {session_id}...")
        status = get_jules_task_status(session_id)
        print(f"  - Status: {status}")
        if status in ['COMPLETE', 'COMPLETED']:
            print(f"  - Task {session_id} is complete! Starting completion workflow...")
            has_completed_a_task = True
            if update_todo_for_completion(full_prompt):
                create_pull_request(session_id, prompt_hash)
        else:
            still_pending_tasks.append([prompt_hash, session_id, full_prompt])
    with open(TRACKING_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(still_pending_tasks)
    if not has_completed_a_task: print("\nNo tasks were completed since the last review.")
    print(f"\nReview complete. {len(still_pending_tasks)} tasks remain pending.")

#==============================================================================
# SCRIPT ENTRYPOINT
#==============================================================================
if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ['create', 'review', 'sync']:
        print("Usage: python agent_controller.py [mode]")
        print("Modes:")
        print("  sync     - Scans for existing Jules sessions and adopts them into the tracking file.")
        print("  create   - Creates Jules tasks for any new, untracked items in TODO.md.")
        print("  review   - Reviews tracked tasks, and if complete, updates TODO and creates a PR.")
        sys.exit(1)

    mode = sys.argv[1]
    
    if mode == "sync":
        run_sync_mode()
    elif mode == "create":
        run_create_mode()
    elif mode == "review":
        run_review_mode()

    print("\nScript finished.")