# imports which i feel i might use in some parts of code
import argparse
import csv
from typing import List, Tuple, Optional, Deque
from collections import deque

# finds shortest path to starting position to goal position and writes in exploration file
def shortest_path(
    maze: List[List[str]],
    starting: Optional[Tuple[int, int]] = None,
    goal: Optional[Tuple[int, int]] = None,
    log_exploration: bool = False,
) -> Tuple[List[Tuple[int, int]], int]:
    if not maze:  # makes sures there's a maze, else would show error
        raise ValueError("Maze cannot be empty.")

    rows, cols = len(maze), len(maze[0])
    starting = starting or (0, 0)  #if no starting position,then it by default sets it to (0,0)
    goal = goal or (rows - 1, cols - 1)  #if no goal then sets it to top-right corner

    # Validate starting and goal positions
    if not (0 <= starting[0] < rows and 0 <= starting[1] < cols) or maze[starting[0]][starting[1]] != '.':
        raise ValueError(f"Invalid starting position: {starting}")
    if not (0 <= goal[0] < rows and 0 <= goal[1] < cols) or maze[goal[0]][goal[1]] != '.':
        raise ValueError(f"Invalid goal position: {goal}")

    directions = [(-1, 0, 'U'), (1, 0, 'D'), (0, -1, 'L'), (0, 1, 'R')]  # Up, Down, Left, Right with actions
    queue: deque[Tuple[int, int]] = deque([starting])
    came_from = {starting: None}
    path = []
    exploration_steps = 0

    # Log for exploration
    exploration_log = []

    while queue:
        current = queue.popleft()
        exploration_steps += 1  # Increment exploration steps for every node dequeued

        if current == goal:
            break

        for dx, dy, action in directions:
            neighbor = (current[0] + dx, current[1] + dy)
            if (
                0 <= neighbor[0] < rows
                and 0 <= neighbor[1] < cols
                and maze[neighbor[0]][neighbor[1]] == '.'
                and neighbor not in came_from
            ):
                queue.append(neighbor)
                came_from[neighbor] = current

                # Log exploration if required
                if log_exploration:
                    exploration_log.append((exploration_steps, neighbor[0], neighbor[1], action))

    if goal not in came_from:
        raise ValueError("No path found from starting to goal.")  # Raises error if goal not found

    # Reconstruct the path
    current = goal
    while current:
        path.append(current)
        current = came_from[current]
    path = path[::-1]  # Reverse to start from the starting position

    # Write exploration log to CSV
    if log_exploration:
        with open('exploration.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Step', 'x-coordinate', 'y-coordinate', 'Action'])  # CSV will have 4 columns
            for step, x, y, action in exploration_log:
                writer.writerow([step, x, y, action])#writes all 4 things in file

    return path, exploration_steps



# reads maze from file and ensures that it follows required structure, else raise error
def maze_reader(maze_file: str) -> List[List[str]]:
    try:
        with open(maze_file, 'r') as file:
            maze = [list(line.strip()) for line in file.readlines()]
    except IOError:
        raise IOError(f"Cannot read the maze file: {maze_file}")  # when can't read from input file

    if not maze:
        raise ValueError("Maze file is empty.")  # when file content dosen't form proper maze

    rows, cols = len(maze), len(maze[0])

    # Validate structure of maze
    if any(len(row) != cols for row in maze):
        raise ValueError("Maze rows are not of consistent length.")
    if not all(c in ('#', '.') for row in maze for c in row):
        raise ValueError("Maze contains invalid characters.")
    if any(c != '#' for c in maze[0] + maze[-1]) or any(row[0] != '#' or row[-1] != '#' for row in maze):
        raise ValueError("Maze is not fully enclosed by walls.")

    return maze


# writes statistics about maze solving process( such as stpes, path length etc)
def write_statistics(maze_file: str, exploration_steps: int, path_length: int,path: List[Tuple[int, int]]):
    score = exploration_steps / 4 + path_length

    with open('statistics.txt', mode='w') as file:  # line below are 5 output line for this file
        file.write(f"Input file: {maze_file}\n")
        file.write(f"Score: {score:.2f}\n")
        file.write(f"Exploration steps: {exploration_steps}\n")
        file.write(f"Shortest path: {path}\n")
        file.write(f"Path length: {path_length}\n")


# this section is responsible for exceuting the program
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ECS Maze Runner")  # provides decription of command line argument
    parser.add_argument("maze", help="The name of the maze file, e.g., maze1.mz")
    parser.add_argument("--starting", help='The starting position, e.g., "2,1"', default=None)
    parser.add_argument("--goal", help='The goal position, e.g., "4,5"', default=None)
    args = parser.parse_args()

    try:
        maze = maze_reader(args.maze)

        # Parse starting and goal positions from command-line arguments
        starting = tuple(map(int, args.starting.split(','))) if args.starting else None
        goal = tuple(map(int, args.goal.split(','))) if args.goal else None

        # Print maze for debugging purposes
        print("Maze:")
        for row in maze:
            print("".join(row))
        print(f"Starting position: {starting}")
        print(f"Goal position: {goal}")

        # Find the shortest path and get exploration data
        path, exploration_steps = shortest_path(maze, starting, goal, log_exploration=True)

        # Display the shortest path and maze with path
        print("Shortest Path:", path)
        print("Maze with Path:")
        for r, row in enumerate(maze):
            row_display = ''.join(
                "@" if (r, c) in path else char
                for c, char in enumerate(row)
            )
            print(row_display)

        # Write statistics to file
        write_statistics(args.maze, exploration_steps, len(path))
        # Write statistics to file
        write_statistics(args.maze, exploration_steps, len(path), path)


    except Exception as e:
        print("Error:", e)  # shows error message if theres any errors and make sure prograam don't crash