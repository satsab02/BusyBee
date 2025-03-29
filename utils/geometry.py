import numpy as np

## im using euclidian distance - we may want to compute the langrangian

# Calculate Euclidian Distance
def euclidean_distance(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

# See if the point is within an exsiting obstacle
def is_point_in_obstacle(point, obstacles, margin = 0.2):
    for obs in obstacles:
        x_min, y_min, x_max, y_max = obs
        if (x_min - margin <= point[0] <= x_max + margin) and (y_min - margin <= point[1] <= y_max + margin):
            return True
    return False

def generate_random_cluster(flowers, x_range, y_range):
    locations_set = []
    x_coords = np.random.uniform(x_range[0], x_range[1], flowers)
    y_coords = np.random.uniform(y_range[0], y_range[1], flowers)

    locations = list(zip(x_coords, y_coords))
    locations = [(float(x), float(y)) for x, y in locations]
    locations_set.append(locations)
    return locations_set