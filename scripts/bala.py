#Jesus ariel Santos 24EISN-2-034
import pygame

class Bala:
    def __init__(self, x, y):
        #este es el tamaño de las balas
        self.ancho = 8
        self.alto = 15 

        #aqui creo la forma para las balas 
        self.rect = pygame.Rect(x, y, self.ancho, self.alto)

        #velocidad con la que sale la bala 
        self.velocidad = 7

        #El color es amarillo 
        self.color = (255, 255, 0)

    def mover(self):
        #la bala se mueve hacia arriba 
        self.rect.y -= self.velocidad 

    def dibujar(self, superficie):
        #aqui dibujo las balas en la pantalla 
        pygame.draw.rect(superficie, self.color, self.rect)
