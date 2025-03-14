import numpy as np

## im using euclidian distance - we may want to compute the langrangian

# Calculate Euclidian Distance
def euclidean_distance(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# See if the point is within an exsiting obstacle
def is_point_in_obstacle(point, obstacles):
    for obs in obstacles:
        if obs[0] <= point[0] <= obs[2] and obs[1] <= point[1] <= obs[3]:
            return True
    return False