# Multithreading and Asynchronous Processing in Godot

This document provides a guide to using multithreading and asynchronous processing in Godot for performance optimization, especially in the context of our large-scale Cyberpunk Colony Simulation. It expands on the concepts mentioned in `docs/optimization_strategy.md`.

## 1. Introduction to Multithreading

By default, all game logic runs on a single main thread. For a large-scale simulation, heavy computations like AI, pathfinding, or procedural generation can block this thread, causing the game to freeze or stutter. Multithreading allows us to offload these intensive tasks to other CPU cores, keeping the main thread free for rendering and player input, resulting in a smoother experience.

Godot provides several tools to manage threads. The primary ones are:

-   **Thread:** The basic object for creating and managing threads.
-   **Mutex:** A synchronization primitive used to protect data from being accessed by multiple threads simultaneously, preventing race conditions.
-   **Semaphore:** A synchronization primitive used to control access to a shared resource or to signal between threads.

**Important Warning:** Godot's API is **not entirely thread-safe**. Accessing nodes in the `SceneTree` (e.g., `get_node`, `add_child`) or most servers (e.g., `RenderingServer`, `PhysicsServer`) from a separate thread can lead to crashes or data corruption. Refer to the official [Thread-safe APIs documentation](https://docs.godotengine.org/en/stable/tutorials/performance/thread_safe_apis.html) for a complete list of what is safe.

## 2. Core Threading Components

### 2.1. Thread

The `Thread` class is used to execute a function in a separate thread.

**Creating a Thread:**

```gdscript
var my_thread: Thread

func _ready():
    my_thread = Thread.new()
    # Start the thread, executing the _heavy_task function
    # You can bind arguments to the function if needed
    my_thread.start(_heavy_task.bind("Some Data"))

func _heavy_task(user_data):
    print("This runs in a separate thread. Data: ", user_data)
    # Perform heavy computation here...

func _exit_tree():
    # It's crucial to wait for the thread to finish before the game exits.
    if my_thread:
        my_thread.wait_to_finish()
```

### 2.2. Mutex (Mutual Exclusion)

A `Mutex` is essential for protecting data that is shared between threads. It ensures that only one thread can access the data at a time.

**Using a Mutex:**

```gdscript
var shared_data := 0
var mutex: Mutex

func _ready():
    mutex = Mutex.new()
    var thread1 = Thread.new()
    var thread2 = Thread.new()
    thread1.start(_increment_shared_data)
    thread2.start(_increment_shared_data)

    # Wait for both threads to complete
    thread1.wait_to_finish()
    thread2.wait_to_finish()
    print("Final shared_data value: ", shared_data) # Expected: 200000

func _increment_shared_data():
    for i in 100000:
        mutex.lock()
        shared_data += 1
        mutex.unlock()
```
Without the `mutex.lock()` and `mutex.unlock()` calls, the final value would be unpredictable due to the race condition.

### 2.3. Semaphore

A `Semaphore` is useful when you want a thread to wait for a signal before proceeding. For example, a worker thread that processes jobs as they become available.

**Using a Semaphore:**

```gdscript
var jobs = []
var jobs_mutex: Mutex
var jobs_semaphore: Semaphore
var worker_thread: Thread
var should_exit := false

func _ready():
    jobs_mutex = Mutex.new()
    jobs_semaphore = Semaphore.new()
    worker_thread = Thread.new()
    worker_thread.start(_job_processor)

func _job_processor():
    while true:
        # Wait until the semaphore is posted (a new job is available)
        jobs_semaphore.wait()

        jobs_mutex.lock()
        if should_exit:
            jobs_mutex.unlock()
            break

        var job = jobs.pop_front()
        jobs_mutex.unlock()

        if job:
            # Process the job
            print("Processing job: ", job)

func add_job(new_job):
    jobs_mutex.lock()
    jobs.push_back(new_job)
    jobs_mutex.unlock()
    # Signal the worker thread that there is a new job
    jobs_semaphore.post()

func _exit_tree():
    jobs_mutex.lock()
    should_exit = true
    jobs_mutex.unlock()
    # Post one last time to unblock the thread so it can exit
    jobs_semaphore.post()
    worker_thread.wait_to_finish()
```

## 3. Practical Applications for Our Project

### 3.1. Asynchronous World Generation (Chunking)

As outlined in our optimization strategy, the game world will be divided into chunks. We can use threads to generate the geometry and data for new chunks in the background without freezing the game.

**Conceptual Workflow:**

1.  **Main Thread:** Detects that the player is approaching an unloaded area.
2.  **Main Thread:** Creates a new thread (or signals a worker thread) and passes it the coordinates of the chunk to be generated.
3.  **Worker Thread:**
    -   Generates noise maps for population, resources, etc.
    -   Runs the L-System and Turtle to create the road network data.
    -   Runs Wave Function Collapse for building placement.
    -   **Important:** The thread should only generate *data* (arrays of positions, tile types, etc.), not Godot nodes.
