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
        #Este es el sistema de vidas del jugador 
        self.vidas = 3 

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

        # Limites de pantalla
        pantalla = pygame.display.get_surface()

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > pantalla.get_width():
            self.rect.right = pantalla.get_width()

        if self.rect.top < 0:
            self.rect.top = 0

        if self.rect.bottom > pantalla.get_height():
            self.rect.bottom = pantalla.get_height()

    def dibujar(self, superficie):
        # Dibujo un rectángulo que representa al jugador
        pygame.draw.rect(
            superficie,
            self.color,
            self.rect
        )

    def recibir_danio(self): 
        #Esto reduce una vida cuando el jugador es golpeado
        self.vidas -= 1 

        def esta_vivo(self): 
            #Esto devuelve true si el jugador tiene vidas restantes, de lo contrario devuelve false
            return self.vidas > 0  
        