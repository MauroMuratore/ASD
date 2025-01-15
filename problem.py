from grid_generator import GridUtil
from node_state import NodeState

class Problem:

    def __init__(self, adj_list, start, end, max_time, n_col, aggl_ratio, aggl_size, list_agent):
        self.adj_list = adj_list
        self.start = start 
        self.end = end
        self.max_time = max_time 
        self.n_col = n_col
        self.aggl_ratio = aggl_ratio
        self.aggl_size = aggl_size
        self.list_agent = list_agent

    def export_problem(self, name, name_grid, export_grid):
        filename = "./data/problem/" + name + ".prob"
        with open(filename, "w") as file:
            file.write("start=" + str(self.start) + "\n")
            file.write("end=" + str(self.end) + "\n")
            file.write("max_time="+ str(self.max_time) + "\n")
            file.write("n_col=" + str(self.n_col)+"\n")
            file.write("agg_ratio=" +str(self.aggl_ratio) + "\n")
            file.write("agg_size="+ str(self.aggl_size)+ "\n")
            for agent in self.list_agent:
                file.write("agent=")
                for state in agent:
                    file.write(str(state) + ", ")
                file.write("\n")
            file.write("name_grid=" +name_grid)
        if export_grid:
            GridUtil.export_adj(self.adj_list, name_grid)

    def import_problem(name):
        filename = name 
        if not "./data/problem/" in name:
            filename = "./data/problem/" + name 
        if not ".prob" in name :
            filename = filename + ".prob"

        list_agent = []

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
                elif "agent" in line:
                    agent_str = line.split("=")[-1]
                    states = agent_str.split(",")
                    agent = []
                    for s in states:
                        comp_s = s.split("-")
                        coord_node = comp_s[0].strip().split("x")
                        if coord_node[0] == "":
                            break
                        node = int(coord_node[0])*int(coord_node[1])
                        time = int(comp_s[1].strip())
                        agent.append(NodeState(node, time))

                    list_agent.append(agent)

        return Problem(adj_list, start, end, max_time, n_col, agg_ratio, agg_size, list_agent)
    
    def __str__(self):
        row_start = self.start // self.n_col
        row_end = self.end // self.n_col
        col_start = self.start % self.n_col
        col_end = self.end % self.n_col
        n_row = int(len(self.adj_list)/self.n_col)
        str_return = f'Start: ({row_start}x{col_start}) \n'
        str_return += f'End: ({row_end}x{col_end}) \n'
        str_return += f'Max_time: {self.max_time}  \n'
        str_return += f'N_row: {n_row}\n'
        str_return += f'N_col: {self.n_col}\n'
        str_return += f'Aggl_ratio: {self.aggl_ratio} \n'
        str_return += f'Aggl_size: {self.aggl_size}\n'
        str_return += f'N_agent:{len(self.list_agent)}\n'
        for agent in self.list_agent:
            str_return += "Agent:[ "
            for state in agent:
                str_return += str(state) + ", "
            str_return += "] \n"
        return str_return

    def str_csv(self):
        n_row = int(len(self.adj_list)/self.n_col)
        row_start = self.start // self.n_col
        row_end = self.end // self.n_col
        col_start = self.start % self.n_col
        col_end = self.end % self.n_col
        str_return = f'{n_row};'
        str_return += f'{self.n_col};'
        str_return += f'({row_start}x{col_start});'
        str_return += f'({row_end}x{col_end});'
        str_return += f'{self.max_time};'
        str_return += f'{self.aggl_ratio:0.2f};'
        str_return += f'{self.aggl_size};'
        str_return += f'{len(self.list_agent)};'
        return str_return
    
    def col_name_csv():
        return 'Row;Column;Start;End;Max_time;Aggl_ratio;Aggl_size;N_agent;'