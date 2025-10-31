# src/resources/resource_manager.gd
extends Node

const Resource_class = preload("res://src/resources/resource.gd")

var resources: Dictionary = {
	"energy": Resource_class.new("Energy", 1000),
	"materials": Resource_class.new("Materials", 500)
}

func add_resource(p_name: String, p_amount: int) -> void:
	if resources.has(p_name.to_lower()):
		resources[p_name.to_lower()].amount += p_amount
	else:
		print("Resource type '%s' does not exist." % p_name)

func remove_resource(p_name: String, p_amount: int) -> bool:
	if resources.has(p_name.to_lower()):
		var res: Resource = resources[p_name.to_lower()]
		if res.amount >= p_amount:
			res.amount -= p_amount
			return true
		else:
			print("Not enough %s. Required: %d, Available: %d" % [p_name, p_amount, res.amount])
			return false
	else:
		print("Resource type '%s' does not exist." % p_name)
		return false

func get_resource(p_name: String) -> Resource:
	if resources.has(p_name.to_lower()):
		return resources[p_name.to_lower()]
	return null

func get_all_resources() -> Dictionary:
	return resources