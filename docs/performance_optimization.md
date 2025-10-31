# Performance Optimization Guide

This document provides a summary of performance optimization techniques for large-scale simulations in Godot, based on the official documentation.

## 1. General Principles

The foundation of optimization is identifying and addressing bottlenecks. Avoid premature optimization; instead, focus on a data-driven approach.

### 1.1. Measuring Performance

- **Use Profilers:** Godot provides built-in profilers to measure performance. The profiler can be accessed from the **Debugger** panel at the bottom of the editor. It provides detailed information on frame times, function call durations, and resource usage.
- **Identify Bottlenecks:** Performance issues typically fall into two categories:
    - **CPU-bound:** The CPU is the limiting factor. This often manifests as high script execution times or physics calculations.
    - **GPU-bound:** The GPU is the limiting factor. This is usually related to rendering, such as complex shaders, high poly counts, or excessive draw calls.

### 1.2. Key Principles

- **Focus on Critical Areas:** As Donald Knuth said, "premature optimization is the root of all evil." Focus on optimizing the parts of your code that are causing the most significant performance issues.
- **Iterative Process:** Optimization is an iterative process of identifying a bottleneck, applying an optimization, and measuring the result.

## 2. Visual Optimization (GPU)

For large-scale simulations, rendering is often a primary bottleneck. These techniques can help reduce the load on the GPU.

### 2.1. Culling

- **Frustum Culling:** Godot automatically performs frustum culling, which prevents rendering objects outside the camera's view.
- **Occlusion Culling:** For scenes where objects are hidden behind other objects (e.g., buildings in a city), occlusion culling can significantly reduce the number of objects rendered. Set up `OccluderInstance3D` nodes to prevent rendering of objects that are not visible to the camera.
- **Visibility Ranges (HLOD):** Use the `visibility_range_*` properties on `Node3D` nodes to hide them when they are far from the camera. This is a form of manual Level of Detail (LOD) and is very effective for managing large numbers of objects.

### 2.2. Level of Detail (LOD)

- **Mesh LOD:** Automatically generate lower-polygon versions of meshes that are displayed at a distance. This can be configured in the import settings for a mesh.
- **Billboards and Impostors:** For very distant objects, consider replacing them with simple billboards (2D images) or impostors (pre-rendered images of the object from different angles).

### 2.3. Instancing

- **Automatic Instancing:** The Forward+ renderer will automatically instance `MeshInstance3D` nodes that share the same mesh and material. This is a powerful feature for reducing draw calls.
- **MultiMeshInstance3D:** For drawing thousands of identical objects (e.g., trees, grass, crowds), use `MultiMeshInstance3D`. This node is highly optimized for this purpose and can render massive numbers of objects with minimal performance impact.

### 2.4. Lighting

- **Baked Lighting:** For static environments, baking lighting into lightmaps (`LightmapGI`) is a highly effective optimization. This pre-calculates lighting, removing the need for expensive real-time calculations.
- **Light Modes:** Set the `Bake Mode` of lights to `Static` for lights that do not need to change at runtime. This will further reduce the cost of lighting.

## 3. CPU Optimization

### 3.1. Animation

- **Animation Rate:** Reduce the animation rate for distant or occluded characters. The `VisibleOnScreenEnabler3D` and `VisibleOnScreenNotifier3D` nodes can be used to pause animations entirely when an object is not visible.
- **Skinning:** The process of deforming a mesh with a skeleton (skinning) can be CPU-intensive. Keep poly counts reasonable for animated characters.

### 3.2. Large Worlds

- **Floating Point Precision:** In very large worlds, floating-point precision issues can cause visual and physics glitches. To resolve this, enable **Use LFW** (Large Float World) in the project settings. This uses 64-bit floats for transforms and physics, but comes with a performance cost.
- **World Partitioning:** For extremely large worlds, consider breaking the world into smaller, manageable chunks that can be loaded and unloaded as the player moves through the environment.

## 4. Further Reading

For more detailed information, refer to the official Godot documentation:

- [General optimization tips](https://docs.godotengine.org/en/stable/tutorials/performance/general_optimization.html)
- [Optimizing 3D performance](https://docs.godotengine.org/en/stable/tutorials/performance/optimizing_3d_performance.html)
- [Using MultiMeshInstance3D](https://docs.godotengine.org/en/stable/tutorials/3d/using_multi_mesh_instance.html)
- [Using LightmapGI](https://docs.godotengine.org/en/stable/tutorials/3d/global_illumination/using_lightmap_gi.html)
- [Occlusion culling](https://docs.godotengine.org/en/stable/tutorials/3d/occlusion_culling.html)