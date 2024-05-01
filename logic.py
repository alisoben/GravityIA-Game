# logic.py
import numpy as np
from config import COLUMNAS, FILAS
from interface import pantalla, fuente, AZUL, AMARILLO, BLANCO, dibujar_tablero
import pygame
import sys

def crear_tablero():
    return np.zeros((FILAS, COLUMNAS))

def aplicar_gravedad(tablero):
    for col in range(COLUMNAS):
        columna_invertida = tablero[:, col][::-1]
        nuevas_fichas = columna_invertida[columna_invertida != 0]
        tablero[:, col] = np.concatenate([np.zeros(FILAS - len(nuevas_fichas)), nuevas_fichas])[::-1]

def rotar_tablero(tablero):
    return np.flipud(np.fliplr(tablero))

def colocar_ficha(tablero, fila, col, pieza):
    tablero[fila][col] = pieza

def borrar_columna(tablero, columna):
    if 0 <= columna < COLUMNAS:
        tablero[:, columna] = 0

def comprobar_victoria(tablero, ficha):
    for c in range(COLUMNAS - 3):
        for r in range(FILAS):
            if all(tablero[r][c + i] == ficha for i in range(4)):
                return True
    for c in range(COLUMNAS):
        for r in range(FILAS - 3):
            if all(tablero[r + i][c] == ficha for i in range(4)):
                return True
    for c in range(COLUMNAS - 3):
        for r in range(FILAS - 3):
            if all(tablero[r + i][c + i] == ficha for i in range(4)):
                return True
    for c in range(COLUMNAS - 3):
        for r in range(3, FILAS):
            if all(tablero[r - i][c + i] == ficha for i in range(4)):
                return True
    return False

def comprobar_resultado(tablero):
    jugador1 = comprobar_victoria(tablero,1)
    jugador2 = comprobar_victoria(tablero,2)
    if jugador1 and jugador2:
        return "Empate"
    elif jugador1:
        return "Jugador 1 gana!"
    elif jugador2:
        return "Jugador 2 gana!"
    else:
        return "Continua"

def juego_terminado(mensaje):
    if "1" in mensaje:
        color=AZUL
    elif "2" in mensaje:
        color=AMARILLO
    else:
        color=BLANCO
    label = fuente.render(mensaje, True, color)
    pantalla.blit(label, (40, 10))
    pygame.display.update()
    pygame.time.wait(4000)
    sys.exit()

def es_ubicacion_valida(tablero, col):
    return tablero[FILAS-1][col] == 0

def obtener_siguiente_fila_libre(tablero, col):
    for r in range(FILAS):
        if tablero[r][col] == 0:
            return r