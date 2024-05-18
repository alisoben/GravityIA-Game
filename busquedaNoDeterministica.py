import random
from config import COLUMNAS

class BusquedaNoDeterministica:
    def noDeterminista(self, tablero, jugadorO):
        alternativas = self.explorar_alternativas(tablero, jugadorO)
        return random.choice(alternativas)
    
    def explorar_alternativas(self, tablero, jugadorO):
        lista_opciones = [("rotar_tablero", None)]  # La acción "rotar_tablero" no necesita un parámetro adicional
        for c in range(COLUMNAS):
            if tablero.es_ubicacion_valida(c):
                lista_opciones.append(("colocar_ficha", c))  # La acción "colocar_ficha" necesita un número de columna
        if jugadorO.borrarPosible():
            for c in range(COLUMNAS):
                lista_opciones.append(("borrar_columna", c))  # La acción "borrar_columna" necesita un número de columna
        return lista_opciones