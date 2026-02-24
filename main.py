# Jesus Ariel Santos 
# 24-EISN-2-034

#Empece mi codigo importando la libreria pygame que me permite crear ventanas, dibujar objetos, detectar teclado y hacer el juego
import pygame

# importe el modulo SYS que me permite usar funciones del sistema como (EXIT) que sirve para cerrar el programa completamente 
import sys 
import random

#aqui cree la instruccion para poder llamar la clase jugador desde el archivo jugador.py
from scripts.jugador import Jugador

#Aqui se define la clase bala 
from scripts.bala import Bala

from scripts.vigilante import Vigilante

#Cree esta funcion que contiene todo el juego 
def iniciar_juego():

    # Aquí iniciamos todos los modulos de pygame correctamente sin esto no funciona el teclado no funciona la ventana, no funcionaria nada
    pygame.init()

    # Utilice pygame.display.Info() para obtener el tamaño real de la pantalla
    info = pygame.display.Info()
    Ancho = info.current_w
    Alto = info.current_h

    # Cree la pantalla en modo RESIZABLE que permite que pueda cambiar el tamaño de la pantalla como minimizar, maximizar y cerrar  
    pantalla = pygame.display.set_mode((Ancho, Alto), pygame.RESIZABLE)

    #Esto permite colocar el nombre del juego arriba en la ventana 
    pygame.display.set_caption("Mision Roja")

    # Aqui cree un objeto de la clase jugador, este sera el personaje que se mueve en la pantalla
    jugador_principal = Jugador(200, 200)

    #Aqui cree una lista vacia que guardara todo los objetos tipo vigilantes
    vigilantes = []

    # Lista que almacenará los tiempos en que cada vigilante debe reaparecer
    vigilantes_muertos = []

    for i in range(3):#Esto es para que el ciclo se ejecute 3 veces
        enemigo = Vigilante(200 * i + 100, 50)
        vigilantes.append(enemigo)

    # cree un reloj para contolar la velocidad del juego
    tiempo = pygame.time.Clock()

    # Cree una Variable de control del juego es la que mantiene el juego activo
    corriendo = True

    game_over = False #Esta funcion controla si el juego termino

    score = 0 #Este es el sistema de puntos 

    balas = []

    # Este es el Bucle principal se ejecuta constantemente, si se detiene se cierra el juego
    while corriendo:

        # Guarde el tiempo actual del juego en milisegundos
        tiempo_actual = pygame.time.get_ticks()

        # Detectar eventos como el teclas mouse y cerrar la ventana 
        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                corriendo = False

            #Aqui se detecta cuando se presiona la tecla escape para salir del juego
            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_ESCAPE:
                    corriendo = False

                #Aqui se crea la bala desde el centro del jugador
                if evento.key == pygame.K_SPACE and not game_over:
                    nueva_bala = Bala(
                        jugador_principal.rect.centerx - 4,
                        jugador_principal.rect.top
                    )
                    balas.append(nueva_bala)

        if not game_over:

            #Aqui se Detecta las teclas presionadas y despues se la pasa al jugador 
            teclas = pygame.key.get_pressed()

            # Esto permite que el jugador se mueva 
            jugador_principal.mover(teclas)

            for vigilante in vigilantes:
                vigilante.mover(jugador_principal)

            # Mover balas
            for bala in balas:
                bala.mover()

            #  AQUI VA LA COLISION
            for bala in balas[:]:
                for vigilante in vigilantes[:]:# Esto lo que hace es copiarla lista para evitar errores al eliminar
                    if bala.rect.colliderect(vigilante.rect):# Esto detecta si la bala golpeo al enemigo
                        if bala in balas:
                            balas.remove(bala) #Esta parte elimina la bala de la lista
                        if vigilante in vigilantes:
                            vigilantes.remove(vigilante)#Elimina al vigilante

                            score += 10 #Este es el sistema de puntos 

                            #  Se Guarda el tiempo en que murio el vigilante
                            # y sumamos 2000 milisegundos (2 segundos)
                            vigilantes_muertos.append(tiempo_actual + 2000)
                        break

            # SISTEMA DE REAPARICION INDIVIDUAL
            for tiempo_muerte in vigilantes_muertos[:]:
                if tiempo_actual > tiempo_muerte:

                    # Aqui Cree nuevo vigilante en posición aleatoria en la parte superior
                    nuevo_vigilante = Vigilante(
                        random.randint(0, pantalla.get_width() - 50),
                        50
                    )

                    vigilantes.append(nuevo_vigilante)
                    vigilantes_muertos.remove(tiempo_muerte)

            # COLISION VIGILANTE CONTRA JUGADOR
            for vigilante in vigilantes[:]:
                if vigilante.rect.colliderect(jugador_principal.rect):

                    vigilantes.remove(vigilante)

                    # El jugador recibe daño al ser golpeado por un vigilante 
                    jugador_principal.recibir_danio()

                    #Aqui se guarda el tiempo en que el vigilante debe reaparecer 
                    vigilantes_muertos.append(tiempo_actual + 2000)

                    # GAME OVER, Aquí verificamos si el jugador todavía está vivo, Si no tiene vidas, el juego se detiene
                    if not jugador_principal.esta_vivo():
                        game_over = True

        # Eliminar balas que salen de la pantalla
        balas = [b for b in balas if b.rect.y > 0]

        # Este es el fondo
        pantalla.fill((60, 0, 0))

        # aqui se llama al metodo Dibujar de la clase jugador para mostrarlo en pantalla 
        jugador_principal.dibujar(pantalla)

        for vigilante in vigilantes:
            vigilante.dibujar(pantalla)

        # Dibujar balas
        for bala in balas:
            bala.dibujar(pantalla)

        # Mostrar sistema de vidas en pantalla
        fuente = pygame.font.SysFont(None, 40)
        texto_vidas = fuente.render(f"Vidas: {jugador_principal.vidas}", True, (255, 255, 255))
        pantalla.blit(texto_vidas, (20, 20))

        # Mostrar sistema de puntos
        texto_score = fuente.render(f"Puntos: {score}", True, (255, 255, 255))
        pantalla.blit(texto_score, (20, 60))

        # Mostrar pantalla de Game Over
        if game_over:
            fuente_grande = pygame.font.SysFont(None, 80)
            texto_game_over = fuente_grande.render("GAME OVER", True, (255, 0, 0))
            pantalla.blit(texto_game_over, (pantalla.get_width()//2 - 200, pantalla.get_height()//2 - 50))

        # Actualiza la pantalla
        pygame.display.flip()

        # Controla los FPS 
        tiempo.tick(60)

    #cierra pygame correctamente 
    pygame.quit()
    
    #Esto termina el programa 
    sys.exit()


if __name__ == "__main__":
    iniciar_juego()
