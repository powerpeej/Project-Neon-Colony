# Project TODO List

This file outlines the tasks for the development team.

---
## **Pending Tasks**
---

### **Programmer**
- **Assignee:** Programmer Agent
- **Status:** Pending
- **Task:**
    1.  Create a `WFC` class in `src/procgen/wfc.gd`.
    2.  The class should be able to take a set of tiles and their adjacency rules as input.
    3.  Implement the core WFC algorithm to generate a tilemap.
    4.  Create a `BuildingGenerator` node that uses the `WFC` class to generate buildings.
- **Goal:** Create a system for procedurally generating buildings.

---

### **Artist**
- **Assignee:** Artist Agent
- **Status:** Pending
- **Task:**
    1.  Design a set of modular, top-down road tiles (e.g., straight, corner, T-junction, cross-section).
    2.  Design a few simple, top-down building footprint sprites that can be used with the WFC algorithm.
    3.  All assets should be 32x32 pixels and fit the cyberpunk theme.
    4.  Export the assets as PNG files and add them to the `art/tiles/` directory.
- **Goal:** Provide the visual assets needed for the procedural city generation.

---
## **Completed Tasks**
---

### **Project Manager**
- **Status:** Complete
- **Task:** Set up the initial project structure, `project.godot` file, `AGENTS.md`, and this `TODO.md`.

---

### **Programmer**
- **Status:** Complete
- **Task:** Create a simple "Player" scene and implement basic top-down movement.

---

### **Programmer**
- **Status:** Complete
- **Task:**
    1.  Create a new `LSystem` class in `src/procgen/lsystem.gd`.
    2.  The class should be able to store rules, an axiom, and generate a string based on a given number of iterations.
    3.  Create a `RoadGenerator` node that uses the `LSystem` to generate a basic road network.
    4.  Implement a "turtle" graphics system within `RoadGenerator` to draw the generated road network on the screen for visualization.
- **Goal:** Create the foundational system for procedural road generation.

---

### **Artist**
- **Status:** Complete
- **Task:** Design and create a placeholder sprite for the main character.

---

### **Researcher**
- **Status:** Complete
- **Task:** Research and summarize findings on procedural generation algorithms.
