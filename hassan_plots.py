import matplotlib.pyplot as plt
from utils.read_goalpoints import readgoals
from utils.geometry import generate_random_cluster
import matplotlib.patches as patches

start_positions, goal_clusters = readgoals("goalpoints.txt")
print("start points", start_positions)
flower_locations = generate_random_cluster(40,(0,40),(0,40))
print("Flower locations:", flower_locations)



fig, ax = plt.subplots()
ax.set_xlim(0, 50)
ax.set_ylim(0, 50)

colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange']


rain_center = (20, 20) 
rain_radius = 7 
rain_circle = patches.Circle(rain_center, rain_radius, color='red', alpha=0.3)  
ax.add_patch(rain_circle)  

# Plot start points
for i, start in enumerate(start_positions):
     ax.plot(start[0], start[1], 'go', markersize=10, label="Start" if i == 0 else "")  # Green for start points

 # Plot goal points
flower_location  = flower_locations[0]
for goals in flower_location:
    ax.plot(goals[0], goals[1], 'bo', markersize=8, label="Goal" if i == 0 else "")  # Red for goal points


# ax.set_title("10x10 square meter region with star cluster")
# ax.grid(True, linestyle="--", alpha=0.5)
ax.legend()
plt.show()