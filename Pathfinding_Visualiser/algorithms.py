import pygame
from maze import GRID_ROWS,GRID_COLS,CELL_SIZE,screen
from collections import deque
import heapq  # For the priority queue


# Colors
BLACK = (0, 0, 0)                # Grid lines
OBSTACLE = (30, 30, 30)          # Dark gray walls (slightly brighter)
WALKABLE = (50, 50, 50)          # Dark gray paths (brighter for contrast)
START = (0, 255, 0)              # Neon green for start point
END = (255, 105, 180)            # Brighter magenta for end point
VISITED = (0, 100, 255)          # Blue for visited cells
SHORTEST_PATH = (255, 255, 0)    # Yellow for shortest path

def drawGrid(grid, start=None, end=None, visited=None):
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            # Calculate cell position
            cell_x = col * CELL_SIZE
            cell_y = row * CELL_SIZE
            cell = pygame.Rect(cell_x, cell_y, CELL_SIZE, CELL_SIZE)

            # Assign colors based on grid value
            if visited and (row, col) in visited:
                pygame.draw.rect(screen, VISITED, cell)  # Visited cells
            elif grid[row][col] == 0:  # Walkable cell
                pygame.draw.rect(screen, WALKABLE, cell)
            else:  # Obstacle
                pygame.draw.rect(screen, OBSTACLE, cell)

            # Draw start and end points
            if start and (row, col) == start:
                pygame.draw.rect(screen, START, cell)
            if end and (row, col) == end:
                pygame.draw.rect(screen, END, cell)

            # Draw grid lines for clarity
            pygame.draw.rect(screen, BLACK, cell, 1)  # Outline


def bfs(grid, start, end):
    queue = deque([start])
    visited = set()
    parent = {}
    visited.add(start)

    clock = pygame.time.Clock()  # To control FPS
    batch_size = 100  # Number of cells to process before updating the screen
    batch_counter = 0

    while queue:
        current = queue.popleft()
        
        # Stop if we reached the end
        if current == end:
            break

        # Explore neighbors
        for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # Right, Down, Left, Up
            next_row, next_col = current[0] + direction[0], current[1] + direction[1]
            if 0 <= next_row < GRID_ROWS and 0 <= next_col < GRID_COLS and grid[next_row][next_col] == 0:
                next_cell = (next_row, next_col)
                if next_cell not in visited:
                    queue.append(next_cell)
                    visited.add(next_cell)
                    parent[next_cell] = current

        # Increment batch counter
        batch_counter += 1
        if batch_counter >= batch_size:
            batch_counter = 0
            drawGrid(grid, start, end, visited)
            pygame.display.flip()
            clock.tick(60)  # Cap frame rate at 60 FPS

    # Reconstruct the shortest path
    path = []
    current = end
    while current in parent:
        path.append(current)
        current = parent[current]
    path.append(start)
    path.reverse()
    
    return visited, path

def heuristic(a, b):
    # Manhattan distance
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(grid, start, end):
    open_set = []
    heapq.heappush(open_set, (0, start))  # (f-cost, node)
    g_cost = {start: 0}
    parent = {}
    visited = set()
    clock = pygame.time.Clock()  # To control FPS

    batch_size = 100  # Number of cells before updating the screen
    batch_counter = 0

    while open_set:
        current_f, current = heapq.heappop(open_set)

        if current == end:  # Goal reached
            break

        visited.add(current)

        # Explore neighbors
        for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # Right, Down, Left, Up
            next_row, next_col = current[0] + direction[0], current[1] + direction[1]
            next_cell = (next_row, next_col)

            if 0 <= next_row < GRID_ROWS and 0 <= next_col < GRID_COLS and grid[next_row][next_col] == 0:
                temp_g = g_cost[current] + 1  # Movement cost is 1
                if next_cell not in g_cost or temp_g < g_cost[next_cell]:
                    g_cost[next_cell] = temp_g
                    f_cost = temp_g + heuristic(next_cell, end)
                    heapq.heappush(open_set, (f_cost, next_cell))
                    parent[next_cell] = current

        # Batch rendering for better performance
        batch_counter += 1
        if batch_counter >= batch_size:
            batch_counter = 0
            drawGrid(grid, start, end, visited)
            pygame.display.flip()
            clock.tick(60)

    # Reconstruct the shortest path
    path = []
    current = end
    while current in parent:
        path.append(current)
        current = parent[current]
    path.append(start)
    path.reverse()

    return visited, path

