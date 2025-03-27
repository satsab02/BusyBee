import numpy as np
from scipy.spatial import KDTree
from utils.geometry import euclidean_distance

def kd_tree_graph(start, goals, random_points=100, k_neighbours=5):

    graph = {} #initialize graph

    req_points = start + [goal for cluster in goals for goal in cluster] #ensures our given start and end points are included in the graph
    random_points = np.random.rand(random_points, 2) * 10 #generates random points in a 10x10 area
    req_points.extend(map(tuple, random_points)) #adds random points to the list of required points by converting the np array to a tuple using map

    kd_tree = KDTree(req_points) #creates a KDTree object with the required points

    for point in req_points:
        graph[point] = [] #initialize the graph with the required points
        distance, indices = kd_tree.query(point, k=k_neighbours + 1) #finds the k nearest neighbours to the point. +1 to avoid adding self
        for index in indices[1:]: #skips the first element which is the point itself
            graph[point].append(tuple(req_points[index])) #adds the k nearest neighbours to the graph

    return graph