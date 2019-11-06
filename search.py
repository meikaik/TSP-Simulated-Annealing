import math, random, sys, tsp
import matplotlib.pyplot as plt



def gen_random_path(nodes):
    """
    Generate a random TSP tour originating and ending at the same location
    
    Input: Nodes [a, b, c, d, e]
    
    Output: Path [e, d, c, a, b, e]
    """
    shuffled = random.sample(nodes, len(nodes))
    shuffled.append(shuffled[0])
    path = tsp.Path(shuffled, 0)
    path.update_dist()
    return path



def accept(current_path, new_path, temp):
    """
    P(e, e', T) = 1 if e' < e, and exp(-(e' - e)/T) otherwise
    """
    if new_path.dist < current_path.dist:
        return 1
    return math.exp(-(new_path.dist - current_path.dist) / temp)


def simulated_annealing(nodes, type, initial_temp, cooling_rate):
    current_path = gen_random_path(nodes)
    best_path = tsp.Path(current_path.nodes, current_path.dist)
    if len(nodes) <= 2:
        return current_path

    current_path_arr = []
    i = 1
    current_path_arr_size = 0
    temp = initial_temp
    while temp > 0.001:
        new_path = tsp.Path(current_path.nodes, current_path.dist)

        # Swap 2 random nodes between new_path[1 to -1] (exclusive)
        idx = range(1, len(nodes) - 1)
        idx_a, idx_b = random.sample(idx, 2)
        new_path.swap_nodes(idx_a, idx_b)

        if accept(current_path, new_path, temp) >= random.uniform(0, 1):
            current_path = tsp.Path(new_path.nodes, new_path.dist)
            current_path_arr.append(current_path.dist)
            current_path_arr_size += 1
            # break early for log function
            if current_path_arr_size == 250:
                break

        if current_path.dist < best_path.dist:
            best_path = tsp.Path(current_path.nodes, current_path.dist)

        if type == "multiply":
            temp *= cooling_rate
        elif type == "log":
            # Geman and Geman
            temp = initial_temp / math.log2(i + 1)
        elif type == "linear":
            temp -= 1 - cooling_rate
        i += 1
    print(i)
    return best_path, current_path_arr


def main():
    if len(sys.argv) != 2:
        return
    filename = sys.argv[1]
    nodes = tsp.parse_nodes(filename)
    args = [["multiply", 1, 0.999980], ["log", 10, 0], ["linear", 1, 0.999995]]
    i = 131
    for arg in args:
        path, current_path_arr = simulated_annealing(nodes, arg[0], arg[1], arg[2])
        print(path)
        plt.subplot(i)
        plt.plot(current_path_arr, label=args[0])
        i += 1
    plt.show()


main()
