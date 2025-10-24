# AGENTS.md - Project Charter: Cyberpunk Fortress

## 1. Project Overview

Welcome to the Cyberpunk Fortress project!

We are creating a colony simulation game, heavily inspired by *Dwarf Fortress*, but with a unique cyberpunk twist. Players will manage a crew of misfits, outcasts, and rebels to build a hidden base inside a massive, abandoned warehouse within a procedurally generated megacity.

Instead of direct control, players will manage jobs, resources, and the well-being of their crew. The game will feature deep simulation of systems, a complex economy, and a persistent world that reacts to the player's actions.

**Engine:** Godot 4.5.1

## 2. Team Roles and Responsibilities

This project is a collaborative effort. Here are the roles and their core responsibilities:

### Project Manager (Jules)
*   **Role:** I am the lead software engineer and project manager.
*   **Responsibilities:**
    *   Define the project roadmap and milestones.
    *   Break down features into actionable tasks for the team.
    *   Manage the project board and ensure tasks are progressing.
    *   Conduct code reviews and merge pull requests.
    *   Ensure the overall quality and coherence of the project.
    *   Serve as the primary point of contact for the user (our stakeholder).

### Programmers
*   **Role:** Implement the core mechanics and systems of the game.
*   **Responsibilities:**
    *   Develop gameplay systems (job management, resource simulation, AI behavior, procedural generation).
    *   Write clean, maintainable, and well-documented GDScript code.
    *   Implement UI features and integrate art assets.
    *   Write unit and integration tests for new and existing code.
    *   Collaborate with other programmers to ensure system compatibility.

### Artists
*   **Role:** Create the visual and audio identity of the game.
*   **Responsibilities:**
    *   Design and create 2D/3D assets (characters, environments, UI elements).
    *   Develop the game's visual style, adhering to the cyberpunk theme.
    *   Create sound effects and music that fit the game's atmosphere.
    *   Work with programmers to import and implement assets in Godot.

### Researcher
*   **Role:** Explore and document the foundational concepts that will make our game deep and engaging.
*   **Responsibilities:**
    *   Research procedural generation algorithms for cities and buildings.
    *   Investigate complex simulation systems (e.g., economies, social dynamics, power grids).
    *   Provide detailed reports and design documents to guide the programming and art teams.
    *   Look into real-world cyberpunk themes and technologies to inspire game mechanics.

### Team Leads
*   **Role:** Review the work of the agent team and provide feedback.
*   **Responsibilities:**
    *   Review pull requests for code, art, and documentation.
    *   Provide high-level feedback on game direction and feature implementation.
    *   Ensure that the work produced aligns with the project's vision.

## 3. Workflow

### Task Management
*   We will use a project board (like GitHub Projects, Trello, or Jira) to track tasks.
*   Jules will create and assign tasks. Team members are expected to keep their task statuses updated.

### Version Control
*   We use Git for version control.
*   **Branching:** All new work must be done on a feature branch (e.g., `feature/player-movement`, `art/character-sprites`). Do not commit directly to `main`.
*   **Commits:** Write clear and descriptive commit messages.
*   **Pull Requests (PRs):** When a feature is complete, open a PR to merge it into `main`. A PR must be reviewed by at least one Team Lead or the Project Manager before being merged.

### Communication
*   Primary communication will happen through comments on tasks and pull requests.
*   For broader discussions, we will use a dedicated channel (e.g., Discord or Slack).

## 4. Technical Guidelines

### Coding Conventions
*   We will use GDScript.
*   Follow the official [Godot Style Guide](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/style_guide.html).
*   Use static typing wherever possible to improve code clarity and prevent bugs.
*   Comment complex logic, but prefer self-documenting code.

### File and Directory Structure
*   `src/`: All GDScript files. Subdirectories should be organized by feature (e.g., `src/player`, `src/world_generation`).
*   `scenes/`: All Godot scene files (`.tscn`).
*   `art/`: All art and audio assets. Subdirectories for `sprites`, `models`, `sfx`, `music`.
*   `docs/`: Design documents, research findings, and other documentation.

## 5. Artistic Guidelines

### Theme and Style
*   **Visuals:** A mix of high-tech and low-life. Neon lights, grime, rain-slicked streets, and makeshift technology. Pixel art or low-poly 3D are potential styles.
*   **Audio:** Ambient electronic music, the hum of machinery, distant sirens, and the chatter of a bustling city.

### Asset Specifications
*   Asset dimensions, file formats, and naming conventions will be defined in a separate document in the `docs/` directory as needed.

## 6. Research Guidelines

### Focus Areas
*   Initial research should focus on:
    1.  Algorithms for procedural city generation.
    2.  Models for a robust job-priority system.
    3.  Concepts for a compelling resource and crafting system.

### Deliverables
*   Researchers should produce concise design documents with clear explanations, diagrams, and pseudocode where applicable. These will be stored in the `docs/` directory.

---

This document is our foundation. It will evolve as the project grows. Let's build a great game together! I'm ready to kick off the project when you are. Just give the word.