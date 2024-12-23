class Solution:

    def __init__(self, heuristic, list_node, t_execute, t_reconstruct, close_len, open_len):
        self.heuristic = heuristic
        self.list_node = list_node
        self.t_execute = t_execute
        self.t_reconstruct = t_reconstruct
        self.close_len = close_len
        self.open_len = open_len
        if len(list_node) > 0:
            end_node = list_node[-1]
            self.weight = end_node.weight
        else:
            self.weight = -1 
    def str_csv(self):
        return f'{self.heuristic};{len(self.list_node)};{self.weight};{self.t_execute*1000:0.4f};{self.t_reconstruct*1000:0.4f};{self.close_len};{self.open_len};'
    
    def __str__(self):
        str_return = f'Heuristic: {self.heuristic}\n'
        str_return += f'Lenght solution: {len(self.list_node)}\n'
        str_return += f'Weight solution: {self.weight}\n'
        str_return += f'Solution: {[str(x) for x in self.list_node]}\n'
        str_return += f'Execution time(ms): {self.t_execute*1000:0.4f}\n'
        str_return += f'Reconstruct time(ms): {self.t_reconstruct*1000:0.4f}\n'
        str_return += f'Lenght close: {self.close_len}\n'
        str_return += f'Lenght open: {self.open_len}\n'
        return str_return

    def col_name_csv():
        return 'Heuristic;Lenght_solution;Weight_solution;Execution_time(ms);Reconstruct_time(ms);Lenght_close;Lenght_open;'
    
