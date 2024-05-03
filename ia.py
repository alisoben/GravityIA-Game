#IA EN poceso aea ....
import random
from logic import *
class IA:
    def __init__(self, nivel):
        self.nivel = nivel

    def elegir_columna(self, tablero):
        columnas_validas = [c for c in range(COLUMNAS) if tablero[FILAS - 1][c] == 0]
        return random.choice(columnas_validas) if columnas_validas else None

class Principiante(IA):
    def elegir_columna(self, tablero):
         # Lógica más avanzada que el principiante
        return super().elegir_columna(tablero)
       
class Normal(IA):
    def elegir_columna(self, tablero):
        # Lógica más avanzada que el principiante
        return super().elegir_columna(tablero)

class Experto(IA):
    def elegir_columna(self, tablero):
        # Lógica aún más sofisticada
        return super().elegir_columna(tablero)

def jugar_humano_ia(nivel, tablero):
    ia = {'principiante': Principiante(nivel), 'normal': Normal(nivel), 'experto': Experto(nivel)}[nivel.lower()]()
    return ia.elegir_columna(tablero)