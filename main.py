import time
import numpy as np
from GA import GA
from pprint import pprint

start = time.time()
np.random.seed(time.gmtime())
tamPopulacaoMain = 200
numCromossomosMain = 3
numGeracoesMain = 1000
intervaloMain = [[-10,10],[-10,10],[0,100]]
resolucaoMain = 32
taxaDeMutacaoMain = 0.05


GA = GA(tamPopulacaoMain, numGeracoesMain, numCromossomosMain, intervaloMain, resolucaoMain, taxaDeMutacaoMain)

print ("-------------------------------------------------------------")

GA.testes()


print("Tempo total: ",end='')
print(time.time() - start)
