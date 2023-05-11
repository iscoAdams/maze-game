import random
from typing import List, Tuple, Optional
from mazekit.props import Props
class Maze:
    def __init__(self):
        self._grid =  []
        self._props = Props()

    @staticmethod
    def generate_maze(rows=None, cols=None) -> 'Maze':
        maze = Maze()
        if not rows or not cols:
            maze.props.rows = rows = random.randint(8, 50)
            maze.props.cols = cols = random.randint(8, 50)
        # print(f"Generating maze of size {rows}x{cols}\nto print it u can call print_grid()")
        maze.grid = [["." for _ in range(cols)] for _ in range(rows)] #O(n*m)
        maze.props.start = (0,0)
        while maze.props.goal == None or maze.props.goal == maze.props.start:
            maze.props.goal = (random.randint(0, rows-1), random.randint(0, cols-1))
        maze.props.invalid_count = int(rows * cols * 0.2)

        maze.props.invalid_positions = set()  # unique positions
        while len(maze.props.invalid_positions) < maze.props.invalid_count: #O(n)
            row = random.randint(0, rows-1)
            col = random.randint(0, cols-1)
            if (row, col) != maze.props.start and (row, col) != maze.props.goal:
                maze.props.invalid_positions.add((row, col))

        for row, col in maze.props.invalid_positions: #O(n)
            maze.grid[row][col] = "X"

        maze.grid[maze.props.start[0]][maze.props.start[1]] = "S"
        maze.grid[maze.props.goal[0]][maze.props.goal[1]] = "E"
        return maze
        
    @staticmethod
    def read_maze(filename) -> Optional['Maze']: #may the input grid is invalid and return None
        try:
            maze = Maze()
            with open(filename,'r') as f:
                lines = f.readlines() #O(n)
                maze.props.rows = len(lines)
                maze.props.cols = len(lines[0].strip("\n"))
                maze.grid = [list(line.strip("\n")) for line in lines]

                if not maze.is_valid_grid(maze.grid):
                    print(f"Invalid maze")
                    raise SystemExit(1)
                
                for row in range(maze.props.rows):
                    for col in range(maze.props.cols):
                        if maze.grid[row][col] == 'S':
                            maze.props.start = (row, col)
                        elif maze.grid[row][col] == 'E':
                            maze.props.goal = (row, col)
                        elif maze.grid[row][col] == 'X':
                            maze.props.invalid_count += 1
                            maze.props.invalid_positions.add((row, col))
            return maze
        except OSError as e:
            print(f"Cannot open {filename}: {e.strerror}")
            raise SystemExit(1)
        
    def is_valid_grid(self,maze) -> bool:
        rows = len(maze)
        if not rows:
            return False
        len_of_row = len(maze[0])
        for row in maze:
            if len(row) != len_of_row:
                return False
        return True

    #some accessors/mutators
    @property
    def grid(self):
        return self._grid
    @grid.setter
    def grid(self, grid): 
        self._grid = grid
    @property
    def props(self):
        return self._props
    @staticmethod
    def print_grid(maze, filename=None):
        for row in maze.grid:
            print("".join(row), file=filename, end="\n")
    
