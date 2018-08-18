import time
import numpy as np
from GA import GA
from pprint import pprint

tamPopulacaoMain = 30
numCromossomosMain = 2
numGeracoesMain = 50
intervaloMain = [[0.1,10],[0.1,1]]
resolucaoMain = 8
taxaDeMutacaoMain = 0.1

GA = GA(tamPopulacaoMain, numGeracoesMain, numCromossomosMain, intervaloMain, resolucaoMain, taxaDeMutacaoMain)

print ("-------------------------------------------------------------")
start = time.time()
GA.testes()
print("Tempo total: ",end='')
print(time.time() - start)
