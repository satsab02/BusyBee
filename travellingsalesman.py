from utils.geometry import euclidean_distance
import numpy as np
from itertools import permutations

def brute_force_tsp(start, goals):
    '''Solves the travelling salesman problem using brute force.
    The issue with this method is that is terrible for large number of points due to O(n!) complexity'''

    best_order = None #initialize the best order
    best_distance = float('inf') #initialize the best distance to infinity

    #For loop to cycle through all possible arrangments of goalpoints to determine shortest path
    for config in permutations(goals):
        path = [start] + list(config) #add the start point to the list of points
        total_distance = sum(euclidean_distance(path[i], path[i+1]) for i in range(len(path)-1)) #calculate the total distance of the path

        if total_distance < best_distance:
            best_distance = total_distance
            best_order = config
    
    return(list(best_order))

def optimized_goal_order(start, goals):
    '''This function uses the brute force method to determine the best order of goalpoints to visit'''
    return brute_force_tsp(start, goals)