4.  **Worker Thread:** Once the data is ready, it can use `Callable.call_deferred()` to signal the main thread that the chunk data is complete.
5.  **Main Thread:** Receives the signal and the generated data. It then instantiates the necessary nodes (`MeshInstance3D`, `RoadDrawer`, etc.) and adds them to the `SceneTree`.

### 3.2. Offloading Agent AI

With hundreds of agents, running AI logic for all of them every frame on the main thread is not feasible. We can use a combination of throttling (updating distant agents less frequently) and multithreading.

**Conceptual Workflow:**

1.  **Agent Manager (Main Thread):** Maintains a list of all agents.
2.  **Agent Manager (Main Thread):** Each frame (or every few frames), it identifies a batch of agents that need their AI updated.
3.  **Agent Manager (Main Thread):** It could use a pool of worker threads. For each worker, it assigns a subset of agents.
4.  **Worker Threads:**
    -   For each assigned agent, run the Behavior Tree or other AI logic.
    -   Perform pathfinding calculations.
    -   The result of the AI tick should be a simple state change (e.g., "moving to X,Y", "performing action Z").
5.  **Main Thread:** After the worker threads are done, the Agent Manager updates the agent's state. Any actions that must be done on the main thread (like playing an animation or moving a `CharacterBody3D`) are executed here.

## 4. Asynchronous Loading

For loading assets like textures, models, or scenes from disk without blocking the main thread, Godot provides the `ResourceLoader` singleton.

```gdscript
func _load_resource_in_background(path):
    ResourceLoader.load_threaded_request(path)
    # The resource is now loading in the background.
    # We can check its status.

func _check_load_status(path):
    var status = ResourceLoader.load_threaded_get_status(path)
    if status == ResourceLoader.THREAD_LOAD_IN_PROGRESS:
        var progress = ResourceLoader.load_threaded_get_progress(path)
        print("Loading... ", progress * 100, "%")
    elif status == ResourceLoader.THREAD_LOAD_LOADED:
        var resource = ResourceLoader.load_threaded_get(path)
        # Now we can use the loaded resource
        get_node("MySprite").texture = resource
    elif status == ResourceLoader.THREAD_LOAD_FAILED:
        print("Failed to load resource!")
```

This is particularly useful for loading new chunks or large assets as the player explores the world.

## 5. Visual (GPU) Optimization

In addition to CPU-bound tasks, GPU performance is critical for large-scale simulations. The following strategies, summarized from `docs/performance_optimization.md` and `docs/optimization_strategy.md`, should be employed.

### 5.1. Instancing with MultiMeshInstance3D

-   **Problem:** Rendering thousands of individual objects (like colonists, trees, or buildings) creates a massive number of draw calls, which is a major GPU bottleneck.
-   **Solution:** Use `MultiMeshInstance3D` to draw many instances of the same mesh with a single draw call. This is the most important optimization for scenes with large numbers of repeated objects.
-   **Implementation:** A central manager should update the transforms (position, rotation, scale) of each instance within the `MultiMesh`. Agent logic should be decoupled from rendering; the agent's state updates the `MultiMesh` buffer, not a `Node3D` transform.

### 5.2. Culling

-   **Occlusion Culling:** Use `OccluderInstance3D` nodes to prevent rendering objects that are hidden behind other large, static objects (like buildings).
-   **Visibility Ranges (HLOD/LOD):** Use the `visibility_range_*` properties on `Node3D` nodes to hide them when they are far from the camera. This is a simple but highly effective form of Level of Detail (LOD).

### 5.3. Baked Lighting

-   For static geometry, pre-calculate lighting using `LightmapGI`. This removes the expensive real-time lighting calculations for the majority of the environment, significantly improving performance. Dynamic objects can then use Light Probes to receive indirect lighting.

## 6. Conclusion & Recommendations

-   **Use Threads for Data Processing:** The safest and most effective way to use threads in Godot is to offload data processing, not scene manipulation. Generate data in a thread, then use `call_deferred` to apply it on the main thread.
-   **Protect Shared Data with Mutexes:** Any variable accessed from more than one thread must be protected by a `Mutex`.
-   **Use Semaphores for Worker Pools:** For recurring tasks like AI updates, a pool of worker threads waiting on a `Semaphore` is an efficient pattern.
-   **Leverage `ResourceLoader` for Assets:** For loading files from disk, always prefer the built-in `ResourceLoader`'s threaded API over manual file access in a thread.
-   **Combine CPU and GPU Strategies:** A holistic approach is required. Use multithreading to handle complex calculations and GPU optimization techniques like `MultiMesh` and culling to render the results efficiently.