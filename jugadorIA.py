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
        self.movimientos_realizadosI = 0
        self.movimientos_realizados = 0
    
    def decidirPrincipiante(self, tablero):
        busqueda = BusquedaNoDeterministica()
        opcion_elegida = busqueda.noDeterminista(tablero, self)
        self.realizarMovimiento(tablero, opcion_elegida)

    def decidirNormal(self, tablero, turno, jugadorX):
        busqueda = CriterioGloton(tablero)
        tableroC, jugadorXC, jugadorOC = copy.deepcopy(tablero), copy.deepcopy(jugadorX), copy.deepcopy(self)
        estado_inicial = Estado(tableroC, turno, jugadorXC, jugadorOC)
        accion_optima = busqueda.gloton(estado_inicial)
        print(f"Acción óptima a tomar: {accion_optima}")
        self.realizarMovimiento(tablero, accion_optima)

    def decidirAvanzado(self, tablero, turno, jugadorX):
        if self.movimientos_realizados < 2:
            columnas_centrales = [COLUMNAS // 2 - 1, COLUMNAS // 2, COLUMNAS // 2 + 1]
            columna_elegida = random.choice(columnas_centrales)
            self.realizarMovimiento(tablero, ("colocar_ficha", tablero, columna_elegida))
        else:
            busqueda = BusquedaMinMax(3)
            tableroC, jugadorXC, jugadorOC = copy.deepcopy(tablero), copy.deepcopy(jugadorX), copy.deepcopy(self)
            estado_inicial=Estado(tableroC, turno, jugadorXC,jugadorOC )
            valor_optimo,accion_optima = busqueda.minimax(estado_inicial, True, 0)
            print(f"Valor óptimo encontrado: {valor_optimo}")
            print(f"Acción óptima a tomar: {accion_optima}")
            if accion_optima is None:  # Si no se encuentra una acción óptima
                self.decidirPrincipiante(tablero)  # Llamar al método decidirPrincipiante
            else:
                self.realizarMovimiento(tablero, accion_optima)
                
    def realizarMovimiento(self, tablero, opcion_elegida):
        if opcion_elegida is None:
            return  # Si no hay una acción, no hacer nada
        if opcion_elegida[0] == "rotar_tablero" and self.movimientos_realizados >= 4:
            self.rotar_tablero(tablero)
        elif opcion_elegida[0] == "colocar_ficha":
            self.colocar_ficha(tablero, opcion_elegida[2])
            self.movimientos_realizados += 1
        elif opcion_elegida[0] == "borrar_columna" and self.movimientos_realizados >= 4:
            self.borrar_columna(tablero, opcion_elegida[2])
        self.movimientos_realizadosI += 1

class Estado:
    def __init__(self, tablero: Tablero, turno, jugadorX: Jugador, jugadorO: JugadorIA):
        self.tablero = tablero
        self.turno = turno
        self.jugadorX=jugadorX
        self.jugadorO=jugadorO
    
    def acciones(self):
        acciones_posibles = []
        if self.turno == 'x':
            for c in range(COLUMNAS):
                if self.tablero.es_ubicacion_valida(c):
                    acciones_posibles.append(("colocar_ficha", self.tablero, c))
        elif self.turno == 'o':
            for c in range(COLUMNAS):
                if self.tablero.es_ubicacion_valida(c):
                    acciones_posibles.append(("colocar_ficha", self.tablero, c))
        # Verificar si el jugador actual ha realizado al menos 4 movimientos
        if len(acciones_posibles) >= 4:
            if self.turno == 'x' and self.jugadorX.movimientos_realizados >= 4:
                if self.jugadorX.borrarPosible():
                    for c in range(COLUMNAS):
                        acciones_posibles.append(("borrar_columna", self.tablero, c))
                acciones_posibles.append(("rotar_tablero", self.tablero))
            elif self.turno == 'o' and self.jugadorO.movimientos_realizados >= 4:
                if self.jugadorO.borrarPosible():
                    for c in range(COLUMNAS):
                        acciones_posibles.append(("borrar_columna", self.tablero, c))
                acciones_posibles.append(("rotar_tablero", self.tablero))
        return acciones_posibles

    def resultado(self, accion):
            tablero, jugadorX, jugadorO = copy.deepcopy(self.tablero), copy.deepcopy(self.jugadorX), copy.deepcopy(self.jugadorO)
            
            if accion[0] == "rotar_tablero":
                (jugadorX if self.turno == 'x' else jugadorO).rotar_tablero(tablero)
            elif accion[0] == "colocar_ficha":
                (jugadorX if self.turno == 'x' else jugadorO).colocar_ficha(tablero, accion[2])
            elif accion[0] == "borrar_columna":
                (jugadorX if self.turno == 'x' else jugadorO).borrar_columna(tablero, accion[2])
            
            return Estado(tablero, 'o' if self.turno == 'x' else 'x', jugadorX, jugadorO)
    
    def terminal(self):
        return self.tablero.comprobar_resultado()!='Continua'
    
    def evaluar(self):
        ficha_IA = self.jugadorO.ficha
        ficha_oponente = self.jugadorX.ficha

        peso_tres = 100
        peso_dos = 10
        peso_uno = 1
        puntaje_final = 0

        # Evaluar jugadas inmediatas para ganar o bloquear
        for c in range(COLUMNAS):
            if self.tablero.es_ubicacion_valida(c):
                fila_disponible = self.tablero.obtener_fila_disponible(c)
                if fila_disponible is not None:
                    # Simular movimiento de la IA
                    self.tablero.tablero[fila_disponible][c] = ficha_IA
                    if self.tablero.comprobar_resultado() == self.jugadorO.ficha:
                        puntaje_final += float('inf')  # Prioridad máxima para ganar
                    # Simular movimiento del oponente
                    self.tablero.tablero[fila_disponible][c] = ficha_oponente
                    if self.tablero.comprobar_resultado() == self.jugadorX.ficha:
                        puntaje_final -= float('inf')  # Prioridad máxima para bloquear
                    # Restaurar estado original
                    self.tablero.tablero[fila_disponible][c] = 0

        for r in range(FILAS):
            for c in range(COLUMNAS):
                if self.tablero.tablero[r][c] == 0:  # Evaluar sólo si la posición está vacía
                    if c <= COLUMNAS - 4:
                        line = self.tablero.tablero[r, c:c+4]
                        puntaje_final += self.evaluar_linea(line, ficha_IA, ficha_oponente, peso_tres, peso_dos, peso_uno)
                    if r <= FILAS - 4:
                        line = self.tablero.tablero[r:r+4, c]
                        puntaje_final += self.evaluar_linea(line, ficha_IA, ficha_oponente, peso_tres, peso_dos, peso_uno)
                    if r <= FILAS - 4 and c <= COLUMNAS - 4:
                        line = np.array([self.tablero.tablero[r+i][c+i] for i in range(4)])
                        puntaje_final += self.evaluar_linea(line, ficha_IA, ficha_oponente, peso_tres, peso_dos, peso_uno)
                    if r >= 3 and c <= COLUMNAS - 4:
                        line = np.array([self.tablero.tablero[r-i][c+i] for i in range(4)])
                        puntaje_final += self.evaluar_linea(line, ficha_IA, ficha_oponente, peso_tres, peso_dos, peso_uno)

        return puntaje_final


    def evaluar_linea(self, line, ficha_IA, ficha_oponente, peso_tres, peso_dos, peso_uno):
        puntaje = 0

        # IA está a punto de ganar
        if np.sum(line == ficha_IA) == 3 and np.sum(line == 0) == 1:
            puntaje += float('inf')  # Ganar es el mejor resultado posible

        # Penalizar si el oponente está a punto de ganar
        if np.sum(line == ficha_oponente) == 3 and np.sum(line == 0) == 1:
            puntaje -= float('inf')  # Perder es el peor resultado posible

        # Evaluar otras configuraciones
        if np.sum(line == ficha_IA) == 2 and np.sum(line == 0) == 2:
            puntaje += peso_dos

        if np.sum(line == ficha_IA) == 1 and np.sum(line == 0) == 3:
            puntaje += peso_uno

        if np.sum(line == ficha_oponente) == 2 and np.sum(line == 0) == 2:
            puntaje -= peso_dos

        if np.sum(line == ficha_oponente) == 1 and np.sum(line == 0) == 3:
            puntaje -= peso_uno

        return puntaje
    
    
    
    def evaluarGloton(self):
        return self.calcular_valor(self.turno) - self.calcular_valor('o' if self.turno == 'x' else 'x')

    def calcular_valor(self, ficha):
        valor = 0
        peso_cuatro = 100
        peso_tres = 10
        peso_dos = 1

        for r in range(self.tablero.filas):
            for c in range(self.tablero.columnas):
                if self.tablero.tablero[r][c] == ficha:
                    if c <= self.tablero.columnas - 4:
                        line = self.tablero.tablero[r][c:c + 4]
                        valor += self.evaluar_linea_normal(line, ficha, peso_cuatro, peso_tres, peso_dos)
                    if r <= self.tablero.filas - 4:
                        line = [self.tablero.tablero[r + i][c] for i in range(4)]
                        valor += self.evaluar_linea_normal(line, ficha, peso_cuatro, peso_tres, peso_dos)
                    if r <= self.tablero.filas - 4 and c <= self.tablero.columnas - 4:
                        line = [self.tablero.tablero[r + i][c + i] for i in range(4)]
                        valor += self.evaluar_linea_normal(line, ficha, peso_cuatro, peso_tres, peso_dos)
                    if r >= 3 and c <= self.tablero.columnas - 4:
                        line = [self.tablero.tablero[r - i][c + i] for i in range(4)]
                        valor += self.evaluar_linea_normal(line, ficha, peso_cuatro, peso_tres, peso_dos)
        return valor

    def evaluar_linea_normal(self, linea, ficha, peso_cuatro, peso_tres, peso_dos):
        count_ficha = linea.count(ficha)
        count_vacio = linea.count('-')

        if count_ficha == 4:
            return peso_cuatro
        elif count_ficha == 3 and count_vacio == 1:
            return peso_tres
        elif count_ficha == 2 and count_vacio == 2:
            return peso_dos
        return 0