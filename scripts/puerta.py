#Jesus Ariel Santos 
#24-EISN-2-034

import pygame # Importe la libreria pygame para crear la ventana, dibujar objetos y manejar eventos 
import os # Importe el modulo OS para asegurar que el programa encuentre la imagen de la puerta

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

        # la CARGA DE LA IMAGEN puerta.png 
        # Buscamos la ruta de la carpeta assets/images/
        ruta_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ruta_imagen = os.path.join(ruta_base, "assets", "images", "puerta.png")
        
        self.imagen_puerta = None
        try:
            # Cargamos la imagen con soporte para transparencia
            img_cargada = pygame.image.load(ruta_imagen).convert_alpha()
            # La escalamos al tamaño exacto que definiste (40x60)
            self.imagen_puerta = pygame.transform.scale(img_cargada, (self.ancho, self.alto))
        except:
            # Si no se encuentra la imagen, el juego usara el rectangulo azul como respaldo
            print("Aviso: No se pudo cargar puerta.png, usando rectangulo de respaldo")

    def dibujar(self, superficie):#metodo para dibujar la puerta en la pantalla
        # Si la imagen existe, la dibujamos en la superficie
        if self.imagen_puerta:
            superficie.blit(self.imagen_puerta, self.rect)
        else:
            # Si no hay imagen, dibujamos el rectangulo azul original
            pygame.draw.rect( 
                superficie,
                self.color,
                self.rect
            )