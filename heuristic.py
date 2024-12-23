import math
class Heuristic:

    TYPE_HEURISTIC =["d_chess_king", "d_chebyshev", "d_manhattan", "d_euclidean"]
    DISTANCE_DIAGONAL = math.sqrt(2)
    DISTANCE_AXIS = 1

    def __init__(self, type, row_end, col_end):
        self.type = type 
        self.row_end = row_end
        self.col_end = col_end 
    
    def execute(self, row_node, col_node):
        if self.type == Heuristic.TYPE_HEURISTIC[0]:
            return self.d_chess_king(row_node, col_node)
        elif self.type == Heuristic.TYPE_HEURISTIC[1]:
            return self.d_chebyshev(row_node, col_node)
        elif self.type == Heuristic.TYPE_HEURISTIC[2]:
            return self.d_manhattan(row_node, col_node)
        elif self.type == Heuristic.TYPE_HEURISTIC[3]:
            return self.d_euclidean(row_node, col_node)
    
    def d_chess_king(self, row_node, col_node):
        dif_min = min(
            abs(row_node - self.row_end),
            abs(col_node - self.col_end)
        )
        dif_max = max(
            abs(row_node - self.row_end),
            abs(col_node - self.col_end)
        )
        distance = Heuristic.DISTANCE_DIAGONAL * dif_min + Heuristic.DISTANCE_AXIS *(dif_max-dif_min)
        return distance
    
    def d_chebyshev(self, row_node, col_node):
        distance = max(
            abs(row_node - self.row_end),
            abs(col_node - self.col_end)
        )
        return distance
    
    def d_manhattan(self, row_node, col_node):
        distance = abs(row_node -self.row_end) + abs(col_node - self.col_end)
        return distance
    
    def d_euclidean(self, row_node, col_node):
        distance = math.sqrt((row_node - self.row_end)**2 + (col_node - self.col_end)**2)
        return distance