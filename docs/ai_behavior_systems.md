# AI Behavior Systems Research Summary

This document summarizes research on simple agent-based AI behavior systems for the Cyberpunk Colony Sim project. The goal is to select a system that is effective for managing the complex behaviors of individual colonists.

---

## 1. Finite State Machines (FSMs)

**Concept:**
A Finite State Machine is a model of computation based on a hypothetical machine that can be in one of a finite number of states. The machine can only be in one state at a time, and it transitions from one state to another in response to external inputs or events.

For a colonist, states could include `Idling`, `Working`, `Eating`, `Sleeping`, etc. Transitions would be triggered by conditions like `Energy < 20%` (triggering a transition to `Sleeping`) or `TaskAssigned` (triggering a transition to `Working`).

**Application for Colony Simulation:**
*   **Colonist States:** Each colonist would have their own FSM to manage their current action.
*   **Simple Logic:** FSMs are excellent for simple, reactive behaviors. For example, if a colonist is `Idle` and their `Hunger` level is high, they transition to an `Eating` state.
*   **Implementation:** Can be implemented easily with a `switch` statement or a dictionary mapping states to functions.

**Advantages:**
*   **Simplicity:** Very easy to understand, implement, and debug for simple AI.
*   **Performance:** Extremely fast, with minimal overhead.
*   **Predictability:** The behavior of an agent is easy to predict, which helps in testing.

**Disadvantages:**
*   **Scalability:** FSMs can become very complex and difficult to manage as the number of states and transitions grows. This is often called a "state explosion."
*   **Lack of Modularity:** It's difficult to reuse or compose states. A `Working` state for a miner might be very different from a `Working` state for a doctor, requiring separate logic.

**Recommendation:**
FSMs are a good starting point for very simple agents or for managing high-level states (e.g., `Passive` vs. `Combat`). However, they are likely too rigid and unscalable for the primary behavior system of our colonists, who will need to handle a wide variety of tasks and goals.

---

## 2. Behavior Trees (BTs)

**Concept:**
A Behavior Tree is a hierarchical model of plan execution. It is a tree of nodes that control the flow of decision-making. BTs are read from the root down to the leaves, and they determine which action an agent should take.

The tree is composed of different types of nodes:
*   **Composite Nodes (Selector, Sequence):** Control the flow of logic. A `Selector` (Fallback) tries each child in order until one succeeds. A `Sequence` tries each child in order until one fails.
*   **Decorator Nodes:** Modify the behavior of a child node (e.g., `Inverter`, `Succeeder`).
*   **Leaf Nodes (Action, Condition):** Perform an action (e.g., `MoveToTarget`) or check a condition (e.g., `IsEnemyVisible?`).

**Application for Colony Simulation:**
A colonist's BT could have a high-level `Selector` at the root:
1.  **Emergency Response:** Is there an immediate threat? (e.g., fire, attack) -> Run away.
2.  **Manage Needs:** Are needs critical? (e.g., starving, exhausted) -> Go eat or sleep.
3.  **Fulfill Job:** Is there an assigned task? -> Go perform the task.
4.  **Idle:** If all else fails -> Wander around.

Each of these would be its own branch with more detailed sequences and actions.

**Advantages:**
*   **Modularity & Reusability:** BTs are highly modular. You can create a subtree for "eating" and reuse it for every colonist.
*   **Scalability:** They scale much better than FSMs. Adding new behaviors is as simple as adding a new branch to the tree, often without touching existing logic.
*   **Readability:** A well-structured BT can be easy for designers to understand and modify, as it reads like a list of priorities.

**Disadvantages:**
*   **Complexity:** More complex to implement the core BT system compared to a simple FSM.
*   **Overhead:** Can have slightly more performance overhead than an FSM, though this is usually negligible in modern engines.

**Recommendation:**
Behavior Trees are the industry standard for complex AI in games like RimWorld and are highly recommended for our project. Their scalability and modularity are essential for managing colonists with diverse jobs, needs, and responses to the environment.

---

## Conclusion

While FSMs are simple and fast, they do not scale well for the complex, multi-layered behaviors required by colonists in a simulation game.

**The final recommendation is to implement a Behavior Tree system.** This will provide the flexibility and scalability needed to create emergent, believable agent behavior as the project grows in complexity. We can start with a basic implementation and add new branches and behaviors as new features are developed.