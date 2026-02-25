#Jesus Ariel Santos 
#24-EISN-2-034

import pygame # Importe la libreria pygame para crear la ventana, dibujar objetos y manejar eventos 

class Puerta:
    def __init__(self, ancho_pantalla, alto_pantalla):# constructor de la clase puerta que recibe el ancho y alto de la pantalla para colocar la puerta en la esquina inferior derecha 
        # Tamaño de la puerta es de 80x100 pixeles
        self.ancho = 80 # ancho de la puerta 
        self.alto = 100 # alto de la puerta

        # La colocamos en la esquina inferior derecha
        self.rect = pygame.Rect( #cree un rectangulo para la puerta 
            ancho_pantalla - self.ancho - 20, 
            alto_pantalla - self.alto - 20,
            self.ancho,
            self.alto
        )

        # Color azul para representar la salida
        self.color = (0, 0, 200) #color azul para la puerta 

    def dibujar(self, superficie):#metodo para dibujar la puerta en la pantalla
        pygame.draw.rect( 
            superficie,
            self.color,
            self.rect
        )