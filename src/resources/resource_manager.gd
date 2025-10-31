# src/resources/resource_manager.gd
extends Node

signal resource_changed(resource_name, new_amount)

var resources: Dictionary = {
	"energy": 1000,
	"materials": 500
}

func get_resource_amount(resource_name: String) -> int:
	if resources.has(resource_name):
		return resources[resource_name]
	else:
		return 0

func add_resource(resource_name: String, amount: int):
	if resources.has(resource_name):
		resources[resource_name] += amount
		emit_signal("resource_changed", resource_name, resources[resource_name])

func remove_resource(resource_name: String, amount: int) -> bool:
	if resources.has(resource_name) and resources[resource_name] >= amount:
		resources[resource_name] -= amount
		emit_signal("resource_changed", resource_name, resources[resource_name])
		return true
	else:
		return false