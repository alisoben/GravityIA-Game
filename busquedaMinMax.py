import random
class BusquedaMinMax:
    def __init__(self, profundidad_maxima):
        self.profundidad_maxima = profundidad_maxima
        
    def minimax(self, estado, es_maximizador, profundidad, alpha=float('-inf'), beta=float('inf')):
        if profundidad == self.profundidad_maxima or estado.terminal():
            return estado.evaluar(), None
        
        mejor_valor = float('-inf') if es_maximizador else float('inf')
        mejor_accion = None
        for accion in estado.acciones():
            siguiente_estado = estado.resultado(accion)
            valor, _ = self.minimax(siguiente_estado, not es_maximizador, profundidad + 1, alpha, beta)
            if es_maximizador:
                if valor > mejor_valor:
                    mejor_valor = valor
                    mejor_accion = accion
                alpha = max(alpha, valor)
            else:
                if valor < mejor_valor:
                    mejor_valor = valor
                    mejor_accion = accion
                beta = min(beta, valor)
            if beta <= alpha:
                break
        if mejor_accion is None:
            return -float('inf'), random.choice(estado.acciones())
        return mejor_valor, mejor_accion