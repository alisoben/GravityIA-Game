import random
from config import COLUMNAS

class BusquedaNoDeterministica:
    def noDeterminista(self, tablero, jugadorO):
        alternativas = self.explorar_alternativas(tablero, jugadorO)
        return random.choice(alternativas)
    
    def explorar_alternativas(self, tablero, jugadorO):
        lista_opciones = [("rotar_tablero", tablero)]
        for c in range(COLUMNAS):
            if tablero.es_ubicacion_valida(c):
                lista_opciones.append(("colocar_ficha", tablero, c))
        if jugadorO.borrarPosible():
            for c in range(COLUMNAS):
                lista_opciones.append(("borrar_columna", tablero, c))
        return lista_opciones