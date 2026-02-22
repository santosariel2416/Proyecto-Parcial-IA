#Jesus Ariel Santos 
#24-EISN-2-034

import pygame
import random

class Vigilante:
    def __init__(self, x, y):
        # Tamaño del vigilante
        self.ancho = 50
        self.alto = 50

        # Rectángulo del enemigo
        self.rect = pygame.Rect(x, y, self.ancho, self.alto)

        # Color azul para diferenciarlo del jugador
        self.color = (0, 0, 200)

        # Velocidad básica
        self.velocidad = 2

    def mover(self):
        # Movimiento simple hacia abajo (temporal)
        self.rect.y += self.velocidad

        # Si sale de pantalla, reaparece arriba
        if self.rect.top > pygame.display.get_surface().get_height():
            self.rect.y = -50
            self.rect.x = random.randint(
                0,
                pygame.display.get_surface().get_width() - self.ancho
            )

    def dibujar(self, superficie):
        pygame.draw.rect(superficie, self.color, self.rect)