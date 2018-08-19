import time
import numpy as np
from GA import GA
from pprint import pprint

start = time.time()

tamPopulacaoMain = 60
numCromossomosMain = 2
numGeracoesMain = 100
intervaloMain = [[0.05,10],[0.05,1]]
resolucaoMain = 32
taxaDeMutacaoMain = 0.5


GA = GA(tamPopulacaoMain, numGeracoesMain, numCromossomosMain, intervaloMain, resolucaoMain, taxaDeMutacaoMain)

print ("-------------------------------------------------------------")

GA.testes()


print("Tempo total: ",end='')
print(time.time() - start)
