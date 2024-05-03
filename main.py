#gravity version X.1
import pygame
import sys
from interface import dibujar_inicio
from interaction import jugar_humano_humano
from ia import jugar_humano_ia

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
        resultado = None
        if modo_juego == "HUMANO_HUMANO":
            resultado = jugar_humano_humano()
        elif modo_juego.startswith("HUMANO_IA_"):  
            nivel = modo_juego.split("_")[-1].lower()
            resultado = jugar_humano_ia(nivel)
        if resultado == "MENU":
            continue
        else:
            break  # Si resultado no es 'MENU' (por error o lógica no contemplada), sale del bucle

if __name__ == "__main__":
    main()