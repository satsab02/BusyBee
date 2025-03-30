from pathfinding import multi_goal_a_star, build_graph
from utils.visualization import plot_path
from utils.read_goalpoints import readgoals
from utils.optimization import kd_tree_graph
from travellingsalesman import optimized_goal_order
from utils.geometry import euclidean_distance, generate_random_cluster
from noise import add_rain, gen_rain

a_star_weight = 0.1  # Weight for A* heuristic

# Preprocess paths to ensure all coordinates are Python floats
def preprocess_paths(paths):
    return [[(float(x), float(y)) for x, y in path] for path in paths]

# Calculate the total distance of a path
def calculate_path_distance(path):
    return sum(euclidean_distance(path[i], path[i + 1]) for i in range(len(path) - 1))

rain = gen_rain(2, 3)  # Generate random rain locations]
flower_locations = generate_random_cluster(20, (0,30), (0,30))  # Generate random flower locations
print("Flower Locations:", flower_locations)
start_positions, goal_clusters = readgoals("goalpoints.txt")
#print("Start Positions:", start_positions)
print("Goal Clusters:", goal_clusters)

graph = kd_tree_graph(start_positions, flower_locations)  # Generate A* graph
graph = add_rain(graph, rain)  # Add noise to the graph
paths = []

for start, goals in zip(start_positions, flower_locations):
    # Calculate path for the given goal order
    print("\nGiven Goal Order:", goals)
    given_path = multi_goal_a_star(graph, start, goals, a_star_weight)
    given_path_distance = calculate_path_distance(given_path)
    print("Given Path Distance:", given_path_distance)

    # Calculate path for the optimized goal order
    '''optimized_goals = optimized_goal_order(start, goals, True)
    print("Optimized Goal Order:", optimized_goals)
    optimized_path = multi_goal_a_star(graph, start, optimized_goals, a_star_weight)
    optimized_path_distance = calculate_path_distance(optimized_path)
    print("Optimized Path Distance:", optimized_path_distance)'''

    # Append the optimized path for visualization
    paths.append(given_path)

# Convert all numpy.float64 values in paths to Python float
paths = preprocess_paths(paths)

# Visualize the paths
plot_path(paths, start_positions, flower_locations, rain)



