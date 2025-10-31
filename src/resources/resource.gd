# src/resources/resource.gd
class_name Resource
extends RefCounted

var name: String
var amount: int

func _init(p_name: String, p_amount: int) -> void:
	name = p_name
	amount = p_amount

func to_string() -> String:
	return "%s: %d" % [name, amount]