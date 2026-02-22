#Jesus Ariel Santos 
#24-EISN-2-034

import pygame
#importe random que se usa para generar numeros aleatorios, lo utilice porque quiero que el vigilante reaparezca en distintas posiciones
import random

#cree la clase vigilante esta va a representar al enemigo del juego 
class Vigilante:
    #Este es el constructor se ejecuta cuando se crea un vigilante
    def __init__(self, x, y):
        # Tamaño del vigilante
        self.ancho = 50
        self.alto = 50

        # Este es un Rectángulo para el enemigo
        self.rect = pygame.Rect(x, y, self.ancho, self.alto)

        # Color azul para diferenciarlo del jugador
        self.color = (0, 0, 200)

        # Velocidad básica
        self.velocidad = 2

        #Este metodo controla el movimiento automatico del vigilante, este se movera solo

    def mover(self, jugador):
        # Movimiento simple hacia abajo (temporal)
        self.rect.y += self.velocidad

        # Movimiento horizontal persiguiendo al jugador
        if jugador.rect.centerx < self.rect.centerx:
            self.rect.x -= self.velocidad

        if jugador.rect.centerx > self.rect.centerx:
            self.rect.x += self.velocidad

        # Si el vigilante sale de pantalla, reaparece arriba
        if self.rect.top > pygame.display.get_surface().get_height():
            self.rect.y = -50
            # Aqui se genera una nueva aleatoria
            self.rect.x = random.randint(
                0,
                pygame.display.get_surface().get_width() - self.ancho
            )

    #Este metodo es el que dibuja al vigilante en pantalla
    def dibujar(self, superficie):
        pygame.draw.rect(superficie, self.color, self.rect)