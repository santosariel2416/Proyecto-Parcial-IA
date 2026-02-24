#Jesus Ariel Santos 
#24-EISN-2-034

import pygame
import random

class Dinero:
    def __init__(self, ancho_pantalla, alto_pantalla):
        # Tamaño del dinero
        self.ancho = 30
        self.alto = 30

        # Posición aleatoria dentro de la pantalla
        self.rect = pygame.Rect(
            random.randint(0, ancho_pantalla - self.ancho),
            random.randint(0, alto_pantalla - self.alto),
            self.ancho,
            self.alto
        )

        # Color verde para representar dinero
        self.color = (0, 200, 0)

    def dibujar(self, superficie):
        pygame.draw.rect(
            superficie,
            self.color,
            self.rect
        )

    def reaparecer(self, ancho_pantalla, alto_pantalla):
        self.rect.x = random.randint(0, ancho_pantalla - self.ancho)
        self.rect.y = random.randint(0, alto_pantalla - self.alto)