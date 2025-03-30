from utils.geometry import euclidean_distance 
import numpy as np

def gen_rain(zones, zone_size):
    return [(float(coord[0]), float(coord[1]), float(zone_size)) for coord in (np.random.rand(2) * zone_size for _ in range(zones))]
def add_rain(graph, rainy_area):
    """
    Adds noise to the graph using predefined rainy areas.
    
    Parameters:
        graph (dict): The graph to which noise will be added.
        rainy_area (list): A list of nodes representing the rainy area.
        
    Returns:
        None: The function modifies the graph in place.
    """
    for node in graph:
        for i, neighbour in enumerate(graph[node]):
            if node in rainy_area or neighbour in rainy_area:
                graph[node][i] = (neighbour, euclidean_distance(node, neighbour) * 1.5)  # Increase cost of rainy area edges

    return graph
              
print("Rainy Area:", gen_rain(2,3)) #generate random rain locations