class_name LSystem
extends RefCounted

var rules: Dictionary = {}
var axiom: String = ""

func _init(axiom: String, rules: Dictionary):
	self.axiom = axiom
	self.rules = rules

func generate(iterations: int) -> String:
	var current_string: String = axiom
	for i in range(iterations):
		var next_string: String = ""
		for char in current_string:
			if rules.has(char):
				next_string += rules[char]
			else:
				next_string += char
		current_string = next_string
	return current_string