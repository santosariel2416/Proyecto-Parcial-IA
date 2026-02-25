#Jesus Ariel Santos
#24-EISN-2-034 
import pygame

class MapaBanco:

    def __init__(self, ancho_pantalla, alto_pantalla):# Esta es el constructor de la clase mapabanco que recibe el ancho y alto de la pantalla para centrar el banco en la pantalla y crear las paredes del banco

        # Dimensiones del edificio (más pequeño que la pantalla)
        self.ancho = 800
        self.alto = 500

        # Centrar el banco en pantalla
        self.rect = pygame.Rect(
            (ancho_pantalla // 2) - (self.ancho // 2),
            (alto_pantalla // 2) - (self.alto // 2),
            self.ancho,
            self.alto
        ) #cree un rectangulo para el banco que se centra en la pantalla usando el ancho y alto del banco y el ancho y alto de la pantalla

        # Puerta (parte inferior centrada)
        self.puerta = pygame.Rect(
            self.rect.centerx - 40,
            self.rect.bottom - 10,
            80,
            10
        )#cree un rectangulo para la puerta que se coloca en la parte inferior del banco y centrada usando el centro del rectangulo del banco y el ancho de la puerta

        # Lista de paredes internas (pasillos)
        self.paredes = [] #aqui cree una lista vacia para almacenar las paredes del banco y luego se llenara con la funcion crear_paredes que se llama al final del constructor para crear las paredes del banco y los pasillos internos tipo laberintos

        self.crear_paredes()

    def crear_paredes(self):

        # Muros exteriores del banco
        self.paredes.append(pygame.Rect(self.rect.left, self.rect.top, self.rect.width, 10))  # arriba
        self.paredes.append(pygame.Rect(self.rect.left, self.rect.top, 10, self.rect.height))  # izquierda
        self.paredes.append(pygame.Rect(self.rect.right - 10, self.rect.top, 10, self.rect.height))  # derecha

        # Parte inferior (dejamos espacio para la puerta)
        self.paredes.append(pygame.Rect(self.rect.left, self.rect.bottom - 10, self.rect.width, 10))

        # Pasillos internos tipo laberinto
        self.paredes.append(pygame.Rect(self.rect.left + 150, self.rect.top + 100, 500, 10))
        self.paredes.append(pygame.Rect(self.rect.left + 150, self.rect.top + 200, 10, 200))
        self.paredes.append(pygame.Rect(self.rect.left + 300, self.rect.top + 150, 10, 250))
        self.paredes.append(pygame.Rect(self.rect.left + 450, self.rect.top + 100, 10, 250))

    def dibujar(self, pantalla):

        # Exterior
        pygame.draw.rect(pantalla, (80, 80, 80), self.rect)

        # Dibujar paredes
        for pared in self.paredes:
            pygame.draw.rect(pantalla, (40, 40, 40), pared)

        # Dibujar puerta
        pygame.draw.rect(pantalla, (150, 75, 0), self.puerta)

    def colisiona_pared(self, rect_objeto):# Esta funcion recibe un rectangulo de un objetivo como el jugador o un vigilante y verifica si colisiona con algunas de las paredes del banco usando la funcion colliderect de pygame que verifica si dos rectangulos colisionan 

        for pared in self.paredes:
            if rect_objeto.colliderect(pared):
                return True
        return False