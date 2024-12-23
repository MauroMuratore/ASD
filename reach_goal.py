from typing import List
from collections import deque
from node_state import NodeState
from priority_queue import PriorityQueue
from problem_generator import Problem
from solution import Solution
from heuristic import Heuristic
import math
import time

class ReachGoal:

    def __init__(self, problem: Problem, type_heuristic):
        self.problem = problem
        self.type_heuristic = type_heuristic
        row_end = problem.end // problem.n_col
        col_end = problem.end % problem.n_col
        self.heuristic = Heuristic(type_heuristic, row_end, col_end)
        # Pensare alle strutture dati
        self.closed = []
        self.open =  PriorityQueue()
        NodeState.n_col=problem.n_col


    def execute(self):
        start_node_state = NodeState(self.problem.start, 0)
        self.open.push(start_node_state, self.call_heuristic(start_node_state))
        tic_exe = time.perf_counter()
        # SET UP
        while len(self.open) > 0:
            f_score_current, current_node_state = self.open.pop()
            self.closed.append(current_node_state)
            toc_exe = time.perf_counter()
            if current_node_state.node == self.problem.end:
                t_exe = toc_exe -tic_exe
                list_sol, t_rec = self.recostruct_path(current_node_state, start_node_state)
                solution = Solution(self.type_heuristic, list_sol, t_exe, t_rec, len(self.closed), len(self.open))
                return solution
            
            if toc_exe - tic_exe > self.problem.max_time:
                print("max time limit")
                break

            if current_node_state.time < self.problem.max_time :
                for child_node, weight in self.problem.adj_list[current_node_state.node].items():
                    child_node_state = NodeState(child_node, 
                                                 current_node_state.time +1,
                                                 current_node_state, 
                                                 current_node_state.weight + weight)

                    if child_node_state not in self.closed:
                        traversable = True

                        ## Da aggiungere foreach agent

                        if traversable :
                            if not child_node_state in self.open:
                                f_score_child = self.call_heuristic(child_node_state)
                                self.open.push(child_node_state, f_score_child)
                            else:
                                if self.open[child_node_state].weight > current_node_state.weight + weight:
                                    f_score_child = self.call_heuristic(child_node_state)
                                    del self.open[child_node_state]
                                    self.open.push(child_node_state, f_score_child)
        return Solution(self.type_heuristic, [], -1, -1, -1,-1)
    
    def call_heuristic(self, node_state):
        row_node = node_state.node // self.problem.n_col
        col_node = node_state.node % self.problem.n_col 
        return node_state.weight + self.heuristic.execute(row_node, col_node)

    
    def recostruct_path(self, end_node_state, start_node_state):
        path = deque([end_node_state])
        current_node_state = end_node_state
        tic_rec = time.perf_counter()
        while current_node_state != start_node_state:
            parent_node_state = current_node_state.parent
            path.appendleft(parent_node_state)
            # Da aggiungere i controlli del wait
            current_node_state = parent_node_state
        toc_rec = time.perf_counter()
        time_rec = toc_rec - tic_rec
        return list(path), time_rec