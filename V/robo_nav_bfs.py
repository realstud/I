import heapq
import time
import matplotlib.pyplot as plt
import numpy as np

def a_star_search(grid, start, goal, visualize=False, delay=0.1):
    """
    Perform A* Search on a grid to find the shortest path from start to goal.
    Optionally visualize search progress step-by-step.
    """
    rows, cols = len(grid), len(grid[0])
    open_list = [(manhattan_distance(start, goal), 0, start, [start])]
    closed_set = set()
    nodes_expanded = 0
    visited_path = set()

    while open_list:
        _, g, current, path = heapq.heappop(open_list)

        if current == goal:
            return path, nodes_expanded

        if current in closed_set:
            continue

        closed_set.add(current)
        visited_path.add(current)
        nodes_expanded += 1

        if visualize:
            visualize_search_progress(grid, visited_path, path, start, goal, delay)

        for neighbor in get_neighbors(current, grid, rows, cols):
            if neighbor not in closed_set:
                new_path = path + [neighbor]
                new_g = g + 1
                f = new_g + manhattan_distance(neighbor, goal)
                heapq.heappush(open_list, (f, new_g, neighbor, new_path))

    return None, nodes_expanded

def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def get_neighbors(position, grid, rows, cols):
    r, c = position
    neighbors = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_r, new_c = r + dr, c + dc
        if 0 <= new_r < rows and 0 <= new_c < cols and grid[new_r][new_c] == 0:
            neighbors.append((new_r, new_c))
    return neighbors

def print_grid(grid, path=None, start=None, goal=None):
    path_set = set(path) if path else set()
    for r in range(len(grid)):
        row_str = ""
        for c in range(len(grid[0])):
            pos = (r, c)
            if pos == start:
                row_str += "S "
            elif pos == goal:
                row_str += "G "
            elif pos in path_set:
                row_str += "* "
            elif grid[r][c] == 1:
                row_str += "■ "
            else:
                row_str += ". "
        print(row_str)

def get_user_input():
    while True:
        try:
            rows = int(input("Enter number of rows: "))
            cols = int(input("Enter number of columns: "))
            if rows > 0 and cols > 0:
                break
            else:
                print("Please enter positive integers for rows and columns.")
        except ValueError:
            print("Please enter valid integers.")

    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    print("\nEnter obstacle positions (row,col). Type 'done' when finished.")
    while True:
        obstacle_input = input("Obstacle position (row,col): ")
        if obstacle_input.lower() == 'done':
            break
        try:
            r, c = map(int, obstacle_input.split(','))
            if 0 <= r < rows and 0 <= c < cols:
                grid[r][c] = 1
            else:
                print("Position out of bounds.")
        except:
            print("Invalid input.")

    while True:
        try:
            start_input = input("\nEnter start position (row,col): ")
            start_r, start_c = map(int, start_input.split(','))
            if 0 <= start_r < rows and 0 <= start_c < cols and grid[start_r][start_c] == 0:
                start = (start_r, start_c)
                break
            else:
                print("Invalid start position.")
        except:
            print("Invalid input.")

    while True:
        try:
            goal_input = input("Enter goal position (row,col): ")
            goal_r, goal_c = map(int, goal_input.split(','))
            if 0 <= goal_r < rows and 0 <= goal_c < cols and grid[goal_r][goal_c] == 0:
                goal = (goal_r, goal_c)
                break
            else:
                print("Invalid goal position.")
        except:
            print("Invalid input.")

    return grid, start, goal

def visualize_path(grid, path, start, goal):
    grid_array = np.array(grid)
    fig, ax = plt.subplots()
    ax.imshow(grid_array, cmap='binary', origin='upper')

    if path:
        path_x, path_y = zip(*path)
        ax.scatter(path_y, path_x, color='blue', label='Path', s=100)

    obstacles = [(r, c) for r in range(len(grid)) for c in range(len(grid[0])) if grid[r][c] == 1]
    if obstacles:
        obstacles_x, obstacles_y = zip(*obstacles)
        ax.scatter(obstacles_y, obstacles_x, color='red', label='Obstacle', s=100)

    ax.scatter(start[1], start[0], color='green', label='Start', s=100)
    ax.scatter(goal[1], goal[0], color='purple', label='Goal', s=100)
    ax.set_xlabel('Columns')
    ax.set_ylabel('Rows')
    ax.legend(loc='upper left')
    plt.show()

def visualize_search_progress(grid, visited, path, start, goal, delay=0.1):
    grid_array = np.array(grid)
    plt.clf()
    plt.imshow(grid_array, cmap='Greys', origin='upper')

    if visited:
        visited_x, visited_y = zip(*visited)
        plt.scatter(visited_y, visited_x, color='lightblue', label='Visited', s=60)

    if path:
        path_x, path_y = zip(*path)
        plt.scatter(path_y, path_x, color='blue', label='Current Path', s=60)

    plt.scatter(start[1], start[0], color='green', label='Start', s=100)
    plt.scatter(goal[1], goal[0], color='purple', label='Goal', s=100)
    plt.legend(loc='upper left')
    plt.pause(delay)

def main():
    print("A* Search for Robot Navigation")
    print("=============================")

    grid, start, goal = get_user_input()
    print("\nGrid Layout:")
    print_grid(grid, start=start, goal=goal)

    print("\nSearching for path using A* with visualization...")

    plt.ion()  # Enable interactive plotting
    start_time = time.time()
    path, nodes_expanded = a_star_search(grid, start, goal, visualize=True, delay=0.05)
    end_time = time.time()
    plt.ioff()  # Disable interactive plotting

    if path:
        print(f"\nPath found! Length: {len(path)}")
        print(f"Total nodes expanded: {nodes_expanded}")
        print(f"Time taken: {end_time - start_time:.2f} seconds")
        print_grid(grid, path, start, goal)
        visualize_path(grid, path, start, goal)
        print("\nPath steps:")
        for i, (r, c) in enumerate(path):
            print(f"Step {i}: ({r}, {c})")
    else:
        print("\nNo path found!")

if __name__ == "__main__":
    main()
