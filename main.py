from grid_generator import GridGenerator, GridUtil
from problem_generator import ProblemGenerator
from problem import Problem
from reach_goal import ReachGoal
from report import Report
from heuristic import Heuristic
import time
import os

def generate_benchmark():
    command = input("Verranno generati 1200 problemi di dimensione crescente, continuare? (S/n)")
    if command == "S":
        for n_row in range(10, 60, 10):
            for n_col in range(n_row, 60, 10):
                for obs_ratio in range(10, 50,10):
                    for aggl_size in range(1, 5):
                        tic = time.perf_counter()
                        gg = GridGenerator(n_row, n_col, obs_ratio/100, aggl_size)
                        grid_name =f'{n_row}x{n_col}_{obs_ratio/100}_{aggl_size}' 
                        export_grid = True
                        pg = ProblemGenerator(gg, n_col*2)
                        for n_agent in range(0,5):
                            problem = pg.generate_problem(n_agent)
                            name = grid_name + f"_{n_agent}"
                            problem.export_problem(name, grid_name, export_grid)
                            export_grid=False
                        toc = time.perf_counter()
                        print(f'Generation time: {toc-tic}s for 5 problem of {grid_name} grid')


def resolve_benchmark():
    list_file =  os.listdir('./data/problem')
    list_file.sort()
    command = input(f'Verranno risolti {len(list_file)} problemi, continuare? (S/n)')
    if command == "S":
        tic_tot = time.perf_counter()
        for filename in list_file:
            problem_name = filename.replace(".prob", "")
            problem = Problem.import_problem(problem_name)
            for heu in Heuristic.TYPE_HEURISTIC:
                reach_goal = ReachGoal(problem, type_heuristic=heu)
                tic = time.perf_counter()
                solution=reach_goal.execute()
                toc = time.perf_counter()
                report = Report(problem, solution)
                report_name = problem_name + "_" + heu
                report.export_report(report_name)
                report.export_csv()
                print(f'Execution time: {toc-tic} of {report_name}')
        toc_tot = time.perf_counter()
        print(f'Total time execution: {toc_tot - tic_tot}')

def input_generate_problem():
    dict_return = {}
    dict_return["n_row"] = int(input("Numero di righe \n"))
    dict_return["n_col"] = int(input("Numero di colonne \n"))
    dict_return["aggl_ratio"] = float(input("Percentuali di ostacoli \n")) / 100
    dict_return["aggl_size"] = int(input("Inserire dimensione degli agglomerati \n"))
    dict_return["n_agent"] = int(input("Numero di agenti preesistenti \n"))
    dict_return["t_max"] = int(input("Tempo massimo \n"))
    dict_return["name"] = input("Inserisci nome del file \n")
    return dict_return

def generate_problem():
    print("Inserisci i seguenti valori per generare il problema")
    in_problem = input_generate_problem()
    gg = GridGenerator(in_problem["n_row"], in_problem["n_col"], in_problem["aggl_ratio"], in_problem["aggl_size"])
    pg = ProblemGenerator(gg, in_problem["t_max"])
    problem = pg.generate_problem(in_problem["n_agent"])
    problem.export_problem(in_problem["name"], in_problem["name"], True)

def resolve_problem():
    name = input("Inserisci nome del file del problema da risolvere \n")
    problem = Problem.import_problem(name)
    rg = ReachGoal(problem, Heuristic.TYPE_HEURISTIC[0])
    solution = rg.execute()
    print(solution)
    report = Report(problem, solution)
    report.export_report(name, True)
    report.export_csv(True)

def generate_resolve_problem():
    print("Inserisci i seguenti valori per generare e risolvere il problema")
    in_problem = input_generate_problem()
    gg = GridGenerator(in_problem["n_row"], in_problem["n_col"], in_problem["aggl_ratio"], in_problem["aggl_size"])
    pg = ProblemGenerator(gg, in_problem["t_max"])
    problem = pg.generate_problem(in_problem["n_agent"])
    problem.export_problem(in_problem["name"], in_problem["name"], True)
    rg = ReachGoal(problem, Heuristic.TYPE_HEURISTIC[0])
    solution = rg.execute()
    print(solution)
    report = Report(problem, solution)
    report.export_report(in_problem["name"], True)
    report.export_csv(True)

help = "Comandi: \n"
help += "1 - Genera un problema \n"
help += "2 - Risolvi un problema \n"
help += "3 - Genera e risolvi un problema \n"
help += "4 - Genera una lista di problemi \n"
help += "5 - Risolvi tutti i problemi presenti nella directory 'data/problem' \n"
help += "0 - Esci \n \n"
help += "La lista dei problemi si trovano nella cartella 'data/problem' \n"
help += "Scegli: "

if __name__=="__main__":
    while True:
        print("\n\n\n")
        command = input(help)
        if command == "0":
            break
        elif command == "1":
            generate_problem()
        elif command == "2":
            resolve_problem()
        elif command == "3":
            generate_resolve_problem()
        elif command == "4":
            generate_benchmark()
        elif command == "5":
            resolve_benchmark()
        else:
            continue
    