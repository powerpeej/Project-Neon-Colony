# Project TODO List

This file outlines the tasks for the development team.

---
## **Pending Tasks**
---

### **Programmer**
- **Assignee:** Programmer Agent
- **Status:** Pending
- **Task:**
    1. Refactor the `RoadGenerator` to be more modular. Create a new `Turtle` class that handles the drawing logic, and move the L-System generation to a separate function.
    2. Modify the `RoadGenerator` to place road tiles in a `TileMap` instead of drawing `Line2D` nodes.
    3. Externalize the L-System rules to a JSON file (`res://procgen/lsystem_rules.json`) to allow for easier modification.
- **Goal:** Improve the flexibility and modularity of the road generation system and integrate it with a `TileMap`.

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

### **Programmer**
- **Assignee:** Programmer Agent
- **Status:** Pending
- **Task:**
    1. Implement a basic resource system (e.g., energy, materials).
    2. Create a global script (`/src/resource_manager.gd`) to manage resource storage and access.
    3. Create a simple UI scene (`/scenes/ui/resource_display.tscn`) to display the current resource levels.
- **Goal:** Establish the foundational economic loop of the game.

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

### **Artist**
- **Assignee:** Artist Agent
- **Status:** Pending
- **Task:**
    1. Design UI elements for the resource display (e.g., icons for energy and materials, a background panel).
    2. Create sprites for the initial building types (power plant, housing, factory).
- **Goal:** Create the visual assets for the resource system and initial buildings.

---

### **Researcher**
- **Assignee:** Researcher Agent
- **Status:** Pending
- **Task:**
    1. Research and write a report on simple agent-based AI behavior systems (e.g., state machines, behavior trees).
    2. Propose a basic AI architecture for the colonists (e.g., what needs they should have, how they should interact with buildings).
- **Goal:** To inform the design of the colonist AI system.

---

### **Researcher**
- **Assignee:** Researcher Agent
- **Status:** Pending
- **Task:**
    1. Investigate performance optimization techniques for large-scale simulations in Godot (e.g., multithreading, visual optimization).
    2. Write a document summarizing the findings and providing recommendations.
- **Goal:** To ensure the game can handle a large number of entities and complex systems without performance issues.

---
## **Completed Tasks**
---

### **Project Manager**
- **Status:** Complete
- **Task:** 
    1. Review the implemented L-System and road generation.
    2. Define the requirements for the initial building types (e.g., power plants, housing, factories).
    3. Set up the initial project structure, `project.godot` file, `AGENTS.md`, and this `TODO.md`.

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
