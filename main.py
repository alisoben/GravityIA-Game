from interaccion import * 

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Gravity")

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
            resultado = jugar_humano_maquina('principiante')
            pass
        elif modo_juego == "HUMANO_IA_NORMAL":
            resultado = jugar_humano_maquina('intermedio')
            pass
        elif modo_juego == "HUMANO_IA_EXPERTO":
            resultado = jugar_humano_maquina('avanzado')
            pass

    
        if resultado == "MENU":
            continue
        else:
            break  

if __name__ == "__main__":
    main()