#gravity version X.1
#main.py
import pygame
import sys
from interface import dibujar_inicio
from interaction import *
from ia import *

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Gravity Connect 4")
    
    while True:
        modo_juego = dibujar_inicio(pantalla)
        if modo_juego == "QUIT":
            pygame.quit()
            sys.exit()
        elif modo_juego == "REGRESAR":
            continue
        
        if modo_juego == "HUMANO_HUMANO":
            resultado = jugar_humano_humano()
        elif modo_juego == "HUMANO_IA_PRINCIPIANTE":
            resultado = jugar_humano_ia("principiante")
        elif modo_juego == "HUMANO_IA_NORMAL":
            resultado = jugar_humano_ia("normal")
        elif modo_juego == "HUMANO_IA_EXPERTO":
            resultado = jugar_humano_ia("experto")

        # Se podría implementar un menú final o una pantalla de resultados antes de romper el bucle o reiniciar
        if resultado == "MENU":
            continue
        else:
            break  # Sale del bucle si el resultado no requiere volver al menú

if __name__ == "__main__":
    main()