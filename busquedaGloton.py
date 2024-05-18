class CriterioGloton:
    def __init__(self, tablero):
        self.tablero = tablero

    def gloton(self, estado):
        mejor_accion = None
        mejor_valor = float('-inf')

        for accion in estado.acciones():
            siguiente_estado = estado.resultado(accion)
            valor = siguiente_estado.evaluar()

            if valor > mejor_valor:
                mejor_valor = valor
                mejor_accion = accion

        return mejor_accion