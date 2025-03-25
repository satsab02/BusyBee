from pathfinding import multi_goal_a_star, build_graph
from utils.visualization import plot_path
from utils.read_goalpoints import readgoals


# Preprocess paths to ensure all coordinates are Python floats
def preprocess_paths(paths):
    return [[(float(x), float(y)) for x, y in path] for path in paths]

start_positions, goal_clusters = readgoals("goalpoints.txt")
print(start_positions)
print(goal_clusters)
graph = build_graph(start_positions, goal_clusters)  # Generate A* graph
paths = []
for start, goals in zip(start_positions, goal_clusters):
    path = multi_goal_a_star(graph, start, goals)
    paths.append(path)

# Convert all numpy.float64 values in paths to Python float
paths = preprocess_paths(paths)
plot_path(paths, start_positions, goal_clusters)



