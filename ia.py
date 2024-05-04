#ia.py
import random
from logic import *

class IA:
    def __init__(self, nivel):
        self.nivel = nivel

    def elegir_columna(self, tablero):
        columnas_validas = [c for c in range(COLUMNAS) if es_ubicacion_valida(tablero, c)]
        return random.choice(columnas_validas) if columnas_validas else None

class Principiante(IA):
    pass  # Utiliza la misma lógica de la clase padre para principiantes.

def crear_ia(nivel):
    if nivel == "principiante":
        return Principiante(nivel)
    # Agregar aquí más niveles cuando se implementen.