#Jesus Ariel Santos 
#24-EISN-2-034

import pygame
#Aquí creo una clase llamada Jugador. Esta clase representa al personaje principal del juego.
class Jugador:
    def __init__(self, posicion_x, posicion_y):
        # Aquí guardo la posición inicial donde aparece el jugador
        # En lugar de usar solo x e y, ahora usare un rectángulo
        # porque me permitirá detectar colisiones más adelante
        self.ancho = 50 #Defino el tamaño del jugador.Va a medir 50 píxeles de ancho y 50 de alto.
        self.alto = 50
        
        # Creo el rectángulo del jugador con posición y tamaño
        self.rect = pygame.Rect(posicion_x, posicion_y, self.ancho, self.alto) #Uso pygame.Rect porque facilita detectar colisiones más adelante.
        
        # Velocidad con la que se mueve
        self.velocidad = 5
        
        # Color del jugador (rojo un poco más claro que el fondo)
        self.color = (200, 30, 30)

        #Este método sirve para mover al jugador según las teclas que esté presionando.
    def mover(self, teclas_presionadas):

        # Movimiento horizontal
        if teclas_presionadas[pygame.K_LEFT]:#Si se presiona la flecha izquierda, el jugador se mueve hacia la izquierda restando velocidad a su posición en X.
            self.rect.x -= self.velocidad

        if teclas_presionadas[pygame.K_RIGHT]:#Si se presiona la flecha derecha, el jugador se mueve hacia la derecha sumando velocidad en X.
            self.rect.x += self.velocidad

        # Movimiento vertical
        if teclas_presionadas[pygame.K_UP]:#Si se presiona la flecha arriba, el jugador sube restando velocidad en Y.
            self.rect.y -= self.velocidad

        if teclas_presionadas[pygame.K_DOWN]:#Si se presiona la flecha abajo, el jugador baja sumando velocidad en Y.
            self.rect.y += self.velocidad

        # Aquí obtengo la superficie actual de la pantalla para poder saber sus límites (ancho y alto).
        pantalla = pygame.display.get_surface()

        if self.rect.left < 0: #Si el jugador intenta salir por la izquierda, lo detengo en el borde.
            self.rect.left = 0

        if self.rect.right > pantalla.get_width(): #Si intenta salir por la derecha, lo limito al ancho máximo de la pantalla.
            self.rect.right = pantalla.get_width()

        if self.rect.top < 0: #Aqui Evito que el jugador salga por arriba.
            self.rect.top = 0

        if self.rect.bottom > pantalla.get_height(): # Aqui se evita que el jugador salga por abajo.
            self.rect.bottom = pantalla.get_height()

    def dibujar(self, superficie):
        # Dibujo un rectángulo que representa al jugador
        pygame.draw.rect(
            superficie,
            self.color,
            self.rect
        )