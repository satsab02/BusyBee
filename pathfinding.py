# A* Algorithm
import heapq
from utils.geometry import euclidean_distance, manhattan_distance
import numpy as np


def build_graph(start_positions, goal_clusters):
    graph = {}  # Initialize graph

    # Combine start and goal points into a single list
    all_points = start_positions + [goal for cluster in goal_clusters for goal in cluster]

    # Generate random points and add them to the graph
    random_points = np.random.rand(50, 2) * 10  # Generate random points in a 10x10 area
    for p in random_points:
        graph[tuple(p)] = []

    # Add start and goal points explicitly to the graph
    for point in all_points:
        graph[tuple(point)] = []

    # Connect each point to its nearest neighbors
    for point in graph:
        distances = [(other, euclidean_distance(point, other)) for other in graph if other != point]
        distances.sort(key=lambda x: x[1])  # Sort by distance
        graph[point] = [neighbor for neighbor, _ in distances[:5]]  # Connect to 5 nearest neighbors

    return graph

def a_star(graph, start, goal, weight = 0.2):
    # CUE starts here
    open_set = []
    heapq.heappush(open_set, (0, start))
    open_set_lookup = {start}
    
    came_from = {}
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0
    
    f_score = {node: float('inf') for node in graph}
    f_score[start] = weight * manhattan_distance(start, goal)
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current == goal:
            # constructing a path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]
        
        for neighbor in graph[current]:
            tentative_g_score = g_score[current] + manhattan_distance(current, neighbor)
            
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                dynamic_weight = max(1.0, weight - (tentative_g_score / 100))
                f_score[neighbor] = g_score[neighbor] + dynamic_weight*manhattan_distance(neighbor, goal)
                
                if neighbor not in open_set_lookup:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
                    open_set_lookup.add(neighbor)
    
    return []  # No Solution beeep boop beep 


# Require multi-goal A* algorithm

def multi_goal_a_star(graph, start, goals):
    total_path = []
    current = start  # Current position

    for goal in goals:
        if current not in graph:
            print(f"Warning: Start point {current} not in graph.")
            continue

        if goal not in graph:
            print(f"Warning: Goal point {goal} not in graph.")
            continue

        segment = a_star(graph, current, goal)
        if segment:
            total_path.extend(segment[:-1])  # Avoid duplicating the goal point
        else:
            print(f"Warning: No path found from {current} to {goal}.")
        current = goal

    # Return to the start point
    return_path = a_star(graph, current, start)
    if return_path:
        total_path.extend(return_path[:-1])
    else:
        print(f"Warning: No path found from {current} back to start {start}.")

    return total_path