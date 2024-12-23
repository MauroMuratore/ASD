import heapq

class PriorityQueue:

    def __init__(self):
        self.list = []


    def push(self, node_state, f_score: float):
        heapq.heappush(self.list, (f_score, node_state))

    def pop(self): 
        heapq.heapify(self.list)
        f_score, node_state = heapq.heappop(self.list)
        return f_score, node_state
    
    def last_pop(self):
        for i in range(0,20):
            f_score, _ = self.pop()
            print(f_score)
    
    def __contains__(self, node_state):
        for e in self.list:
            if e[-1] == node_state:
                return True
        return False
    
    def __str__(self):
        str_return = ""
        for e in self.list:
            str_return = str_return +str(e[0]) + " -- "+ str(e[-1]) + "\n"
        return str_return
    
    def __delitem__(self, node_state):
        for e in self.list:
            if e[-1] == node_state:
                self.list.remove(e)
                break

    def __getitem__(self, node_state):
        for e in self.list:
            if e[-1] == node_state:
                return e[-1]
        return None 

    def __len__(self):
        return len(self.list)