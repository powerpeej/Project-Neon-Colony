# src/resources/resource_manager.gd
extends Node
signal resource_changed(resource_name, new_amount)

const Resource_class = preload("res://src/resources/resource.gd")

var resources: Dictionary = {
	"energy": Resource_class.new("Energy", 1000),
	"materials": Resource_class.new("Materials", 500)
}

func get_resource(resource_name: String) -> Resource:
	var key = resource_name.to_lower()
	if resources.has(key):
		return resources[key]
	return null

func get_resource_amount(resource_name: String) -> int:
	var res: Resource = get_resource(resource_name)
	return res.amount if res != null else 0

func get_all_resources() -> Dictionary:
	return resources

func add_resource(resource_name: String, amount: int) -> void:
	var key = resource_name.to_lower()
	if resources.has(key):
		var res: Resource = resources[key]
		res.amount += amount
		emit_signal("resource_changed", key, res.amount)
	else:
		# create a new Resource entry if it doesn't exist
		resources[key] = Resource_class.new(resource_name.capitalize(), amount)
		emit_signal("resource_changed", key, amount)

func remove_resource(resource_name: String, amount: int) -> bool:
	var key = resource_name.to_lower()
	if resources.has(key):
		var res: Resource = resources[key]
		if res.amount >= amount:
			res.amount -= amount
			emit_signal("resource_changed", key, res.amount)
			return true
		else:
			print("Not enough %s. Required: %d, Available: %d" % [resource_name, amount, res.amount])
			return false
	else:
		print("Resource type '%s' does not exist." % resource_name)
		return false
