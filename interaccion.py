import numpy as np
import math
from config import *
from interfaz import *
from tablero import *
from jugador import *
from jugadorIA import *
import pygame
import sys

def jugar_humano_humano():
    pygame.init()
    pantalla = pygame.display.set_mode((COLUMNAS * TAMANO + MARGEN_DER, FILAS * TAMANO + MARGEN_SUP))
    pygame.display.set_caption("Gravity-HvsH")
    tablero=Tablero(FILAS,COLUMNAS)
    jugadorX=Jugador(1)
    jugadorO=Jugador(2)
    turno='x'
    dibujar_escenario(tablero,jugadorX,jugadorO,turno)
    juego_en_curso = True

    while juego_en_curso:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                posx = evento.pos[0]
                if posx<TAMANO*COLUMNAS:
                    columna = int(math.floor(posx / TAMANO))
                else:
                    break
                    
                if evento.button == 1:  # Click izquierdo para colocar ficha
                    if tablero.es_ubicacion_valida(columna):
                        if turno == 'x':
                            jugadorX.colocar_ficha(tablero,columna)
                            turno = 'o'
                        else:
                            jugadorO.colocar_ficha(tablero,columna)
                            turno = 'x'
                        dibujar_escenario(tablero,jugadorX,jugadorO,turno)
                elif evento.button == 3:  # Click derecho para borrar columna
                    if turno == 'x' and jugadorX.borrarPosible():
                        jugadorX.borrar_columna(tablero,columna)
                        turno = 'o'
                    elif turno == 'o' and jugadorO.borrarPosible():
                        jugadorO.borrar_columna(tablero,columna)
                        turno = 'x'
                    dibujar_escenario(tablero,jugadorX,jugadorO,turno)

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:  # Presionar 'r' para rotar el tablero
                    if turno == 'x':
                        jugadorX.rotar_tablero(tablero)
                        turno = 'o'
                    else:
                        jugadorO.rotar_tablero(tablero)
                        turno = 'x'
                    dibujar_escenario(tablero,jugadorX,jugadorO,turno)
            
            resultado=tablero.comprobar_resultado()
            if resultado != "Continua":  # Revisar si el jugador actual ha ganado después de girar
                juego_en_curso = False
                juego_terminado(resultado)

    return "MENU"

def jugar_humano_maquina():
    pygame.init()
    pantalla = pygame.display.set_mode((COLUMNAS * TAMANO + MARGEN_DER, FILAS * TAMANO + MARGEN_SUP))
    pygame.display.set_caption("Gravity-HvsH")
    tablero=Tablero(FILAS,COLUMNAS)
    jugadorX=Jugador(1)
    jugadorO=JugadorIA(2)
    turno='x'
    dibujar_escenario(tablero,jugadorX,jugadorO,turno)
    juego_en_curso = True
    
    while juego_en_curso:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if turno =='x':
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    posx = evento.pos[0]
                    if posx<TAMANO*COLUMNAS:
                        columna = int(math.floor(posx / TAMANO))
                    else:
                        break
                    if evento.button == 1:  # Click izquierdo para colocar ficha
                        if tablero.es_ubicacion_valida(columna):
                            jugadorX.colocar_ficha(tablero,columna)
                            turno = 'o'
                            dibujar_escenario(tablero,jugadorX,jugadorO,turno)
                            resultado=tablero.comprobar_resultado()
                            if resultado != "Continua":  # Revisar si el jugador actual ha ganado después de girar
                                juego_en_curso = False
                                juego_terminado(resultado)

                    elif evento.button == 3:  # Click derecho para borrar columna
                        if jugadorX.borrarPosible():
                            jugadorX.borrar_columna(tablero,columna)
                            turno = 'o'
                            dibujar_escenario(tablero,jugadorX,jugadorO,turno)

                    if evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_r:  # Presionar 'r' para rotar el tablero
                            jugadorX.rotar_tablero(tablero)
                            turno = 'o'
                            dibujar_escenario(tablero,jugadorX,jugadorO,turno)
                            resultado=tablero.comprobar_resultado()
                            if resultado != "Continua":  # Revisar si el jugador actual ha ganado después de girar
                                juego_en_curso = False
                                juego_terminado(resultado)
            else:
                jugadorO.decidirPrincipiante(tablero, turno, jugadorX)
                turno = 'x'
                dibujar_escenario(tablero,jugadorX,jugadorO,turno)
                resultado=tablero.comprobar_resultado()
                if resultado != "Continua":  # Revisar si el jugador actual ha ganado después de girar
                    juego_en_curso = False
                    juego_terminado(resultado)
    return "MENU"