def greedy_bfs(grid, start, end):
    open_set = []
    heapq.heappush(open_set, (heuristic(start, end), start))
    visited = set()
    parent = {}
    batch_size = 100
    batch_counter = 0
    clock = pygame.time.Clock()  # To control FPS

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == end:
            break
        
        visited.add(current)
        for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            next_row, next_col = current[0] + direction[0], current[1] + direction[1]
            next_cell = (next_row, next_col)
            if 0 <= next_row < GRID_ROWS and 0 <= next_col < GRID_COLS and grid[next_row][next_col] == 0:
                if next_cell not in visited:
                    heapq.heappush(open_set, (heuristic(next_cell, end), next_cell))
                    visited.add(next_cell)
                    parent[next_cell] = current

        # Increment batch counter
        batch_counter += 1
        if batch_counter >= batch_size:
            batch_counter = 0
            drawGrid(grid, start, end, visited)
            pygame.display.flip()
            clock.tick(60)  # Cap frame rate at 60 FPS

    # Reconstruct path
    path = []
    current = end
    while current in parent:
        path.append(current)
        current = parent[current]
    path.append(start)
    path.reverse()

    return visited, path

def dijkstra(grid, start, end):
    open_set = []
    heapq.heappush(open_set, (0, start))  # (cost, current node)
    g_cost = {start: 0}  # Cost to reach each cell
    parent = {}
    visited = set()
    
    clock = pygame.time.Clock()
    batch_size = 100  # Batch size for visualization
    batch_counter = 0

    while open_set:
        current_cost, current = heapq.heappop(open_set)
        
        if current == end:
            break
        
        if current in visited:
            continue
        
        visited.add(current)

        # Explore neighbors
        for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # Right, Down, Left, Up
            next_row, next_col = current[0] + direction[0], current[1] + direction[1]
            next_cell = (next_row, next_col)
            
            if 0 <= next_row < GRID_ROWS and 0 <= next_col < GRID_COLS and grid[next_row][next_col] == 0:
                new_cost = g_cost[current] + 1  # Cost is 1 for all moves
                if next_cell not in g_cost or new_cost < g_cost[next_cell]:
                    g_cost[next_cell] = new_cost
                    heapq.heappush(open_set, (new_cost, next_cell))
                    parent[next_cell] = current

        # Visualization batching
        batch_counter += 1
        if batch_counter >= batch_size:
            batch_counter = 0
            drawGrid(grid, start, end, visited)
            pygame.display.flip()
            clock.tick(60)

    # Reconstruct the shortest path
    path = []
    current = end
    while current in parent:
        path.append(current)
        current = parent[current]
    path.append(start)
    path.reverse()
    
    return visited, path

def dfs(grid, start, end):
    stack = [start]  # Stack to manage exploration
    visited = set()
    parent = {}
    
    clock = pygame.time.Clock()
    batch_size = 100  # Batch size for visualization
    batch_counter = 0
    
    while stack:
        current = stack.pop()
        
        if current == end:
            break
        
        if current in visited:
            continue
        
        visited.add(current)

        # Explore neighbors
        for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # Right, Down, Left, Up
            next_row, next_col = current[0] + direction[0], current[1] + direction[1]
            next_cell = (next_row, next_col)
            
            if 0 <= next_row < GRID_ROWS and 0 <= next_col < GRID_COLS and grid[next_row][next_col] == 0:
                if next_cell not in visited:
                    stack.append(next_cell)
                    parent[next_cell] = current

        # Visualization batching
        batch_counter += 1
        if batch_counter >= batch_size:
            batch_counter = 0
            drawGrid(grid, start, end, visited)
            pygame.display.flip()
            clock.tick(60)

    # Reconstruct the path (note: not guaranteed to be shortest)
    path = []
    current = end
    while current in parent:
        path.append(current)
        current = parent[current]
    path.append(start)
    path.reverse()
    
    return visited, path
