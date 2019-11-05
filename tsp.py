import math


# Calculate the Euclidian Distance
# sqrt( (x1-x2)^2 + (y1-y2)^2 )
def euclidean_distance(p1, p2):
    return math.sqrt(math.pow((p1.x - p2.x), 2) + math.pow((p1.y - p2.y), 2))


# Given filename, return list of Nodes
def parse_nodes(filename):
    nodes = []
    with open(filename) as file:
        for row in file:
            col = row.split()
            if len(col) == 3:
                nodes.append(Node(col[0], col[1], col[2]))
    return nodes


class Node:
    def __init__(self, id, x, y):
        self.id = id
        self.x = int(x)
        self.y = int(y)


class Path:
    def __init__(self, nodes, dist):
        self.nodes = list(nodes)
        self.dist = dist

    def __repr__(self):
        path = ""
        for node in self.nodes:
            path += node.id + ","
        return "Cost: {}, Path: {}".format(self.dist, path)

    def swap_nodes(self, idx_a, idx_b):
        self.nodes[idx_a], self.nodes[idx_b] = self.nodes[idx_b], self.nodes[idx_a]
        self.update_dist()

    def update_dist(self):
        self.dist = 0
        for i in range(len(self.nodes) - 1):
            self.dist += euclidean_distance(self.nodes[i], self.nodes[i + 1])
