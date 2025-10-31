# src/procgen/road_drawer.gd
class_name RoadDrawer
extends RefCounted

var road_network: RoadNetwork
var tile_map: TileMap

const TILE_STRAIGHT = Vector2i(0, 0)
const TILE_CORNER = Vector2i(0, 0)
const TILE_T_JUNCTION = Vector2i(0, 0)
const TILE_CROSS = Vector2i(0, 0)
const TILE_END = Vector2i(0, 0)

const SOURCE_STRAIGHT = 0
const SOURCE_CORNER = 1
const SOURCE_T_JUNCTION = 2
const SOURCE_CROSS = 3
const SOURCE_END = 4

func _init(road_network: RoadNetwork, tile_map: TileMap):
	self.road_network = road_network
	self.tile_map = tile_map

func draw_tiles():
	if not tile_map:
		printerr("RoadDrawer: TileMap not set!")
		return

	var tileset = load("res://scenes/tiles/road_tileset.tres") as TileSet
	if not tileset:
		printerr("RoadDrawer: Failed to load TileSet resource.")
		return

	tile_map.tile_set = tileset

	for pos in road_network.grid.keys():
		var up = road_network.get_road(pos + Vector2i.UP) != null
		var down = road_network.get_road(pos + Vector2i.DOWN) != null
		var left = road_network.get_road(pos + Vector2i.LEFT) != null
		var right = road_network.get_road(pos + Vector2i.RIGHT) != null

		var result = get_tile_info(up, down, left, right)
		if result:
			tile_map.set_cell(0, pos, result.source_id, result.atlas_coords, result.alternative_tile)

func get_tile_info(up: bool, down: bool, left: bool, right: bool) -> Dictionary:
	var neighbor_count = int(up) + int(down) + int(left) + int(right)

	match neighbor_count:
		1: # End caps
			var alternative_tile = 0
			if up: alternative_tile = 1 # Rotated 90 degrees
			if down: alternative_tile = 3 # Rotated -90 degrees
			if left: alternative_tile = 2 # Rotated 180 degrees
			return { "source_id": SOURCE_END, "atlas_coords": TILE_END, "alternative_tile": alternative_tile }
		2: # Straights or corners
			if up and down:
				return { "source_id": SOURCE_STRAIGHT, "atlas_coords": TILE_STRAIGHT, "alternative_tile": 1 } # Vertical
			if left and right:
				return { "source_id": SOURCE_STRAIGHT, "atlas_coords": TILE_STRAIGHT, "alternative_tile": 0 } # Horizontal

			var alternative_tile = 0
			if down and right: alternative_tile = 0 # TL
			if down and left: alternative_tile = 1 # TR
			if up and right: alternative_tile = 3 # BL
			if up and left: alternative_tile = 2 # BR
			return { "source_id": SOURCE_CORNER, "atlas_coords": TILE_CORNER, "alternative_tile": alternative_tile }
		3: # T-junctions
			var alternative_tile = 0
			if !up: alternative_tile = 0 # T-down
			if !down: alternative_tile = 2 # T-up
			if !left: alternative_tile = 1 # T-right
			if !right: alternative_tile = 3 # T-left
			return { "source_id": SOURCE_T_JUNCTION, "atlas_coords": TILE_T_JUNCTION, "alternative_tile": alternative_tile }
		4: # Cross-section
			return { "source_id": SOURCE_CROSS, "atlas_coords": TILE_CROSS, "alternative_tile": 0 }

	return {}