# Jesus Ariel Santos 
# 24-EISN-2-034

import pygame # Importe la libreria pygame para crear la ventana, dibujar objetos y manejar eventos 
import os # Importe el modulo OS para asegurar que el programa encuentre la imagen de la puerta

class Puerta:
    def __init__(self, mapa):# constructor de la clase puerta que ahora recibe el mapa para colocarse en la entrada del edificio
        # Tamaño de la puerta ajustado para que encaje con el nuevo tile_size y el ancho del borde
        self.ancho = 20 # Más delgada para que quede "dentro" de la línea de la pared
        self.alto = 64 # Altura completa de un cuadro del mapa (tile_size)

        # Cálculo para que la puerta quede exactamente en la entrada (Fila 5 del grid)
        # mapa.rect.top nos da el inicio del dibujo del banco
        # (5 * mapa.tile_size) nos lleva a la fila de la entrada donde pusimos el '0'
        fila_entrada = 5
        
        # La colocamos en el borde izquierdo exacto del rectángulo del mapa
        # Se ubica en la parte izquierda pegada a la pared para que se vea bien alineada
        self.rect = pygame.Rect( #cree un rectangulo para la puerta 
            mapa.rect.left, 
            mapa.rect.top + (fila_entrada * mapa.tile_size),
            self.ancho,
            self.alto
        )

        # Color amarillo dorado para resaltar (contraste) sobre el fondo oscuro del banco
        self.color = (255, 215, 0) #color dorado para la puerta 

        # la CARGA DE LA IMAGEN puerta.png 
        # Buscamos la ruta de la carpeta assets/images/
        ruta_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ruta_imagen = os.path.join(ruta_base, "assets", "images", "puerta.png")
        
        self.imagen_puerta = None
        try:
            # Cargamos la imagen con soporte para transparencia
            img_cargada = pygame.image.load(ruta_imagen).convert_alpha()
            # La escalamos al tamaño exacto que definiste para que se vea bien en la entrada
            self.imagen_puerta = pygame.transform.scale(img_cargada, (self.ancho, self.alto))
        except:
            # Si no se encuentra la imagen, el juego usara el rectangulo dorado como respaldo
            print("Aviso: No se pudo cargar puerta.png, usando rectangulo de respaldo")

    def dibujar(self, superficie):#metodo para dibujar la puerta en la pantalla
        # Si la imagen existe, la dibujamos en la superficie
        if self.imagen_puerta:
            superficie.blit(self.imagen_puerta, self.rect)
        else:
            # Si no hay imagen, dibujamos el rectangulo dorado de alto contraste
            pygame.draw.rect( 
                superficie,
                self.color,
                self.rect
            )