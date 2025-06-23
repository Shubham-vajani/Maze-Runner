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

# changes the runner's oritention based on direction
def turn(runner, direction: str):
    # this part turns runner to either left or right and returs runner, if not proper direction then shows value error
    orientations = ["N", "E", "S", "W"]
    current_idx = orientations.index(runner["orientation"])
    if direction == "Left":
        new_idx = (current_idx - 1) % 4
    elif direction == "Right":
        new_idx = (current_idx + 1) % 4
    else:
        raise ValueError("Invalid direction. Use 'Left' or 'Right'.")# raises error for other direction
    runner["orientation"] = orientations[new_idx]  # changes oritentation of runner rather than position
    return runner # return runner

# moves runner forward in current orrientation and updates its position
def forward(runner):
    if runner["orientation"] == "N":
        runner["y"] += 1
    elif runner["orientation"] == "E":
        runner["x"] += 1
    elif runner["orientation"] == "S":
        runner["y"] -= 1
    elif runner["orientation"] == "W":
        runner["x"] -= 1
    return runner # returns runner


# checks it theres any wall on way of runners immediate vicinity(left,right,front)
# function returns a tuple of three Booleans, about whether or not there is a wall on(left,right,fron)
def sense_walls(runner, maze: List[List[int]]) -> Tuple[bool, bool, bool]:
    x, y = runner["x"], runner["y"]
    orientation = runner["orientation"]

    directions = {
        "N": [(-1, 0), (0, 1), (1, 0)],
        "E": [(0, 1), (1, 0), (0, -1)],
        "S": [(1, 0), (0, -1), (-1, 0)],
        "W": [(0, -1), (-1, 0), (0, 1)],
    }

    left, front, right = directions[orientation]
    maze_width, maze_height = len(maze[0]), len(maze)

#this is a helper function to determine whether a neighboring position in a maze contains a wall or is out of bounds
    def has_wall(dx, dy):
        nx, ny = x + dx, y + dy
        return nx < 0 or nx >= maze_width or ny < 0 or ny >= maze_height or maze[ny][nx] == 1

    return has_wall(*left), has_wall(*front), has_wall(*right) # returns whether or there's a wall


#  moves runner forward if theres no wall and raises value error if wall
def go_straight(runner, maze: List[List[int]]):
    left, front, right = sense_walls(runner, maze)
    if front:
        raise ValueError("There is a wall in front of the runner. The runner cannot go forward.")
    return forward(runner)  # returns the updated runner after the move

# uses left hug alogrithm to mov runner based on wall position
def move(runner, maze: List[List[int]]) -> Tuple[dict, str]:
    left, front, right = sense_walls(runner, maze)

    if not left:
        runner = turn(runner, "Left")
        runner = go_straight(runner, maze)
        return runner, "LF"
    elif not front:
        runner = go_straight(runner, maze)
        return runner, "F"
    elif not right:
        runner = turn(runner, "Right")
        runner = go_straight(runner, maze)
        return runner, "RF"
    else:
        runner = turn(runner, "Right")
        runner = turn(runner, "Right")
        runner = go_straight(runner, maze)
        return runner, "RRF"


# makes runner to go to goal and records steps taken to reach goal, and returns it.
def explore(runner, maze: List[List[int]], goal: Optional[Tuple[int, int]] = None) -> str:
    if goal is None:
        goal = (len(maze[0]) - 1, len(maze) - 1)  # Default top-right corner

    actions = []
    while (runner["x"], runner["y"]) != goal:
        try:
            runner, action = move(runner, maze)
            actions.append(action)
        except ValueError as e:  # if move fn raises value error then it provides additonal context
            raise RuntimeError(f"Error: {str(e)}") from e

    # Join the actions into a single string representing the path taken
    return "".join(actions)
