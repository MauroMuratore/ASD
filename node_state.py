class NodeState:
    n_col = 1

    def __init__(self, node: int, time: int, parent: "NodeState" = None, weight: float = 0):
        self.node = node
        self.time = time
        self.parent = parent 
        self.weight = weight
    
    
    def __eq__(self, other_node):
        if other_node is None:
            return False
        return self.node == other_node.node and self.time == other_node.time

    def __str__(self):
        row_node = self.node // NodeState.n_col
        col_node = self.node % NodeState.n_col
        return f'{row_node}x{col_node} - {self.time} - {self.weight}'

    def __lt__(self, other_node):
        return self.weight < other_node.weight
    
    def __le__(self, other_node):
        return self.weight<= other_node.weight
