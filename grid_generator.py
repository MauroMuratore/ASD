import math
import random

class GridGenerator:

    def __init__(self, n_rows: int, n_cols: int, obstacles_ratio: float, agglomerate_size: int):
        # Create nodes and empty adjacency list
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.size = n_rows * n_cols 
        self.nodes = [ node for node in range(0, self.size)]
        self.adj_list = [ {} for node in self.nodes]
        self.obstacles_ratio = obstacles_ratio
        self.agglomerate_size = agglomerate_size

        self.fill_adjacency_list()
        self.generate_obstacles()

    def fill_adjacency_list(self):
        """
        To populate adjacency lists for each node, only look in the North-East, East, South-East, and South directions.
        Add the adjacent node to the list and add the current node to the adjacent node's list.
        """
        axis_weight = 1
        diagonal_weight = math.sqrt(2)
        for node in self.nodes: 
            i_node = node // self.n_cols
            j_node = node % self.n_cols
            # East
            if j_node < self.n_cols - 1:
                e_node = node + 1
                self.add_edge(node, e_node, axis_weight)
                # North-East
                if i_node > 0:
                    ne_node = node - self.n_cols + 1
                    self.add_edge(node, ne_node, diagonal_weight)
                # South-East
                if i_node < self.n_rows -1:
                    se_node = node + self.n_cols + 1
                    self.add_edge(node, se_node, diagonal_weight)
            # South
            if i_node < self.n_rows -1:
                s_node = node + self.n_cols
                self.add_edge(node, s_node, axis_weight)

    def add_edge(self, node_0, node_1, weight):
        self.adj_list[node_0][node_1]=weight
        self.adj_list[node_1][node_0]=weight

    def generate_obstacles(self):
        """
        Generates clusters of obstacles on the grid.
        - For each cluster to be created:
            - Randomly selects a `start` node from `available_nodes` to initiate the cluster.
            - Expands the cluster (`agglomerate`) by repeatedly finding available neighbors of the current node,
            selecting one at random, and adding it to the cluster.
            - Stops expanding if no neighbors are available or cluster is big enough.
        - Once a cluster is built, all nodes in the cluster (`agglomerate`) and their available neighbors 
        are removed from `available_nodes` to prevent overlap.
        """

        available_nodes = self.nodes.copy()
        n_agglomerate = math.ceil(self.size * self.obstacles_ratio / self.agglomerate_size)
        for _i in range(0,n_agglomerate) :
            if len(available_nodes) == 0:
                break
            
            current_node = random.choice(available_nodes)
            available_nodes.remove(current_node)
            agglomerate = [current_node]

            for _i in range(0, self.agglomerate_size-1) :
                available_neighbours = self.get_available_neighbours(current_node, available_nodes) 
                if len(available_neighbours) == 0:
                    break
                current_node = random.choice(available_neighbours)
                available_nodes.remove(current_node)
                agglomerate.append( current_node)
            
            for node in agglomerate :
                available_neighbours = self.get_available_neighbours(node, available_nodes)
                for neighbour in available_neighbours :
                    available_nodes.remove(neighbour)
                self.insert_obstacle(node)
                
    
    def insert_obstacle (self, node_obstacle):
        neighbour_nodes = list(self.adj_list[node_obstacle].keys())
        self.adj_list[node_obstacle] = {}
        for linked_node in neighbour_nodes :
            del self.adj_list[linked_node][node_obstacle]


    def get_available_neighbours(self, node, available_nodes):
        available_neighbours = []
        for key_node in list(self.adj_list[node].keys()):
            if key_node in available_nodes and self.adj_list[node][key_node] <= 1:
                available_neighbours.append(key_node)

        return available_neighbours
    

    def get_adj_list(self):
        return self.adj_list
    
    
class GridUtil:

    def export_adj(adj_list, name):
        filename = "./data/adj_list/" + name +".grid"
        with open(filename, "w") as file:
            for node in range(0, len(adj_list)):
                for link_node in adj_list[node]:
                    file.write(str(link_node) + "," + str(adj_list[node][link_node]) + ";")
                file.write("\n")

    def import_adj(name):
        filename = name 
        if not "./data/adj_list/" in name:
            filename = "./data/adj_list/" + name 
        if not ".grid" in name :
            filename = filename + ".grid"
            
        adj_list = []
        with open(filename) as file:
            for line in file:
                adj_list.append({})
                for edge in line.split(";"):
                    if not "," in edge:
                        break
                    node, weight = edge.split(",", 2)
                    adj_list[-1][int(node)] = float(weight)

        return adj_list
    
    def get_matrix(adj_list, n_col):
        n_row = len(adj_list) // n_col
        matrix = [["___" for _ in range(0, n_col)] for _ in range(0, n_row)]
        for node in range(0, len(adj_list)) :
            if len(adj_list[node]) == 0 :
                i_node = node // n_col
                j_node = node % n_col
                matrix[i_node][j_node] = "X-X"
        
        return matrix