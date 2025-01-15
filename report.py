from grid_generator import GridUtil
from problem_generator import Problem
from solution import Solution
import os.path

class Report:

    def __init__(self, problem, solution):
        self.problem = problem 
        self.solution = solution 
    
    def export_report(self, name, verbose=False):
        report = str(self.problem)
        report += str(self.solution)
        row_start = self.problem.start // self.problem.n_col
        row_end = self.problem.end // self.problem.n_col
        col_start = self.problem.start % self.problem.n_col
        col_end = self.problem.end % self.problem.n_col
        matrix = GridUtil.get_matrix(self.problem.adj_list,self.problem.n_col)

        n_agent =0
        for agent in self.problem.list_agent:
            for state in agent:
                row_s = state.node // self.problem.n_col
                col_s = state.node % self.problem.n_col
                if state.time == 0:
                    matrix[row_s][col_s] = f'AS{n_agent}'
                elif state.time == len(agent)-1:
                    matrix[row_s][col_s] = f'AE{n_agent}'
                else: 
                    matrix[row_s][col_s] = f'A{n_agent:{0}{2}}'
            
            n_agent += 1

        if not self.solution is None:
            for e in self.solution.list_node:
                row_e = e.node // self.problem.n_col
                col_e = e.node % self.problem.n_col
                matrix[row_e][col_e] = f'{e.time:{0}{3}}'

        matrix[row_start][col_start] = "STR"
        matrix[row_end][col_end] = "END"

        report += "Grid:\n"
        for e in matrix:
            report += str(e) + "\n"
        
        if verbose:
            print(report)

        filename = "./data/result/"+name 
        if not ".result" in name:
            filename += ".result"

        with open(filename, "w") as file:
            file.write(report)
    
    def export_csv(self, verbose=False):
        header = Problem.col_name_csv() + Solution.col_name_csv() + "\n"
        csv = self.problem.str_csv()
        if not self.solution is None:
            csv += self.solution.str_csv() + "\n"
        else :
            csv += ";;;;;;;; \n"
        if verbose:
            print(header + csv)

        filename = "./data/result.csv"
        cond_header = os.path.isfile(filename)
        with open(filename, "a+") as file:
            if not cond_header:
                file.write(header)
            file.write(csv) 
