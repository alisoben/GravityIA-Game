import copy
import numpy as np
from jugador import *
from tablero import *
from config import *
from busquedaMinMax import *
from busquedaNoDeterministica import *
from busquedaGloton import *


class JugadorIA(Jugador):
    def __init__(self, ficha):
        super().__init__(ficha)

    def decidirPrincipiante(self, tablero,turno,jugadorX):
        busqueda = BusquedaNoDeterministica()
        tableroC, jugadorXC, jugadorOC = copy.deepcopy(tablero), copy.deepcopy(jugadorX), copy.deepcopy(self)
        estado_inicial=Estado(tableroC, turno, jugadorXC,jugadorOC)
        accion_azar = busqueda.noDeterminista(estado_inicial)
        self.realizarMovimiento(tablero,accion_azar)

    def decidirNormal(self, tablero, turno, jugadorX):
        busqueda = CriterioGloton(tablero)
        tableroC, jugadorXC, jugadorOC = copy.deepcopy(tablero), copy.deepcopy(jugadorX), copy.deepcopy(self)
        estado_inicial = Estado(tableroC, turno, jugadorXC, jugadorOC)
        accion_optima = busqueda.gloton(estado_inicial)
        print(f"Acción óptima a tomar: {accion_optima}")
        self.realizarMovimiento(tablero, accion_optima)

    def decidirAvanzado(self, tablero, turno, jugadorX):
        busqueda = BusquedaMinMax(3)
        tableroC, jugadorXC, jugadorOC = copy.deepcopy(tablero), copy.deepcopy(jugadorX), copy.deepcopy(self)
        estado_inicial=Estado(tableroC, turno, jugadorXC,jugadorOC )
        valor_optimo,accion_optima = busqueda.minimax(estado_inicial, True, 0)
        print(f"Valor óptimo encontrado: {valor_optimo}")
        print(f"Acción óptima a tomar: {accion_optima}")
        self.realizarMovimiento(tablero, accion_optima)
                
    def realizarMovimiento(self, tablero, opcion_elegida):
        if opcion_elegida is None:
            return  # Si no hay una acción, no hacer nada
        if opcion_elegida == "rotar_tablero":
            self.rotar_tablero(tablero)
        elif opcion_elegida[0] == "colocar_ficha":
            self.colocar_ficha(tablero, opcion_elegida[1])
        elif opcion_elegida[0] == "borrar_columna":
            self.borrar_columna(tablero, opcion_elegida[1])

