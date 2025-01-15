from grid_generator import GridGenerator, GridUtil
from problem_generator import ProblemGenerator
from problem import Problem
from reach_goal import ReachGoal
from report import Report
from heuristic import Heuristic
import time
import os

def generate_benchmark():
    for n_row in range(25, 50, 25):
        for n_col in range(n_row, 50, 25):
            for obs_ratio in range(1,2,1):
                for aggl_size in range(1,2):
                    for i in range(0,1):
                        tic = time.perf_counter()
                        gg = GridGenerator(n_row, n_col, obs_ratio/10, aggl_size)
                        grid_name =f'{n_row}x{n_col}_{obs_ratio/10}_{aggl_size}_{i}' 
                        export_grid = True
                        for agent in range(1,2):
                            pg = ProblemGenerator(gg, agent, n_col*2)
                            problem = pg.generate_problem()
                            name = grid_name + f"_{agent}"
                            problem.export_problem(name, grid_name, export_grid)
                            export_grid=False
                        toc = time.perf_counter()
                        print(f'Generation time: {toc-tic}s for 5 problem of {grid_name} grid')


def execute_benchmark(list_file):
    tic_tot = time.perf_counter()
    for filename in list_file:
        problem_name = filename.replace(".prob", "")
        problem = Problem.import_problem(problem_name)
        for heu in Heuristic.TYPE_HEURISTIC:
            reach_goal = ReachGoal(problem, type_heuristic=heu)
            tic = time.perf_counter()
            solution=reach_goal.execute()
            print(solution)
            toc = time.perf_counter()
            report = Report(problem, solution)
            report_name = problem_name + "_" + heu
            report.export_report(report_name)
            report.export_csv()
            print(f'Execution time: {toc-tic} of {report_name}')
    toc_tot = time.perf_counter()
    print(f'Total time execution: {toc_tot - tic_tot}')

generate_benchmark()
#list_file = []
#list_file =  os.listdir('./data/problem')
#list_file.sort()
#list_file.append("100x100_0.4_4_0.prob")
#list_file.append("100x100_0.4_4_1.prob")
#list_file.append("100x100_0.4_4_2.prob")
#list_file.append("100x100_0.4_3_0.prob")
#execute_benchmark(list_file)
#pg = ProblemGenerator(25,25,0.1,1,100)
#pb = pg.generate_problem()
#reach_goal = ReachGoal(pb, "d_chess_king")
#solution = reach_goal.execute()

#report = Report(pb, solution)
#report.export_report("test", verbose=True)
#report.export_csv(verbose=True)

#gg = GridGenerator(10,10,0.1,2)
#pg = ProblemGenerator(gg, 7, 100)
#problem = pg.generate_problem()
#problem.export_problem("test", "test", True)
#problem2 = Problem.import_problem("test.prob")
#rg = ReachGoal(problem2, Heuristic.TYPE_HEURISTIC[0])
#solution = rg.execute()
#print(solution)
#report = Report(problem2, solution)
#report.export_report("test", True)
#report.export_csv(True)