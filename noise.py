from utils.geometry import euclidean_distance 
import numpy as np

def gen_rain(zones, zone_size):
    return [(float(coord[0]), float(coord[1]), float(zone_size)) for coord in (np.random.rand(2) * zone_size for _ in range(zones))]

def gen_rain(zones, zone_size, area_size= (40,40), min_distance=5):
    rain_clusters = []
    
    while len(rain_clusters) < zones:
        # Generate a random (x, y) within the area_size
        x, y = np.random.uniform(0, area_size[0]), np.random.uniform(0, area_size[1])
        
        
        too_close = False
        for existing_cluster in rain_clusters:
            dist = np.sqrt((x - existing_cluster[0]) ** 2 + (y - existing_cluster[1]) ** 2)
            if dist < min_distance:
                too_close = True
                break
        
        
        if not too_close:
            rain_clusters.append((x, y, zone_size))
    
    return rain_clusters
def add_rain(graph, rainy_areas):
    """
    Adds increased travel cost to edges passing through rain regions.
    
    Parameters:
        graph (dict): The graph structure with nodes and edges.
        rainy_areas (list of tuples): [(x, y, radius), ...] representing rain patches.

    Returns:
        dict: Updated graph with increased costs on rainy edges.
    """
    new_graph = {}

    for node in graph:
        new_graph[node] = []
        for neighbor in graph[node]:  # Ensure neighbor is (x, y)
            base_cost = euclidean_distance(node, neighbor)
            
            # Check if the edge (node → neighbor) crosses any rain region
            for rain_x, rain_y, rain_radius in rainy_areas:
                dist_to_rain = euclidean_distance((rain_x, rain_y), node)
                dist_to_rain_neigh = euclidean_distance((rain_x, rain_y), neighbor)

                # If either node is inside rain OR the edge passes through rain
                if dist_to_rain <= rain_radius or dist_to_rain_neigh <= rain_radius:
                    base_cost *= 2  # Increase cost (adjustable factor)
                    break  # No need to check further rain areas for this edge

            # Append the modified cost properly
            new_graph[node].append((neighbor, base_cost))  

    return new_graph
              
print("Rainy Area:", gen_rain(2,3)) #generate random rain locations