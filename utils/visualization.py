import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.spatial import Voronoi, voronoi_plot_2d

def plot_path(start, goal, path, vor, obstacles):
    fig, ax = plt.subplots()
    voronoi_plot_2d(vor, ax=ax)

    for obs in obstacles:
        rect = plt.Rectangle((obs[0], obs[1]), obs[2] - obs[0], obs[3] - obs[1], color='red', alpha=0.5)
        ax.add_patch(rect)
    
    
        
    ax.plot(start[0], start[1], 'go', markersize = 8, label = "Start")  # Start 
    ax.plot(goal[0], goal[1], markersize = 8, label = "Goal")   # Goal 

    if not path:    
        ax.text(5, 5, "No Path Found!", fontsize=12, color="red", ha="center")  
        plt.show()  
        return
    
    px, py = zip(*path)
    plt.plot(px, py, 'g-', linewidth=2, label = "planned path")
    robot, = ax.plot ([], [], 'bo', markersize = 8, label = "Robot")  # Robot

    def update(frame):
        if frame < len(path):
            robot.set_data(path[frame][0], path[frame][1])
        return robot,

    visualize_path = animation.FuncAnimation(fig, update, frames=len(path), interval=300, blit=True)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.legend()
    plt.show()