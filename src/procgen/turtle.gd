# src/procgen/turtle.gd
class_name Turtle
extends RefCounted

var tile_size: int
var road_network: RoadNetwork

func _init(road_network: RoadNetwork, tile_size: int):
	self.road_network = road_network
	self.tile_size = tile_size

func interpret(lsystem_string: String):
	var current_pos := Vector2.ZERO
	var current_angle: float = -90.0 # Start facing up
	var delta_angle: float = 90.0
	var step_length: float = tile_size

	var pos_stack = []
	var angle_stack = []

	var current_grid_pos = road_network.world_to_grid(current_pos)
	road_network.add_road(current_grid_pos)

	for char in lsystem_string:
		match char:
			"F":
				var direction_vector = Vector2.RIGHT.rotated(deg_to_rad(current_angle))
				var new_pos = current_pos + direction_vector * step_length

				var start_grid_pos = road_network.world_to_grid(current_pos)
				var end_grid_pos = road_network.world_to_grid(new_pos)

				var line_points = _bresenham_line(start_grid_pos, end_grid_pos)
				for point in line_points:
					road_network.add_road(point)

				current_pos = new_pos

			"+":
				current_angle += delta_angle
			"-":
				current_angle -= delta_angle
			"[":
				pos_stack.push_back(current_pos)
				angle_stack.push_back(current_angle)
			"]":
				if pos_stack.size() > 0:
					current_pos = pos_stack.pop_back()
					current_angle = angle_stack.pop_back()

# Bresenham's line algorithm to get all grid cells between two points
func _bresenham_line(start: Vector2i, end: Vector2i) -> Array[Vector2i]:
	var points: Array[Vector2i] = []
	var x0 = start.x
	var y0 = start.y
	var x1 = end.x
	var y1 = end.y

	var dx = abs(x1 - x0)
	var dy = -abs(y1 - y0)
	var sx = 1 if x0 < x1 else -1
	var sy = 1 if y0 < y1 else -1
	var err = dx + dy

	while true:
		points.append(Vector2i(x0, y0))
		if x0 == x1 and y0 == y1:
			break
		var e2 = 2 * err
		if e2 >= dy:
			err += dy
			x0 += sx
		if e2 <= dx:
			err += dx
			y0 += sy

	return points