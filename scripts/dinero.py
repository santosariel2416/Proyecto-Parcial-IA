#Jesus Ariel Santos 
#24-EISN-2-034

import pygame # importe la libreria pygame para crear la ventana, dibujar objetos y manejar eventos
import random # importe la libreria random para generar posiciones aleatorias para el dinero

class Dinero:# cree la clase dinero que representa el dinero que el jugador debe recoger para ganar el juego 
    def __init__(self, mapa):# Este es el constructor de la clase dinero se jecuta cuando se crea un objeto de tipo dinero, recibe el mapa para posiciones aleatorias dentro del banco
        # Tamaño del dinero
        self.ancho = 30
        self.alto = 30

        # Posición aleatoria dentro de la pantalla
        # He corregido esto para que se inicialice correctamente dentro del rango
        # Ahora usa el rect del mapa para aparecer dentro del banco
        self.rect = pygame.Rect(
            random.randint(mapa.rect.left + 20, mapa.rect.right - self.ancho - 20),
            random.randint(mapa.rect.top + 20, mapa.rect.bottom - self.alto - 20),
            self.ancho,
            self.alto
        )

        # Color verde para representar dinero
        self.color = (0, 200, 0)

    def dibujar(self, superficie):# Este es el metodo para dibujar el dinero en la pantalla, recibe la superficie donde se va a dibujar
        pygame.draw.rect(
            superficie,
            self.color,
            self.rect
        )

    def reaparecer(self, mapa):
        # Mantiene la lógica de posición aleatoria pero corregida
        # Se ajusta para que el dinero siempre aparezca dentro del edificio del banco
        self.rect.x = random.randint(mapa.rect.left + 20, mapa.rect.right - self.ancho - 20)
        self.rect.y = random.randint(mapa.rect.top + 20, mapa.rect.bottom - self.alto - 20)