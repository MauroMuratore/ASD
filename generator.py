import os
import time
import numpy as np
import random

STRATEGY = {
    "RANDOM" : 0,
    "RANGE" : 1
}
"""
Inserisce un agglomerato nella matrice g.

Args:
    g: La matrice mxn.
    axis: L'asse su cui inserire l'agglomerato. 0 per l'asse orizzontale, 1 per l'asse verticale.
    line: La riga o la colonna (a seconda dell'asse) in cui inserire l'agglomerato.
    agg: Le coordinate iniziali e finali dell'agglomerato rispetto all'asse specificato.

Returns:
    None

"""
def insert_agglomerate_in_g(g, axis, line,agg):
    if axis == 0:
        for j in range(agg[0], agg[1] + 1): g[line][j] = 1
    else :
        for i in range(agg[0], agg[1] + 1): g[i][line] = 1

"""
Aggiorna il dizionario dict a seguito dell'inserimento di un agglomerato in un range, 
eliminandolo dalla lista della line corrispondente. Nel caso si formino degli intervalli grandi
almeno la dimensione degli agglomerati vengono aggiunti alla lista.

Args:
    dict: Dizionario
    line: Chiave per scegliere la lista
    range: Intervallo in cui è stato inserito l'agglomerato
    agg : Le coordinate iniziali e finali dell'agglomerato rispetto al range.

Returns:
    None
"""
def update_dictionary(dict, line, range, agg, agg_size):
    dict[line].remove(range)
    if agg[0] - range[0] >= agg_size :
        dict[line].append((range[0], agg[0] - 1))
    if range[1] - agg[1] >= agg_size :
        dict[line].append((agg[1]+1, range[1]))
    if len(dict[line]) < 1 :
        dict.pop(line)

"""
Inserisce nella matrice g un agglomerato in una posizione semi-casuale in modo che 
non si sovrapponga agli agglomerati già presenti

Args:
    g: matrice mxn
    agglomerate: dimensione dell'agglomerato
    dict_row: dizionario degli intervalli delle righe
    dict_col: dizionario degli intervalli delle colonne

Return:
    None
"""
def create_range_agglomerate(g, agglomerate, dict_row, dict_col):
    # check dictionary and set up variable 
    if len(dict_row) < 1 and len(dict_col) < 1 :
        return
    elif len(dict_row) < 1 :
        main_axis = 1
    elif len(dict_col) < 1 :
        main_axis = 0
    else :
        main_axis = round(random.random())
    main_dict, sec_dict = (dict_row, dict_col) if main_axis < 1 else (dict_col, dict_row)
    main_line = random.choice(list(main_dict.keys()))
    main_range = random.choice(main_dict[main_line])

    # print(f"{main_axis=}")
    # print(f"{main_line=}")
    # print(f"{main_range=}")

    # create and insert agglomerate in the matrix g
    start_agg = random.randint(main_range[0], main_range[1] - agglomerate + 1)
    end_agg = start_agg + agglomerate -1 
    agg = (start_agg, end_agg)
    # print(f"{agg}")
    insert_agglomerate_in_g(g, main_axis, main_line,agg)
    
    # update main dictionary
    update_dictionary(main_dict, main_line, main_range, agg, agglomerate)
    
    # update secondary dictionary
    for sec_line in range(agg[0], agg[1]+1) :
        if sec_line not in sec_dict.keys() :
            continue
        sec_ranges = sec_dict[sec_line]
        for r in sec_ranges:
            if r[0] <= main_line and r[1] >= main_line:
                agg_line = (main_line, main_line)
                update_dictionary(sec_dict, sec_line, r, agg_line, agglomerate)

"""
Inserisce nella matrice g un agglomerato in una posizione casuale

Args:
    g: matrice mxn
    agglomerate: dimensione dell'agglomerato
"""
def create_random_agglomerate(g, agglomerate):
    # axis = 0 horizontal, axis = 1 vertical
    main_axis = round(random.random())
    sec_axis = 1 if main_axis < 1 else 0
    line = random.randint(0, g.shape[main_axis] - 1)
    start_agg = random.randint(0, g.shape[sec_axis] - agglomerate)
    end_agg = start_agg - agglomerate + 1
    agg = (start_agg, end_agg)
    insert_agglomerate_in_g(g, main_axis, line, agg)



def create_grid(nrow: int, ncol: int, density: float, agglomerate: int, strategy: int = 0):
    g = (np.zeros((nrow, ncol))).astype(int)
    n_obstacles = round(nrow * ncol * (1 - density))
    n_agglomerates = n_obstacles // agglomerate

    if strategy == STRATEGY["RANGE"] :
        dict_row = { i : [(0, ncol-1)] for i in range(0, nrow)}
        dict_col = { j : [(0, nrow-1)] for j in range(0, ncol)}
        for _ in range(0, n_agglomerates):
            create_range_agglomerate(g, agglomerate, dict_row, dict_col)
        return g
    for _ in range(0, n_agglomerates):
        create_random_agglomerate(g, agglomerate)
        return g




def main():
    if not os.path.isdir("./data"):
        os.mkdir("./data")
    if not os.path.isdir("./data/grids"):
        os.mkdir("./data/grids")
    print("--------- START MAIN ---------")
    data_time = np.array([["file", "time", "nrow", "density", "agglomerate"]])
    for d in range(60, 100, 5):
        density = d/100
        for agglomerate in range(1, 11):
            for nrow in range(10,51,2):
                for i in range(0,4):
                    filename = "./data/grids/{}x{}_d{}_ag{}_{}.csv".format(nrow, nrow, density, agglomerate, i)
                    start = time.process_time()
                    g = create_grid(nrow, nrow, density, agglomerate, STRATEGY["RANGE"])
                    end = time.process_time()
                    record_time =np.array([[str(filename), str(end-start), str(nrow), str(density), str(agglomerate)]])
                    data_time= np.vstack([data_time, record_time])
                    np.savetxt(filename, g, fmt="%2.0f" ,delimiter=";")
                    print(filename+ " written")
    
    np.savetxt("./data/grids/time.csv", data_time, fmt="%s" , delimiter=";")



if __name__ == "__main__" :
    main()