import numpy as np

## im using euclidian distance - we may want to compute the langrangian

# Calculate Euclidian Distance
def euclidean_distance(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# See if the point is within an exsiting obstacle
def is_point_in_obstacle(point, obstacles, margin = 0.2):
    for obs in obstacles:
        x_min, y_min, x_max, y_max = obs
        if (x_min - margin <= point[0] <= x_max + margin) and (y_min - margin <= point[1] <= y_max + margin):
            return True
    return False

def generate_valid_point(obstacles, boundary=(0, 10, 0, 10), max_attempts=1000):
    """Generate a random valid point outside obstacles within the given boundary."""
    x_min, x_max, y_min, y_max = boundary
    for _ in range(max_attempts):
        point = (np.random.uniform(x_min, x_max), np.random.uniform(y_min, y_max))
        if not is_point_in_obstacle(point, obstacles):
            return point
    raise RuntimeError("⚠️ Could not find a valid point outside obstacles!")

def generate_valid_start_goal(obstacles, min_distance=3):
    """Generate start and goal points that are valid and sufficiently separated."""
    for _ in range(1000):  # Prevent infinite loop
        start = generate_valid_point(obstacles)
        goal = generate_valid_point(obstacles)
        if np.linalg.norm(np.array(start) - np.array(goal)) > min_distance:  
            return start, goal
    raise RuntimeError("⚠️ Could not find valid start & goal points!")