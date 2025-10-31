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
const RoadDrawer = preload("res://src/procgen/road_drawer.gd")

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
	var tile_map = get_node_or_null("RoadTileMap") as TileMap
	if not tile_map:
		tile_map = TileMap.new()
		tile_map.name = "RoadTileMap"
		add_child(tile_map)

	var drawer = RoadDrawer.new(road_network, tile_map)
	drawer.draw_tiles()

func _generate_lsystem_string() -> String:
	lsystem = LSystem.new(axiom, rules)
	return lsystem.generate(iterations)