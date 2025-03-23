import heapq
import numpy as np
from scipy.spatial import Voronoi
from utils.geometry import euclidean_distance, is_point_in_obstacle


# Making voronoi
def make_voronoi(vor, obstacles):
    graph = {}
    for vertex in vor.vertices:
        if not is_point_in_obstacle(vertex, obstacles):
            graph[tuple(vertex)] = []
    
    for ridge in vor.ridge_vertices:
        if -1 not in ridge:  #I think this ignores infinite stuff - not sure
            p1, p2 = vor.vertices[ridge]
            if tuple(p1) in graph and tuple(p2) in graph:
                graph[tuple(p1)].append(tuple(p2))
                graph[tuple(p2)].append(tuple(p1))
    
    return graph

# A* Algorithm
def a_star(graph, start, goal):
    # CUE starts here
    open_set = []
    heapq.heappush(open_set, (0, start))
    
    came_from = {}
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0
    
    f_score = {node: float('inf') for node in graph}
    f_score[start] = euclidean_distance(start, goal)
    
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
            tentative_g_score = g_score[current] + euclidean_distance(current, neighbor)
            
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + euclidean_distance(neighbor, goal)
                
                if neighbor not in [i[1] for i in open_set]:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
    
    return []  # No Solution beeep boop beep 

def voronoi_a_star_path(start, goal, obstacles):
    # points here 
    points = np.random.rand(100, 2) * 10
    for obs in obstacles:
        x_min, y_min, x_max, y_max = obs
        points = np.vstack((points, [[x_min, y_min], [x_min, y_max], [x_max, y_min], [x_max, y_max]]))
    
    # make voronoi diagram 
    vor = Voronoi(points)
    
    # Build the graph from Voronoi diagram
    graph = make_voronoi(vor, obstacles)
    
    # Add start and goal points to the graph by connecting them -  joining to nearest vertex 
    nearest_start = min(graph.keys(), key=lambda v: euclidean_distance(v, start))
    nearest_goal = min(graph.keys(), key=lambda v: euclidean_distance(v, goal))
    
    graph[start] = [nearest_start]
    graph[goal] = [nearest_goal]
    
    path = a_star(graph, start, goal)
    if not path:
        print("No valid path found! Check the Voronoi graph and obstacles.")
    
    return( path, vor)

