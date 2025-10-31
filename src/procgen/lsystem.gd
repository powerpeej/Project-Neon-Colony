class_name LSystem
extends RefCounted

var rules: Dictionary = {}
var axiom: String = ""
var rng = RandomNumberGenerator.new()

func _init(axiom: String, rules: Dictionary):
	self.axiom = axiom
	self.rules = rules
	rng.randomize()

func generate(iterations: int) -> String:
	var current_string: String = axiom
	for i in range(iterations):
		var next_string: String = ""
		for char in current_string:
			if rules.has(char):
				next_string += get_successor(char)
			else:
				next_string += char
		current_string = next_string
	return current_string


func get_successor(predecessor: String) -> String:
	var possible_successors = rules.get(predecessor, null)

	if possible_successors == null:
		return ""

	if typeof(possible_successors) == TYPE_STRING:
		return possible_successors

	var total_weight: float = 0.0
	for rule in possible_successors:
		total_weight += float(rule.get("weight", 1.0))

	if total_weight <= 0.0:
		return ""

	var random_value: float = rng.randf_range(0.0, total_weight)
	var cumulative_weight: float = 0.0

	for rule in possible_successors:
		cumulative_weight += float(rule.get("weight", 1.0))
		if random_value <= cumulative_weight:
			return rule.get("successor", "")

	# Fallback in case of rounding errors or empty rules
	return ""
