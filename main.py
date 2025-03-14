from pathfinding import voronoi_a_star_path
from utils.visualization import plot_path
from utils.read_goalpoints import readgoals


if __name__ == '__main__':
    goalpoints = readgoals('goalpoints.txt')
    for start, goal, obstacles in goalpoints:
        path, vor = voronoi_a_star_path(start, goal, obstacles)
        plot_path(start, goal, path, vor, obstacles)
        #print(start, goal, obstacles)




