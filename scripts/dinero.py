#Jesus Ariel Santos 
#24-EISN-2-034

import pygame # importe la libreria pygame para crear la ventana, dibujar objetos y manejar eventos
import random # importe la libreria random para generar posiciones aleatorias para el dinero
import os # Importe el modulo OS para asegurar que el programa encuentre la imagen del dinero

class Dinero:# cree la clase dinero que representa el dinero que el jugador debe recoger para ganar el juego 
    def __init__(self, mapa):# Este es el constructor de la clase dinero se jecuta cuando se crea un objeto de tipo dinero, recibe el mapa para posiciones aleatorias dentro del banco
        # Tamaño del dinero
        self.ancho = 30
        self.alto = 30

        # CARGA DE LA IMAGEN dinero.png 
        # Buscamos la ruta de la carpeta assets/images/
        ruta_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ruta_imagen = os.path.join(ruta_base, "assets", "images", "dinero.png")
        
        self.imagen_dinero = None
        try:
            # Cargamos la imagen con soporte para transparencia
            img_cargada = pygame.image.load(ruta_imagen).convert_alpha()
            # La escalamos al tamaño exacto que definiste (30x30)
            self.imagen_dinero = pygame.transform.scale(img_cargada, (self.ancho, self.alto))
        except:
            # Si no se encuentra la imagen, el juego usara el rectangulo verde como respaldo
            print("Aviso: No se pudo cargar dinero.png, usando rectangulo de respaldo")

        # Posición aleatoria dentro de la pantalla
        # He corregido esto para que se inicialice correctamente dentro del rango
        # Ahora usa el rect del mapa para aparecer dentro del banco
        
        #Lógica para aparecer SOLO en pasillos (0) 
        pasillos = []
        for fila_idx, fila in enumerate(mapa.grid):
            for col_idx, celda in enumerate(fila):
                if celda == 0: # Solo si es suelo/pasillo
                    pasillos.append((col_idx, fila_idx))
        
        if pasillos:
            col, fila = random.choice(pasillos)
            x = mapa.rect.x + (col * mapa.tile_size) + (mapa.tile_size // 2 - self.ancho // 2)
            y = mapa.rect.y + (fila * mapa.tile_size) + (mapa.tile_size // 2 - self.alto // 2)
            self.rect = pygame.Rect(x, y, self.ancho, self.alto)
        else:
            # Fallback en caso de error de grid
            self.rect = pygame.Rect(mapa.rect.centerx, mapa.rect.centery, self.ancho, self.alto)

        # Color verde para representar dinero
        self.color = (0, 200, 0)

    def dibujar(self, superficie):# Este es el metodo para dibujar el dinero en la pantalla, recibe la superficie donde se va a dibujar
        # Si la imagen existe, la dibujamos en la superficie
        if self.imagen_dinero:
            superficie.blit(self.imagen_dinero, self.rect)
        else:
            # Si no hay imagen, dibujamos el rectangulo verde original
            pygame.draw.rect(
                superficie,
                self.color,
                self.rect
            )

    def reaparecer(self, mapa):
        # Mantiene la lógica de posición aleatoria pero corregida
        # Se ajusta para que el dinero siempre aparezca dentro del edificio del banco
        
        #Buscamos de nuevo una posición de pasillo válida
        pasillos = []
        for fila_idx, fila in enumerate(mapa.grid):
            for col_idx, celda in enumerate(fila):
                if celda == 0:
                    pasillos.append((col_idx, fila_idx))
        
        if pasillos:
            col, fila = random.choice(pasillos)
            self.rect.x = mapa.rect.x + (col * mapa.tile_size) + (mapa.tile_size // 2 - self.ancho // 2)
            self.rect.y = mapa.rect.y + (fila * mapa.tile_size) + (mapa.tile_size // 2 - self.alto // 2)