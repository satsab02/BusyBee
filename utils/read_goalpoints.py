def readgoals(filename):

    goalpoints = []

    with(open(filename, 'r')) as f:
        for line in f:
            path_part, obstacle_part = line.strip().split("|")


            start, goal = path_part.split("->")
            start = tuple(map(float, start.split(",")))
            goal = tuple(map(float, goal.split(",")))

            obstacles = []

            if obstacle_part.strip():
                for obs in obstacle_part.split(";"):
                    obs = tuple(map(float, obs.split(",")))
                    obstacles.append(obs)
        goalpoints.append((start, goal, obstacles))
    return goalpoints