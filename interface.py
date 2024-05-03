# interface.py

import pygame
import sys
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
    
    
def dibujar_inicio(pantalla):
    fuente = pygame.font.Font(None, 36)
    boton_hvh = pygame.Rect(100, 150, 250, 50)
    boton_hvia = pygame.Rect(100, 250, 250, 50)
    boton_salir = pygame.Rect(100, 350, 250, 50)
    subboton_principiante = pygame.Rect(350, 150, 200, 50)
    subboton_normal = pygame.Rect(350, 250, 200, 50)
    subboton_experto = pygame.Rect(350, 350, 200, 50)
    boton_regresar = pygame.Rect(350, 450, 200, 50)  # Botón para regresar al menú principal
    corriendo = True

    while corriendo:
        pantalla.fill((0, 0, 0))
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_hvh.collidepoint(evento.pos):
                    return "HUMANO_HUMANO"
                elif boton_hvia.collidepoint(evento.pos):
                    while True:
                        pantalla.fill((0, 0, 0))
                        pygame.draw.rect(pantalla, (130, 0, 80), subboton_principiante)
                        pygame.draw.rect(pantalla, (130, 0, 80), subboton_normal)
                        pygame.draw.rect(pantalla, (130, 0, 80), subboton_experto)
                        pygame.draw.rect(pantalla, (130, 0, 80), boton_regresar)
                        texto_principiante = fuente.render("Principiante", True, (255, 255, 255))
                        texto_normal = fuente.render("Normal", True, (255, 255, 255))
                        texto_experto = fuente.render("Experto", True, (255, 255, 255))
                        texto_regresar = fuente.render("Regresar", True, (255, 255, 255))
                        pantalla.blit(texto_principiante, subboton_principiante.topleft)
                        pantalla.blit(texto_normal, subboton_normal.topleft)
                        pantalla.blit(texto_experto, subboton_experto.topleft)
                        pantalla.blit(texto_regresar, boton_regresar.topleft)
                        pygame.display.flip()

                        for sub_evento in pygame.event.get():
                            if sub_evento.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            if sub_evento.type == pygame.MOUSEBUTTONDOWN:
                                if subboton_principiante.collidepoint(sub_evento.pos):
                                    return "HUMANO_IA_PRINCIPIANTE"
                                elif subboton_normal.collidepoint(sub_evento.pos):
                                    return "HUMANO_IA_NORMAL"
                                elif subboton_experto.collidepoint(sub_evento.pos):
                                    return "HUMANO_IA_EXPERTO"
                                elif boton_regresar.collidepoint(sub_evento.pos):
                                    return "REGRESAR" # Sale del bucle interno, regresa al menú principal
                elif boton_salir.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()

        pygame.draw.rect(pantalla, (130, 0, 80), boton_hvh)
        pygame.draw.rect(pantalla, (130, 0, 80), boton_hvia)
        pygame.draw.rect(pantalla, (130, 0, 80), boton_salir)
        texto_hvh = fuente.render("Humano vs Humano", True, (255, 255, 255))
        texto_hvia = fuente.render("Humano vs IA", True, (255, 255, 255))
        texto_salir = fuente.render("Salir", True, (255, 255, 255))
        pantalla.blit(texto_hvh, boton_hvh.topleft)
        pantalla.blit(texto_hvia, boton_hvia.topleft)
        pantalla.blit(texto_salir, boton_salir.topleft)
        pygame.display.flip()

    return None