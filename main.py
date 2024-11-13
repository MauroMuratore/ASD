from grid_generator import GridGenerator

gg = GridGenerator(10, 8, 0.25, 3)

list = gg.get_adj_list()
matrix = gg.get_matrix()

check = [len(x) for x in list]
print(check)
for i in matrix :
    print(i)