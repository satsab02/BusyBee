import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d

def plot_path(start, goal, path, vor, obstacles):
    fig, ax = plt.subplots()
    voronoi_plot_2d(vor, ax=ax)

    for obs in obstacles:
        rect = plt.Rectangle((obs[0], obs[1]), obs[2] - obs[0], obs[3] - obs[1], color='red', alpha=0.5)
        ax.add_patch(rect)
    
    if path:
        px, py = zip(*path)
        plt.plot(px, py, 'g-', linewidth=2)
        plt.plot(start[0], start[1], 'go')  # Start 
        plt.plot(goal[0], goal[1], 'ro')   # Goal
        
    plt.xlim(0, 10)
    plt.ylim(0, 10)
    plt.show()