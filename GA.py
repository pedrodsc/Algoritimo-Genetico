import copy
import math
import numpy as np
from Individuo import Individuo
from pprint import pprint

class GA(object):

    def __init__(self, tamPopulacao, numGeracoes, numCromossomos, intervalos, resolucao, taxaDeMutacao):
        super(GA, self).__init__()
        self.tamPopulacao = tamPopulacao
        self.numGeracoes = numGeracoes
        self.numCromossomos = numCromossomos
        self.intervalos = intervalos
        self.resolucao = resolucao
        self.taxaDeMutacao = taxaDeMutacao
        self.numeroDeMutacoes = 0

        self.populacao = np.empty(tamPopulacao,dtype=np.object)

        for x in range(tamPopulacao):
            tempIndividuo = Individuo(self.numCromossomos,self.intervalos,self.resolucao, randomizar = True)
            tempIndividuo.bin2dec()
            self.populacao[x] = tempIndividuo

    def calculaFitness(self):
        # TODO: Implementar a função. Ainda à decidir se será com cada individuo ou com a populacao inteira
        maiorPontuacao = 0
        indexMelhorIndividuo = 0
        for iterador, individuo in enumerate(self.populacao):
            X = individuo.cromossomos[0]
            Y = individuo.cromossomos[1]
            Z = individuo.cromossomos[2]


            self.populacao[iterador].fitness = 1 / ((X + 2*Y - 7)**2 + ( 2*X + Y - 5)**2  + (Z - 10)**2)
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
                filho[x][np.random.randint(self.resolucao)] = filho[x][np.random.randint(self.resolucao)] ^ 1
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
        if indexMelhorIndividuo != None:
            indexDePais[0][0] = indexMelhorIndividuo
        return indexDePais

    def testes(self):
        numeroDeMutacoesAnt = 0
        indexMelhorIndividuo = 0
        for x in range(0,self.numGeracoes):
            self.calculaFitness()
            print("Geração: %d ====================================" % (x))
            pais = self.selecionarPais(indexMelhorIndividuo)
            self.cruzarPopulacao(pais)
            melhorFitness,indexMelhorIndividuo = self.calculaFitness()
            '''
            for iterador, individuo in enumerate(self.populacao):
                print("F: %.4f" % self.populacao[iterador].fitness,end='\t')
            print("\n")
            for iterador, individuo in enumerate(self.populacao):
                print("X= %.4f" % self.populacao[iterador].cromossomos[0],end='\t')
            print("\n")
            for iterador, individuo in enumerate(self.populacao):
                print("Y= %.4f" % self.populacao[iterador].cromossomos[1],end='\t')
            print("\n")
            '''

            #pprint(pais)
            print("Maior fitness: %.4f" % (melhorFitness))
            print("Mutações: %d" % (self.numeroDeMutacoes - numeroDeMutacoesAnt))
            numeroDeMutacoesAnt = self.numeroDeMutacoes
        print("========= FIM =========")
        print("Maior fitness: %.4f" % (melhorFitness))
        X = self.populacao[indexMelhorIndividuo].cromossomos[0]
        Y = self.populacao[indexMelhorIndividuo].cromossomos[1]
        Z = self.populacao[indexMelhorIndividuo].cromossomos[2]
        print("X= %.4f" % X )
        print("Y= %.4f" % Y )
        print("Z= %.4f" % Z )

        print(1 / ((X + 2*Y - 7)**2 + ( 2*X + Y - 5)**2) + (Z - 10)**2)
        #self.cruzarIndividuos(self.populacao[0],self.populacao[1])
