# AI Systems Research: FSMs vs. Behavior Trees

## 1. Finite State Machines (FSMs)

### Concept
A Finite State Machine is a model of computation based on a hypothetical machine that can be in only one of a finite number of states at any given time. The machine can transition from one state to another in response to some external inputs; the change from one state to another is called a transition.

In game development, an FSM is a common pattern for structuring AI. An agent's behavior is broken down into a set of distinct states (e.g., "Idle", "Patrolling", "Attacking", "Fleeing"). The agent can only be in one state at a time, and transitions between states are triggered by game events or conditions.

### Application
FSMs are well-suited for simple AI with a limited and clearly defined set of behaviors. For example:
- A simple enemy that cycles between patrolling and attacking the player.
- A door that can be "Open" or "Closed".
- UI elements that have different states (e.g., a button that is "Normal", "Hovered", "Pressed").

### Advantages
- **Simplicity:** FSMs are easy to understand, implement, and debug for simple scenarios.
- **Efficiency:** They are computationally lightweight and have a low performance overhead.
- **Rigidity:** The strict state-based structure makes behavior predictable and easy to reason about.

### Disadvantages
- **Scalability:** FSMs become difficult to manage as the number of states and transitions grows. The connections between states can become a tangled "spaghetti" of logic, making it hard to add new behaviors or debug existing ones.
- **Reusability:** States are often tightly coupled to a specific agent's logic, making them difficult to reuse for different types of agents.
- **Concurrency:** FSMs inherently represent a single state of being, making it difficult to model behaviors that should run in parallel (e.g., an agent that needs to talk while walking).

## 2. Behavior Trees (BTs)

### Concept
A Behavior Tree is a hierarchical model for representing and executing complex AI behaviors. It is a tree of nodes that controls the flow of decision-making. Unlike FSMs, where the state itself contains the logic, a BT is "ticked" on each frame, and the tree is traversed from the root down to determine which action to perform.

The tree is composed of different types of nodes:
- **Composite Nodes:** Control the flow of execution of their children (e.g., `Sequence`, `Selector`/`Fallback`, `Parallel`).
- **Decorator Nodes:** Modify the behavior of a child node (e.g., `Inverter`, `Succeeder`).
- **Leaf Nodes:** Represent the actual actions or conditions (e.g., `MoveToTarget`, `IsHealthLow`).

### Application
BTs excel at creating complex, layered, and reactive AI. They are a standard in modern game development for creating sophisticated NPCs and enemies. For a colony simulation game, BTs can model a wide range of colonist behaviors:
- A colonist's daily routine: `Sequence`("Wake Up", "Go to Work", "Eat", "Sleep").
- A colonist's reaction to danger: `Selector`("Fight", "Flee").
- A colonist performing multiple actions: `Parallel`("Walk", "Carry Resource").

### Advantages
- **Modularity & Reusability:** Behaviors are broken down into small, independent nodes that can be easily reused and rearranged to create new behaviors.
- **Scalability:** The hierarchical nature makes it easy to add new behaviors without modifying existing logic. You can simply add new branches to the tree.
- **Readability:** A well-structured BT can be very readable, even for non-programmers, as it visually represents the decision-making logic.
- **Reactivity:** BTs are evaluated every tick, allowing them to react to changes in the game world instantly.

### Disadvantages
- **Complexity:** BTs have a steeper learning curve than FSMs.
- **Overhead:** There can be a slight performance overhead due to traversing the tree each frame, though this is generally negligible in modern engines.

## 3. Recommendation

For the "Cyberpunk Colony Sim" project, **Behavior Trees are the recommended system for agent AI.**

The nature of a colony simulation game requires agents (colonists) to handle a wide array of complex, layered, and often concurrent behaviors. A colonist needs to make decisions based on their needs (hunger, sleep), their job (mining, building), their environment (danger, available resources), and their social interactions.

Attempting to model this complexity with a Finite State Machine would quickly lead to an unmanageable number of states and transitions. For example, an "Attacking" state would need transitions to "Fleeing", "Eating", "Sleeping", etc., and the logic to decide between these would become incredibly complex.

Behavior Trees are designed for this exact problem. We can create a root `Selector` node for a colonist that chooses between high-level behaviors like "Work", "Rest", or "Emergency". Each of these would be its own subtree, composed of reusable, modular actions. This approach is far more scalable and maintainable in the long run, which is crucial for a project of this scope. While there is an initial investment in setting up the BT framework, the benefits in terms of modularity and scalability will be invaluable as the game's complexity grows.