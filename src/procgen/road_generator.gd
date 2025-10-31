# src/procgen/road_generator.gd
class_name RoadGenerator
extends Node2D

var lsystem: LSystem
var start_pos: Vector2 = Vector2(500, 500)
var length: float = 100.0
var delta_angle: float = 90.0

func _ready():
	var rules = {"F": "F+F-F-F+F"}
	lsystem = LSystem.new("F", rules)
	var lsystem_string = lsystem.generate(3)
	draw_turtle(lsystem_string)

func draw_turtle(lsystem_string: String):
	var current_pos = start_pos
	var current_angle = 0.0
	var pos_stack = []
	var angle_stack = []

	for char in lsystem_string:
		match char:
			"F":
				var new_pos = current_pos + Vector2(length, 0).rotated(deg_to_rad(current_angle))
				var line = Line2D.new()
				line.add_point(current_pos)
				line.add_point(new_pos)
				line.width = 5
				add_child(line)
				current_pos = new_pos
			"+":
				current_angle += delta_angle
			"-":
				current_angle -= delta_angle
			"[":
				pos_stack.push_back(current_pos)
				angle_stack.push_back(current_angle)
			"]":
				current_pos = pos_stack.pop_back()
				current_angle = angle_stack.pop_back()
