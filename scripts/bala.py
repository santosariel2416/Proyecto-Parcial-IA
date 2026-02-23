#Jesus ariel Santos 24EISN-2-034
import pygame

#Aquí creo la clase Bala, que representa los disparos que hace el jugador en el juego.
class Bala:

    #Este es el constructor de la clase.Se ejecuta cada vez que se crea una bala nueva.
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

    def mover(self):# Este método se encarga de mover la bala.
        #la bala se mueve hacia arriba 
        self.rect.y -= self.velocidad 

    def dibujar(self, superficie):
        #aqui dibujo las balas en la pantalla 
        pygame.draw.rect(superficie, self.color, self.rect)
