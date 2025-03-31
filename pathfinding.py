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

def a_star(graph, start, goal, weight):
    # CUE starts here
    open_set = []
    heapq.heappush(open_set, (0, start))
    open_set_lookup = {start}
    
    came_from = {}
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0
    
    f_score = {node: float('inf') for node in graph}
    f_score[start] = weight * euclidean_distance(start, goal) #using a wieght to the distances
    
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
            tentative_g_score = g_score[current] + weight*euclidean_distance(current, neighbor)
            
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + weight*euclidean_distance(neighbor, goal)
                
                if neighbor not in open_set_lookup:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
                    open_set_lookup.add(neighbor)
    
    return []  # No Solution beeep boop beep 


# Require multi-goal A* algorithm

def multi_goal_a_star(graph, start, goals, weight):
    total_path = []
    current = start  # Current position
    failed_paths = 0

    for goal in goals:
        if current not in graph:
            print(f"Warning: Start point {current} not in graph.")
            continue

        if goal not in graph:
            print(f"Warning: Goal point {goal} not in graph.")
            continue

        segment = a_star(graph, current, goal, weight)
        if segment:
            total_path.extend(segment[:-1])  # Avoid duplicating the goal point
        else:
            print(f"Warning: No path found from {current} to {goal}.")
            failed_paths += 1
        current = goal

    # Return to the start point
    return_path = a_star(graph, current, start, weight)
    if return_path:
        total_path.extend(return_path[:-1])
    else:
        print(f"Warning: No path found from {current} back to start {start}.")
        failed_paths += 1

    print(f"Total failed paths: {failed_paths}")
    return total_path


def bidirectional_a_star(graph, start, goal, weight):
    if start not in graph or goal not in graph:
        print("Start or goal point not in graph.")
        return []
    
    open_forward = []
    open_backward = []
    heapq.heappush(open_forward, (0, start))
    heapq.heappush(open_backward, (0, goal))

    open_forward_lookup = {start}
    open_backward_lookup = {goal}

    came_from_forward = {}
    came_from_backward = {}
    g_score_forward = {node: float('inf') for node in graph}
    g_score_backward = {node: float('inf') for node in graph}

    g_score_forward[start] = 0
    g_score_backward[goal] = 0

    poi = None
    min_cost = float('inf')

    while open_forward and open_backward:
       
       for open_set, came_from, one_way_g_score, other_way_g_score, direction in [(open_forward, came_from_forward, g_score_forward, g_score_backward, 'forward'),
                                                                                  (open_backward, came_from_backward, g_score_backward, g_score_forward, 'backward')]:
            _, current = heapq.heappop(open_set)

            if current in other_way_g_score and one_way_g_score[current] + other_way_g_score[current] < min_cost:
                min_cost = one_way_g_score[current] + other_way_g_score[current]
                poi = current
            
            for neighbour, _ in graph[current]:
                tentative_g_score = one_way_g_score[current] + weight*euclidean_distance(current, neighbour)

                if tentative_g_score < one_way_g_score[neighbour]:
                    came_from[neighbour] = current
                    one_way_g_score[neighbour] = tentative_g_score
                    heapq.heappush(open_set, (tentative_g_score, neighbour))
                    open_forward_lookup.add(neighbour) if direction == 'forward' else open_backward_lookup.add(neighbour)
    
    if not poi:
        print("No path found.")
        return []
    
    path_forward, path_backward = [], []
    current = poi

    while current in came_from_forward:
        path_forward.append(current)
        current = came_from_forward[current]
    path_forward.append(start)

    current = poi
    while current in came_from_backward:
        path_backward.append(current)
        current = came_from_backward[current]
    path_backward.append(goal)

    return path_forward[::-1] + path_backward[1:]  # Combine paths, avoiding duplicate meeting point

def multi_bidirectional(graph, start, goals, weight):
    total_path = []
    current = start
    failed_paths = 0

    for goal in goals:
        if current not in graph or goal not in graph:
            print(f"Warning: Start point {current} or goal point {goal} not in graph.")
            continue
        segment = bidirectional_a_star(graph, current, goal, weight)
        if segment:
            total_path.extend(segment[:-1])
        else:
            print(f"Warning: No path found from {current} to {goal}.")
            failed_paths += 1
        current = goal
    return_path = bidirectional_a_star(graph, current, start, weight)
    if return_path:
        total_path.extend(return_path[:-1])
    else:
        print(f"Warning: No path found from {current} back to start {start}.")
        failed_paths += 1
    
    print(f"Total failed paths: {failed_paths}")
    return total_path


                    