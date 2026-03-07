# Jesus Ariel Santos 
# 24-EISN-2-034

import pygame 
import random
import math 
import os 
from scripts.mapa import EstadoMapa
from scripts.a_estrella import Astar  
from scripts.arbol_comportamiento import Selector, Secuencia, Accion


class Vigilante:
    def __init__(self, x, y):

        self.ancho = 50
        self.alto = 50

        self.rect = pygame.Rect(0, 0, 40, 40)
        self.rect.center = (x, y)
        
        self.color = (0, 0, 200)

        # MÁS RÁPIDO
        self.velocidad = 3  

        self.direccion = "abajo" 

        # CARGA DE la IMAGEN
        ruta_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ruta_imagen = os.path.join(ruta_base, "assets", "images", "vigilante.png")
        self.imagenes = {}

        try:
            hoja = pygame.image.load(ruta_imagen).convert_alpha()
            f = 256
            self.imagenes["abajo"] = pygame.transform.smoothscale(hoja.subsurface((0, 0, f, f)), (50, 50))
            self.imagenes["izquierda"] = pygame.transform.smoothscale(hoja.subsurface((0, f, f, f)), (50, 50))
            self.imagenes["derecha"] = pygame.transform.smoothscale(hoja.subsurface((0, f*2, f, f)), (50, 50))
            self.imagenes["arriba"] = pygame.transform.smoothscale(hoja.subsurface((0, f*3, f, f)), (50, 50))
        except:
            self.imagenes = None

        # ARBOL DE COMPORTAMIENTO
        self.objetivo = None
        self.mapa_actual = None
        self.comportamiento = Selector()
        
        self.secuenciaAtaque = Secuencia()
        self.secuenciaAtaque.agregar_hijo(Accion(self.objetivo_detectado))
        self.secuenciaAtaque.agregar_hijo(Accion(self.atacar))

        self.comportamiento.agregar_hijo(self.secuenciaAtaque)
        self.comportamiento.agregar_hijo(Accion(self.Reposo))

        # OPTIMIZACIÓN de A*
        self.camino_actual = []
        self.ultima_meta = None


    def objetivo_detectado(self):
        return self.objetivo is not None


    def atacar(self):

        if not self.objetivo or not self.mapa_actual:
            return False

        vx = (self.rect.centerx - self.mapa_actual.rect.x) // self.mapa_actual.tile_size
        vy = (self.rect.centery - self.mapa_actual.rect.y) // self.mapa_actual.tile_size

        jx = (self.objetivo.rect.centerx - self.mapa_actual.rect.x) // self.mapa_actual.tile_size
        jy = (self.objetivo.rect.centery - self.mapa_actual.rect.y) // self.mapa_actual.tile_size

        vx = max(0, min(int(vx), len(self.mapa_actual.grid[0]) - 1))
        vy = max(0, min(int(vy), len(self.mapa_actual.grid) - 1))
        jx = max(0, min(int(jx), len(self.mapa_actual.grid[0]) - 1))
        jy = max(0, min(int(jy), len(self.mapa_actual.grid) - 1))

        inicio = EstadoMapa(vx, vy, self.mapa_actual.grid)
        meta = EstadoMapa(jx, jy, self.mapa_actual.grid)

        #Recalcular camino si cambia meta O si ya no hay camino
        if self.ultima_meta != (jx, jy) or not self.camino_actual:
            self.camino_actual, _, _ = Astar(inicio, meta)
            self.ultima_meta = (jx, jy)

        camino = self.camino_actual

        if camino and len(camino) > 1:

            proximo = camino[1]

            dest_x = self.mapa_actual.rect.x + (proximo.x * self.mapa_actual.tile_size) + (self.mapa_actual.tile_size // 2)
            dest_y = self.mapa_actual.rect.y + (proximo.y * self.mapa_actual.tile_size) + (self.mapa_actual.tile_size // 2)

            dx = dest_x - self.rect.centerx
            dy = dest_y - self.rect.centery

            distancia = math.hypot(dx, dy)

            #si estamos muy cerca del sigiente punto del camino, pasamos al siguiente para evitar que se trabe en la pared 
            if distancia < 5:
                self.camino_actual.pop(0)
                return True

            # Dirección visual
            if abs(dx) > abs(dy):
                self.direccion = "derecha" if dx > 0 else "izquierda"
            else:
                self.direccion = "abajo" if dy > 0 else "arriba"

            # Movimiento normalizado, evita que se trabe enfrente de las paredes 
            if distancia != 0:
                self.rect.centerx += (dx / distancia) * self.velocidad
                self.rect.centery += (dy / distancia) * self.velocidad

            return True

        else:
            #Movimiento directo mejorado cuando está MUY CERCA
            dx = self.objetivo.rect.centerx - self.rect.centerx
            dy = self.objetivo.rect.centery - self.rect.centery

            distancia = math.hypot(dx, dy)

            if distancia > 3:
                self.rect.centerx += (dx / distancia) * self.velocidad
                self.rect.centery += (dy / distancia) * self.velocidad

            return True


    def Reposo(self):

        self.rect.y += 1
        self.direccion = "abajo"

        if self.rect.top > 800:
            self.rect.bottom = 0

        return True


    def mover(self, jugador, mapa):

        self.mapa_actual = mapa

        dist = math.hypot(
            jugador.rect.centerx - self.rect.centerx,
            jugador.rect.centery - self.rect.centery
        )

        #DETECCIÓN MÁS LEJOS, antes 600 
        if dist < 800:
            self.objetivo = jugador
        else:
            self.objetivo = None
            self.camino_actual = []
            self.ultima_meta = None

        self.comportamiento.ejecutar()


    def dibujar(self, superficie):

        if self.imagenes and self.direccion in self.imagenes:
            img_rect = self.imagenes[self.direccion].get_rect(center=self.rect.center)
            superficie.blit(self.imagenes[self.direccion], img_rect)
        else:
            pygame.draw.rect(superficie, self.color, self.rect)