import time
import numpy as np
from GA import GA
from pprint import pprint

start = time.time()

tamPopulacaoMain = 50
numCromossomosMain = 2
numGeracoesMain = 100
intervaloMain = [[-10,10],[-10,10]]
resolucaoMain = 16
taxaDeMutacaoMain = 0.5


GA = GA(tamPopulacaoMain, numGeracoesMain, numCromossomosMain, intervaloMain, resolucaoMain, taxaDeMutacaoMain)

print ("-------------------------------------------------------------")

GA.testes()


print("Tempo total: ",end='')
print(time.time() - start)
