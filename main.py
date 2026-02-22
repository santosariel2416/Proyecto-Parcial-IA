# Jesus Ariel Santos 24-EISN-2-034

#Empece mi codigo importando la libreria pygame que me permite crear ventanas, dibujar objetos, detectar teclado y hacer el juego
import pygame

# importe el modulo SYS que me permite usar funciones del sistema como (EXIT) que sirve para cerrar el programa completamente 
import sys 
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

    vigilantes = []

    for i in range(3):
        enemigo = Vigilante(200 * i + 100, 50)
    vigilantes.append(enemigo) 

    # cree un reloj para contolar la velocidad del juego
    tiempo = pygame.time.Clock()

    # Cree una Variable de control del juego es la que mantiene el juego activo
    corriendo = True

    balas = []

    # Este es el Bucle principal se ejecuta constantemente, si se detiene se cierra el juego
    while corriendo:

        # Detectar eventos como el teclas mouse y cerrar la ventana 
        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                corriendo = False

            #Aqui se detecta cuando se presiona la tecla escape para salir del juego
            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_ESCAPE:
                    corriendo = False

                #Aqui se crea la bala desde el centro del jugador
                if evento.key == pygame.K_SPACE:
                    nueva_bala = Bala(
                        jugador_principal.rect.centerx - 4,
                        jugador_principal.rect.top
                    )
                    balas.append(nueva_bala)

        #Aqui se Detecta las teclas presionadas y despues se la pasa al jugador 
        teclas = pygame.key.get_pressed()

        # Esto permite que el jugador se mueva 
        jugador_principal.mover(teclas)

        # Mover balas
        for bala in balas:
            bala.mover()

            for vigilante in vigilantes:
                vigilante.mover(jugador_principal)

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