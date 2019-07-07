import pygame
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

        self.populacao = np.empty(tamPopulacao,dtype=np.object)

        for x in range(tamPopulacao):
            tempIndividuo = Individuo(self.numCromossomos,self.intervalos,self.resolucao, randomizar = True)
            tempIndividuo.bin2dec()
            self.populacao[x] = tempIndividuo

    def calculaFitness(self):
        # TODO: Implementar a função. Ainda à decidir se será com cada individuo ou com a populacao inteira
        # Por enquanto toda a populacao é avaliada, não sendo possível avaliar um único individuo se necessário
        maiorPontuacao = 0
        indexMelhorIndividuo = 0
        for iterador, individuo in enumerate(self.populacao):
            X = individuo.cromossomos[0]
            Y = individuo.cromossomos[1]
            Z = individuo.cromossomos[2]
            
            fit,penality,caiu = self.funcAvaliacao(X,Y,Z,1000)
            self.populacao[iterador].fitness = (fit**2)/(penality)
            
            # Funções obtidas em http://benchmarkfcns.xyz/
            
            #self.populacao[iterador].fitness = 1 / ((X + 2*Y - 7)**2 + ( 2*X + Y - 5)**2  + (Z - 10)**2) # Booth(modificada)
            #self.populacao[iterador].fitness = 1 / ((1.5-X+X*Y)**2+(2.25-X+X*Y**2)**2+(2.625-X+X*Y**3)**2) #
            #self.populacao[iterador].fitness = (1 / ((4/3)*(((X ** 2 + Y ** 2) - (X * Y))**(0.75)) + Z)) + (1 / ((4/3)*(((A ** 2 + B ** 2) - (A * B))**(0.75)) + C)) # Wolfe
            
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
        if indexMelhorIndividuo != None:
            indexDePais[0][0] = indexMelhorIndividuo
        return indexDePais

    def testes(self):
        
        # O nome diz tudo. É uma função pra testes, não implemente assim.
        
        numeroDeMutacoesAnt = 0
        indexMelhorIndividuo = 0
        
        done = False
                
        for x in range(0,self.numGeracoes):
            self.calculaFitness()
            print("Gen: %d ====================================" % (x+1))
            pais = self.selecionarPais(indexMelhorIndividuo)
            self.cruzarPopulacao(pais)
            melhorFitness,indexMelhorIndividuo = self.calculaFitness()

            #pprint(pais)
            print("Highest Fitness: %.4f" % (melhorFitness))
            print("Mutations: %d" % (self.numeroDeMutacoes - numeroDeMutacoesAnt))
            numeroDeMutacoesAnt = self.numeroDeMutacoes
            
            if done:
                break
            
        ########### ########### ########### ########### ########### ########### ########### ###########
        # DESENHO         
        #
        #
        # SIMULA O MELHOR de cada geração
        #
        #
        #
        ########### ########### ########### ########### ########### ########### ########### ###########
            
            pygame.init()
            
            locStartTime = time.time()
            gravity = 4
            theta = -0.001

            raio = 20
            screenHeight = 800
            screenWidth = 1000

            screenCenter = (int(screenWidth/2),int(screenHeight/2))
            groundHeigth = int(0.8*screenHeight)

            corCeu = (58,218,232)
            corChao = (30,176,71)
            corBola = (197,0,0)
            corPlataforma = (126,97,25)

            bola = Circulo(1,screenCenter[0],screenCenter[1],raio,corBola)

            plataforma  = Retangulo(1,screenCenter[0],screenCenter[1],400,10,corPlataforma)
            
            kp = self.populacao[indexMelhorIndividuo].cromossomos[0]
            ki = self.populacao[indexMelhorIndividuo].cromossomos[1]
            kd = self.populacao[indexMelhorIndividuo].cromossomos[2]
            
            meuPID = PID(kp,ki,kd,1000)
            
            xc = plataforma.x + 100
            yc = plataforma.y
            
            setpoint = plataforma.x
            
            myfont = pygame.font.SysFont("Comic Sans MS", 30)
            
            clock = pygame.time.Clock()
            
            screen = pygame.display.set_mode((screenWidth,screenHeight))
            pygame.display.set_caption('PID')
            caiu = False
            done = False
            while not caiu and not done:
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                            done = True
                ### PID 
                theta = -meuPID.atualiza(plataforma.x,xc)
                
                ### Plataforma
                p0 = plataforma.pontos[0]
                p1 = plataforma.pontos[1]
                m = (p1[1] - p0[1])/(p1[0] - p0[0]) if (p1[0] != p0[0]) else 100
                phi = np.arctan(m)
                plataforma.rotaciona(theta[0]+phi) 
                ### Bola
                # xc = x de contato com a plataforma
                # yc = y de contato com a plataforma
                
                # Interação bola e plataforma
                
                if (screenCenter[0] - np.cos(phi)*(plataforma.largura/2) < bola.x < screenCenter[0] + np.cos(phi)*(plataforma.largura/2) and caiu == 0):
                    
                    xc += bola.velocidade[0] + bola.velocidade[1]*np.sin(phi)
                    
                    yc = m*(xc-plataforma.x) - np.cos(phi)*plataforma.comprimento/2 + plataforma.y
                    
                    bola.x = xc + bola.raio*np.sin(phi)
                    bola.y = yc - bola.raio*np.cos(phi)
                    
                    bola.velocidade[0] += np.sin(phi)*gravity/3
                    bola.velocidade[0] *= 0.96
                    tVivo = time.time()-locStartTime
                    #print('X:'+'{:.2f}'.format(bola.x) + ' Y:'+'{:.2f}'.format(bola.y)+ ' m:'+'{:.5f}'.format(m))
                else:
                    caiu = True
                    bola.velocidade[0] = bola.velocidade[0]*0.96
                    bola.x += bola.velocidade[0]
                    if (bola.y + bola.raio >= groundHeigth):
                        bola.velocidade[1] = -bola.velocidade[1]*0.9
                    else:
                        bola.y += bola.velocidade[1]
                        bola.velocidade[1] += gravity
                # Paisagem
                screen.fill(corCeu)
                pygame.draw.rect(screen, corChao, pygame.Rect(0,groundHeigth,screenWidth,screenHeight))
                # Plataforma
                pygame.draw.polygon(screen,plataforma.cor,np.int32(plataforma.pontos))
                pygame.draw.circle(screen,(0,0,0),(int(plataforma.x),int(plataforma.y)),5) 
                # Bola
                pygame.draw.circle(screen,bola.cor,(int(bola.x),int(bola.y)),bola.raio)
                
                text = myfont.render('Gen: '+str(x+1), 1, (12, 12, 127))
                screen.blit(text, (screenCenter[0]-40,30))
                
                text = myfont.render('X: '+str(int(bola.x)), 1, (12, 12, 12))
                screen.blit(text, (20,50))
                text = myfont.render('Y: '+str(int(bola.y)), 1, (12, 12, 12))
                screen.blit(text, (20,80))
                
                text = myfont.render('T: '+'{:.3f}'.format(tVivo)+'s', 1, (12, 12, 12))
                screen.blit(text, (20,110))

                text = myfont.render('Kp: '+'{:.4f}'.format(float(kp)), 1, (100, 12, 12))
                screen.blit(text, (20,150))
                
                text = myfont.render('Ki: '+'{:.4f}'.format(float(ki)), 1, (100, 12, 12))
                screen.blit(text, (20,180))
                
                text = myfont.render('Kd: '+'{:.4f}'.format(float(kd)), 1, (100, 12, 2))
                screen.blit(text, (20,210))
                
                pygame.display.flip()
                clock.tick(60)
                if (tVivo > 7):
                    break
                else:
                    continue
            
            
        print("========= END =========")
        print("Maior fitness: %.4f" % (melhorFitness))
        X = self.populacao[indexMelhorIndividuo].cromossomos[0]
        Y = self.populacao[indexMelhorIndividuo].cromossomos[1]
        Z = self.populacao[indexMelhorIndividuo].cromossomos[2]
        print("Kp= %.4f" % X )
        print("Ki= %.4f" % Y )
        print("Kd= %.4f" % Z )
        pygame.quit()
