# src/procgen/road_generator.gd
class_name RoadGenerator
extends Node2D

@export var iterations: int = 3
@export var tile_size: int = 64
@export var axiom: String = "X"
@export var rules: Dictionary = {
	"X": [
		{"successor": "F[+X]F[-X]+X", "weight": 0.7},
		{"successor": "F[-X]F[+X]-X", "weight": 0.3}
	],
	"F": [
		{"successor": "FF", "weight": 0.8},
		{"successor": "F", "weight": 0.2}
	]
}

var lsystem: LSystem
var road_network: RoadNetwork

func _ready():
	generate_and_draw()

func generate_and_draw():
	# 1. Setup
	lsystem = LSystem.new(axiom, rules)
	road_network = RoadNetwork.new(tile_size)

	# 2. Generate L-System String
	var lsystem_string = lsystem.generate(iterations)

	# 3. Populate Road Network
	populate_road_network(lsystem_string)

	# 4. Instantiate Tiles
	draw_tiles()

func draw_tiles():
	# Preload road textures
	var road_tiles = {
		"end_up": load("res://art/tiles/roads/road_end.svg"),
		"end_down": load("res://art/tiles/roads/road_end.svg"),
		"end_left": load("res://art/tiles/roads/road_end.svg"),
		"end_right": load("res://art/tiles/roads/road_end.svg"),
		"straight_v": load("res://art/tiles/roads/road_straight.svg"),
		"straight_h": load("res://art/tiles/roads/road_straight.svg"),
		"corner_tl": load("res://art/tiles/roads/road_corner.svg"),
		"corner_tr": load("res://art/tiles/roads/road_corner.svg"),
		"corner_bl": load("res://art/tiles/roads/road_corner.svg"),
		"corner_br": load("res://art/tiles/roads/road_corner.svg"),
		"t_up": load("res://art/tiles/roads/road_t_junction.svg"),
		"t_down": load("res://art/tiles/roads/road_t_junction.svg"),
		"t_left": load("res://art/tiles/roads/road_t_junction.svg"),
		"t_right": load("res://art/tiles/roads/road_t_junction.svg"),
		"cross": load("res://art/tiles/roads/road_cross.svg")
	}

	for pos in road_network.grid.keys():
		var up = road_network.get_road(pos + Vector2i.UP) != null
		var down = road_network.get_road(pos + Vector2i.DOWN) != null
		var left = road_network.get_road(pos + Vector2i.LEFT) != null
		var right = road_network.get_road(pos + Vector2i.RIGHT) != null

		var tile_key = get_tile_key(up, down, left, right)
		if tile_key:
			var sprite = Sprite2D.new()
			sprite.texture = road_tiles[tile_key]
			sprite.position = road_network.grid_to_world(pos) + Vector2(tile_size / 2, tile_size / 2)

			# Apply rotations for different tile variations
			match tile_key:
				"end_up": sprite.rotation_degrees = -90
				"end_down": sprite.rotation_degrees = 90
				"end_left": sprite.rotation_degrees = 180
				"straight_v": sprite.rotation_degrees = 90
				"corner_tr": sprite.rotation_degrees = 90
				"corner_br": sprite.rotation_degrees = 180
				"corner_bl": sprite.rotation_degrees = -90
				"t_up": sprite.rotation_degrees = -90
				"t_left": sprite.rotation_degrees = 180
				"t_down": sprite.rotation_degrees = 90

			add_child(sprite)

func get_tile_key(up: bool, down: bool, left: bool, right: bool) -> String:
	var neighbor_count = int(up) + int(down) + int(left) + int(right)

	match neighbor_count:
		1: # End caps
			if up: return "end_down"
			if down: return "end_up"
			if left: return "end_right"
			if right: return "end_left"
		2: # Straights or corners
			if up and down: return "straight_v"
			if left and right: return "straight_h"
			if down and right: return "corner_tl"
			if down and left: return "corner_tr"
			if up and right: return "corner_bl"
			if up and left: return "corner_br"
		3: # T-junctions
			if !up: return "t_down"
			if !down: return "t_up"
			if !left: return "t_right"
			if !right: return "t_left"
		4: # Cross-section
			return "cross"

	return "" # No tile for isolated road segment

func populate_road_network(lsystem_string: String):
	var current_pos := Vector2.ZERO
	var current_angle: float = -90.0 # Start facing up
	var delta_angle: float = 22.5
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

				# Add road segments along the path
				var start_grid_pos = road_network.world_to_grid(current_pos)
				var end_grid_pos = road_network.world_to_grid(new_pos)

				# A simple line drawing algorithm for the grid
				var line_points = bresenham_line(start_grid_pos, end_grid_pos)
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
func bresenham_line(start: Vector2i, end: Vector2i) -> Array[Vector2i]:
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