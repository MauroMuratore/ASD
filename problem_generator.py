from grid_generator import GridGenerator, GridUtil
from reach_goal import ReachGoal
from heuristic import Heuristic
from node_state import NodeState
from problem import Problem
import random

class ProblemGenerator:

    def __init__(self, grid_generator: GridGenerator, max_time: int):
        self.adj_list = grid_generator.get_adj_list()
        self.aggl_ratio = grid_generator.obstacles_ratio
        self.aggl_size = grid_generator.agglomerate_size
        # Choose start and end
        self.available_nodes = self.get_available_nodes()
        start_end = random.sample(self.available_nodes, 2)
        self.start = start_end[0]
        self.end = start_end[-1]
        self.available_nodes.remove(self.start)
        self.available_nodes.remove(self.end)

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
    
    def generate_agent(self, start, end, list_agent):
        pb = Problem(self.adj_list, start, end, 1000, self.n_cols, self.aggl_ratio, self.aggl_size, list_agent)
        rg = ReachGoal(pb, Heuristic.TYPE_HEURISTIC[0])
        sol = rg.execute()
        agent = sol.list_node
        return agent
        

    def generate_problem(self, n_agents):
        nodes_start = random.sample(self.available_nodes, n_agents)
        nodes_end = random.sample(self.available_nodes, n_agents)
        list_agent = []
        for i in range(0, n_agents):
            agent = self.generate_agent(nodes_start[i], nodes_end[i], list_agent)
            list_agent.append(agent)

        pb = Problem(self.adj_list, self.start, self.end, self.max_time, self.n_cols, self.aggl_ratio, self.aggl_size, list_agent)
        return pb
        