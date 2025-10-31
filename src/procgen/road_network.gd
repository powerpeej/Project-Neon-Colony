# src/procgen/road_network.gd
class_name RoadNetwork
extends RefCounted

# Using a Dictionary to store the grid for sparse data representation.
# Key: Vector2i (coordinates), Value: RoadSegment
var grid: Dictionary = {}
var tile_size: int = 64 # Default tile size, can be configured

# A simple inner class to represent a road segment
class RoadSegment:
	var position: Vector2i

	func _init(pos: Vector2i):
		self.position = pos

func _init(tile_size: int = 64):
	self.tile_size = tile_size

func add_road(pos: Vector2i):
	if !grid.has(pos):
		grid[pos] = RoadSegment.new(pos)

func get_road(pos: Vector2i):
	return grid.get(pos, null)

func world_to_grid(world_pos: Vector2) -> Vector2i:
	return Vector2i(
		int(snapped(world_pos.x / tile_size, 1)),
		int(snapped(world_pos.y / tile_size, 1))
	)

func grid_to_world(grid_pos: Vector2i) -> Vector2:
	return Vector2(grid_pos.x * tile_size, grid_pos.y * tile_size)

func get_neighbors(pos: Vector2i) -> Array[RoadSegment]:
	var neighbors: Array[RoadSegment] = []
	var directions = [
		Vector2i.UP,
		Vector2i.DOWN,
		Vector2i.LEFT,
		Vector2i.RIGHT
	]
	for dir in directions:
		var neighbor_pos = pos + dir
		var neighbor_road = get_road(neighbor_pos)
		if neighbor_road:
			neighbors.append(neighbor_road)
	return neighbors