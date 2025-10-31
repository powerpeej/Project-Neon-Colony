# src/procgen/wfc.gd
# Implements the Wave Function Collapse algorithm for procedural generation.

extends Object
class_name WFC

# The grid of cells, where each cell holds its possible states (tiles).
var _grid: Array = []

# The dimensions of the grid.
var _width: int = 0
var _height: int = 0

# A list of all possible tile identifiers.
var _tiles: Array = []

# Rules defining which tiles can be adjacent to each other.
# Expected format: { "tile_name": {"up": ["tile1", ...], "down": [...], ...} }
var _rules: Dictionary = {}

# Direction vectors for neighbor finding.
const _directions = {
	"up": Vector2.UP, "down": Vector2.DOWN,
	"left": Vector2.LEFT, "right": Vector2.RIGHT
}


func _init(width: int, height: int, tiles: Array, rules: Dictionary):
	"""
	Initializes the WFC solver.
	- width: The width of the grid to generate.
	- height: The height of the grid to generate.
	- tiles: An array of all possible tile identifiers.
	- rules: A dictionary defining adjacency constraints for each tile.
	"""
	self._width = width
	self._height = height
	self._tiles = tiles
	self._rules = rules

	# Initialize the grid. Each cell starts with all possible tiles.
	var all_tiles = _tiles.duplicate(true)
	for y in range(_height):
		var row: Array = []
		for x in range(_width):
			row.append(all_tiles.duplicate(true))
		_grid.append(row)


func run():
	"""
	Executes the WFC algorithm to generate a result.
	Returns the generated grid or an empty array on failure.
	"""
	# Main loop: continue until every cell is collapsed to a single state.
	while not is_fully_collapsed():
		# 1. Find the cell with the lowest entropy (fewest possibilities).
		var next_cell_coords = find_lowest_entropy_cell()

		if next_cell_coords == Vector2(-1, -1):
			printerr("WFC Error: Contradiction reached. Aborting.")
			return [] # Failure due to contradiction

		if next_cell_coords == Vector2.ZERO and not is_fully_collapsed():
			# This indicates all remaining cells are collapsed, but we double-check.
			break

		# 2. Collapse this cell to a single, randomly chosen state.
		if not observe(next_cell_coords):
			printerr("WFC Error: Observation failed, cell had no possibilities.")
			return [] # Failure

		# 3. Propagate the consequences of this collapse to all neighbors.
		propagate(next_cell_coords)

	return get_collapsed_grid()


func is_fully_collapsed() -> bool:
	"""
	Checks if every cell in the grid has been collapsed to a single state.
	"""
	for y in range(_height):
		for x in range(_width):
			if _grid[y][x].size() > 1:
				return false
	return true


func find_lowest_entropy_cell() -> Vector2:
	"""
	Finds the uncollapsed cell with the fewest possible states (lowest entropy).
	Returns:
	- Coordinates of the cell to collapse.
	- Vector2.ZERO if all cells are already collapsed.
	- Vector2(-1, -1) if a contradiction (a cell with 0 possibilities) is found.
	"""
	var min_entropy = _tiles.size() + 1
	var lowest_entropy_cells: Array = []

	for y in range(_height):
		for x in range(_width):
			var cell_entropy = _grid[y][x].size()
			if cell_entropy == 0:
				return Vector2(-1, -1) # Contradiction found

			if cell_entropy > 1:
				if cell_entropy < min_entropy:
					min_entropy = cell_entropy
					lowest_entropy_cells = [Vector2(x, y)]
				elif cell_entropy == min_entropy:
					lowest_entropy_cells.append(Vector2(x, y))

	if lowest_entropy_cells.is_empty():
		return Vector2.ZERO # All cells are collapsed.

	# Pick one randomly from the candidates to break ties
	return lowest_entropy_cells[randi() % lowest_entropy_cells.size()]


