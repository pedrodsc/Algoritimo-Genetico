import numpy as np

class Objeto(object):
    def __init__(self):
        super(Objeto, self).__init__()
        self.x = 0
        self.y = 0
        self.velocidade = [0,0]


class Circulo(Objeto) :

    def __init__(self, massa, x, y, raio, cor = (255,0,0)):
        super(Circulo, self).__init__()
        self.massa = massa
        self.x = x
        self.y = y
        self.raio = raio
        self.cor = cor
        self.velocidade = [0,0]

        self.largura = self.raio
        self.comprimento = self.raio

class Retangulo(Objeto) :

    def __init__(self, massa, x, y, largura, comprimento, cor = (255,0,0)):
        super(Retangulo, self).__init__()
        self.massa = massa
        self.largura = largura
        self.comprimento = comprimento

        self.x = (x)
        self.y = (y)

        self.velocidade = [0,0]

        self.cor = cor

        self.pontos = np.array(\
        [[self.x - self.largura/2 , self.y - self.comprimento/2],\
        [self.x + self.largura/2 , self.y - self.comprimento/2],\
        [self.x + self.largura/2 , self.y + self.comprimento/2],\
        [self.x - self.largura/2 , self.y + self.comprimento/2]], dtype=np.float)
        '''
        self.pontos = np.array(\
        [[self.x, self.y],\
        [self.x , self.y + self.comprimento],\
        [self.x + self.largura, self.y + self.comprimento/2],\
        [self.x, self.y + self.comprimento]], dtype=np.float)
        '''
    def rotaciona(self, arg):
        matrizDeRotacao = np.array([[np.cos(arg),-np.sin(arg)],[np.sin(arg),np.cos(arg)]],dtype=np.float)
        xOriginal = self.x
        yOriginal = self.y
        self.translada(-xOriginal,-yOriginal)
        self.pontos = np.dot(self.pontos,matrizDeRotacao)
        self.translada(xOriginal,yOriginal)

    def translada(self, x, y):
        matrizDeTranslacao = np.array(\
        [[x, y],\
        [x, y],\
        [x, y],\
        [x, y]], dtype=np.float)
        self.x += x
        self.y += y
        self.pontos = self.pontos + matrizDeTranslacao
