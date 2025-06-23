from typing import Tuple, List

# reason for choosing 2d list was because its straight forward to visulaize a maze grid with list,
# list are more flexible like each cell can store a value indicating if it's a wall or a path and
# additional information like visited status can also be stored, and it easy to access and update cell in list

# Create a maze with specified width and height, and external walls
def create_maze(width: int = 5, height: int = 5) -> List[List[int]]:
    maze = [[1] * width for _ in range(height)]
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            maze[y][x] = 0
    return maze # returns generated maze with external walls and no internal wall


# Adds a horizontal wall to the maze at the specified (x_coordinate)
def add_horizontal_wall(maze: List[List[int]], x_coordinate: int, horizontal_line: int) -> List[List[int]]:
    if 0 <= horizontal_line < len(maze) and 0 <= x_coordinate < len(maze[0]): # Check if coordinates are within bounds
        maze[horizontal_line][x_coordinate] = 1 #will mark specified position as wall
        if horizontal_line + 1 < len(maze):
            maze[horizontal_line + 1][x_coordinate] = 1
    return maze # returns generated maze


# Add a vertical wall to the maze at the specified (y_coordinate)
def add_vertical_wall(maze: List[List[int]], y_coordinate: int, vertical_line: int) -> List[List[int]]:
    if 0 <= y_coordinate < len(maze) and 0 <= vertical_line < len(maze[0]):# Check if coordinates are within bounds
        maze[y_coordinate][vertical_line] = 1# Set a vertical wall at the specified position
        if vertical_line - 1 >= 0:
            maze[y_coordinate][vertical_line - 1] = 1
    return maze #returns generated maze


# Returns the dimensions (width, height) of the maze
def get_dimensions(maze: List[List[int]]) -> Tuple[int, int]:
    height = len(maze)
    width = len(maze[0]) if height > 0 else 0
    return width, height

# tuple has a straight forward way to return multiple values, they are immutable (can't change)
# so reduces error, more readable, and easy to use.

# Returns the wall status (North, East, South, West) at a given (x, y) coordinate
def get_walls(maze: List[List[int]], x_coordinate: int, y_coordinate: int) -> Tuple[bool, bool, bool, bool]:
    width, height = get_dimensions(maze)

    # Initialize the wall status for each direction
    north = south = east = west = False

    # Check if there's an external wall at the boundary
    if y_coordinate == 0: north = True
    if y_coordinate == height - 1: south = True
    if x_coordinate == 0: west = True
    if x_coordinate == width - 1: east = True

    # Check for internal horizontal walls
    if y_coordinate + 1 < height and maze[y_coordinate + 1][x_coordinate] == 1:
        south = True
    if y_coordinate - 1 >= 0 and maze[y_coordinate - 1][x_coordinate] == 1:
        north = True

    # Check for internal vertical walls
    if x_coordinate + 1 < width and maze[y_coordinate][x_coordinate + 1] == 1:
        east = True
    if x_coordinate - 1 >= 0 and maze[y_coordinate][x_coordinate - 1] == 1:
        west = True

    return north, east, south, west #returns updated wall status

# to make our code suitable to work with maze with # and .
def load_maze_from_file(filename: str) -> List[List[int]]:
    maze = []
    with open(filename, 'r') as file:
        for line in file:
            maze.append([1 if char == '#' else 0 for char in line.rstrip()])
            #1 represents a wall (# in the file).
            #0 represents an open path (anything else in the file).
    return maze # return the maze with 1 and 0
