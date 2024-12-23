from grid_generator import GridGenerator, GridUtil
import random

class ProblemGenerator:

    def __init__(self, grid_generator: GridGenerator, max_time: int):
        # Create the grid
        #self.gg = GridGenerator(n_rows, n_cols, obstacles_ratio, agglomerate_size)
        self.adj_list = grid_generator.get_adj_list()
        self.aggl_ratio = grid_generator.obstacles_ratio
        self.aggl_size = grid_generator.agglomerate_size

        # Choose start and end
        self.available_nodes = self.get_available_nodes()

        self.n_cols = grid_generator.n_cols

        # Set maximum time
        self.max_time = max_time

    def get_available_nodes(self):
        available_nodes = []
        index = 0
        for node_adj_list in self.adj_list:
            if len(node_adj_list) > 0:
                available_nodes.append(index)
            index = index + 1

        return available_nodes

    def generate_problem(self):
        nodes = random.choices(self.available_nodes, k=2)
        start = nodes[0]
        end = nodes[-1]
        pb = Problem(self.adj_list, start, end, self.max_time, self.n_cols, self.aggl_ratio, self.aggl_size)
        return pb
        
class Problem:

    def __init__(self, adj_list, start, end, max_time, n_col, aggl_ratio, aggl_size):
        self.adj_list = adj_list
        self.start = start 
        self.end = end
        self.max_time = max_time 
        self.n_col = n_col
        self.aggl_ratio = aggl_ratio
        self.aggl_size = aggl_size

    def export_problem(self, name, name_grid, export_grid):
        filename = "./data/problem/" + name + ".prob"
        with open(filename, "w") as file:
            file.write("start=" + str(self.start) + "\n")
            file.write("end=" + str(self.end) + "\n")
            file.write("max_time="+ str(self.max_time) + "\n")
            file.write("n_col=" + str(self.n_col)+"\n")
            file.write("agg_ratio=" +str(self.aggl_ratio) + "\n")
            file.write("agg_size="+ str(self.aggl_size)+ "\n")
            file.write("name_grid=" +name_grid)
        if export_grid:
            GridUtil.export_adj(self.adj_list, name_grid)

    def import_problem(name):
        filename = name 
        if not "./data/problem/" in name:
            filename = "./data/problem/" + name 
        if not ".prob" in name :
            filename = filename + ".prob"

        with open(filename) as file:
            for line in file:
                if "start" in line:
                    start = int(line.split("=")[-1])
                elif "end" in line:
                    end = int(line.split("=")[-1])
                elif "max_time" in line :
                    max_time = int(line.split("=")[-1])
                elif "n_col" in line :
                    n_col = int(line.split("=")[-1])
                elif "agg_ratio" in line:
                    agg_ratio = float(line.split("=")[-1])
                elif "agg_size" in line:
                    agg_size = int(line.split("=")[-1])
                elif "name_grid" in line:
                    name_grid = line.split("=")[-1]
                    adj_list = GridUtil.import_adj(name_grid)

        return Problem(adj_list, start, end, max_time, n_col, agg_ratio, agg_size)
    
    def __str__(self):
        row_start = self.start // self.n_col
        row_end = self.end // self.n_col
        col_start = self.start % self.n_col
        col_end = self.end % self.n_col
        n_row = int(len(self.adj_list)/self.n_col)
        return f'Start: ({row_start}x{col_start}) \nEnd: ({row_end}x{col_end}) \nMax_time: {self.max_time}  \nN_row: {n_row}\nN_col: {self.n_col}\nAggl_ratio: {self.aggl_ratio} \nAggl_size: {self.aggl_size}\n'

    def str_csv(self):
        n_row = int(len(self.adj_list)/self.n_col)
        row_start = self.start // self.n_col
        row_end = self.end // self.n_col
        col_start = self.start % self.n_col
        col_end = self.end % self.n_col
        return f'{n_row};{self.n_col};({row_start}x{col_start});({row_end}x{col_end});{self.max_time};{self.aggl_ratio:0.2f};{self.aggl_size};'
    
    def col_name_csv():
        return 'Row;Column;Start;End;Max_time;Aggl_ratio;Aggl_size;'