#Jesus Ariel Santos 
#24-EISN-2-034

import pygame # Importe la libreria pygame para crear la ventana, dibujar objetos y manejar eventos 

class Puerta:
    def __init__(self, mapa):# constructor de la clase puerta que ahora recibe el mapa para colocarse en la entrada del edificio
        # Tamaño de la puerta es de 40x60 pixeles (ajustado para que encaje con el tamaño del banco)
        self.ancho = 40 # ancho de la puerta 
        self.alto = 60 # alto de la puerta

        # La colocamos en el borde del banco para que sirva de entrada
        # Se ubica en la parte izquierda central del rectángulo del banco
        self.rect = pygame.Rect( #cree un rectangulo para la puerta 
            mapa.rect.left - self.ancho // 2, 
            mapa.rect.centery - self.alto // 2,
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