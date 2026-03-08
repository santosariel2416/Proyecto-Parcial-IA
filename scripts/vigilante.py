# Jesus Ariel Santos 
# 24-EISN-2-034

import pygame 
import random
import math # para calcular distancia y direccion entre el vigilante y el jugador 
import os # para manejar rutas de archivos de manera mas segura y compatible entre sistemas operativos 
from scripts.mapa import EstadoMapa
from scripts.a_estrella import Astar  
from scripts.arbol_comportamiento import Selector, Secuencia, Accion

class Vigilante:# clase para el enemigo vigilante que patrulla y persigue al jugador 
    def __init__(self, x, y):
        self.ancho = 50
        self.alto = 50

        # El rectangulo de colision es mas pequeño que la imagen para evitar que se quede atascado en las paredes 
        self.rect = pygame.Rect(0, 0, 28, 28) 
        self.rect.center = (x, y)
        
        self.color = (0, 0, 200)
        self.velocidad = 5 
        self.direccion = "abajo" 

        # CARGA DE IMAGEN (Tu lógica original)
        ruta_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ruta_imagen = os.path.join(ruta_base, "assets", "images", "vigilante.png")
        self.imagenes = {}
        try:
            hoja = pygame.image.load(ruta_imagen).convert_alpha() # carga de la hoja de sprites del vigilante 
            f = 256
            self.imagenes["abajo"] = pygame.transform.smoothscale(hoja.subsurface((0, 0, f, f)), (50, 50)) # se extraen las 4 direcciones del vigilante de la hoja de sprites y se escalan a 50x50 para que coincida con el tamaño del rectangulo de colision 
            self.imagenes["izquierda"] = pygame.transform.smoothscale(hoja.subsurface((0, f, f, f)), (50, 50))
            self.imagenes["derecha"] = pygame.transform.smoothscale(hoja.subsurface((0, f*2, f, f)), (50, 50))
            self.imagenes["arriba"] = pygame.transform.smoothscale(hoja.subsurface((0, f*3, f, f)), (50, 50))
        except:
            self.imagenes = None

        self.objetivo = None
        self.mapa_actual = None
        self.comportamiento = Selector() # el vigilante primero intentara atacar al jugador si lo detecta, sino se movera aleatoriamente por el mapa patrullando 
        
        self.secuenciaAtaque = Secuencia() # si el jugador esta dentro del rango de detenccion del vigilante, se ejecutara esta secuencia que primero verifica que el objetivo esta detectado y luego intenta atacarlo moviendose hacia el jugador utilizando el algoritmo A* para encontrar el camino mas corto evitando paredes y obstaculos
        
        self.secuenciaAtaque.agregar_hijo(Accion(self.objetivo_detectado))
        self.secuenciaAtaque.agregar_hijo(Accion(self.atacar))

        self.comportamiento.agregar_hijo(self.secuenciaAtaque) # el vigilante intentara atacar al jugador si lo detecta, sino se movera aleatoriamente por el mapa patrullando 
        self.comportamiento.agregar_hijo(Accion(self.Reposo))

        self.camino_actual = []# para almacenar el camino calculado por A* hacia el jugador y evitar recalcularlo cada frame si el jugador no se ha movido significativamente
        self.ultima_meta = None
        self.punto_patrulla = None

    def objetivo_detectado(self):# verifica si el jugador esta dentro del rango de deteccion del vigilante para iniciar la persecucion 
        return self.objetivo is not None

    def atacar(self):
        if not self.objetivo or not self.mapa_actual:
            return False

        # Localización en la rejilla
        vx = (self.rect.centerx - self.mapa_actual.rect.x) // self.mapa_actual.tile_size  # se calcula la posicion del vigilante y del jugador en la rejilla del mapa dividiendo sus coordenadas por el tamaño de los tiles y ajustando por la posicion del mapa en la pantalla 
        vy = (self.rect.centery - self.mapa_actual.rect.y) // self.mapa_actual.tile_size
        jx = (self.objetivo.rect.centerx - self.mapa_actual.rect.x) // self.mapa_actual.tile_size
        jy = (self.objetivo.rect.centery - self.mapa_actual.rect.y) // self.mapa_actual.tile_size

        vx = max(0, min(int(vx), len(self.mapa_actual.grid[0]) - 1))
        vy = max(0, min(int(vy), len(self.mapa_actual.grid) - 1))
        jx = max(0, min(int(jx), len(self.mapa_actual.grid[0]) - 1))
        jy = max(0, min(int(jy), len(self.mapa_actual.grid) - 1))

        inicio = EstadoMapa(vx, vy, self.mapa_actual.grid) # se crean los estados inicial y meta para el algoritmo A* utilizando las posiciones en la rejilla del vigilante y el jugador 
        meta = EstadoMapa(jx, jy, self.mapa_actual.grid)

        if self.ultima_meta != (jx, jy) or not self.camino_actual:
            self.camino_actual, _, _ = Astar(inicio, meta)
            self.ultima_meta = (jx, jy)

        if self.camino_actual and len(self.camino_actual) > 1: 
            proximo = self.camino_actual[1]
            # Ir al centro del tile
            dest_x = self.mapa_actual.rect.x + (proximo.x * self.mapa_actual.tile_size) + (self.mapa_actual.tile_size // 2)
            dest_y = self.mapa_actual.rect.y + (proximo.y * self.mapa_actual.tile_size) + (self.mapa_actual.tile_size // 2)

            dx = dest_x - self.rect.centerx
            dy = dest_y - self.rect.centery
            distancia = math.hypot(dx, dy)

            if distancia < 8: # Umbral para cambiar de nodo
                self.camino_actual.pop(0)
                return True

            if distancia != 0:
                # Movimiento paso a paso con verificación de colisión
                nueva_x = self.rect.centerx + (dx / distancia) * self.velocidad
                nueva_y = self.rect.centery + (dy / distancia) * self.velocidad
                
                # Guardamos posición vieja
                pos_vieja = self.rect.center
                
                # Intentamos mover en X
                self.rect.centerx = nueva_x
                if self.mapa_actual.colisiona_pared(self.rect):
                    self.rect.centerx = pos_vieja[0]
                
                # Intentamos mover en Y
                self.rect.centery = nueva_y
                if self.mapa_actual.colisiona_pared(self.rect):
                    self.rect.centery = pos_vieja[1]

                # Dirección visual
                if abs(dx) > abs(dy):
                    self.direccion = "derecha" if dx > 0 else "izquierda"
                else:
                    self.direccion = "abajo" if dy > 0 else "arriba"
            return True
        return False

    def Reposo(self): 
        if not self.mapa_actual: return False
        
        if not self.punto_patrulla or math.hypot(self.punto_patrulla[0]-self.rect.centerx, self.punto_patrulla[1]-self.rect.centery) < 15:
            intentos = 0
            while intentos < 50:
                rx = random.randint(0, len(self.mapa_actual.grid[0])-1)
                ry = random.randint(0, len(self.mapa_actual.grid)-1)
                if self.mapa_actual.grid[ry][rx] == 0:
                    self.punto_patrulla = (self.mapa_actual.rect.x + rx * 50 + 25, self.mapa_actual.rect.y + ry * 50 + 25)
                    break
                intentos += 1
        
        if self.punto_patrulla:
            dx = self.punto_patrulla[0] - self.rect.centerx
            dy = self.punto_patrulla[1] - self.rect.centery
            dist = math.hypot(dx, dy)
            if dist > 0:
                self.rect.centerx += (dx/dist) * 1.5
                if self.mapa_actual.colisiona_pared(self.rect): self.rect.centerx -= (dx/dist) * 1.5
                self.rect.centery += (dy/dist) * 1.5
                if self.mapa_actual.colisiona_pared(self.rect): self.rect.centery -= (dy/dist) * 1.5
        return True

    def mover(self, jugador, mapa): # el metodo mover del vigilante se llama cada frame desde el bucle principal del juego 
        self.mapa_actual = mapa
        dist = math.hypot(jugador.rect.centerx - self.rect.centerx, jugador.rect.centery - self.rect.centery)
        if dist < 350: self.objetivo = jugador
        elif dist > 700: self.objetivo = None
        self.comportamiento.ejecutar()

    def dibujar(self, superficie):# el metodo dibujar del vigilante se llama cada frame desde el bucle principal del juego para mostrar al vigilante en pantalla
        if self.imagenes and self.direccion in self.imagenes:
            img_rect = self.imagenes[self.direccion].get_rect(center=self.rect.center)
            superficie.blit(self.imagenes[self.direccion], img_rect)
        else:
            pygame.draw.rect(superficie, self.color, self.rect) # si no se pudo cargar la imagen, se dibuja un rectangulo azul como  sustituto del videojuego para que el vigilante siga siendo visible y funcional aunque sin la aparirncia original 