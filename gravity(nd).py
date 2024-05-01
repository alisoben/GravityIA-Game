#gravity version 1.1

import math
import pygame
import numpy as np
import sys

# Colores
GUINDA = (130, 0, 80)
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)
ROJO = (255, 0, 0)
BLANCO = (255, 255, 255)

# Configuración del tablero
FILAS = 7
COLUMNAS = 7
TAMANO = 100
RADIO = int(TAMANO / 2 - 5)
MARGEN_SUP=100
MARGEN_DER=150


pygame.init()
ancho = (COLUMNAS * TAMANO) + MARGEN_DER
alto = FILAS * TAMANO + MARGEN_SUP
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Gravity Game")
fuente = pygame.font.SysFont("monospace", 75)
fuente2 = pygame.font.SysFont("monospace", 30)

cx, co = 4, 4  # Contadores de turnos para borrar columnas
cex, ceo = 0, 0  # Contadores de usos de borrar columnas


def crear_tablero():
    return np.zeros((FILAS, COLUMNAS))

# Jugador 1->Azul->X
# Jugador 2->Amarillo->O

def dibujar_tablero(tablero, turno):
    pantalla.fill(NEGRO)
    for c in range(COLUMNAS):
        for r in range(FILAS):
            pygame.draw.rect(pantalla, GUINDA, (c * TAMANO, r * TAMANO + MARGEN_SUP, TAMANO, TAMANO))
            pygame.draw.circle(pantalla, NEGRO, (int(c * TAMANO + TAMANO / 2), int(r * TAMANO + MARGEN_SUP + TAMANO / 2)), RADIO)
    for c in range(COLUMNAS):
        for r in range(FILAS):
            if tablero[r][c] == 1:
                pygame.draw.circle(pantalla, AZUL, (int(c * TAMANO + TAMANO / 2), alto - int(r * TAMANO + TAMANO / 2)), RADIO)
            elif tablero[r][c] == 2:
                pygame.draw.circle(pantalla, AMARILLO, (int(c * TAMANO + TAMANO / 2), alto - int(r * TAMANO + TAMANO / 2)), RADIO)
    
    #Indicador del turno
    turno = 1 - turno
    ficha = turno + 1
    label = fuente2.render("Turno", True, BLANCO)
    pantalla.blit(label, (COLUMNAS * TAMANO, 10))
    pygame.draw.circle(pantalla, AZUL if ficha == 1 else AMARILLO, ((COLUMNAS * TAMANO) + 120,25), 20)
    
    
    
    pygame.display.update()


def aplicar_gravedad(tablero):
    for col in range(COLUMNAS):
        columna_invertida = tablero[:, col][::-1]
        nuevas_fichas = columna_invertida[columna_invertida != 0]
        tablero[:, col] = np.concatenate([np.zeros(FILAS - len(nuevas_fichas)), nuevas_fichas])[::-1]

#agregar contadores
def rotar_tablero(tablero):
    return np.flipud(np.fliplr(tablero))

#agregar contadores
def colocar_ficha(tablero, fila, col, pieza):
    tablero[fila][col] = pieza

#agregar contadores
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



tablero = crear_tablero()
turno = 0
dibujar_tablero(tablero, turno+1)
juego_en_curso = True




while juego_en_curso:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            sys.exit()

        if evento.type == pygame.MOUSEBUTTONDOWN:
            posx = evento.pos[0]
            columna = int(math.floor(posx / TAMANO))

            if evento.button == 1:  # Click izquierdo para soltar ficha
                if es_ubicacion_valida(tablero, columna):
                    fila = obtener_siguiente_fila_libre(tablero, columna)
                    colocar_ficha(tablero, fila, columna, turno+1)
                    dibujar_tablero(tablero,turno)
                    resultado=comprobar_resultado(tablero)
                    if resultado!="Continua":
                        juego_terminado(resultado)
                    if turno == 0:
                        cx = max(0, cx - 1)
                    else:
                        co = max(0, co - 1)
                    turno = 1 - turno
                    
                    print("cx:", cx)
                    print("co:", co)
                    print("cex:", cex)
                    print("ceo:", ceo)
                    

            elif evento.button == 3:  # Click derecho para borrar columna
                if(turno == 0 and cx == 0 and cex < 4):
                    borrar_columna(tablero, columna)
                    cex += 1
                    cx = 4
                    dibujar_tablero(tablero,turno)
                    turno = 1 - turno
                elif (turno == 1 and co == 0 and ceo < 4):
                    borrar_columna(tablero, columna)
                    ceo += 1
                    co = 4
                    dibujar_tablero(tablero,turno)
                    turno = 1 - turno
                    
                    print("cx:", cx)
                    print("co:", co)
                    print("cex:", cex)
                    print("ceo:", ceo)
                    

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_r:  # Presionar 'r' para rotar el tablero
                tablero = rotar_tablero(tablero)
                aplicar_gravedad(tablero)
                dibujar_tablero(tablero,turno)
                resultado=comprobar_resultado(tablero)
                if resultado!="Continua":  # Revisar si el jugador actual ha ganado después de girar
                    juego_terminado(resultado)
                if turno == 0:
                    cx = max(0, cx - 1)
                else:
                    co = max(0, co - 1)
                turno = 1 - turno
                
                print("cx:", cx)
                print("co:", co)
                print("cex:", cex)
                print("ceo:", ceo)
