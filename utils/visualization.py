import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.spatial import Voronoi, voronoi_plot_2d

def plot_path(paths, start_positions, goal_clusters, rain):
    fig, ax = plt.subplots()
    ax.set_xlim(0, 40)
    ax.set_ylim(0, 40)

    colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange']
    robots = []

    # Plot start points
    for i, start in enumerate(start_positions):
        ax.plot(start[0], start[1], 'go', markersize=10, label="Start" if i == 0 else "")  # Green for start points

    #plot rain points
    for i, rain_point in enumerate(rain):
        circle = plt.Circle((rain_point[0], rain_point[1]), rain_point[2], color='red', alpha=0.5, label="Rain" if i == 0 else "")
        ax.add_patch(circle)
    # Plot goal points
    goal_plotted = False
    for i, goals in enumerate(goal_clusters):
        for goal in goals:
            ax.plot(goal[0], goal[1], 'bo', markersize=8, label="Goal" if not goal_plotted else "")  # Blue for goal points
            goal_plotted = True

    # Plot paths and initialize robots
    for i, path in enumerate(paths):
        if not path:  # Skip empty paths
            print(f"Skipping empty path for start position {start_positions[i]}.")
            continue

        x_pos, y_pos = zip(*path)  # Unpack path into x and y coordinates
        ax.plot(x_pos, y_pos, '--', alpha=0.5, color=colors[i % len(colors)], label=f"Path {i + 1}")
        robot, = ax.plot([], [], 'o', markersize=8, color=colors[5], label=f"Robot {i + 1}")
        robots.append((robot, x_pos, y_pos))

    def update(frame):
    # Get the x and y position for the current frame
        x_data = x_pos[frame]  # Get the current x position
        y_data = y_pos[frame]  # Get the current y position

        # Pass x_data and y_data as lists (sequences) for the set_data function
        robot.set_data([x_data], [y_data])  # Make sure to pass them as sequences

 
    fps = 7
    if robots:  # Ensure there are robots to animate
        max_frames = max(len(x_pos) for _, x_pos, _ in robots)
        time = max_frames / fps  # Calculate the time duration for the animation
        print(f"Animation time: {time:.2f} seconds")
        ani = animation.FuncAnimation(fig, update, frames=max_frames, interval=300, repeat=False)
        ani.save('Animations/path_animation.gif', writer='pillow', fps=7)  # Save the animation as a video file
        ax.legend()
        plt.show()
    else:
        print("No valid paths to animate.")