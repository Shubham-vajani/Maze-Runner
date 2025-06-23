from typing import Tuple, Optional, List

# initializes a runner's starting position to (0,0) and orientation to north.
def create_runner(x: int = 0, y: int = 0, orientation: str = "N"):
    return {"x": x, "y": y, "orientation": orientation}
#the reason for using dictonary is that i can assess and modify specific attributes of runer
# using keys, additional attributes can easily be added when needed, make code more readable.


# returns x-coordinate of runner (horizontal position) in the maze
def get_x(runner):
    return runner["x"]

# returns y-coordinate of runner (vertical position) in the maze
def get_y(runner):
    return runner["y"]

# returns current orientation (direction) of runner
def get_orientation(runner):
    return runner["orientation"]

#updates the "orientation" of a runner based on a given direction.
def turn(runner, direction: str):
    # this part turns runner to either left or right and returs runner, not proper direction then shows
    orientations = ["N", "E", "S", "W"]
    current_idx = orientations.index(runner["orientation"])
    if direction == "Left":
        new_idx = (current_idx - 1) % 4  # Turning left
    elif direction == "Right":
        new_idx = (current_idx + 1) % 4  # Turning right
    else:
        raise ValueError(f"Invalid direction {direction}. Use 'Left' or 'Right'.")
    runner["orientation"] = orientations[new_idx] # # changes oritentation of runner rather than position
    return runner


# moves runner forward in current orrientation and updates its position
def forward(runner):
    if runner["orientation"] == "N":
        runner["y"] -= 1
    elif runner["orientation"] == "E":
        runner["x"] += 1
    elif runner["orientation"] == "S":
        runner["y"] += 1
    elif runner["orientation"] == "W":
        runner["x"] -= 1
    return runner


#Moves the runner in the specified direction.
def move(runner, direction: str):
    directions_map = {
        "North": "N",
        "East": "E",
        "South": "S",
        "West": "W"
    } #Provides a mapping between full direction names ("North") and their shorthand representations ("N"

    # Turn the runner to the desired direction
    while runner["orientation"] != directions_map[direction]:
        turn(runner, "Left")  # Adjust orientation iteratively

    # Move forward in the correct direction
    return forward(runner)


# checks presence of wall arround runner in all 4 direction
def get_walls(maze: List[List[int]], x: int, y: int) -> Tuple[bool, bool, bool, bool]:
    width = len(maze[0])  # number of columns (width of the maze)
    height = len(maze)  # number of rows (height of the maze)

    def is_wall(nx, ny): ## this inner helper function checks if a given coordinate (nx, ny) represents a wall or is out of bounds.
        return not (0 <= nx < width and 0 <= ny < height) or maze[ny][nx] == 1

    # Checks for walls in the four directions relative to the given position
    north = is_wall(x, y - 1)
    south = is_wall(x, y + 1)
    west = is_wall(x - 1, y)
    east = is_wall(x + 1, y)

    return north, east, south, west
#The new get_walls function improves clarity and modularity by using a helper function, is_wall,
# to check for walls or out-of-bound conditions in 	each cardinal direction. It eliminates redundant
# logic for external walls and directly computes north, east, south, and west statuses.


# checks if given x,y position is with the bounds of the maze
def is_within_bounds(x, y, maze):
    return 0 <= y < len(maze) and 0 <= x < len(maze[0])


# fucntion detects presene of wall around runner based on its orientation and position in maze
def sense_walls(runner, maze):
    x, y = runner["x"], runner["y"]
    orientation = runner["orientation"]

    # Helper function to check bounds
    def is_within_bounds(x, y, maze):
        return 0 <= y < len(maze) and 0 <= x < len(maze[0])

    # Get absolute wall directions (North, East, South, West)
    # Add boundary checks before accessing the maze
    north = not is_within_bounds(x, y - 1, maze) or maze[y - 1][x] == "#"
    east = not is_within_bounds(x + 1, y, maze) or maze[y][x + 1] == "#"
    south = not is_within_bounds(x, y + 1, maze) or maze[y + 1][x] == "#"
    west = not is_within_bounds(x - 1, y, maze) or maze[y][x - 1] == "#"

    # Convert to relative walls (Left, Front, Right, Back) based on the orientation
    if orientation == "N":
        return (west, north, east, south)
    elif orientation == "E":
        return (north, east, south, west)
    elif orientation == "S":
        return (east, south, west, north)
    elif orientation == "W":
        return (south, west, north, east)



# it performs Depth first search to explore maze from current positon to goal of runner
# it check wall surrounding runner and recursively explores available direction and backtraps
# when necessary, it marks position visited to avoid revisting them, check all 4 possible direction,
# if valid path found return actions taken to find path and path, fn ends when goal reached or no possible way
def dfs_explore(runner, maze, goal, visited=None, verbose=False):

    if visited is None:
        visited = set()

    x, y = get_x(runner), get_y(runner)

    # Print the current position and the goal
    if verbose and not visited:
        print(f"Visiting: ({x}, {y}), Goal: {goal}")

    # Base case: if we have reached the goal
    if (x, y) == goal:
        if verbose:
            print(f"Reached goal at: ({x}, {y})")
        return []  # Found the goal, no more steps to take

    # Mark the current position as visited
    visited.add((x, y))

    # Get the walls relative to the runner
    left, front, right, back = sense_walls(runner, maze)

    if verbose:
        print(f"Wall Status at ({x}, {y}): Left={left}, Front={front}, Right={right}, Back={back}")
        # verbose is helps while debugging

    # Define possible directions in terms of (dx, dy, direction string)
    directions = [
        ("West", -1, 0, left),
        ("East", 1, 0, right),
        ("North", 0, -1, front),
        ("South", 0, 1, back),
    ]

    for direction, dx, dy, has_wall in directions:
        if not has_wall:  # Check if there's no wall in the given direction
            new_x, new_y = x + dx, y + dy

            # Skip out-of-bounds positions
            if not (0 <= new_x < len(maze[0]) and 0 <= new_y < len(maze)):
                continue

            # Skip already visited positions
            if (new_x, new_y) in visited:
                continue

            # Save the runner's state before moving
            prev_state = runner.copy()

            # Move the runner in the chosen direction
            move(runner, direction)

            # Recursively explore from the new position
            actions = dfs_explore(runner, maze, goal, visited, verbose)

            # If a valid path is found, append the current direction to the path
            if actions is not None:
                return [direction] + actions

            # Backtrack: restore the runner's previous state
            runner.update(prev_state)

    return None  # No valid moves found

# Note = I have used DFS which analyse all possible routes hence takes more steps
# to find a path, compare to BFS