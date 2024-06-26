import numpy as np
class Jugador:
    def __init__(self,ficha):
        self.c=4  #turnos hasta poder borrar
        self.ce=0  #borrados usados
        self.ficha=ficha
    
    def jugar(self):
        if self.c>0:
            self.c-=1
    
    def jugar_mov_especial(self):
            self.ce+=1
            self.c=4

    def mov_especial_posible(self):
        return self.ce<4 and self.c==0

    def getC(self):
        return self.c

    def getCE(self):
        return self.ce

    def rotar_tablero(self,tablero):
        self.jugar_mov_especial()
        tablero.rotar_tablero()

    def colocar_ficha(self,tablero,col):
        self.jugar()
        tablero.colocar_ficha(self.ficha,col)
    
    def borrar_columna(self,tablero,col):
        self.jugar_mov_especial()
        tablero.borrar_columna(col)