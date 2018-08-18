import numpy as np
from pprint import pprint

class Individuo(object):

    cromossomosGray = []
    cromossomos = []

    numCromossomos = 0
    intervalos = []
    resolucao = 0

    fitness = 0

    def __init__(self, numCromossomos, intervalos, resolucao, randomizar=False):
        super(Individuo, self).__init__()

        self.cromossomosGray = np.empty(shape=(numCromossomos,resolucao), dtype=np.uint8)
        self.cromossomos = np.empty(shape=(numCromossomos,1), dtype=np.float64)

        self.numCromossomos = numCromossomos
        self.intervalos = intervalos
        self.resolucao = resolucao

        if randomizar:
            self.cromossomosGray = np.random.randint(2, size=(numCromossomos, resolucao), dtype=np.uint8)

    def __setitem__(self, key):
        return self.receberGenes()


    def bin2dec(self):
        arrayDePotencias = 1 << np.arange(self.resolucao)[::-1] # [2^resolucao, ... , 16, 8, 4, 2, 1]
        denominador = 2**self.resolucao

        cromossomosBin = np.empty(shape=(self.numCromossomos,self.resolucao), dtype=np.uint8)

        for i,linha in enumerate(self.cromossomosGray):
            for j, elemento in enumerate(linha):
                if j == 0:
                    cromossomosBin[i][j] = self.cromossomosGray[i][j]
                else:
                    cromossomosBin[i][j] = cromossomosBin[i][j-1] ^ self.cromossomosGray[i][j]

        tempCromossomos = np.inner(cromossomosBin,arrayDePotencias)


        for iterador,x in enumerate(tempCromossomos):
            self.cromossomos[iterador] = self.intervalos[iterador][0] + (self.intervalos[iterador][1] - self.intervalos[iterador][0]) * (x / denominador)

    def receberGenes(self, cromossomosBin):
        self.cromossomosGray = cromossomosBin