def jugar_humano_normal():
    pygame.init()
    pantalla = pygame.display.set_mode((COLUMNAS * TAMANO + MARGEN_DER, FILAS * TAMANO + MARGEN_SUP))
    pygame.display.set_caption("Gravity-HvsH")
    tablero=Tablero(FILAS,COLUMNAS)
    jugadorX=Jugador(1)
    jugadorO=JugadorIA(2)
    turno='x'
    dibujar_escenario(tablero,jugadorX,jugadorO,turno)
    juego_en_curso = True
    
    while juego_en_curso:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if turno =='x':
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    posx = evento.pos[0]
                    if posx<TAMANO*COLUMNAS:
                        columna = int(math.floor(posx / TAMANO))
                    else:
                        break
                    if evento.button == 1:  # Click izquierdo para colocar ficha
                        if tablero.es_ubicacion_valida(columna):
                            jugadorX.colocar_ficha(tablero,columna)
                            turno = 'o'
                            dibujar_escenario(tablero,jugadorX,jugadorO,turno)
                            resultado=tablero.comprobar_resultado()
                            if resultado != "Continua":  # Revisar si el jugador actual ha ganado después de girar
                                juego_en_curso = False
                                juego_terminado(resultado)

                    elif evento.button == 3:  # Click derecho para borrar columna
                        if jugadorX.borrarPosible():
                            jugadorX.borrar_columna(tablero,columna)
                            turno = 'o'
                            dibujar_escenario(tablero,jugadorX,jugadorO,turno)

                    if evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_r:  # Presionar 'r' para rotar el tablero
                            jugadorX.rotar_tablero(tablero)
                            turno = 'o'
                            dibujar_escenario(tablero,jugadorX,jugadorO,turno)
                            resultado=tablero.comprobar_resultado()
                            if resultado != "Continua":  # Revisar si el jugador actual ha ganado después de girar
                                juego_en_curso = False
                                juego_terminado(resultado)
            else:
                jugadorO.decidirNormal(tablero, turno, jugadorX)
                turno = 'x'
                dibujar_escenario(tablero,jugadorX,jugadorO,turno)
                resultado=tablero.comprobar_resultado()
                if resultado != "Continua":  # Revisar si el jugador actual ha ganado después de girar
                    juego_en_curso = False
                    juego_terminado(resultado)
    return "MENU"

def jugar_humano_maquina3():
    pygame.init()
    pantalla = pygame.display.set_mode((COLUMNAS * TAMANO + MARGEN_DER, FILAS * TAMANO + MARGEN_SUP))
    pygame.display.set_caption("Gravity-HvsH")
    tablero=Tablero(FILAS,COLUMNAS)
    jugadorX=Jugador(1)
    jugadorO=JugadorIA(2)
    turno='x'
    dibujar_escenario(tablero,jugadorX,jugadorO,turno)
    juego_en_curso = True
    
    while juego_en_curso:
        for evento in pygame.event.get():            
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if turno =='x':
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    posx = evento.pos[0]
                    if posx<TAMANO*COLUMNAS:
                        columna = int(math.floor(posx / TAMANO))
                    else:
                        break
                    if evento.button == 1:  # Click izquierdo para colocar ficha
                        if tablero.es_ubicacion_valida(columna):
                            jugadorX.colocar_ficha(tablero,columna)
                            turno = 'o'

                    elif evento.button == 3:  # Click derecho para borrar columna
                        if jugadorX.borrarPosible():
                            jugadorX.borrar_columna(tablero,columna)
                            turno = 'o'
                    dibujar_escenario(tablero,jugadorX,jugadorO,turno)

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_r:  # Presionar 'r' para rotar el tablero
                        jugadorX.rotar_tablero(tablero)
                        turno = 'o'
                        dibujar_escenario(tablero,jugadorX,jugadorO,turno)
                        
            else:
                jugadorO.decidirAvanzado(tablero, turno, jugadorX)
                turno = 'x'
                dibujar_escenario(tablero,jugadorX,jugadorO,turno)
            
            resultado=tablero.comprobar_resultado()
            if resultado != "Continua":  # Revisar si el jugador actual ha ganado después de girar
                juego_en_curso = False
                juego_terminado(resultado)
    return "MENU"