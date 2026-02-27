#Jesus Ariel Santos 
#24-EISN-2-034

import pygame
#importe random que se usa para generar numeros aleatorios, lo utilice porque quiero que el vigilante reaparezca en distintas posiciones
import random
import math
from scripts.mapa import EstadoMapa
from scripts.a_estrella import Astar  #importe el algoritmo a estrella para que el vigilantes puedan persegir al jugador de manera inteligente y no solo moverse hacia abajo como lo hacia 

# ESTRUCTURA DEL ÁRBOL DE COMPORTAMIENTO 
class Nodo:#Esta es la clase base para los nodos del arbol de comportamiento, cada nodo puede tener hijos y una funcion de ejecucion 
    def __init__(self):# es el constructor de la clase nodo, se ejecuta cada vez que se crea un nodo, en este caso inicializa una lista vacia de hujos
        self.hijos = []

    def agregar_hijo(self, hijo):#Este metodo se utiliza para agregar un hijo a un nodo
        self.hijos.append(hijo)

    def ejecutar(self):#Este metodo es el que se llama para ejecutar la logica del nodo
        pass

class Selector(Nodo):#Este nodo ejecuta a sus hijos en orden y devuelve True si alguno de ellos devuelve True, si todos devuelven False, devuelve false 
    def ejecutar(self):
        for hijo in self.hijos:
            if hijo.ejecutar():
                return True
        return False

class Secuencia(Nodo):#Este nodo ejecuta a sus hijos en orden y devuelve False si alguno de ellos devuelve False, si todos devuelven True, devuelven True 
    def ejecutar(self):
        for hijo in self.hijos:
            if not hijo.ejecutar():
                return False
        return True

class Accion(Nodo):#Este nodo ejecuta una accion especifico, se le pasa una funcion al constructor y se ejecuta esa funcion cuando se llama a ejecutar 
    def __init__(self, accion):
        super().__init__()
        self.accion = accion

    def ejecutar(self):# Aqui se ejecuta la funcion que se le paso al constructor, esta funcion debe devolver un booleano para que el arbol de comportamiento funcione correctamente
        return self.accion()

class Invertir(Nodo):#Este nodo invierte el resultado de su hijo , si el hijo devuelve true, devuelve false y viceversa
    def __init__(self, accion):
        super().__init__()
        self.agregar_hijo(accion)

    def ejecutar(self):# Aqui se ejecuta el hijo y se invierte su resultado
        return not self.hijos[0].ejecutar()

class Timer(Nodo):#Este es un nodo que se ejecuta durante un tiempo determinado y luego se reinicia 
    def __init__(self, tiempo):
        super().__init__()
        self.tiempo = tiempo
        self.tiempo_restante = tiempo

    def ejecutar(self):#Este metodo se ejecuta cada vez que se llama a ejecutar, si el tiempo restante es mayor a 0, se decrementa y devuelve false, si el tiempo restante es 0, se reinicia el tiempo y se ejecuta el hijo
        if self.tiempo_restante > 0:
            self.tiempo_restante -= 1
            return False
        else:
            self.tiempo_restante = self.tiempo
            return self.hijos[0].ejecutar()#aqui se ejecuta el hijo del timer, este hijo debe ser una accion que se quiera ejecutar cada cierto tiempo, en este caso es la accion de desactivar el objetivo del vigilante cada 180 frames 

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

        # --- CONFIGURACIÓN DEL ÁRBOL DE COMPORTAMIENTO ---
        self.objetivo = None
        self.mapa_actual = None
        
        self.comportamiento = Selector()
        secuenciaAtaque = Secuencia()
        secuenciaReposo = Secuencia()

        self.comportamiento.agregar_hijo(secuenciaAtaque)
        self.comportamiento.agregar_hijo(secuenciaReposo)

        hay_objetivo = Accion(lambda: self.objetivo is not None)

        # Rama de Reposo: Si no hay objetivo, esperar/patrullar
        secuenciaReposo.agregar_hijo(Invertir(hay_objetivo))
        secuenciaReposo.agregar_hijo(Accion(self.Reposo))

        # Rama de Ataque: Si hay objetivo, atacar (A*)
        secuenciaAtaque.agregar_hijo(Accion(self.objetivo_cerca))
        secuenciaAtaque.agregar_hijo(Accion(self.atacar))

        # Timer para desactivar el objetivo (cada 180 frames intenta desactivarlo)
        tiempoAtacando = Timer(180)
        tiempoAtacando.agregar_hijo(Accion(self.Desactivar_objetivo))
        secuenciaAtaque.agregar_hijo(tiempoAtacando)

    # Métodos del Árbol de Comportamiento
    def Desactivar_objetivo(self):
        self.objetivo = None
        return True

    def objetivo_cerca(self):
        # Si tenemos un objetivo asignado, consideramos que está "cerca" para activar la secuencia
        return self.objetivo is not None

    def atacar(self):
        # Aquí va tu lógica de A* original
        if self.objetivo and self.mapa_actual:
            grid_x_vig = (self.rect.x - self.mapa_actual.rect.x) // self.mapa_actual.tile_size
            grid_y_vig = (self.rect.y - self.mapa_actual.rect.y) // self.mapa_actual.tile_size
            grid_x_jug = (self.objetivo.rect.x - self.mapa_actual.rect.x) // self.mapa_actual.tile_size
            grid_y_jug = (self.objetivo.rect.y - self.mapa_actual.rect.y) // self.mapa_actual.tile_size
            

            inicio = EstadoMapa(grid_x_vig, grid_y_vig, self.mapa_actual.grid)
            objetivo_a_estrella = EstadoMapa(grid_x_jug, grid_y_jug, self.mapa_actual.grid)

            resultado = Astar(inicio, objetivo_a_estrella)
            camino = resultado[0] if isinstance(resultado, tuple) else resultado

            if camino and len(camino) > 1:
                proximo_paso = camino[1]
                destino_x = self.mapa_actual.rect.x + (proximo_paso.x * self.mapa_actual.tile_size) + (self.mapa_actual.tile_size // 2 - self.ancho // 2)
                destino_y = self.mapa_actual.rect.y + (proximo_paso.y * self.mapa_actual.tile_size) + (self.mapa_actual.tile_size // 2 - self.alto // 2)

                if self.rect.x < destino_x: self.rect.x += self.velocidad
                elif self.rect.x > destino_x: self.rect.x -= self.velocidad
                if self.rect.y < destino_y: self.rect.y += self.velocidad
                elif self.rect.y > destino_y: self.rect.y -= self.velocidad
        return True

    def Reposo(self):
        # Tu lógica original de movimiento simple cuando no hay persecución
        self.rect.y += self.velocidad
        # Reaparecer si sale de pantalla (tu lógica original)
        if self.rect.top > pygame.display.get_surface().get_height():
            self.rect.y = -50
            self.rect.x = random.randint(0, pygame.display.get_surface().get_width() - self.ancho)
        return True

    #Este metodo controla el movimiento automatico del vigilante, este se movera solo
    def mover(self, jugador, mapa):
        self.mapa_actual = mapa
        
        # Lógica de detección: si el jugador está cerca, se vuelve el objetivo
        distancia = math.hypot(jugador.rect.centerx - self.rect.centerx, jugador.rect.centery - self.rect.centery)
        if distancia < 300: # Rango de visión de 300 píxeles
            self.objetivo = jugador
        
        # Ejecutar el árbol de comportamiento
        self.comportamiento.ejecutar()

    #Este metodo es el que dibuja al vigilante en pantalla
    def dibujar(self, superficie):
        pygame.draw.rect(superficie, self.color, self.rect)