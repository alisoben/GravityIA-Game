import pygame
import sys
from config import *
from tablero import *
from jugador import *

pygame.init()
ancho = (COLUMNAS * TAMANO) + MARGEN_DER
alto = FILAS * TAMANO + MARGEN_SUP
pantalla = pygame.display.set_mode((ancho, alto))

try:
    fondo_imagen = pygame.image.load('fondo.jpeg').convert() 
    fondo_rect = fondo_imagen.get_rect()
    fondo_ratio = fondo_rect.width / fondo_rect.height
    if ancho / alto > fondo_ratio:
        nuevo_ancho = ancho
        nuevo_alto = int(ancho / fondo_ratio)
    else:
        nuevo_ancho = int(alto * fondo_ratio)
        nuevo_alto = alto
    fondo_imagen = pygame.transform.scale(fondo_imagen, (nuevo_ancho, nuevo_alto))
except FileNotFoundError:
    print("Error al cargar la imagen de fondo")
    sys.exit()
     
pygame.display.set_caption("Gravity Game")
fuente = pygame.font.SysFont("monospace", 70)
fuente2 = pygame.font.SysFont("monospace", 25, bold=True)

def dibujar_escenario(tablero, jugadorX,jugadorO,turno):
    posicion=tablero.getPosiciones()
    cx=jugadorX.getC()
    cex=jugadorX.getCE()
    co=jugadorO.getC()
    ceo=jugadorO.getCE()
    pantalla.fill((0, 0, 0))
    for c in range(COLUMNAS):
        for r in range(FILAS):
            pygame.draw.rect(pantalla, GUINDA, (c * TAMANO, r * TAMANO + MARGEN_SUP, TAMANO, TAMANO))
            pygame.draw.circle(pantalla, NEGRO, (int(c * TAMANO + TAMANO / 2), int(r * TAMANO + MARGEN_SUP + TAMANO / 2)), RADIO)
    for c in range(COLUMNAS):
        for r in range(FILAS):
            if posicion[r][c] == 1:
                pygame.draw.circle(pantalla, AZUL, (int(c * TAMANO + TAMANO / 2), alto - int(r * TAMANO + TAMANO / 2)), RADIO)
            elif posicion[r][c] == 2:
                pygame.draw.circle(pantalla, AMARILLO, (int(c * TAMANO + TAMANO / 2), alto - int(r * TAMANO + TAMANO / 2)), RADIO)
    pygame.display.update()

    label1 = fuente2.render("Turno", True, BLANCO)
    pantalla.blit(label1, (COLUMNAS * TAMANO, 10))
    pygame.draw.circle(pantalla, AZUL if turno == 'x' else AMARILLO, ((COLUMNAS * TAMANO) + 120, 25), 20)

    if cex < 4:
        label2 = fuente2.render(" Borrados usados: " + str(cex), True, AZUL)
    else:
        label2 = fuente2.render(" Borrados agotados", True, AZUL)
    label3 = fuente2.render(" Turnos para borrar: " + str(cx), True, AZUL)
    pantalla.blit(label2, (COLUMNAS * TAMANO, 100))
    pantalla.blit(label3, (COLUMNAS * TAMANO, 200))

    if ceo < 4:
        label4 = fuente2.render(" Borrados usados: " + str(ceo), True, AMARILLO)
    else:
        label4 = fuente2.render(" Borrados agotados", True, AMARILLO)
    label5 = fuente2.render(" Turnos para borrar: " + str(co), True, AMARILLO)
    pantalla.blit(label4, (COLUMNAS * TAMANO, 500))
    pantalla.blit(label5, (COLUMNAS * TAMANO, 600))

    pygame.display.update()

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
    
    end_time = pygame.time.get_ticks() + 4000
    while pygame.time.get_ticks() < end_time:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


def dibujar_inicio(pantalla):
    fuente = pygame.font.Font(None, 36)
    ancho_ventana, alto_ventana = pantalla.get_size()
    
    boton_hvh = pygame.Rect((ancho_ventana - 250) // 2, 150, 280, 60)
    boton_hvia = pygame.Rect((ancho_ventana - 250) // 2, 250, 280, 60)
    boton_salir = pygame.Rect((ancho_ventana - 250) // 2, 350, 280, 60)
    
    subboton_principiante = pygame.Rect((ancho_ventana - 200) // 2, 150, 200, 50)
    subboton_normal = pygame.Rect((ancho_ventana - 200) // 2, 250, 200, 50)
    subboton_experto = pygame.Rect((ancho_ventana - 200) // 2, 350, 200, 50)
    boton_regresar = pygame.Rect((ancho_ventana - 200) // 2, 450, 200, 50)
    
    corriendo = True

    while corriendo:
        pantalla.blit(fondo_imagen, (0, 0))  # Dibuja la imagen de fondo
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_hvh.collidepoint(evento.pos):
                    return "HUMANO_HUMANO"
                elif boton_hvia.collidepoint(evento.pos):
                    while True:
                        pantalla.blit(fondo_imagen, (0, 0)) 
                        dibujar_boton(pantalla, subboton_principiante, "Principiante", fuente)
                        dibujar_boton(pantalla, subboton_normal, "Normal", fuente)
                        dibujar_boton(pantalla, subboton_experto, "Experto", fuente)
                        dibujar_boton(pantalla, boton_regresar, "Regresar", fuente)
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
                    
        dibujar_boton(pantalla, boton_hvh, "Humano vs Humano", fuente)
        dibujar_boton(pantalla, boton_hvia, "Humano vs IA", fuente)
        dibujar_boton(pantalla, boton_salir, "Salir", fuente)
        pygame.display.flip()

    return None

def dibujar_boton(pantalla, rect, texto, fuente, color_boton=(130, 0, 80), color_texto=(255, 255, 255)):
    pygame.draw.rect(pantalla, color_boton, rect, border_radius=10)
    texto_renderizado = fuente.render(texto, True, color_texto)
    pantalla.blit(texto_renderizado, texto_renderizado.get_rect(center=rect.center))
