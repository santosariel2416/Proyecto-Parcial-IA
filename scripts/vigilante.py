#Jesus Ariel Santos 
#24-EISN-2-034

import pygame
#importe random que se usa para generar numeros aleatorios, lo utilice porque quiero que el vigilante reaparezca en distintas posiciones
import random
from scripts.mapa import EstadoMapa
from scripts.a_estrella import Astar  #importe el algoritmo a estrella para que el vigilantes puedan persegir al jugador de manera inteligente y no solo moverse hacia abajo como lo hacia 

#cree la clase vigilante esta va a representar al enemigo del juego 
class Vigilante:
    #Este es el constructor se ejecuta cuando se crea un vigilante
    def __init__(self, x, y):
        # Tamaño del vigilante (ajustado a 30 para que quepa en los pasillos del banco)
        self.ancho = 30
        self.alto = 30

        # Este es un Rectángulo para el enemigo
        self.rect = pygame.Rect(x, y, self.ancho, self.alto)

        # Color azul para diferenciarlo del jugador
        self.color = (0, 0, 200)

        # Velocidad básica
        self.velocidad = 2

        #Este metodo controla el movimiento automatico del vigilante, este se movera solo

    def mover(self, jugador, mapa):
        # Convertimos la posición de píxeles a coordenadas del grid para el A*
        grid_x_vig = (self.rect.x - mapa.rect.x) // mapa.tile_size
        grid_y_vig = (self.rect.y - mapa.rect.y) // mapa.tile_size
        
        grid_x_jug = (jugador.rect.x - mapa.rect.x) // mapa.tile_size
        grid_y_jug = (jugador.rect.y - mapa.rect.y) // mapa.tile_size

        # Creamos los estados para el algoritmo
        inicio = EstadoMapa(grid_x_vig, grid_y_vig, mapa.grid)
        objetivo = EstadoMapa(grid_x_jug, grid_y_jug, mapa.grid)

        # Ejecutamos el algoritmo A* (obtenemos el camino de la tupla que devuelve)
        resultado = Astar(inicio, objetivo)
        camino = resultado[0] if isinstance(resultado, tuple) else resultado

        # Si el A* encontró un camino, nos movemos hacia la siguiente celda
        if camino and len(camino) > 1:
            proximo_paso = camino[1]
            
            # Convertimos la celda del grid de vuelta a píxeles
            destino_x = mapa.rect.x + (proximo_paso.x * mapa.tile_size) + (mapa.tile_size // 2 - self.ancho // 2)
            destino_y = mapa.rect.y + (proximo_paso.y * mapa.tile_size) + (mapa.tile_size // 2 - self.alto // 2)

            # Movimiento inteligente persiguiendo al jugador
            if self.rect.x < destino_x:
                self.rect.x += self.velocidad
            elif self.rect.x > destino_x:
                self.rect.x -= self.velocidad

            if self.rect.y < destino_y:
                self.rect.y += self.velocidad
            elif self.rect.y > destino_y:
                self.rect.y -= self.velocidad
        else:
            # Movimiento simple hacia abajo (temporal) si no hay camino A*
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
