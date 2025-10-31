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

# ... (All functions from Section 0 and 1 are unchanged) ...

def update_todo_for_completion(full_prompt_text: str) -> bool:
    """
    --- COMPLETELY REWRITTEN FUNCTION ---
    Fully automates the update of TODO.md:
    1. Finds the exact task block in the "Pending" section.
    2. Deletes that block.
    3. Adds a new, formatted block to the "Completed" section.
    """
    print(f"  - Starting fully automated update of {TODO_FILENAME}...")
    try:
        with open(TODO_FILENAME, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # --- Step 1: Find the block to delete in the Pending section ---
        pending_start_index = -1
        completed_start_index = -1
        for i, line in enumerate(lines):
            if line.strip().startswith('## **Pending Tasks**'):
                pending_start_index = i
            elif line.strip().startswith('## **Completed Tasks**'):
                completed_start_index = i
                break # Stop once we've found both

        if pending_start_index == -1:
            print("  - ERROR: Could not find '## **Pending Tasks**' section.")
            return False

        block_start_line = -1
        block_end_line = -1
        current_block_lines = []
        in_a_block = False

        # Search only within the pending section for the task
        for i in range(pending_start_index, completed_start_index if completed_start_index != -1 else len(lines)):
            line = lines[i]
            if line.strip() == '---':
                if not in_a_block:
                    in_a_block = True
                    block_start_line = i
                    current_block_lines = []
                else: # This is the end of a block
                    in_a_block = False
                    block_end_line = i
                    
                    # Parse the prompt from the captured block
                    task_lines = []
                    is_task_section = False
                    for block_line in current_block_lines:
                        if block_line.strip() == '- **Task:**':
                            is_task_section = True
                            continue
                        if is_task_section and block_line.strip():
                            task_lines.append(block_line.strip())
                    
                    extracted_prompt = "\n".join(task_lines)

                    # Check if we found the correct block
                    if extracted_prompt == full_prompt_text:
                        break # We found our block, exit the loop
                    else: # Reset for the next block
                        block_start_line = -1
                        block_end_line = -1
            elif in_a_block:
                current_block_lines.append(line)
        
        if block_start_line == -1 or block_end_line == -1:
            print(f"  - ERROR: Could not find the exact task block to delete in the Pending section.")
            return False

        print(f"  - Found task block from line {block_start_line + 1} to {block_end_line + 1}. Deleting it.")
        
        # --- Step 2: Create the new list of lines with the block removed ---
        remaining_lines = lines[:block_start_line] + lines[block_end_line + 1:]

        # --- Step 3: Add the new block to the Completed section ---
        # We need to find the new index of the completed section header
        new_completed_start_index = -1
        for i, line in enumerate(remaining_lines):
            if line.strip().startswith('## **Completed Tasks**'):
                new_completed_start_index = i
                break
        
        if new_completed_start_index == -1:
            print("  - ERROR: Could not find '## **Completed Tasks**' section after deleting block.")
            return False

        completed_block_text = f"---\n\n### **[AUTO-COMPLETED]**\n- **Status:** Complete\n- **Task:**\n{full_prompt_text}\n"
        
        # Insert the new block right after the '---' under the completed header
        insert_position = new_completed_start_index + 2
        remaining_lines.insert(insert_position, completed_block_text)
        
        print("  - Adding new completed task block to the Completed section.")

        # --- Step 4: Write the updated content back to the file ---
        with open(TODO_FILENAME, 'w', encoding='utf-8') as f:
            f.writelines(remaining_lines)
        
        print(f"  - Successfully updated and reorganized {TODO_FILENAME}.")
        return True

    except Exception as e:
        print(f"  - ERROR: An unexpected error occurred during file update: {e}")
        return False

# --- The rest of the script is included below for completeness but is unchanged ---
#==============================================================================
# SECTION 0: GIT SYNCHRONIZATION
#==============================================================================
def sync_with_remote_and_prepare() -> bool:
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
# SECTION 1: PARSING AND JULES INTERACTION
#==============================================================================
def parse_structured_todo(filename: str) -> dict[str, str]:
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

def create_jules_task_with_cli(prompt: str) -> str | None:
    print("---")
    print(f"-> Creating task for prompt:\n{prompt}\n")
    try:
        command = [JULES_EXECUTABLE_PATH, "remote", "new", "--repo", ".", "--session", prompt]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        session_id = None
        for line in result.stdout.splitlines():
            clean_line = line.strip().lower()
            if clean_line.startswith("session id:") or clean_line.startswith("id:"):
                session_id = line.split(":")[-1].strip()
                break
        if session_id:
            print(f"--> Success! Parsed Session ID: {session_id}")
            return session_id
        else:
            print("--> Task created, but could not parse Session ID from output.")
            print("--> Full output from CLI:")
            print(result.stdout)
            return None
    except Exception as e:
        print(f"--> Failed to create task. Error: {e}")
        return None

def get_all_jules_statuses() -> dict[str, str]:
    print("  - Fetching status of all remote sessions...")
    statuses = {}
    try:
        command = [JULES_EXECUTABLE_PATH, "remote", "list", "--session"]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        lines = result.stdout.strip().splitlines()
        for line in lines[1:]:
            words = line.split()
            if len(words) < 2: continue
            truncated_id = words[0]
            status = words[-1]
            if truncated_id.endswith('…'):
                truncated_id = truncated_id[:-1]
            statuses[truncated_id] = status
        print(f"  - Successfully parsed {len(statuses)} session statuses.")
        return statuses
    except Exception as e:
        print(f"  - WARNING: Could not retrieve or parse session statuses. Error: {e}")
        return {}

#==============================================================================
# SECTION 2: FILE AND GIT MANIPULATION
#==============================================================================
def create_pull_request(session_id: str, prompt_hash: str):
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
# SECTION 3: MAIN WORKFLOWS
#==============================================================================
def run_sync_mode():
    print("Running in SYNC mode...")
    if not sync_with_remote_and_prepare(): return
    # ... (rest of sync mode is unchanged)
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
    existing_sessions = get_existing_jules_sessions()
    if not existing_sessions:
        print("No existing remote sessions found to sync with.")
        return
    adopted_tasks = []
    for prompt_hash, full_prompt in untracked_tasks.items():
        first_line_of_prompt = full_prompt.splitlines()[0]
        for desc, session_id in existing_sessions.items():
            if first_line_of_prompt.startswith(desc.replace('…','')):
                print(f"  - MATCH FOUND! Adopting session '{session_id}' for task: '{first_line_of_prompt}'")
                adopted_tasks.append([prompt_hash, session_id, full_prompt])
                break
    if adopted_tasks:
        with open(TRACKING_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(adopted_tasks)
        print(f"\nSuccessfully adopted and tracked {len(adopted_tasks)} existing sessions.")
    else:
        print("\nFound no existing sessions that match untracked tasks.")

def run_create_mode():
    print("Running in CREATE mode...")
    if not sync_with_remote_and_prepare(): return
    # ... (rest of create mode is unchanged)
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
    print("Running in REVIEW mode...")
    if not sync_with_remote_and_prepare(): return
    # ... (rest of review mode is unchanged)
    if not os.path.exists(TRACKING_FILE):
        print(f"Tracking file '{TRACKING_FILE}' not found. Nothing to review.")
        return
    all_statuses = get_all_jules_statuses()
    if not all_statuses:
        print("Could not retrieve any session statuses. Aborting review.")
        return
    with open(TRACKING_FILE, 'r', newline='', encoding='utf-8') as f:
        all_tasks = list(csv.reader(f))
    still_pending_tasks = []
    has_completed_a_task = False
    for prompt_hash, full_session_id, full_prompt in all_tasks:
        print(f"- Checking task {full_session_id}...")
        found_status = "NOT FOUND"
        for truncated_id, status in all_statuses.items():
            if full_session_id.startswith(truncated_id):
                found_status = status
                break
        print(f"  - Status: {found_status}")
        if found_status in ['COMPLETE', 'COMPLETED']:
            print(f"  - Task {full_session_id} is complete! Starting completion workflow...")
            has_completed_a_task = True
            if update_todo_for_completion(full_prompt):
                create_pull_request(full_session_id, prompt_hash)
        else:
            still_pending_tasks.append([prompt_hash, full_session_id, full_prompt])
    with open(TRACKING_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(still_pending_tasks)
    if not has_completed_a_task:
        print("\nNo tasks were completed since the last review.")
    print(f"\nReview complete. {len(still_pending_tasks)} tasks remain pending.")

#==============================================================================
# SCRIPT ENTRYPOINT
#==============================================================================
if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ['create', 'review', 'sync']:
        print("Usage: python agent_controller_final_v5.py [mode]")
        print("Modes:")
        print("  sync     - Scans for existing Jules sessions and adopts them into the tracking file.")
        print("  create   - Creates Jules tasks for any new, untracked items in TODO.md.")
        print("  review   - Reviews tracked tasks, and if complete, fully updates TODO and creates a PR.")
        sys.exit(1)

    mode = sys.argv[1]
    
    if mode == "sync":
        run_sync_mode()
    elif mode == "create":
        run_create_mode()
    elif mode == "review":
        run_review_mode()

    print("\nScript finished.")