class Estado:
    def __init__(self, tablero: Tablero, turno, jugadorX: Jugador, jugadorO: JugadorIA):
        self.tablero = tablero
        self.turno = turno
        self.jugadorX=jugadorX
        self.jugadorO=jugadorO
    
    def acciones(self):
        acciones_posibles = []
        for c in range(COLUMNAS):
            if self.tablero.es_ubicacion_valida(c):
                acciones_posibles.append(("colocar_ficha", c))
        
        if self.turno == 'x':
            if self.jugadorX.borrarPosible():
                for c in range(COLUMNAS):
                    acciones_posibles.append(("borrar_columna", c))
                acciones_posibles.append("rotar_tablero")
        elif self.turno == 'o':
            if self.jugadorO.borrarPosible():
                for c in range(COLUMNAS):
                    acciones_posibles.append(("borrar_columna", c))
                acciones_posibles.append("rotar_tablero")
        return acciones_posibles

    def resultado(self, accion):
            tablero, jugadorX, jugadorO = copy.deepcopy(self.tablero), copy.deepcopy(self.jugadorX), copy.deepcopy(self.jugadorO)
            
            if accion == "rotar_tablero":
                (jugadorX if self.turno == 'x' else jugadorO).rotar_tablero(tablero)
            if accion[0] == "colocar_ficha":
                (jugadorX if self.turno == 'x' else jugadorO).colocar_ficha(tablero, accion[1])
            elif accion[0] == "borrar_columna":
                (jugadorX if self.turno == 'x' else jugadorO).borrar_columna(tablero, accion[1])
            
            return Estado(tablero, 'o' if self.turno == 'x' else 'x', jugadorX, jugadorO)
    
    def terminal(self):
        return self.tablero.comprobar_resultado()!='Continua'
    
    def evaluar(self):
        ficha_IA = self.jugadorO.ficha
        ficha_oponente = self.jugadorX.ficha
        puntaje_final = 0

        if self.tablero.comprobar_victoria(ficha_IA):
            return float('inf')
        if self.tablero.comprobar_victoria(ficha_oponente):
            return -float('inf')
        
        # Líneas horizontales
        for fila in range(FILAS):
            for col in range(COLUMNAS - 3):
                linea = [self.tablero.tablero[fila][col + i] for i in range(4)]
                puntaje_final+=self.contar_linea(linea)
        # Líneas verticales
        for col in range(COLUMNAS):
            for fila in range(FILAS - 3):
                linea = [self.tablero.tablero[fila + i][col] for i in range(4)]
                puntaje_final+=self.contar_linea(linea)
        # Líneas diagonales (de izquierda a derecha)
        for fila in range(FILAS - 3):
            for col in range(COLUMNAS - 3):
                linea = [self.tablero.tablero[fila + i][col + i] for i in range(4)]
                puntaje_final+=self.contar_linea(linea)
        # Líneas diagonales (de derecha a izquierda)
        for fila in range(FILAS - 3):
            for col in range(3, COLUMNAS):
                linea = [self.tablero.tablero[fila + i][col - i] for i in range(4)]
                puntaje_final+=self.contar_linea(linea)
        return puntaje_final


    def contar_linea(self,linea):
        if not (1 in linea and 2 in linea):
            if not 1 in linea and not 2 in linea:
                return 0
            if 1 in linea and 2 not in linea:
                cantidad=len([x for x in linea if x != 0])
                if cantidad==1:
                    return -1
                elif cantidad==2:
                    return -5
                elif cantidad==3:
                    return -50
            if 2 in linea and 1 not in linea:
                cantidad=len([x for x in linea if x != 0])
                if cantidad==1:
                    return 1
                elif cantidad==2:
                    return 5
                elif cantidad==3:
                    return 50
        return 0
    
    def evaluarGloton(self):
        ficha_IA = self.jugadorO.ficha
        ficha_oponente = self.jugadorX.ficha

        puntaje_final = 0

        if self.tablero.comprobar_victoria(ficha_IA):
            return float('inf')
        if self.tablero.comprobar_victoria(ficha_oponente):
            return -float('inf')
        
        # Líneas horizontales
        for fila in range(self.tablero.filas):
            for col in range(self.tablero.columnas - 3):
                linea = [self.tablero.tablero[fila][col + i] for i in range(4)]
                puntaje_final += self.contar_linea_normal(linea)
        
        # Líneas verticales
        for col in range(self.tablero.columnas):
            for fila in range(self.tablero.filas - 3):
                linea = [self.tablero.tablero[fila + i][col] for i in range(4)]
                puntaje_final += self.contar_linea_normal(linea)
        
        # Líneas diagonales (de izquierda a derecha)
        for fila in range(self.tablero.filas - 3):
            for col in range(self.tablero.columnas - 3):
                linea = [self.tablero.tablero[fila + i][col + i] for i in range(4)]
                puntaje_final += self.contar_linea_normal(linea)
        
        # Líneas diagonales (de derecha a izquierda)
        for fila in range(self.tablero.filas - 3):
            for col in range(3, self.tablero.columnas):
                linea = [self.tablero.tablero[fila + i][col - i] for i in range(4)]
                puntaje_final += self.contar_linea_normal(linea)
        
        return puntaje_final
    
    def contar_linea_normal(self, linea):
        if not (1 in linea and 2 in linea):
            if not 1 in linea and not 2 in linea:
                return 0
            if 1 in linea and 2 not in linea:
                cantidad = len([x for x in linea if x != 0])
                if cantidad == 1:
                    return -1
                elif cantidad == 2:
                    return -5
                elif cantidad == 3:
                    return -50
            if 2 in linea and 1 not in linea:
                cantidad = len([x for x in linea if x != 0])
                if cantidad == 1:
                    return 1
                elif cantidad == 2:
                    return 5
                elif cantidad == 3:
                    return 50
        return 0