import math
import pygame
import numpy as np
import sys

class GravityGame:
    def __init__(self):
        self.colores()
        self.medidas()

        pygame.init()
        self.ancho = (self.COLUMNAS * self.TAMANO) + self.MARGEN_DER
        self.alto = self.FILAS * self.TAMANO + self.MARGEN_SUP
        self.pantalla = pygame.display.set_mode((self.ancho, self.alto))
        pygame.display.set_caption("Gravity Game")
        self.fuente1 = pygame.font.SysFont("monospace", 75)
        self.fuente2 = pygame.font.SysFont("monospace", 30)

        self.cx, self.co = 4, 4  # Contadores de turnos para borrar columnas
        self.cex, self.ceo = 0, 0  # Contadores de usos de borrar columnas

    def colores(self):
        self.GUINDA = (130, 0, 80)
        self.NEGRO = (0, 0, 0)
        self.AZUL = (80, 80, 255)
        self.AMARILLO = (255, 255, 80)
        self.ROJO = (255, 0, 0)
        self.BLANCO = (255, 255, 255)

    def medidas(self):
        self.FILAS = 7
        self.COLUMNAS = 7
        self.TAMANO = 100
        self.RADIO = int(self.TAMANO / 2 - 5)
        self.MARGEN_SUP = 100
        self.MARGEN_DER = 400

    def crear_tablero(self):
        return np.zeros((self.FILAS, self.COLUMNAS))

    def dibujar_escenario(self):
        self.pantalla.fill(self.NEGRO)
        for c in range(self.COLUMNAS):
            for r in range(self.FILAS):
                pygame.draw.rect(self.pantalla, self.GUINDA, (c * self.TAMANO, r * self.TAMANO + self.MARGEN_SUP, self.TAMANO, self.TAMANO))
                pygame.draw.circle(self.pantalla, self.NEGRO, (int(c * self.TAMANO + self.TAMANO / 2), int(r * self.TAMANO + self.MARGEN_SUP + self.TAMANO / 2)), self.RADIO)
        for c in range(self.COLUMNAS):
            for r in range(self.FILAS):
                if self.tablero[r][c] == 1:
                    pygame.draw.circle(self.pantalla, self.AZUL, (int(c * self.TAMANO + self.TAMANO / 2), self.alto - int(r * self.TAMANO + self.TAMANO / 2)), self.RADIO)
                elif self.tablero[r][c] == 2:
                    pygame.draw.circle(self.pantalla, self.AMARILLO, (int(c * self.TAMANO + self.TAMANO / 2), self.alto - int(r * self.TAMANO + self.TAMANO / 2)), self.RADIO)
        pygame.display.update()

        label1 = self.fuente2.render("Turno", True, self.BLANCO)
        self.pantalla.blit(label1, (self.COLUMNAS * self.TAMANO, 10))
        pygame.draw.circle(self.pantalla, self.AZUL if self.turno == 'x' else self.AMARILLO, ((self.COLUMNAS * self.TAMANO) + 120, 25), 20)

        if self.cex < 4:
            label2 = self.fuente2.render("Borrados usados: " + str(self.cex), True, self.AZUL)
        else:
            label2 = self.fuente2.render("Borrados agotados", True, self.AZUL)
        label3 = self.fuente2.render("Turnos para borrar: " + str(self.cx), True, self.AZUL)
        self.pantalla.blit(label2, (self.COLUMNAS * self.TAMANO, 100))
        self.pantalla.blit(label3, (self.COLUMNAS * self.TAMANO, 200))
    
        if self.ceo < 4:
            label4 = self.fuente2.render("Borrados usados: " + str(self.ceo), True, self.AMARILLO)
        else:
            label4 = self.fuente2.render("Borrados agotados", True, self.AMARILLO)
        label5 = self.fuente2.render("Turnos para borrar: " + str(self.co), True, self.AMARILLO)
        self.pantalla.blit(label4, (self.COLUMNAS * self.TAMANO, 500))
        self.pantalla.blit(label5, (self.COLUMNAS * self.TAMANO, 600))

        pygame.display.update()

    def aplicar_gravedad(self):
        for col in range(self.COLUMNAS):
            columna_invertida = self.tablero[:, col][::-1]
            nuevas_fichas = columna_invertida[columna_invertida != 0]
            self.tablero[:, col] = np.concatenate([np.zeros(self.FILAS - len(nuevas_fichas)), nuevas_fichas])[::-1]

    def es_ubicacion_valida(self, col):
        return self.tablero[self.FILAS - 1][col] == 0

    def obtener_siguiente_fila_libre(self, col):
        for r in range(self.FILAS):
            if self.tablero[r][col] == 0:
                return r

    def rotar_tableroX(self):
        self.cx = max(0, self.cx - 1)
        self.turno = 'o'
        self.tablero = np.flipud(np.fliplr(self.tablero))
        self.aplicar_gravedad()

    def rotar_tableroO(self):
        self.co = max(0, self.co - 1)
        self.turno = 'x'
        self.tablero = np.flipud(np.fliplr(self.tablero))
        self.aplicar_gravedad()

    def colocar_fichaX(self, col):
        fila = self.obtener_siguiente_fila_libre(col)
        self.tablero[fila][col] = 1
        self.cx = max(0, self.cx - 1)
        self.turno = 'o'
        
    def colocar_fichaO(self, col):
        fila = self.obtener_siguiente_fila_libre(col)
        self.tablero[fila][col] = 2
        self.co = max(0, self.co - 1)
        self.turno = 'x'

    def borrar_columnaX(self, columna):
        if 0 <= columna < self.COLUMNAS:
            self.tablero[:, columna] = 0
        self.cex += 1
        self.cx = 4
        self.turno = 'o'

    def borrar_columnaO(self, columna):
        if 0 <= columna < self.COLUMNAS:
            self.tablero[:, columna] = 0
        self.ceo += 1
        self.co = 4
        self.turno = 'x'

    def comprobar_victoria(self, ficha):
        for c in range(self.COLUMNAS - 3):
            for r in range(self.FILAS):
                if all(self.tablero[r][c + i] == ficha for i in range(4)):
                    return True
        for c in range(self.COLUMNAS):
            for r in range(self.FILAS - 3):
                if all(self.tablero[r + i][c] == ficha for i in range(4)):
                    return True
        for c in range(self.COLUMNAS - 3):
            for r in range(self.FILAS - 3):
                if all(self.tablero[r + i][c + i] == ficha for i in range(4)):
                    return True
        for c in range(self.COLUMNAS - 3):
            for r in range(3, self.FILAS):
                if all(self.tablero[r - i][c + i] == ficha for i in range(4)):
                    return True
        return False

    def comprobar_tablero_lleno(self):
        return np.all(self.tablero != 0)

    def comprobar_resultado(self):
        gana_j1 = self.comprobar_victoria(1)
        gana_j2 = self.comprobar_victoria(2)
        lleno = self.comprobar_tablero_lleno()
        if (gana_j1 and gana_j2) or lleno:
            return "Empate"
        elif gana_j1:
            return "Jugador 1 gana!"
        elif gana_j2:
            return "Jugador 2 gana!"
        else:
            return "Continua"

    def juego_terminado(self, mensaje):
        if mensaje == "Jugador 1 gana!":
            color = self.AZUL
        elif mensaje == "Jugador 2 gana!":
            color = self.AMARILLO
        else:
            color = self.BLANCO
        label = self.fuente1.render(mensaje, True, color)
        self.pantalla.blit(label, (40, 10))
        pygame.display.update()
        pygame.time.wait(4000)
        self.mostrar_menu()

    def jugar_humano(self):
        
        self.tablero = self.crear_tablero()
        self.turno = 'x'
        self.dibujar_escenario()
        juego_en_curso = True

        while juego_en_curso:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    sys.exit()

                if evento.type == pygame.MOUSEBUTTONDOWN:
                    posx = evento.pos[0]
                    if posx<self.TAMANO*self.COLUMNAS:
                        columna = int(math.floor(posx / self.TAMANO))
                    else:
                        break

                    if evento.button == 1:  # Click izquierdo para colocar ficha
                        if self.es_ubicacion_valida(columna):
                            if self.turno == 'x':
                                self.colocar_fichaX(columna)
                            else:
                                self.colocar_fichaO(columna)
                            self.dibujar_escenario()
                            resultado = self.comprobar_resultado()
                            if resultado != "Continua":  # Revisar si el jugador actual ha ganado después de girar
                                self.juego_terminado(resultado)

                    elif evento.button == 3:  # Click derecho para borrar columna
                        if self.turno == 'x' and self.cx == 0 and self.cex < 4:
                            self.borrar_columnaX(columna)
                        elif self.turno == 'o' and self.co == 0 and self.ceo < 4:
                            self.borrar_columnaO(columna)
                        self.dibujar_escenario()

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_r:  # Presionar 'r' para rotar el tablero
                        if self.turno == 'x':
                            self.rotar_tableroX()
                        else:
                            self.rotar_tableroO()
                        self.dibujar_escenario()
                        resultado = self.comprobar_resultado()
                        if resultado != "Continua":  # Revisar si el jugador actual ha ganado después de girar
                            self.juego_terminado(resultado)

    def jugar_maquina(self, nivel):
        # Código para jugar contra una máquina con el nivel especificado
        pass



    def mostrar_menu(self):
        menu_en_curso = True
        boton_vs_humano = pygame.Rect(150, 150, 200, 50)
        boton_vs_maquina1 = pygame.Rect(150, 250, 200, 50)
        boton_vs_maquina2 = pygame.Rect(150, 350, 200, 50)
        boton_vs_maquina3 = pygame.Rect(150, 450, 200, 50)
        while menu_en_curso:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    sys.exit()
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if boton_vs_humano.collidepoint(pos):
                        menu_en_curso = False
                        self.jugar_humano()
                    elif boton_vs_maquina1.collidepoint(pos):
                        menu_en_curso = False
                        self.jugar_maquina(1)
                    elif boton_vs_maquina2.collidepoint(pos):
                        menu_en_curso = False
                        self.jugar_maquina(2)
                    elif boton_vs_maquina3.collidepoint(pos):
                        menu_en_curso = False
                        self.jugar_maquina(3)
            self.pantalla.fill(self.NEGRO)
            pygame.draw.rect(self.pantalla, self.AMARILLO, boton_vs_humano)
            texto_jugar = self.fuente2.render("Vs Humano", True, self.NEGRO)
            self.pantalla.blit(texto_jugar, (boton_vs_humano.x + 10, boton_vs_humano.y + 10))

            pygame.draw.rect(self.pantalla, self.AMARILLO, boton_vs_maquina1)
            texto_maquina1 = self.fuente2.render("Vs Máquina 1", True, self.NEGRO)
            self.pantalla.blit(texto_maquina1, (boton_vs_maquina1.x + 10, boton_vs_maquina1.y + 10))

            pygame.draw.rect(self.pantalla, self.AMARILLO, boton_vs_maquina2)
            texto_maquina2 = self.fuente2.render("Vs Máquina 2", True, self.NEGRO)
            self.pantalla.blit(texto_maquina2, (boton_vs_maquina2.x + 10, boton_vs_maquina2.y + 10))

            pygame.draw.rect(self.pantalla, self.AMARILLO, boton_vs_maquina3)
            texto_maquina3 = self.fuente2.render("Vs Máquina 3", True, self.NEGRO)
            self.pantalla.blit(texto_maquina3, (boton_vs_maquina3.x + 10, boton_vs_maquina3.y + 10))

            pygame.display.update()

if __name__ == "__main__":
    juego = GravityGame()
    juego.mostrar_menu()
