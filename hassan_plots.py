import matplotlib.pyplot as plt
from utils.read_goalpoints import readgoals

start_positions, goal_clusters = readgoals("goalpoints.txt")
print("start points", start_positions)
print("goal points", goal_clusters)

fig, ax = plt.subplots()
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)

colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange']

# Plot start points
for i, start in enumerate(start_positions):
     ax.plot(start[0], start[1], 'go', markersize=10, label="Start" if i == 0 else "")  # Green for start points

 # Plot goal points
for i, goals in enumerate(goal_clusters):
     for goal in goals:
         ax.plot(goal[0], goal[1], 'bo', markersize=8, label="Goal" if i == 0 else "")  # Red for goal points


ax.set_title("10x10 square meter region with star cluster")
ax.grid(True, linestyle="--", alpha=0.5)
ax.legend()
plt.show()