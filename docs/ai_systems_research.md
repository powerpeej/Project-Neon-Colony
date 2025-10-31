# Agent-Based AI Behavior Systems: A Research Summary

## Introduction

This report provides an overview and comparison of two common agent-based AI behavior systems: Finite State Machines (FSMs) and Behavior Trees (BTs). The goal is to inform the decision of which system to adopt for the "Cyberpunk Colony Sim" project.

## 1. Finite State Machines (FSMs)

### Concept

A Finite State Machine is a model of computation based on a hypothetical machine that can be in one of a finite number of states at any given time. The machine can transition from one state to another in response to some external inputs or events. An FSM is defined by:

- A finite number of **states**.
- A set of **transitions** between states.
- **Triggers** or **conditions** that cause a transition.

For example, an NPC guard's states could be `Patrolling`, `Chasing`, and `Attacking`. A trigger like "seeing the player" would transition the guard from `Patrolling` to `Chasing`.

### Application

FSMs are widely used in game development for simple AI due to their straightforward nature. They are excellent for characters with a limited and well-defined set of behaviors.

**Example:** The classic ghosts in Pac-Man use an FSM with states like `Wandering`, `Chasing`, and `Fleeing`.

### Advantages

- **Simplicity:** FSMs are easy to understand, design, and implement, especially for simple AI.
- **Predictability:** The behavior of an FSM is deterministic and easy to debug.
- **Low Performance Overhead:** They are computationally very cheap.

### Disadvantages

- **Scalability:** FSMs do not scale well. As the number of states and transitions grows, the "state graph" can become a tangled mess, often referred to as a "state explosion".
- **Lack of Reusability:** Logic is often duplicated across multiple states. For example, the logic for "checking health" might need to be implemented in every state.
- **No Sense of History:** An FSM only knows its current state. It has no memory of past states without adding extra complexity.

## 2. Behavior Trees (BTs)

### Concept

A Behavior Tree is a hierarchical tree of nodes that controls the flow of decision-making for an AI agent. It provides a more modular and scalable way to create complex AI behaviors compared to FSMs. The tree consists of different types of nodes:

- **Root:** The entry point of the tree.
- **Composites:** Control the flow of execution of their children (e.g., `Sequence`, `Selector`).
- **Decorators:** Modify the behavior of a child node (e.g., `Inverter`, `Succeeder`).
- **Leafs:** The actual action or condition nodes (e.g., `MoveToTarget`, `IsPlayerVisible?`).

Execution starts at the root and "ticks" down the tree each frame. The tree returns a status: `Running`, `Success`, or `Failure`, which determines how the tree is traversed in subsequent ticks.

### Application

BTs are favored for more complex AI in modern games, such as squad-based shooters, open-world RPGs, and strategy games where agents need to handle a wide range of situations and goals.

**Example:** An enemy in a stealth game might use a BT to combine behaviors like patrolling, investigating noises, seeking cover, and engaging the player.

### Advantages

- **Modularity & Reusability:** Behaviors are encapsulated in small, reusable nodes that can be combined in many ways.
- **Scalability:** The hierarchical nature makes it easy to add new behaviors without affecting existing ones. The tree structure remains clean and organized.
- **Readability:** A well-structured BT can be easily understood even by non-programmers, like game designers.

### Disadvantages

- **Complexity:** BTs can be more complex to implement from scratch than simple FSMs.
- **Debugging:** While readable, debugging the flow of a complex BT can sometimes be tricky without specialized visualization tools.
- **Slight Performance Overhead:** BTs can have a slightly higher performance cost than a very simple FSM, though they are still very efficient.

## Recommendation

For the "Cyberpunk Colony Sim" project, which is inspired by complex simulation games like Dwarf Fortress, agents (colonists, enemies, etc.) will likely require a wide range of dynamic and emergent behaviors.

- **Finite State Machines** would be suitable for very simple entities (e.g., a door, a simple turret) but would quickly become unmanageable for the core AI of colonists who need to handle tasks like working, eating, sleeping, socializing, and defending.

- **Behavior Trees** offer the modularity and scalability required for such complex agents. We can create a library of reusable actions (e.g., `FindFood`, `GoToBed`, `OperateMachine`) and compose them into complex decision-making trees for different colonist roles or personalities.

**Therefore, it is strongly recommended to adopt Behavior Trees as the primary AI behavior system for the project.** FSMs can still be used for simpler, "state-based" objects where a full BT would be overkill. This hybrid approach will provide both power and efficiency.