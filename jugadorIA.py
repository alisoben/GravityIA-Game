import copy
import numpy as np
from jugador import *
from tablero import *
from config import *
from busquedaMinMax import *
from busquedaNoDeterministica import *
from busquedaGloton import *


class JugadorIA(Jugador):
    def __init__(self, ficha,nivel):
        super().__init__(ficha)
        self.nivel=nivel

    def decidir(self, tablero, turno, jugadorX):
        if self.nivel=='principiante':
            self.decidirPrincipiante(tablero,turno,jugadorX)
        elif self.nivel=='intermedio':
            self.decidirNormal(tablero,turno,jugadorX)
        else:
            self.decidirAvanzado(tablero,turno,jugadorX)
    
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
        busqueda = BusquedaMinMax(4)
        tableroC, jugadorXC, jugadorOC = copy.deepcopy(tablero), copy.deepcopy(jugadorX), copy.deepcopy(self)
        estado_inicial=Estado(tableroC, turno, jugadorXC,jugadorOC )
        valor_optimo,accion_optima = busqueda.minimax(estado_inicial, True, 0, float('-inf'), float('inf'))
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
            if self.jugadorX.mov_especial_posible():
                for c in range(COLUMNAS):
                    acciones_posibles.append(("borrar_columna", c))
                acciones_posibles.append("rotar_tablero")
        elif self.turno == 'o':
            if self.jugadorO.mov_especial_posible():
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
        
        gana_IA = self.tablero.comprobar_victoria(ficha_IA)
        gana_j = self.tablero.comprobar_victoria(ficha_oponente)
        if gana_IA and gana_j:
            return 0
        elif gana_IA:
            return float('inf')
        elif gana_j:
            return -float('inf')
        
        for fila in range(FILAS):
            for col in range(COLUMNAS):
                if col <= COLUMNAS - 4:
                    # Líneas horizontales
                    linea = self.tablero.tablero[fila][col:col+4]
                    puntaje_final += self.calcular_puntaje_linea(linea)
                if fila <= FILAS - 4:
                    # Líneas verticales
                    linea = [self.tablero.tablero[fila+i][col] for i in range(4)]
                    puntaje_final += self.calcular_puntaje_linea(linea)
                if col <= COLUMNAS - 4 and fila <= FILAS - 4:
                    # Líneas diagonales (de izquierda a derecha)
                    linea = [self.tablero.tablero[fila+i][col+i] for i in range(4)]
                    puntaje_final += self.calcular_puntaje_linea(linea)
                if col >= 3 and fila <= FILAS - 4:
                    # Líneas diagonales (de derecha a izquierda)
                    linea = [self.tablero.tablero[fila+i][col-i] for i in range(4)]
                    puntaje_final += self.calcular_puntaje_linea(linea)
                    
        puntaje_final +=2*(self.tablero.contarFichas(ficha_IA)-self.tablero.contarFichas(ficha_oponente))
        
        return puntaje_final


    def calcular_puntaje_linea(self,linea):
        suma = sum(linea)
        if 1 in linea and not 2 in linea:
            if suma==1:
                return -1
            elif suma==2:
                return -5
            elif suma==3:
                return -30
        if 2 in linea and 1 not in linea:
            suma=suma/2
            if suma==1:
                return 1
            elif suma==2:
                return 5
            elif suma==3:
                return 30
        return 0