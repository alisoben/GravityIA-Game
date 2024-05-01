#gravity version X.1
# main.py
import pygame
import math
import sys
from logic import crear_tablero, colocar_ficha, es_ubicacion_valida, obtener_siguiente_fila_libre, comprobar_resultado, juego_terminado, borrar_columna, rotar_tablero, aplicar_gravedad
from interface import dibujar_tablero
from config import TAMANO

tablero = crear_tablero()
turno = 0
cx, co = 4, 4  # Contadores de turnos para borrar columnas
cex, ceo = 0, 0  # Contadores de usos de borrar columnas
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
                    colocar_ficha(tablero, fila, columna, turno + 1)
                    dibujar_tablero(tablero, turno)
                    resultado = comprobar_resultado(tablero)
                    if resultado != "Continua":
                        juego_terminado(resultado)
                    if turno == 0:
                        cx = max(0, cx - 1)
                    else:
                        co = max(0, co - 1)
                    turno = 1 - turno
                    print("Después de colocar ficha:")
                    print("cx:", cx, "co:", co, "cex:", cex, "ceo:", ceo)

            elif evento.button == 3:  # Click derecho para borrar columna
                if (turno == 0 and cx == 0 and cex < 4):
                    borrar_columna(tablero, columna)
                    cex += 1
                    cx = 4
                    dibujar_tablero(tablero, turno)
                    turno = 1 - turno
                    print("Columna borrada por Jugador 1")
                elif (turno == 1 and co == 0 and ceo < 4):
                    borrar_columna(tablero, columna)
                    ceo += 1
                    co = 4
                    dibujar_tablero(tablero, turno)
                    turno = 1 - turno
                    print("Columna borrada por Jugador 2")
                print("Después de borrar columna:")
                print("cx:", cx, "co:", co, "cex:", cex, "ceo:", ceo)

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_r:  # Presionar 'r' para rotar el tablero
                tablero = rotar_tablero(tablero)
                aplicar_gravedad(tablero)
                dibujar_tablero(tablero, turno)
                resultado = comprobar_resultado(tablero)
                if resultado != "Continua":  # Revisar si el jugador actual ha ganado después de girar
                    juego_terminado(resultado)
                if turno == 0:
                    cx = max(0, cx - 1)
                else:
                    co = max(0, co - 1)
                turno = 1 - turno
                print("Después de rotar tablero:")
                print("cx:", cx, "co:", co, "cex:", cex, "ceo:", ceo)