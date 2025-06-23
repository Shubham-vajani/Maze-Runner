 Maze Runner – Python Maze Exploration & Solving

This project is a Python-based maze exploration and solving simulation, built to model an autonomous agent navigating through a 2D grid maze. 
The system supports basic movement, wall sensing, exploration, and shortest-path calculation. 
In addition, a modular extension has been developed to implement a depth-first search (DFS) solver, capable of handling more complex maze configurations.

---

Overview

The Maze Runner simulates a virtual runner navigating a maze environment using both simple heuristic movement and a depth-first search strategy. 
It reads maze data from structured text files, interprets wall and path configurations, and determines a valid route from a starting point to a defined goal.

The project is divided into two major components:

- *Base version*: A wall-following runner that explores the maze using simple logic and then computes a shortest path based on visited cells.
- *Extension version*: A more advanced runner that uses DFS to fully explore the maze and determine a direct path from start to goal, without relying on heuristic exploration.

---

Project Structure

### Core Files

- **maze.py**  
  Handles the creation and structure of the maze grid.
  This includes defining the maze’s size, internal wall placement (horizontal and vertical), and providing access to wall information for any grid position.

- **runner.py**  
  Contains the logic for the maze runner's behavior. This includes movement controls, direction tracking, and the ability to sense nearby walls.
  It also implements a basic exploration strategy that allows the runner to traverse the maze systematically.

- **maze_runner.py**  
  Acts as the main driver for running the simulation using the basic maze and runner setup.
  It handles reading the maze file, initializing the runner, logging exploration data, and generating statistics about the exploration and the shortest discovered path.

---

### Extension Files (DFS Solver)

- **maze_extension.py**  
  An enhanced version of the maze logic that supports more robust interaction needed for the DFS algorithm.
  It mirrors the structure of the base maze.py file but introduces flexibility to better support algorithmic exploration, in this part maze could have spaces, no route etc.

- **runner_extension.py**  
  An updated runner implementation that works with the extended maze class.
  It includes more advanced path-tracking and decision-making logic to facilitate DFS traversal.

- **maze_runner_extension.py**  
  The entry point for running the DFS-based solver.
  This script parses command-line arguments, loads the maze from a file, invokes the DFS pathfinding process, and writes exploration logs and performance statistics to output files.

---

 Features

- Read and interpret structured maze files in .mz format
- Represent a maze with horizontal and vertical walls
- Simulate an autonomous runner that can:
  - Turn and move forward
  - Detect walls on all sides
  - Keep track of its position and orientation
- Explore the maze systematically and avoid revisiting cells
- Calculate a valid path from start to goal
- Log the steps taken during exploration in CSV format
- Output maze-solving statistics to a text file
- Use a DFS algorithm to solve complex or non-standard mazes

---

Maze File Format

The maze is defined in a plain text .mz file using ASCII characters:

- # indicates a wall
- . represents an open path
- The runner is rendered using directional symbols such as ^, >, v, and < depending on its orientation

Maze files are parsed line-by-line and converted into an internal representation suitable for navigation and wall detection.

---
