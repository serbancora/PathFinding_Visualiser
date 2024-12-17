import random
import pygame

pygame.init()

# Grid Size
GRID_ROWS, GRID_COLS = 121,221  # Ensure rows and cols are odd numbers
CELL_SIZE = 7
GRID_WIDTH = CELL_SIZE * GRID_COLS
GRID_HEIGHT = CELL_SIZE * GRID_ROWS

# Window Size
WINDOW_HEIGHT = GRID_HEIGHT
WINDOWS_WIDTH = GRID_WIDTH

screen = pygame.display.set_mode((WINDOWS_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pathfinding Visualisation")

def createMaze():
    # Initialize the grid with walls (1)
    maze = [[1 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]

    # Start carving paths using a stack
    stack = [(1, 1)]  # Start point
    maze[1][1] = 0  # Make start point a path

    def neighbors(x, y):
        # Return valid neighbors that can be carved (2 steps away)
        dirs = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(dirs)
        result = []
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 < nx < GRID_ROWS - 1 and 0 < ny < GRID_COLS - 1 and maze[nx][ny] == 1:
                result.append((nx, ny))
        return result

    while stack:
        current = stack[-1]
        nbors = neighbors(*current)

        if nbors:
            # Choose a random neighbor
            nx, ny = nbors.pop()
            # Carve path between current and chosen neighbor
            maze[(current[0] + nx) // 2][(current[1] + ny) // 2] = 0
            maze[nx][ny] = 0
            stack.append((nx, ny))  # Add the chosen neighbor to the stack
        else:
            stack.pop()  # Backtrack if no neighbors available

    # Place start and end points
    maze[1][1] = 0  # Start
    maze[GRID_ROWS - 2][GRID_COLS - 2] = 0  # End

    return maze