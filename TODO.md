# Project TODO List

This file outlines the initial tasks for the development team. Each task is assigned to a specific role.

---

### **Project Manager**
- **Status:** Complete
- **Task:** Set up the initial project structure, `project.godot` file, `AGENTS.md`, and this `TODO.md`.
- **Next:** Oversee the tasks below and review completed work.

---

### **Programmer**
- **Assignee:** Programmer Agent
- **Status:** Pending
- **Task:**
    1.  Create a simple "Player" scene with a `CharacterBody2D` node.
    2.  Implement a basic movement script (`player.gd`) that allows for top-down movement (up, down, left, right).
    3.  Create a "Main" scene to instance and test the Player scene.
    4.  Set the "Main" scene as the default scene to run when the project starts.
- **Goal:** Establish a playable character in a test environment.

---

### **Artist**
- **Assignee:** Artist Agent
- **Status:** Pending
- **Task:**
    1.  Design and create a placeholder sprite for the main character.
    2.  The sprite should be a simple, top-down view that fits a 32x32 pixel dimension.
    3.  Export the sprite as a PNG file and add it to the `art/` directory.
- **Goal:** Provide a visual representation for the player character for the Programmer to use.

---

### **Researcher**
- **Assignee:** Researcher Agent
- **Status:** Pending
- **Task:**
    1.  Begin research on procedural generation algorithms for creating cyberpunk-style city maps.
    2.  Focus on techniques like L-Systems for road networks and Wave Function Collapse (WFC) for building placement.
    3.  Summarize findings in a document within the `docs/` folder.
- **Goal:** Provide a foundational understanding of the algorithms we will use for world generation.