from jugador import Jugador
from config import COLUMNAS
import random

class JugadorIA(Jugador):
    def __init__(self, ficha):
        super().__init__(ficha)

    def decidirPrincipiante(self, tablero):
        busqueda = BusquedaNoDeterministica()
        opcion_elegida = busqueda.tomarDecision(tablero, self)
        
        if opcion_elegida[0] == "rotar_tablero":
            self.rotar_tablero(opcion_elegida[1])
        elif opcion_elegida[0] == "colocar_ficha":
            self.colocar_ficha(opcion_elegida[1], opcion_elegida[2])
        elif opcion_elegida[0] == "borrar_columna":
            self.borrar_columna(opcion_elegida[1], opcion_elegida[2])



class BusquedaNoDeterministica:
    def explorar_alternativas(self, tablero, jugadorO):
        lista_opciones = [("rotar_tablero", tablero)]
        for c in range(COLUMNAS):
            if tablero.es_ubicacion_valida(c):
                lista_opciones.append(("colocar_ficha", tablero, c))
        if jugadorO.borrarPosible():
            for c in range(COLUMNAS):
                lista_opciones.append(("borrar_columna", tablero, c))
        return lista_opciones

    def tomarDecision(self, tablero, jugadorO):
        alternativas = self.explorar_alternativas(tablero, jugadorO)
        return random.choice(alternativas)
