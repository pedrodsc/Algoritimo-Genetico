import numpy as np
from pprint import pprint

cromossomosGray = np.array(([1,0,0,0],[1,0,0,1],[1,0,1,1],[1,0,1,0],[1,1,1,0],[1,1,1,1]),dtype=np.uint8)
cromossomosBin = np.empty(shape=np.shape(cromossomosGray),dtype=np.uint8)

for i,linha in enumerate(cromossomosGray):
    for j, elemento in enumerate(linha):
        if j == 0:
            cromossomosBin[i][j] = cromossomosGray[i][j]
        else:
            cromossomosBin[i][j] = cromossomosBin[i][j-1] ^ cromossomosGray[i][j]

pprint(cromossomosGray)
pprint(cromossomosBin)

