class PID(object):
    """PID é easy peasy. Olha o tamanho"""
    def __init__(self, kp, ki, kd, divisor = 1):
        super(PID, self).__init__()
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.divisor = divisor

        self.integral = 0
        self.derivada = 0

        self.valorAterior = 0
        self.erroAnterior = 0

    def atualiza(self,setPoint, valorAtual):
        # O divisor aqui é pra alguns sistemas onde o input é umas ordens de
        # grandeza maior que o feedback.
        #calcula o erro
        erro = (setPoint - valorAtual)/self.divisor
        
        #integra o erro
        self.integral += erro
        #deriva o erro
        self.derivada = erro - self.erroAnterior
        
        self.erroAnterior = erro
        self.valorAterior = valorAtual
        
        #soma tudo, multiplica pelos ks e retorna como feedback
        feedback = self.ki * self.integral - self.kd * self.derivada + self.kp * erro

        return feedback
