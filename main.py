import time
import sys
import pygame
import numpy as np
#from mpl_toolkits.mplot3d import Axes3D
#import matplotlib.pyplot as plt
#from matplotlib import cm
from GA import GA
from Objeto import Circulo, Retangulo
from pid import PID

# Parâmetros do GA

np.random.seed(time.gmtime())
tamPopulacaoMain = 50
numCromossomosMain = 3
numGeracoesMain = 20
intervaloMain = [[0,10],[0,10],[0,10]]
resolucaoMain = 16
taxaDeMutacaoMain = 0.1 # 1 = 100%
dividerMain = 1000

# Variáveis e inicialização do pygame
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
    
myfont = pygame.font.SysFont("Comic Sans MS", 30)

clock = pygame.time.Clock()

screen = pygame.display.set_mode((screenWidth,screenHeight))
pygame.display.set_caption('PID')

# Função de avaliação

def funcAvaliacao(kp,ki,kd,divider):
    caiu = False
    
    startTime = time.time()
    tVivo = 0
    nFrames = 0
    gravity = 4
    #theta = 0.52359 # pi/6 = 30 graus
    theta = -0.001
    SumdToSetpoint = 0
    raio = 20
    screenHeight = 800
    screenWidth = 1000

    screenCenter = (int(screenWidth/2),int(screenHeight/2))
    groundHeigth = int(0.8*screenHeight)

    corCeu = (232,218,58)
    corChao = (71,176,30)
    corBola = (0,0,197)
    corPlataforma = (25,97,126)

    bola = Circulo(1,screenCenter[0],screenCenter[1],raio,corBola)

    plataforma  = Retangulo(1,screenCenter[0],screenCenter[1],400,10,corPlataforma)
    
    meuPID = PID(kp,ki,kd,divider)
    
    xc = plataforma.x + 100
    yc = plataforma.y
    
    setpoint = plataforma.x
    
    frame = np.zeros((screenHeight,screenWidth,3),dtype=np.uint8)
    
    while not caiu:
        ### PID 
        nFrames += 1
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
        
        if (screenCenter[0] - np.cos(phi)*(plataforma.largura/2) < bola.x < screenCenter[0] + np.cos(phi)*(plataforma.largura/2) and caiu == False):
            
            xc += bola.velocidade[0] + bola.velocidade[1]*np.sin(phi)
            
            yc = m*(xc-plataforma.x) - np.cos(phi)*plataforma.comprimento/2 + plataforma.y
            
            bola.x = xc + bola.raio*np.sin(phi)
            bola.y = yc - bola.raio*np.cos(phi)
            
            bola.velocidade[0] += np.sin(phi)*gravity/3

            bola.velocidade[0] *= 0.96
            tVivo = time.time()-startTime

        else:
            caiu = True
            bola.velocidade[0] = bola.velocidade[0]*0.96
            bola.x += bola.velocidade[0]
            if (bola.y + bola.raio >= groundHeigth):
                bola.velocidade[1] = -bola.velocidade[1]*0.9
            else:
                bola.y += bola.velocidade[1]
                bola.velocidade[1] += gravity
        
        SumdToSetpoint += (abs(setpoint - bola.x))
        fitness = (nFrames**2)/SumdToSetpoint
        if nFrames > 420:
            return (fitness)
    
    return (fitness)

# Função de simulação

def simula(initalPos,kp,ki,kd,divider):
    bola = Circulo(1,screenCenter[0],screenCenter[1],raio,corBola)
    plataforma  = Retangulo(1,screenCenter[0],screenCenter[1],400,10,corPlataforma)
    
    meuPID = PID(kp,ki,kd,1000)
    
    setpoint = plataforma.x
    xc = plataforma.x + int(plataforma.largura*initalPos/2)
    yc = plataforma.y
    
    caiu = False
    done = False
    locStartTime = time.time()
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
        
        if (screenCenter[0] - np.cos(phi)*(plataforma.largura/2) < bola.x < screenCenter[0] + np.cos(phi)*(plataforma.largura/2) and caiu == False):
            
            xc += bola.velocidade[0] + bola.velocidade[1]*np.sin(phi)
            
            yc = m*(xc-plataforma.x) - np.cos(phi)*plataforma.comprimento/2 + plataforma.y
            
            bola.x = xc + bola.raio*np.sin(phi)
            bola.y = yc - bola.raio*np.cos(phi)
            
            bola.velocidade[0] += np.sin(phi)*gravity/3
            bola.velocidade[0] *= 0.96
            tVivo = time.time()-locStartTime
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
    return done
    
start = time.time()

# inicialização do GA

GA = GA(funcAvaliacao,tamPopulacaoMain, numGeracoesMain, numCromossomosMain, intervaloMain, resolucaoMain, taxaDeMutacaoMain)

print ("-------------------------------------------")
print("Population size: "+str(tamPopulacaoMain))

GA.init()

done = False
for x in range(0,GA.numGeracoes):
   
    print("Gen: %d ====================================" % (x+1))
    melhorFitness,indexMelhorIndividuo,totalMutacoes = GA.itera()

    print("Highest Fitness: %.4f" % (melhorFitness))
    print("Mutations: %d" % (totalMutacoes))
    
    if done:
        break
    
    bola = Circulo(1,screenCenter[0],screenCenter[1],raio,corBola)
    plataforma  = Retangulo(1,screenCenter[0],screenCenter[1],400,10,corPlataforma)
    
    kp = GA.populacao[indexMelhorIndividuo].cromossomos[0]
    ki = GA.populacao[indexMelhorIndividuo].cromossomos[1]
    kd = GA.populacao[indexMelhorIndividuo].cromossomos[2]
    initalPos = 0.5
    done = simula(initalPos,kp,ki,kd,dividerMain)
    

print("========= END =========")
print("Maior fitness: %.4f" % (melhorFitness))
X = GA.populacao[indexMelhorIndividuo].cromossomos[0]
Y = GA.populacao[indexMelhorIndividuo].cromossomos[1]
Z = GA.populacao[indexMelhorIndividuo].cromossomos[2]
print("Kp= %.4f" % X )
print("Ki= %.4f" % Y )
print("Kd= %.4f" % Z )

print("Elapsed time: ",end='')
print(time.time() - start)