func observe(coords: Vector2) -> bool:
	"""
	Collapses a cell to a single, randomly chosen state from its possibilities.
	Returns false if the cell has no possibilities left (a contradiction).
	"""
	var x = int(coords.x)
	var y = int(coords.y)

	var possibilities = _grid[y][x]
	if possibilities.is_empty():
		return false # Contradiction

	# Randomly choose one of the remaining possibilities
	var chosen_state = possibilities[randi() % possibilities.size()]

	# Collapse the cell to this single state
	_grid[y][x] = [chosen_state]

	return true


func propagate(initial_coords: Vector2):
	"""
	Starting from an initial cell, propagates constraints to its neighbors,
	and their neighbors, and so on, until stability is reached.
	"""
	var stack: Array = [initial_coords]

	while not stack.is_empty():
		var current_coords = stack.pop_back()
		var current_possibilities = _grid[int(current_coords.y)][int(current_coords.x)]

		var neighbors = _get_valid_neighbors(current_coords)

		# For each direction, update the neighboring cell
		for dir_name in neighbors.keys():
			var neighbor_coords = neighbors[dir_name]
			var nx = int(neighbor_coords.x)
			var ny = int(neighbor_coords.y)

			var neighbor_possibilities = _grid[ny][nx]
			var original_neighbor_size = neighbor_possibilities.size()

			# Determine the set of tiles that are valid for the neighbor
			# based on the current cell's possibilities and the rules.
			var valid_neighbor_tiles = _get_valid_adjacencies(current_possibilities, dir_name)

			# Filter the neighbor's possibilities against the valid set
			var updated_possibilities = []
			for tile in neighbor_possibilities:
				if tile in valid_neighbor_tiles:
					updated_possibilities.append(tile)

			# If the neighbor's possibilities have been reduced, update the grid
			# and add the neighbor to the stack to propagate its own changes.
			if updated_possibilities.size() < original_neighbor_size:
				_grid[ny][nx] = updated_possibilities

				if not neighbor_coords in stack:
					stack.push_back(neighbor_coords)


func _get_valid_adjacencies(possibilities: Array, direction: String) -> Dictionary:
	"""
	Helper function.
	Given the possible states of a cell, returns a dictionary (used as a set)
	of all states that are allowed to be adjacent in the given direction.
	"""
	var valid_tiles_set = {}

	for tile in possibilities:
		if _rules.has(tile) and _rules[tile].has(direction):
			for allowed_tile in _rules[tile][direction]:
				valid_tiles_set[allowed_tile] = true

	return valid_tiles_set


func _get_valid_neighbors(coords: Vector2) -> Dictionary:
	"""
	Helper function.
	Returns a dictionary of valid neighbor coordinates and their direction name.
	e.g. { "up": Vector2(x, y-1), ... }
	Filters out neighbors that are outside the grid boundaries.
	"""
	var neighbors = {}
	for dir_name in _directions.keys():
		var neighbor_coords = coords + _directions[dir_name]
		if (neighbor_coords.x >= 0 and neighbor_coords.x < _width and
			neighbor_coords.y >= 0 and neighbor_coords.y < _height):
			neighbors[dir_name] = neighbor_coords
	return neighbors


func get_collapsed_grid() -> Array:
	"""
	Returns a simple 2D array of the final, collapsed states.
	If a cell is not collapsed, its value will be null.
	"""
	var result: Array = []
	for y in range(_height):
		var row: Array = []
		for x in range(_width):
			if _grid[y][x].size() == 1:
				row.append(_grid[y][x][0])
			else:
				row.append(null) # An uncollapsed or error state
		result.append(row)
	return result


func get_grid_state_string() -> String:
	"""
	Returns a string representation of the grid's current state for debugging.
	Shows the number of possibilities for each cell.
	"""
	var output = "WFC Grid State (%d x %d):\n" % [_width, _height]
	for y in range(_height):
		var row_str = "| "
		for x in range(_width):
			var count = _grid[y][x].size()
			if count == 1:
				row_str += "%s | " % _grid[y][x][0]
			else:
				row_str += str(count).pad_zeros(2) + " | "
		output += row_str + "\n"
	return output