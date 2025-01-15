from grid_generator import GridGenerator, GridUtil
from reach_goal import ReachGoal
from heuristic import Heuristic
from node_state import NodeState
from problem import Problem
import random

class ProblemGenerator:

    def __init__(self, grid_generator: GridGenerator, n_agents: int, max_time: int):
        self.adj_list = grid_generator.get_adj_list()
        self.aggl_ratio = grid_generator.obstacles_ratio
        self.aggl_size = grid_generator.agglomerate_size
        self.n_agents = n_agents
        self.list_agent = []
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
    
    def generate_agent(self, start, end):
        pb = Problem(self.adj_list, start, end, 1000, self.n_cols, self.aggl_ratio, self.aggl_size, self.list_agent)
        rg = ReachGoal(pb, Heuristic.TYPE_HEURISTIC[2])
        sol = rg.execute()
        agent = sol.list_node
        self.list_agent.append(agent)

    def generate_problem(self):
        nodes_start = random.sample(self.available_nodes, self.n_agents+1)
        nodes_end = random.sample(self.available_nodes, self.n_agents+1)
        for i in range(0, self.n_agents):
            self.generate_agent(nodes_start[i], nodes_end[i])

        start = nodes_start[-1]
        end = nodes_end[-1]
        pb = Problem(self.adj_list, start, end, self.max_time, self.n_cols, self.aggl_ratio, self.aggl_size, self.list_agent)
        return pb
        