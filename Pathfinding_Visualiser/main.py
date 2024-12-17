import algorithms as ag
import maze as mz
import pygame

pygame.init()

# Example start and end points
start_point = (1, 1)
end_point = (mz.GRID_ROWS - 2, mz.GRID_COLS - 2)

def main():
    start_time = pygame.time.get_ticks()
    running = True
    clock = pygame.time.Clock()
    grid = mz.createMaze()

    # Algorithm selection
    algorithm = "A*"  # Change to "A*" / "BFS" / "DFS" / "GBFS" / "Dijkstra"
    algo_complete = False
    visited, path = set(), []

    while running:
        ag.screen.fill(ag.BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Run the selected algorithm
        if not algo_complete:
            if algorithm == "BFS":
                visited, path = ag.bfs(grid, start_point, end_point)
            elif algorithm == "A*":
                visited, path = ag.a_star(grid, start_point, end_point)
            elif algorithm == "GBFS":
                visited, path = ag.greedy_bfs(grid, start_point, end_point)
            elif algorithm == "DFS":
                visited, path = ag.dfs(grid, start_point, end_point)
            elif algorithm == "Dijkstra":
                visited, path = ag.dijkstra(grid, start_point, end_point)
            algo_complete = True
            end_time = pygame.time.get_ticks()
            print((end_time-start_time) / 1000)

        # Draw the grid and visited cells
        ag.drawGrid(grid, start=start_point, end=end_point, visited=visited)

        # Batch draw the final path in yellow
        if algo_complete:
            for row, col in path:
                cell_x = col * ag.CELL_SIZE
                cell_y = row * ag.CELL_SIZE
                cell = pygame.Rect(cell_x, cell_y, ag.CELL_SIZE, ag.CELL_SIZE)
                pygame.draw.rect(ag.screen, ag.SHORTEST_PATH, cell)

        # Refresh the display after all updates
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
