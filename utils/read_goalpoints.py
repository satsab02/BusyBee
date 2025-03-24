from utils.geometry import generate_valid_point, generate_valid_start_goal

def readgoals(filename, boundary=(0, 10, 0, 10)):
    start_points = []
    goal_sets = []

    with open(filename, 'r') as file:
        lines = file.readlines()
        current_goals = []

        for line in lines:
            line = line.strip()

            if line.startswith("Start Points:"):
                start_points = [
                    tuple(map(float, sp.split(','))) 
                    for sp in line.split(":")[1].split('|') 
                    if sp.strip()  # Filter out empty strings
                ]
                for sp in start_points:
                    if not (boundary[0] <= sp[0] <= boundary[1] and boundary[2] <= sp[1] <= boundary[3]):
                        print(f"Warning: Start point {sp} is out of bounds.")

            elif line.startswith("Goal Points:"):
                current_goals = [
                    tuple(map(float, gp.split(','))) 
                    for gp in line.split(":")[1].split('|') 
                    if gp.strip()  # Filter out empty strings
                ]
                for gp in current_goals:
                    if not (boundary[0] <= gp[0] <= boundary[1] and boundary[2] <= gp[1] <= boundary[3]):
                        print(f"Warning: Goal point {gp} is out of bounds.")
                goal_sets.append(current_goals)

    return start_points, goal_sets