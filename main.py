import time
import sys
import numpy as np
#from mpl_toolkits.mplot3d import Axes3D
#import matplotlib.pyplot as plt
#from matplotlib import cm
from GA import GA
from Objeto import Circulo, Retangulo
from pid import PID

def simula(kp,ki,kd,divider):
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
        if nFrames > 420:
            return (nFrames,SumdToSetpoint,caiu)
    return (nFrames,SumdToSetpoint,caiu)

start = time.time()

np.random.seed(time.gmtime())
tamPopulacaoMain = 300
numCromossomosMain = 3
numGeracoesMain = 20
intervaloMain = [[0,10],[0,10],[0,10]]
resolucaoMain = 16
taxaDeMutacaoMain = 0.1 # 1 = 100%


GA = GA(simula,tamPopulacaoMain, numGeracoesMain, numCromossomosMain, intervaloMain, resolucaoMain, taxaDeMutacaoMain)

print ("-------------------------------------------")
print("Population size: "+str(tamPopulacaoMain))
GA.testes()


print("Elapsed time: ",end='')
print(time.time() - start)
