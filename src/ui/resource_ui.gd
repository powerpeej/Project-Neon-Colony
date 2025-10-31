extends Control

@onready var energy_label: Label = %EnergyLabel
@onready var materials_label: Label = %MaterialsLabel

func _ready() -> void:
	if not ResourceManager:
		push_warning("ResourceManager not found. UI will not update.")
		return

	ResourceManager.resource_changed.connect(_on_resource_changed)
	_update_labels()


func _on_resource_changed(_resource_name: String, _new_value: int) -> void:
	_update_labels()


func _update_labels() -> void:
	if not ResourceManager:
		return
	energy_label.text = str(ResourceManager.get_resource_amount("energy"))
	materials_label.text = str(ResourceManager.get_resource_amount("materials"))