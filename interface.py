# interface.py

import pygame
import numpy as np
from config import *

pygame.init()
ancho = (COLUMNAS * TAMANO) + MARGEN_DER
alto = FILAS * TAMANO + MARGEN_SUP
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Gravity Game")
fuente = pygame.font.SysFont("monospace", 75)
fuente2 = pygame.font.SysFont("monospace", 30)

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
    
    turno = 1 - turno
    ficha = turno + 1
    label = fuente2.render("Turno", True, BLANCO)
    pantalla.blit(label, (COLUMNAS * TAMANO, 10))
    pygame.draw.circle(pantalla, AZUL if ficha == 1 else AMARILLO, ((COLUMNAS * TAMANO) + 120,25), 20)
    
    pygame.display.update()