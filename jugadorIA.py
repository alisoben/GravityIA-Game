import copy
from jugador import *
from tablero import *
from busquedaMinMax import *
from busquedaNoDeterministica import *

class JugadorIA(Jugador):
    def __init__(self, ficha):
        super().__init__(ficha)
    
    def decidirPrincipiante(self, tablero):
        busqueda = BusquedaNoDeterministica()
        opcion_elegida = busqueda.noDeterminista(tablero, self)
        self.realizarMovimiento(opcion_elegida)

    def decidirAvanzado(self, tablero, turno, jugadorX):
        busqueda = BusquedaMinMax(4)
        tableroC, jugadorXC, jugadorOC = copy.deepcopy(tablero), copy.deepcopy(jugadorX), copy.deepcopy(self)
        estado_inicial=Estado(tableroC, turno, jugadorXC,jugadorOC )
        valor_optimo,accion_optima = busqueda.minimax(estado_inicial, True, 0)
        print(f"Valor óptimo encontrado: {valor_optimo}")
        print(f"Acción óptima a tomar: {accion_optima}")
        self.realizarMovimiento(tablero, accion_optima)

    def realizarMovimiento(self, tablero, opcion_elegida):
        if opcion_elegida[0] == "rotar_tablero":
            self.rotar_tablero(tablero)
        elif opcion_elegida[0] == "colocar_ficha":
            self.colocar_ficha(tablero, opcion_elegida[2])
        elif opcion_elegida[0] == "borrar_columna":
            self.borrar_columna(tablero, opcion_elegida[2])

class Estado:
    def __init__(self, tablero: Tablero, turno, jugadorX: Jugador, jugadorO: JugadorIA):
        self.tablero = tablero
        self.turno = turno
        self.jugadorX=jugadorX
        self.jugadorO=jugadorO
    
    def acciones(self):
        acciones_posibles = [("rotar_tablero", self.tablero)]
        if self.turno=='x':
            for c in range(COLUMNAS):
                if self.tablero.es_ubicacion_valida(c):
                    acciones_posibles.append(("colocar_ficha", self.tablero, c))
            if self.jugadorX.borrarPosible():
                for c in range(COLUMNAS):
                    acciones_posibles.append(("borrar_columna", self.tablero, c))

        if self.turno=='o':
            for c in range(COLUMNAS):
                if self.tablero.es_ubicacion_valida(c):
                    acciones_posibles.append(("colocar_ficha", self.tablero, c))
            if self.jugadorO.borrarPosible():
                for c in range(COLUMNAS):
                    acciones_posibles.append(("borrar_columna", self.tablero, c))
        
        return acciones_posibles

    def resultado(self, accion):
            tablero, jugadorX, jugadorO = copy.deepcopy(self.tablero), copy.deepcopy(self.jugadorX), copy.deepcopy(self.jugadorO)
            
            if accion[0] == "rotar_tablero":
                (jugadorX if self.turno == 'x' else jugadorO).rotar_tablero(accion[1])
            elif accion[0] == "colocar_ficha":
                (jugadorX if self.turno == 'x' else jugadorO).colocar_ficha(accion[1], accion[2])
            elif accion[0] == "borrar_columna":
                (jugadorX if self.turno == 'x' else jugadorO).borrar_columna(accion[1], accion[2])
            
            return Estado(tablero, 'o' if self.turno == 'x' else 'x', jugadorX, jugadorO)
    
    def terminal(self):
        return self.tablero.comprobar_resultado()!='Continua'
    
    def evaluar(self):
        #fichas al medio tienen mas probabilidades de formar 4
        #mas fichas mas probabilidad de ganar
        #
        
        
        
        




    
