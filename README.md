To change the maze size: Go to maze.py and change the GRID_ROWS, GRID_COLS (Line 7).
To change the used algorithm for pathfinding: Go to main.py and change algorithm = "A*" into "A*" / "BFS" / "DFS" / "GBFS" / "Dijkstra". (Line 18)

A dynamic pathfinding visualizer built in Python using Pygame. Visualize popular pathfinding algorithms like:
- Breadth-First Search (BFS)
- Depth-First Search (DFS)
- Dijkstra's Algorithm
- A* Search
- Greedy Best-First Search
The tool generates mazes and allows real-time visualization of how each algorithm explores the grid to find the shortest path.

Features
- Dynamic Maze Generation: Procedurally generates solvable mazes of any size.
- Algorithm Visualizations: Step-by-step rendering of visited nodes and the final shortest path.
- Customizable Grid: Supports large grids optimized with efficient rendering and batching.
- Interactive Visualization: Start/End points and algorithm selection are integrated into the workflow.
