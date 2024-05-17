import numpy as np
class Tablero:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.tablero = self.inicializar_tablero()
    
    def inicializar_tablero(self):
        return np.zeros((self.filas, self.columnas))
    
    def obtener_siguiente_fila_libre(self, col):
        for r in range(self.filas):
            if self.tablero[r][col] == 0:
                return r
    
    def rotar_tablero(self):
        self.tablero = np.flipud(np.fliplr(self.tablero))
        self.aplicar_gravedad()
    
    def colocar_ficha(self, ficha, col):
        fila = self.obtener_siguiente_fila_libre(col)
        self.tablero[fila][col] = ficha
    
    def borrar_columna(self, columna):
        if 0 <= columna < self.columnas:
            self.tablero[:, columna] = 0

    def aplicar_gravedad(self):
        for col in range(self.columnas):
            columna_invertida = self.tablero[:, col][::-1]
            nuevas_fichas = columna_invertida[columna_invertida != 0]
            self.tablero[:, col] = np.concatenate([np.zeros(self.filas - len(nuevas_fichas)), nuevas_fichas])[::-1]
    
    def es_ubicacion_valida(self, col):
        return self.tablero[self.filas - 1][col] == 0
    
    def comprobar_tablero_lleno(self):
        return np.all(self.tablero != 0)
    
    def comprobar_victoria(self, ficha):
        for c in range(self.columnas - 3):
            for r in range(self.filas):
                if all(self.tablero[r][c + i] == ficha for i in range(4)):
                    return True
        for c in range(self.columnas):
            for r in range(self.filas - 3):
                if all(self.tablero[r + i][c] == ficha for i in range(4)):
                    return True
        for c in range(self.columnas - 3):
            for r in range(self.filas - 3):
                if all(self.tablero[r + i][c + i] == ficha for i in range(4)):
                    return True
        for c in range(self.columnas - 3):
            for r in range(3, self.filas):
                if all(self.tablero[r - i][c + i] == ficha for i in range(4)):
                    return True
        return False
    
    def comprobar_resultado(self):
        gana_j1 = self.comprobar_victoria(1)
        gana_j2 = self.comprobar_victoria(2)
        lleno = self.comprobar_tablero_lleno()
        if (gana_j1 and gana_j2) or lleno:
            return "Empate"
        elif gana_j1:
            return "Jugador 1 gana!"
        elif gana_j2:
            return "Jugador 2 gana!"
        else:
            return "Continua"

    def getPosiciones(self):
        return self.tablero
    
    def contarFichas(self,ficha):
        return np.count_nonzero(self.tablero==ficha)
    
    def contar_linea_3(self,ficha):
        contador=0
        for c in range(self.columnas - 2):
            for r in range(self.filas):
                if all(self.tablero[r][c + i] == ficha for i in range(3)):
                    contador+=1
        for c in range(self.columnas):
            for r in range(self.filas - 2):
                if all(self.tablero[r + i][c] == ficha for i in range(3)):
                    contador+=1
        for c in range(self.columnas - 2):
            for r in range(self.filas - 2):
                if all(self.tablero[r + i][c + i] == ficha for i in range(3)):
                    contador+=1
        for c in range(self.columnas - 3):
            for r in range(2, self.filas):
                if all(self.tablero[r - i][c + i] == ficha for i in range(3)):
                    contador+=1
        return contador
    
