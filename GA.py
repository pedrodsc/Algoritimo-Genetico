import numpy as np
import time
from Individuo import Individuo
from Objeto import Circulo, Retangulo
from pid import PID

class GA(object):

    def __init__(self, funcAvaliacao,tamPopulacao, numGeracoes, numCromossomos, intervalos, resolucao, taxaDeMutacao):
        super(GA, self).__init__()
        self.funcAvaliacao = funcAvaliacao
        self.tamPopulacao = tamPopulacao
        self.numGeracoes = numGeracoes
        self.numCromossomos = numCromossomos
        self.intervalos = intervalos
        self.resolucao = resolucao
        self.taxaDeMutacao = taxaDeMutacao
        self.numeroDeMutacoes = 0
        self.indexMelhorIndividuo = 0
        
        self.populacao = np.empty(tamPopulacao,dtype=np.object)

        for x in range(tamPopulacao):
            tempIndividuo = Individuo(self.numCromossomos,self.intervalos,self.resolucao, randomizar = True)
            tempIndividuo.bin2dec()
            self.populacao[x] = tempIndividuo
    
    def init(self):
        # Pra evitar redundância no calculo do Fitness nas iterações a geração 0 é calculada aqui.
        _,self.indexMelhorIndividuo = self.calculaFitness()
        
    def calculaFitness(self):

        maiorPontuacao = 0
        indexMelhorIndividuo = 0
        
        for iterador, individuo in enumerate(self.populacao):
            
            fit = self.funcAvaliacao(individuo)
            self.populacao[iterador].fitness = fit
            
            if self.populacao[iterador].fitness > maiorPontuacao:
                maiorPontuacao = self.populacao[iterador].fitness
                indexMelhorIndividuo = iterador

        return (maiorPontuacao, indexMelhorIndividuo)


    def cruzarPopulacao(self, indexDePais):
        # Troquei o array de nativo python para numpyself.
        # O tempo de exceução reduziu em 20%  (~1s para ~800ms)
        #populacaoDePais = copy.deepcopy(self.populacao)
        populacaoDePais = np.copy(self.populacao)
        for iterador, filho in enumerate(self.populacao):
            cromossomoTeste = np.ones(shape=(self.numCromossomos,self.resolucao), dtype=np.uint64)
            self.populacao[iterador].receberGenes(self.cruzarIndividuos(populacaoDePais[indexDePais[0][iterador]],populacaoDePais[indexDePais[1][iterador]]))

            self.populacao[iterador].bin2dec()


    def cruzarIndividuos(self, A, B):

        filho = np.empty(shape=(self.numCromossomos,self.resolucao),dtype=np.uint8)
        #pontosDeCorte = np.random.randint(self.resolucao, size=self.numCromossomos)
        pontosDeCorte = np.ones(self.resolucao, dtype=np.uint8) * (self.resolucao // 2)

        for x in range(0,self.numCromossomos):
            filho[x] = np.concatenate((A.cromossomosGray[x][0:pontosDeCorte[x]],B.cromossomosGray[x][pontosDeCorte[x]:self.resolucao]),axis=None)
            if np.random.rand() < self.taxaDeMutacao:
                bitParaMudar = np.random.randint(self.resolucao)
                filho[x][bitParaMudar] = filho[x][bitParaMudar] ^ 1
                self.numeroDeMutacoes += 1
        return filho

    def selecionarPais(self, indexMelhorIndividuo = None):
        indexDePais = np.empty(shape=(2,self.tamPopulacao), dtype=np.int64)
        fitnessTotalAtual = 0
        fitnessTotal = 0

        # Método da roleta viciada

        for individuo in self.populacao:
            fitnessTotal = fitnessTotal + individuo.fitness

        for iteradorLoopExterno in (0,1):

            for iteradorLoopInterno in range(0,self.tamPopulacao):
                for indexDoIndividuo, individuo in enumerate(self.populacao):
                    pontuacaoDeCorte = fitnessTotal * np.random.rand()
                    fitnessTotalAtual = fitnessTotalAtual + individuo.fitness
                    if fitnessTotalAtual > pontuacaoDeCorte:
                            indexDePais[iteradorLoopExterno][iteradorLoopInterno] = indexDoIndividuo
                            fitnessTotalAtual = 0
                            break
        # Manter o melhor individuo ajudou nos resultados
        #if indexMelhorIndividuo != None:
        #    indexDePais[0][0] = indexMelhorIndividuo
        return indexDePais
    
    def itera(self):
        numeroDeMutacoesAnt = 0
        
        numeroDeMutacoesAnt = self.numeroDeMutacoes
        
        pais = self.selecionarPais(self.indexMelhorIndividuo)
        self.cruzarPopulacao(pais)
        melhorFitness,self.indexMelhorIndividuo = self.calculaFitness()
        
        totalMutacoes = self.numeroDeMutacoes - numeroDeMutacoesAnt
        
        return melhorFitness,self.indexMelhorIndividuo,totalMutacoes
