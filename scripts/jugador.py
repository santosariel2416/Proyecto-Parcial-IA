#Jesus Ariel Santos 
#24-EISN-2-034

import pygame

class Jugador:
    def __init__(self, posicion_x, posicion_y):
        # Aquí guardo la posición inicial donde aparece el jugador
        # En lugar de usar solo x e y, ahora usare un rectángulo
        # porque nos permitirá detectar colisiones más adelante
        self.ancho = 50
        self.alto = 50
        
        # Creo el rectángulo del jugador con posición y tamaño
        self.rect = pygame.Rect(posicion_x, posicion_y, self.ancho, self.alto)
        
        # Velocidad con la que se mueve
        self.velocidad = 5
        
        # Color del jugador (rojo un poco más claro que el fondo)
        self.color = (200, 30, 30)

    def mover(self, teclas_presionadas):
        # Movimiento horizontal
        if teclas_presionadas[pygame.K_LEFT]:
            self.rect.x -= self.velocidad
        if teclas_presionadas[pygame.K_RIGHT]:
            self.rect.x += self.velocidad

        # Movimiento vertical
        if teclas_presionadas[pygame.K_UP]:
            self.rect.y -= self.velocidad
        if teclas_presionadas[pygame.K_DOWN]:
            self.rect.y += self.velocidad

    def dibujar(self, superficie):
        # Dibujo un rectángulo que representa al jugador
        pygame.draw.rect(
            superficie,
            self.color,
            self.rectS
        )
