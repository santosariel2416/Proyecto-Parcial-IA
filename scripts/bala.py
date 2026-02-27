#Jesus ariel Santos 24EISN-2-034
import pygame

class Bala:
    # Agregamos 'direccion' aquí para que acepte los 4 argumentos que le manda el main
    def __init__(self, x, y, direccion):
        #este es el tamaño de las balas
        self.ancho = 8
        self.alto = 15 

        #aqui creo la forma para las balas 
        self.rect = pygame.Rect(x, y, self.ancho, self.alto)

        #velocidad con la que sale la bala 
        self.velocidad = 7

        #El color es amarillo 
        self.color = (255, 255, 0)

        # Guardamos la direccion que viene del jugador para saber hacia donde movernos
        self.dir_x = direccion[0]
        self.dir_y = direccion[1]

        #cree esta variable para saber si la bala sigue activa o si ya choco con una pared
        self.activa = True

    def mover(self, mapa=None):
        # Ahora la bala se mueve segun la direccion guardada multiplicada por la velocidad
        self.rect.x += self.dir_x * self.velocidad
        self.rect.y += self.dir_y * self.velocidad

        #si la bala toca una pared del banco, se desactiva para que desaparezca y no la atraviese
        if mapa and mapa.colisiona_pared(self.rect):
            self.activa = False

    def dibujar(self, superficie):
        #solo dibujo la bala si todavia no ha chocado con nada
        if self.activa:
            #aqui dibujo las balas en la pantalla 
            pygame.draw.rect(superficie, self.color, self.rect)