# Jesus Ariel Santos 
# 24-EISN-2-034

import pygame
import os # Importe el modulo OS para asegurar que el programa encuentre el spritesheet sin importar donde este guardado el juego

class Jugador:
    def __init__(self, posicion_x, posicion_y):
        # Aquí guardo la posición inicial donde aparece el jugador
        # En lugar de usar solo x e y, ahora usare un rectángulo
        # porque nos permitirá detectar colisiones más adelante
        
        # He ajustado el ancho y alto a 50 para que el jugador se vea mejor
        # y aproveche el espacio de los pasillos que ahora son de 64
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

        # Cree esta variable para que el jugador sepa hacia donde esta mirando y pueda disparar en esa direccion
        # Por defecto mira hacia arriba (0 en X, -1 en Y)
        self.direccion = (0, -1)

        # aqui es donde cargamos el spritesheet deljugador
        ruta_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ruta_imagen = os.path.join(ruta_base, "assets", "images", "imagen_jugador.png")
        
        try:
            # Cargamos con convert_alpha para respetar la transparencia original
            full_sheet = pygame.image.load(ruta_imagen).convert_alpha()
            
            # Tu imagen tiene 8 columnas. Calculamos el tamaño real de cada cuadro original
            self.frame_width = full_sheet.get_width() // 8
            self.frame_height = full_sheet.get_height() // 4
            self.spritesheet = full_sheet
        except Exception as e:
            print(f"Error cargando imagen: {e}")
            self.spritesheet = pygame.Surface((120, 120), pygame.SRCALPHA)
            self.frame_width = 50
            self.frame_height = 50

        # Función mejorada para eliminar el rastro de sombra
        def get_frame(sheet, col, row):
            # 1. Creamos el área de recorte
            area = (col * self.frame_width, row * self.frame_height, self.frame_width, self.frame_height)
            
            # 2. Creamos una superficie nueva con soporte de transparencia total
            cuadro_final = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
            
            # 3. Recortamos el muñequito del original
            temp_sub = sheet.subsurface(area)
            
            # 4. Lo escalamos usando 'scale' en lugar de 'smoothscale' 
            # Esto evita que Pygame invente píxeles borrosos en los bordes (la sombra)
            personaje_escalado = pygame.transform.scale(temp_sub, (self.ancho, self.alto))
            
            # 5. Pegamos el personaje limpio en nuestra superficie final
            cuadro_final.blit(personaje_escalado, (0, 0))
            
            return cuadro_final

        # Organizamos las animaciones (Fila 0 y 2 según tu imagen de 8 columnas)
        self.animaciones = {
            "derecha": [get_frame(self.spritesheet, i, 0) for i in range(4)],
            "izquierda": [get_frame(self.spritesheet, i+4, 0) for i in range(4)],
            "abajo": [get_frame(self.spritesheet, i, 2) for i in range(4)],
            "arriba": [get_frame(self.spritesheet, i+4, 2) for i in range(4)],
        }
        
        self.animacion_actual = "abajo"
        self.current_frame = 0
        self.timer_animacion = 0
        self.imagen_actual = self.animaciones[self.animacion_actual][0]
        self.caminando = False

    def mover(self, teclas_presionadas):# Este metodo se encarga de mover al jugador segun las teclas que se presionen, recibe un diccionario con las teclas presionadas
        self.caminando = False

        # Movimiento horizontal
        if teclas_presionadas[pygame.K_LEFT]:
            self.rect.x -= self.velocidad
            self.direccion = (-1, 0)
            self.animacion_actual = "izquierda"
            self.caminando = True
        elif teclas_presionadas[pygame.K_RIGHT]:
            self.rect.x += self.velocidad
            self.direccion = (1, 0)
            self.animacion_actual = "derecha"
            self.caminando = True

        # Movimiento vertical
        if teclas_presionadas[pygame.K_UP]:
            self.rect.y -= self.velocidad
            self.direccion = (0, -1)
            self.animacion_actual = "arriba"
            self.caminando = True
        elif teclas_presionadas[pygame.K_DOWN]:
            self.rect.y += self.velocidad
            self.direccion = (0, 1)
            self.animacion_actual = "abajo"
            self.caminando = True

        # Control de la animación
        if self.caminando:
            self.timer_animacion += 1
            if self.timer_animacion >= 8:
                self.current_frame = (self.current_frame + 1) % 4
                self.timer_animacion = 0
            self.imagen_actual = self.animaciones[self.animacion_actual][self.current_frame]
        else:
            self.imagen_actual = self.animaciones[self.animacion_actual][0]

        # Limites de pantalla
        pantalla = pygame.display.get_surface()
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > pantalla.get_width(): self.rect.right = pantalla.get_width()
        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > pantalla.get_height(): self.rect.bottom = pantalla.get_height()

    def dibujar(self, superficie):
        # Dibujamos la imagen del personaje (el spray)
        superficie.blit(self.imagen_actual, self.rect)

    def recibir_danio(self): 
        #Esto reduce una vida cuando el jugador es golpeado
        self.vidas -= 1 

    def esta_vivo(self): 
        #Esto devuelve true si el jugador tiene vidas restantes, de lo contrario devuelve false
        return self.vidas > 0