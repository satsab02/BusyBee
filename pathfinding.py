import heapq
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d


## im using euclidian distance - we may want to compute the langrangian

# Calculate Euclidian Distance
def euclidean_distance(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

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

# See if the point is within an exsiting obstacle
def is_point_in_obstacle(point, obstacles):
    for obs in obstacles:
        if obs[0] <= point[0] <= obs[2] and obs[1] <= point[1] <= obs[3]:
            return True
    return False

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
    
    # Find the shortest path using A*
    path = a_star(graph, start, goal)
    
    fig, ax = plt.subplots()
    voronoi_plot_2d(vor, ax=ax)
    
    # Making onbstacles 
    for obs in obstacles:
        rect = plt.Rectangle((obs[0], obs[1]), obs[2]-obs[0], obs[3]-obs[1], color='red', alpha=0.5)
        ax.add_patch(rect)
    
    # plotting the path
    if path:
        px, py = zip(*path)
        plt.plot(px, py, 'g-', linewidth=2)
        plt.plot(start[0], start[1], 'go')  # Start 
        plt.plot(goal[0], goal[1], 'ro')   # Goal
        
    plt.xlim(0, 10)
    plt.ylim(0, 10)
    plt.show()

start_point = (0.5, 0.5)
goal_point = (9.5, 9.5)
obstacles_list = [(3, 3, 4, 4), (6, 6, 7.5, 7.5)]  # List of rectangular obstacles (x_min, y_min, x_max, y_max)

voronoi_a_star_path(start_point, goal_point, obstacles_list)

start_point_1 = (2, 5)
goal_point_1 = (9.75, 2)
obstacles_list_1 = [(1, 1, 2, 2), (5, 5, 8, 8)]  # List of rectangular obstacles (x_min, y_min, x_max, y_max)

voronoi_a_star_path(start_point_1, goal_point_1, obstacles_list_1)