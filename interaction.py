#interaction.py

import pygame
import sys
import math
from logic import *
from interface import *
from config import *
from ia import *

def jugar_humano_humano():
    pygame.init()
    pantalla = pygame.display.set_mode((COLUMNAS * TAMANO + MARGEN_DER, FILAS * TAMANO + MARGEN_SUP))
    pygame.display.set_caption("Gravity Connect 4")
    tablero = crear_tablero()
    turno = 0
    cx, co = 4, 4
    cex, ceo = 0, 0
    dibujar_tablero(tablero, turno+1)  
    
    juego_en_curso = True

    while juego_en_curso:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
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
                            juego_en_curso = False  # Termina el bucle de juego
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
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:  # Presionar 'r' para rotar el tablero
                    tablero = rotar_tablero(tablero)
                    aplicar_gravedad(tablero)
                    dibujar_tablero(tablero, turno)
                    resultado = comprobar_resultado(tablero)
                    if resultado != "Continua":  # Revisar si el jugador actual ha ganado después de girar
                        juego_terminado(resultado)
                        juego_en_curso = False
                    if turno == 0:
                        cx = max(0, cx - 1)
                    else:
                        co = max(0, co - 1)
                    turno = 1 - turno
                    print("Después de rotar tablero:")
                    print("cx:", cx, "co:", co, "cex:", cex, "ceo:", ceo)
    
    return "MENU" 

def jugar_humano_ia(nivel):
    pygame.init()
    pantalla = pygame.display.set_mode((COLUMNAS * TAMANO + MARGEN_DER, FILAS * TAMANO + MARGEN_SUP))
    pygame.display.set_caption("Gravity Connect 4")
    tablero = crear_tablero()
    turno = 0  # 0 para humano, 1 para IA
    juego_en_curso = True

    ia = crear_ia(nivel)  # Crea la instancia de la IA
    last_ia_move_time = pygame.time.get_ticks()

    # Contadores para el humano y la IA
    cx, co = 4, 4
    cex, ceo = 0, 0

    while juego_en_curso:
        current_time = pygame.time.get_ticks()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if turno == 0:  # Turno del humano
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    posx = evento.pos[0]
                    columna = int(math.floor(posx / TAMANO))

                    if evento.button == 1 and es_ubicacion_valida(tablero, columna):
                        fila = obtener_siguiente_fila_libre(tablero, columna)
                        colocar_ficha(tablero, fila, columna, 1)
                        if comprobar_resultado(tablero) != "Continua":
                            dibujar_tablero(tablero, turno)
                            juego_terminado(comprobar_resultado(tablero))
                            juego_en_curso = False
                        cx = max(0, cx - 1)
                        turno = 1

                    elif evento.button == 3 and cex < 4:
                        if cx == 0:
                            borrar_columna(tablero, columna)
                            cex += 1
                            cx = 4
                            if comprobar_resultado(tablero) != "Continua":
                                dibujar_tablero(tablero, turno)
                                juego_terminado(comprobar_resultado(tablero))
                                juego_en_curso = False
                            turno = 1

                elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
                    if cx == 0:
                        tablero = rotar_tablero(tablero)
                        aplicar_gravedad(tablero)
                        if comprobar_resultado(tablero) != "Continua":
                            dibujar_tablero(tablero, turno)
                            juego_terminado(comprobar_resultado(tablero))
                            juego_en_curso = False
                        cx = 4
                        turno = 1

        if turno == 1 and juego_en_curso and current_time >= last_ia_move_time:  # Turno de la IA
            ia_accion = random.choice(['colocar', 'colocar', 'colocar'])

            if ia_accion == 'colocar':
                columna_ia = ia.elegir_columna(tablero)
                if columna_ia is not None and es_ubicacion_valida(tablero, columna_ia):
                    fila_ia = obtener_siguiente_fila_libre(tablero, columna_ia)
                    colocar_ficha(tablero, fila_ia, columna_ia, 2)
                    if comprobar_resultado(tablero, vs_ia=True) != "Continua":
                        dibujar_tablero(tablero, turno)
                        juego_terminado(comprobar_resultado(tablero, vs_ia=True))
                        pygame.time.wait(2000) 
                        juego_en_curso = False
                    co = max(0, co - 1)
                    turno = 0

            elif ia_accion == 'borrar' and ceo < 4:
                columna_ia = random.choice([c for c in range(COLUMNAS)])
                borrar_columna(tablero, columna_ia)
                ceo += 1
                co = 4
                if comprobar_resultado(tablero) != "Continua":
                    dibujar_tablero(tablero, turno)
                    juego_terminado(comprobar_resultado(tablero))
                    juego_en_curso = False
                turno = 0

            elif ia_accion == 'rotar'and ceo < 4:
                tablero = rotar_tablero(tablero)
                aplicar_gravedad(tablero)
                if comprobar_resultado(tablero) != "Continua":
                    dibujar_tablero(tablero, turno)
                    juego_terminado(comprobar_resultado(tablero))
                    juego_en_curso = False
                turno = 0
                
            last_ia_move_time = current_time + 2000 
        dibujar_tablero(tablero, turno)
        

    return "MENU"

#if __name__ == "__main__":
#   jugar_humano_humano()