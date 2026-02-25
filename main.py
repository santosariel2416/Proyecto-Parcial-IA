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

from scripts.vigilante import Vigilante #aqui se importa la clase vigilante para crear los enemigos que persiguen al jugador 

#Importar dinero
from scripts.dinero import Dinero

from scripts.puerta import Puerta # importe la clase puerta para colocarlo en la esquina inferior derecha de la pantalla


# Menu principal del juego
def menu_principal():

    pygame.init()

    info = pygame.display.Info()
    Ancho = info.current_w
    Alto = info.current_h

    pantalla = pygame.display.set_mode((Ancho, Alto))
    pygame.display.set_caption("Mision Roja")

    reloj = pygame.time.Clock()
    en_menu = True

    while en_menu:

        pantalla.fill((30, 0, 0))

        fuente_titulo = pygame.font.SysFont(None, 100)
        texto_titulo = fuente_titulo.render("MISION ROJA", True, (255, 0, 0))
        pantalla.blit(texto_titulo, (Ancho//2 - 300, Alto//2 - 200))

        fuente_opcion = pygame.font.SysFont(None, 50)
        texto_jugar = fuente_opcion.render("Presiona ENTER para jugar", True, (255, 255, 255))
        pantalla.blit(texto_jugar, (Ancho//2 - 250, Alto//2))

        texto_salir = fuente_opcion.render("Presiona ESC para salir", True, (200, 200, 200))
        pantalla.blit(texto_salir, (Ancho//2 - 220, Alto//2 + 60))

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_RETURN:
                    en_menu = False
                    iniciar_juego()

                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        reloj.tick(60)



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

    #qui cree el objeto dinero
    dinero = Dinero(Ancho, Alto)
    dinero_recolectado = 0 #Esta es la variable que lleva el conteo del dinero recolectado por el jugador 

    #cree el objeto puerta
    puerta = Puerta(Ancho, Alto)
    victoria = False #Esta variable contola si el jugador llego a la puerta para ganar el juego
    dinero_necesario = 5 #Esta variable controla cuanto dinero necesita el jugador para ganar el juego

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

        tiempo_actual = pygame.time.get_ticks() 

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                corriendo = False

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_ESCAPE:
                    corriendo = False

                if evento.key == pygame.K_SPACE and not game_over:
                    nueva_bala = Bala(
                        jugador_principal.rect.centerx - 4,
                        jugador_principal.rect.top
                    )
                    balas.append(nueva_bala)

                if evento.key == pygame.K_r and game_over:

                    jugador_principal.vidas = 3
                    jugador_principal.rect.x = 200
                    jugador_principal.rect.y = 200

                    vigilantes.clear()
                    vigilantes_muertos.clear()
                    balas.clear()

                    for i in range(3):
                        enemigo = Vigilante(200 * i + 100, 50)
                        vigilantes.append(enemigo)

                    score = 0 
                    game_over = False
                    victoria = False
                    dinero_recolectado = 0

        if not game_over:

            teclas = pygame.key.get_pressed()
            jugador_principal.mover(teclas)

            if jugador_principal.rect.colliderect(dinero.rect):
                dinero_recolectado += 1
                dinero.reaparecer(pantalla.get_width(), pantalla.get_height())

            if jugador_principal.rect.colliderect(puerta.rect):
                if dinero_recolectado >= dinero_necesario:
                    victoria = True
                    game_over = True

            for vigilante in vigilantes:
                vigilante.mover(jugador_principal)

            for bala in balas:
                bala.mover()

            for bala in balas[:]:
                for vigilante in vigilantes[:]:
                    if bala.rect.colliderect(vigilante.rect):
                        if bala in balas:
                            balas.remove(bala)
                        if vigilante in vigilantes:
                            vigilantes.remove(vigilante)
                            score += 10 
                            vigilantes_muertos.append(tiempo_actual + 2000)
                        break

            for tiempo_muerte in vigilantes_muertos[:]:
                if tiempo_actual > tiempo_muerte:

                    nuevo_vigilante = Vigilante(
                        random.randint(0, pantalla.get_width() - 50),
                        50
                    )

                    vigilantes.append(nuevo_vigilante)
                    vigilantes_muertos.remove(tiempo_muerte)

            for vigilante in vigilantes[:]:
                if vigilante.rect.colliderect(jugador_principal.rect):

                    vigilantes.remove(vigilante)
                    jugador_principal.recibir_danio()
                    vigilantes_muertos.append(tiempo_actual + 2000)

                    if not jugador_principal.esta_vivo():
                        game_over = True

        balas = [b for b in balas if b.rect.y > 0]

        pantalla.fill((60, 0, 0))

        jugador_principal.dibujar(pantalla)
        dinero.dibujar(pantalla)
        puerta.dibujar(pantalla)

        for vigilante in vigilantes:
            vigilante.dibujar(pantalla)

        for bala in balas:
            bala.dibujar(pantalla)

        fuente = pygame.font.SysFont(None, 40)
        texto_vidas = fuente.render(f"Vidas: {jugador_principal.vidas}", True, (255, 255, 255))
        pantalla.blit(texto_vidas, (20, 20))

        texto_score = fuente.render(f"Puntos: {score}", True, (255, 255, 255))
        pantalla.blit(texto_score, (20, 60))

        texto_dinero = fuente.render(f"Dinero: {dinero_recolectado}", True, (0, 255, 0))
        pantalla.blit(texto_dinero, (20, 100))

        if game_over:
            fuente_grande = pygame.font.SysFont(None, 80)

            if victoria:
                texto_estado = fuente_grande.render("VICTORIA", True, (0, 255, 0))
            else:
                texto_estado = fuente_grande.render("GAME OVER", True, (255, 0, 0))

            pantalla.blit(texto_estado, (pantalla.get_width()//2 - 200, pantalla.get_height()//2 - 50))

            fuente_pequena = pygame.font.SysFont(None, 40)
            texto_reiniciar = fuente_pequena.render("Presiona R para reiniciar", True, (255, 255, 255))
            pantalla.blit(texto_reiniciar, (pantalla.get_width()//2 - 200, pantalla.get_height()//2 + 20))

        pygame.display.flip()
        tiempo.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    menu_principal() #este es el punto de entrada de mi juego, aqui se llama a la funcion menu_principal que muestra el menu del juego y desde ahi se puede iniciar el juego o salir completamente del programa
