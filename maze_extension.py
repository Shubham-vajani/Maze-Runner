from typing import Tuple, List
# reason for choosing 2d list was because its straight forward to visulaize a maze grid with list,
# list are more flexible like each cell can store a value indicating if it's a wall or a path and
# additional information like visited status can also be stored, and it easy to access and update cell in list

# Create a maze with specified width and height, and external walls
def create_maze(width: int = 5, height: int = 5) -> List[List[int]]:
    maze = [[1] * width for _ in range(height)]  # Initialize maze with walls (1)
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            maze[y][x] = 0
    return maze # returns generated maze


# Add a horizontal wall to the maze at the specified (x_coordinate)
def add_horizontal_wall(maze: List[List[int]], x_coordinate: int, horizontal_line: int) -> List[List[int]]:
    if 0 <= horizontal_line < len(maze) and 0 <= x_coordinate < len(maze[0]): # Check if coordinates are within bounds
        maze[horizontal_line][x_coordinate] = 1# will mark specified position as wall
        if horizontal_line + 1 < len(maze):
            maze[horizontal_line + 1][x_coordinate] = 1
    return maze # returns generated maze


# Add a vertical wall to the maze at the specified (y_coordinate)
def add_vertical_wall(maze: List[List[int]], y_coordinate: int, vertical_line: int) -> List[List[int]]:
    if 0 <= y_coordinate < len(maze) and 0 <= vertical_line < len(maze[0]):# Check if coordinates are within bounds
        maze[y_coordinate][vertical_line] = 1# Set a vertical wall at the specified position
        if vertical_line - 1 >= 0:
            maze[y_coordinate][vertical_line - 1] = 1
    return maze # returns generated maze


# Returns the dimensions (width, height) of the maze
def get_dimensions(maze: List[List[int]]) -> Tuple[int, int]:
    height = len(maze)
    width = len(maze[0]) if height > 0 else 0
    return width, height

# tuple has a straight forward way to return multiple values, they are immutable (can't change)
# so reduces error, more readable, and easy to use.


# this function will return wall status
def get_walls(maze: List[List[int]], x: int, y: int) -> Tuple[bool, bool, bool, bool]:
    width = len(maze[0])  # number of columns (width of the maze)
    height = len(maze)  # number of rows (height of the maze)

    def is_wall(nx, ny): # this inner helper function checks if a given coordinate (nx, ny) represents a wall or is out of bounds.
        return not (0 <= nx < width and 0 <= ny < height) or maze[ny][nx] == 1

# Checks for walls in the four directions relative to the given position
    north = is_wall(x, y - 1)
    south = is_wall(x, y + 1)
    west = is_wall(x - 1, y)
    east = is_wall(x + 1, y)

    return north, east, south, west # returns wall status
#The new get_walls function improves clarity and modularity by using a helper function, is_wall,
# to check for walls or out-of-bound conditions in 	each cardinal direction. It eliminates redundant
# logic for external walls and directly computes north, east, south, and west statuses.


# Load a maze from a file, supporting non-regular structures
def load_maze_from_file(filename: str) -> List[List[int]]:
    maze = []
    with open(filename, 'r') as file:
        for line in file:
            # Accept '#' as walls and '.' or spaces as paths
            maze.append([1 if char == '#' else 0 for char in line.rstrip()])
    return maze


# Visualize the maze in a user-friendly format
def display_maze(maze: List[List[int]]):
    for row in maze:
        print(''.join('#' if cell == 1 else '.' for cell in row))

