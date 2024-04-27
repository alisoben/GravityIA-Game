import numpy as np
import pygame
import sys
import math

# Colores
AZUL = (130, 0, 80)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
AMARILLO = (255, 255, 0)

# Configuración del tablero
FILAS = 6
COLUMNAS = 7
TAMANO = 100
RADIO = int(TAMANO / 2 - 5)

pygame.init()
ancho = COLUMNAS * TAMANO
alto = (FILAS + 1) * TAMANO
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Gravity Game")
fuente = pygame.font.SysFont("monospace", 75)

def crear_tablero():
    return np.zeros((FILAS, COLUMNAS))

def dibujar_tablero(tablero):
    pantalla.fill(NEGRO)
    for c in range(COLUMNAS):
        for r in range(FILAS):
            pygame.draw.rect(pantalla, AZUL, (c * TAMANO, r * TAMANO + TAMANO, TAMANO, TAMANO))
            pygame.draw.circle(pantalla, NEGRO, (int(c * TAMANO + TAMANO / 2), int(r * TAMANO + TAMANO + TAMANO / 2)), RADIO)
    for c in range(COLUMNAS):
        for r in range(FILAS):
            if tablero[r][c] == 1:
                pygame.draw.circle(pantalla, ROJO, (int(c * TAMANO + TAMANO / 2), alto - int(r * TAMANO + TAMANO / 2)), RADIO)
            elif tablero[r][c] == 2:
                pygame.draw.circle(pantalla, AMARILLO, (int(c * TAMANO + TAMANO / 2), alto - int(r * TAMANO + TAMANO / 2)), RADIO)
    pygame.display.update()

def borrar_columna(tablero, columna):
    """Borra una columna del tablero estableciendo todos sus valores a 0."""
    if 0 <= columna < COLUMNAS:
        tablero[:, columna] = 0

def comprobar_victoria(tablero, ficha):
    # Comprobaciones horizontales, verticales y diagonales
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

def juego_terminado(mensaje):
    label = fuente.render(mensaje, True, ROJO if "1" in mensaje else AMARILLO)
    pantalla.blit(label, (40, 10))
    pygame.display.update()
    pygame.time.wait(3000)
    sys.exit()

def colocar_ficha(tablero, fila, col, pieza):
    tablero[fila][col] = pieza

def es_ubicacion_valida(tablero, col):
    return tablero[FILAS-1][col] == 0

def obtener_siguiente_fila_libre(tablero, col):
    for r in range(FILAS):
        if tablero[r][col] == 0:
            return r

tablero = crear_tablero()
dibujar_tablero(tablero)
turno = 0
juego_en_curso = True

while juego_en_curso:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            sys.exit()

        if evento.type == pygame.MOUSEBUTTONDOWN:
            posx = evento.pos[0]
            columna = int(math.floor(posx / TAMANO))

            if evento.button == 1:  # Click izquierdo para colocar ficha
                if es_ubicacion_valida(tablero, columna):
                    fila = obtener_siguiente_fila_libre(tablero, columna)
                    colocar_ficha(tablero, fila, columna, turno+1)

                    if comprobar_victoria(tablero, turno+1):
                        juego_terminado(f"Jugador {turno + 1} gana!")
                    turno = 1 - turno
                    dibujar_tablero(tablero)
            elif evento.button == 3:  # Click derecho para borrar columna
                borrar_columna(tablero, columna)
                dibujar_tablero(tablero)
                turno = 1 - turno 