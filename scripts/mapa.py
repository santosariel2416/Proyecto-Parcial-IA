# Jesus Ariel Santos 
# 24-EISN-2-034
import pygame # Importe la libreria pygame para crear la ventana, dibujar objetos y manejar eventos 

class MapaBanco:# cree la clase mapa banco que representa el mapa del banco donde se desarrolla el juego 
    def __init__(self, ancho, alto):# Constructor de la clase mapa banco que se ejecuta cuando se crea un objeto de tipo mapa banco, recibe el ancho y alto de la pantalla para centrar el mapa del banco en la pantalla
        self.ancho = ancho
        self.alto = alto

        # Aumentamos el tamaño de cada cuadro para que se vea mejor
        self.tile_size = 50 

        # 0 = Pasillo, 1 = Pared
        # He ampliado tu grid para que sea un laberinto de banco más grande
        # NOTA: He cambiado el primer '1' de la fila 5 por un '0' para permitir la entrada/salida
        self.grid = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,1,0,1,0,1,1,1,1,1,1,1,0,1],
            [1,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1],
            [1,0,1,0,1,1,1,1,1,1,1,1,0,1,0,1],
            [0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1], # <--- ENTRADA: Cambiado 1 por 0 al inicio
            [1,1,1,0,1,0,1,1,1,1,0,1,0,1,1,1],
            [1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,1],
            [1,0,1,1,1,1,1,0,0,1,1,1,1,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ]

        ancho_mapa = len(self.grid[0]) * self.tile_size
        alto_mapa = len(self.grid) * self.tile_size

        # Centre el banco en la pantalla usando el rect del mapa 
        self.rect = pygame.Rect(
            (self.ancho - ancho_mapa) // 2,
            (self.alto - alto_mapa) // 2,
            ancho_mapa,
            alto_mapa
        )

    def es_pared(self, grid_x, grid_y):# Este metodo verifica si una celda del grid es una pared
        # Seguridad para no revisar fuera de la lista
        if 0 <= grid_y < len(self.grid) and 0 <= grid_x < len(self.grid[0]):
            return self.grid[grid_y][grid_x] == 1
        return True

    def colisiona_pared(self, rect): 
        #Verifica si un rectángulo colisiona con alguna pared del mapa 
        for y, fila in enumerate(self.grid):
            for x, celda in enumerate(fila):
                if celda == 1:  # si es pared
                    rect_pared = pygame.Rect(
                        self.rect.x + x * self.tile_size, 
                        self.rect.y + y * self.tile_size,
                        self.tile_size,
                        self.tile_size
                    )
                    if rect.colliderect(rect_pared):
                        return True
        return False

    def dibujar(self, pantalla): #Este metodo se encarga de dibujar el mapa del banco en la pantalla, recibe la pantalla donde se va a dibujar el mapa
        for y, fila in enumerate(self.grid):
            for x, celda in enumerate(fila):
                rect = pygame.Rect(
                    self.rect.x + x * self.tile_size,
                    self.rect.y + y * self.tile_size,
                    self.tile_size,
                    self.tile_size
                )
                if celda == 1:
                    pygame.draw.rect(pantalla, (100, 100, 100), rect) # Pared gris
                    pygame.draw.rect(pantalla, (150, 150, 150), rect, 2) # Borde pared
                else:
                    pygame.draw.rect(pantalla, (40, 40, 40), rect) # Suelo oscuro

# Estas clases sirven para la Inteligencia Artificial (A*)
class EstadoMapa:
    def __init__(self, x, y, mapa_grid):
        self.x = x
        self.y = y
        self.mapa_grid = mapa_grid

    def __eq__(self, otro):
        return self.x == otro.x and self.y == otro.y

    def __hash__(self):
        return hash((self.x, self.y))

    def Costo(self, objetivo):
        # Distancia Manhattan para la IA
        return abs(self.x - objetivo.x) + abs(self.y - objetivo.y)

    def GenerarSucesores(self):
        sucesores = []
        movimientos = [(0,1), (0,-1), (1,0), (-1,0)]

        for dx, dy in movimientos:
            nx = self.x + dx
            ny = self.y + dy

            # Verificamos límites y que no sea pared (0 es camino libre)
            if 0 <= ny < len(self.mapa_grid) and 0 <= nx < len(self.mapa_grid[0]):
                if self.mapa_grid[ny][nx] == 0:
                    sucesores.append(
                        EstadoMapa(nx, ny, self.mapa_grid)
                    )
        return sucesores