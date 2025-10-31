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

const Turtle = preload("res://src/procgen/turtle.gd")

var lsystem: LSystem
var road_network: RoadNetwork

func _ready():
	generate_and_draw()

func generate_and_draw():
	# 1. Setup
	road_network = RoadNetwork.new(tile_size)

	# 2. Generate L-System String
	var lsystem_string = _generate_lsystem_string()

	# 3. Populate Road Network
	var turtle = Turtle.new(road_network, tile_size)
	turtle.interpret(lsystem_string)

	# 4. Instantiate Tiles
	draw_tiles()

func _generate_lsystem_string() -> String:
	lsystem = LSystem.new(axiom, rules)
	return lsystem.generate(iterations)

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