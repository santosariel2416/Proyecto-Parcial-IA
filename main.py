# Jesus Ariel Santos 
# 24-EISN-2-034

#Empece mi codigo importando la libreria pygame que me permite crear ventanas, dibujar objetos, detectar teclado y hacer el juego
import pygame

# importe el modulo SYS que me permite usar funciones del sistema como (EXIT) que sirve para cerrar el programa completamente 
import sys 
import random #importe random que se usa para generar numeros aleatorios, lo utilice porque quiero que el vijilante reaparezca en distintas posiciones 
import os # Importe el modulo OS para asegurar que el programa encuentre la carpeta de sonidos sin importar donde este guardado el juego

#aqui cree la instruccion para poder llamar la clase jugador desde el archivo jugador.py
from scripts.jugador import Jugador

#Aqui se define la clase bala 
from scripts.bala import Bala

from scripts.vigilante import Vigilante #aqui se importa la clase vigilante para crear los enemigos que persiguen al jugador 

#Importar dinero
from scripts.dinero import Dinero

from scripts.puerta import Puerta # importe la clase puerta para colocarlo en la esquina inferior derecha de la pantalla

from scripts.mapa import MapaBanco 

# Menu principal del juego
def menu_principal():

    pygame.init() #inicie todos los modulos de pygame correctamente sin esto no funciona nada 

    info = pygame.display.Info()# utilice pygame.display.Info() para obtener el tamaño real de la pantalla
    Ancho = info.current_w
    Alto = info.current_h

    pantalla = pygame.display.set_mode((Ancho, Alto))#Cree la pantalla usando el ancho y alto de la pantalla obtenida con pygame.display.Info()
    pygame.display.set_caption("Mision Roja")

    reloj = pygame.time.Clock() #cree un reloj para controlar la velocidad del menu y que no consuma muchos recursos de la computadora 
    en_menu = True

    while en_menu: #Este es el bucle del menu principal que se ejecuta constantemente hasta que se presiona la tecla Enter para iniciar el juego o Esc para salir completamente del programa

        pantalla.fill((30, 0, 0))#Color del fondo del menu 

        fuente_titulo = pygame.font.SysFont(None, 100)
        texto_titulo = fuente_titulo.render("MISION ROJA", True, (255, 0, 0))
        pantalla.blit(texto_titulo, (Ancho//2 - 300, Alto//2 - 200))

        fuente_opcion = pygame.font.SysFont(None, 50)
        texto_jugar = fuente_opcion.render("Presiona ENTER para jugar", True, (255, 255, 255))
        pantalla.blit(texto_jugar, (Ancho//2 - 250, Alto//2))

        texto_salir = fuente_opcion.render("Presiona ESC para salir", True, (200, 200, 200))
        pantalla.blit(texto_salir, (Ancho//2 - 220, Alto//2 + 60))

        for evento in pygame.event.get(): #Este es el bucle de eventos que detecta las teclas presionadas por el usuario

            if evento.type == pygame.QUIT:#si el usuario cierra la ventana del menu, se cierra completamente el programa 
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN: #si el usuario presiona una tecla, se verifica cual es la tecla presionada para tomar la accion correspondiente 

                if evento.key == pygame.K_RETURN:
                    en_menu = False
                    iniciar_juego()

                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        reloj.tick(60) #Este es l contador de el reloj que controla la velocidad del menu,



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

    mapa = MapaBanco(Ancho, Alto) #aqui se crea el objeto mapa usando la clase mapabanco que se encarga de crear el mapa del banco con paredes y pasillos tipos laberintos, el mapa se centra en la pantalla usando el ancho y alto de la pantalla que se obtiene con pygame.display.Info() para que se adapte a cualquier tamaño de la pantalla

    # Inicializo el audio y cargo los archivos
    pygame.mixer.init()
    
    # He definido las variables de sonido como None al principio para que el juego no se cierre si no encuentra los archivos
    sonido_disparo = None
    sonido_moneda = None
    sonido_muerte = None

    # Correccion tecnica de ruta para la carpeta sonidos y assets
    ruta_script = os.path.dirname(os.path.abspath(__file__))
    dir_sonidos = os.path.join(ruta_script, "sonidos")
    ruta_fondo = os.path.join(ruta_script, "assets", "images", "fondo.png")

    # Intentamos cargar la imagen de fondo.png
    try:
        fondo_img = pygame.image.load(ruta_fondo).convert()
        fondo_juego = pygame.transform.scale(fondo_img, (Ancho, Alto))
    except:
        # Si no la encuentra, creamos una superficie de color sólido para que el juego no falle
        fondo_juego = pygame.Surface((Ancho, Alto))
        fondo_juego.fill((60, 0, 0))

    try: # aqui se cargan los sonidos del juego que se encuentran en la carpeta sonido 
        sonido_disparo = pygame.mixer.Sound(os.path.join(dir_sonidos, "sonido_dinero.wav"))
        sonido_moneda = pygame.mixer.Sound(os.path.join(dir_sonidos, "sonido_moneda.wav"))
        sonido_muerte = pygame.mixer.Sound(os.path.join(dir_sonidos, "sonido_muerte.wav"))
    except:
        pass

    #Esto permite colocar el nombre del juego arriba en la ventana 
    pygame.display.set_caption("Mision Roja")

    # El jugador empieza FUERA del banco (a la izquierda) 
    jugador_principal = Jugador(mapa.rect.left - 100, mapa.rect.centery)

    # El objeto dinero se crea pasando el objeto mapa para que aparezca dentro 
    # MODIFICACIÓN: Creamos una lista para manejar múltiples dineros si lo deseas o solo uno
    dinero_objetivo = Dinero(mapa)
    dinero_recolectado = 0 #Esta es la variable que lleva el conteo del dinero recolectado por el jugador 

    # El objeto puerta se crea pasando el objeto mapa para ubicarse en la entrada 
    puerta = Puerta(mapa)
    victoria = False #Esta variable contola si el jugador llego a la puerta para ganar el juego
    dinero_necesario = 5 #Esta variable controla cuanto dinero necesita el jugador para ganar el juego

    #Aqui cree una lista vacia que guardara todo los objetos tipo vigilantes
    vigilantes = []

    # Lista que almacenará los tiempos en que cada vigilante debe reaparecer
    vigilantes_muertos = []

    for i in range(3):#Esto es para que el ciclo se ejecute 3 veces
        intentos = 0 # Variable de seguridad para no quedar atrapado en el bucle
        while intentos < 100:
            x = random.randint(mapa.rect.left + 50, mapa.rect.right - 50)
            y = random.randint(mapa.rect.top + 50, mapa.rect.bottom - 50)
            enemigo = Vigilante(x, y)
            if not mapa.colisiona_pared(enemigo.rect):
                vigilantes.append(enemigo)
                break
            intentos += 1

    # cree un reloj para contolar la velocidad del juego
    tiempo = pygame.time.Clock()

    # Cree una Variable de control del juego es la que mantiene el juego activo
    corriendo = True

    game_over = False #Esta funcion controla si el juego termino

    score = 0 #Este es el sistema de puntos 

    balas = []

    # Este es el Bucle principal se ejecuta constantemente, si se detiene se cierra el juego
    while corriendo:

        tiempo_actual = pygame.time.get_ticks() #Esta variable obtiene el tiempo actual 

        for evento in pygame.event.get():#este es el bucle de eventos que detecta las teclas presionadas por el usuario

            if evento.type == pygame.QUIT:#si la ventana del juego es cerrada por el usuario se cierra completamente el programa
                corriendo = False

            if evento.type == pygame.KEYDOWN:# si el usuario presiona una tecla se verifica cual es la tecla presionada para tomar la accion correspondiente 

                if evento.key == pygame.K_ESCAPE:# si el usuario presiona la tecla ESC se cierra completamente el programa 
                    corriendo = False

                if evento.key == pygame.K_SPACE and not game_over:# si el usuario presiona la tecla espacio y el juego no ha terminado, se crea una nueva bala en la posicion del jugador y se agrega a la lista de balas para que se mueva y pueda eliminar a los vigilantes 
                    # Suena el disparo
                    if sonido_disparo:
                        sonido_disparo.play()# si el sonido de disparos esta cargando, se reproduce el sonido al disparar

                    # He corregido la creacion de la bala para que use la direccion actual del jugador y dispare a cualquier angulo
                    nueva_bala = Bala(
                        jugador_principal.rect.centerx - 4,
                        jugador_principal.rect.centery - 4,
                        jugador_principal.direccion
                    )
                    balas.append(nueva_bala)

                if evento.key == pygame.K_r and game_over:#si el usuario presina la tecla R y el juaego ha terminado se reinicia el juego, se restablecen las vidas del jugador 

                    jugador_principal.vidas = 3
                    # Reiniciar fuera del banco
                    jugador_principal.rect.x = mapa.rect.left - 100 
                    jugador_principal.rect.y = mapa.rect.centery

                    vigilantes.clear()
                    vigilantes_muertos.clear()
                    balas.clear()

                    for i in range(3):#Esto es para que el ciclo se ejecute 3 veces y se generen 3 vigilantes al reiniciar el juego 
                        intentos = 0
                        while intentos < 100:
                            x = random.randint(mapa.rect.left + 50, mapa.rect.right - 50)
                            y = random.randint(mapa.rect.top + 50, mapa.rect.bottom - 50)
                            enemigo = Vigilante(x, y)
                            if not mapa.colisiona_pared(enemigo.rect):
                                vigilantes.append(enemigo)
                                break
                            intentos += 1

                    score = 0 # esto reinicia el puntaje al reiniciar el juego 
                    game_over = False
                    victoria = False
                    dinero_recolectado = 0
                    dinero_objetivo.reaparecer(mapa)

        if not game_over: # si el juego no ha terminado se ejecuta la logica del juego, si el juego ha terminado se detiene toda la logica y solo se muestra el mensaje de victoria o game over y la opcion de reiniciar el juego 

            teclas = pygame.key.get_pressed()

            rect_original = jugador_principal.rect.copy()

            jugador_principal.mover(teclas)

            if mapa.colisiona_pared(jugador_principal.rect):#si el jugador colisiona con una pared del mapa, se devuelve a su posicion original antes de moverse para que no pueda atravesar las paredes
                jugador_principal.rect = rect_original

            if jugador_principal.rect.left < 0:
                jugador_principal.rect.left = 0
            if jugador_principal.rect.right > pantalla.get_width():
                jugador_principal.rect.right = pantalla.get_width()
            if jugador_principal.rect.top < 0:
                jugador_principal.rect.top = 0
            if jugador_principal.rect.bottom > pantalla.get_height():
                jugador_principal.rect.bottom = pantalla.get_height()

            # Lógica de colisión con el dinero mejorada
            if jugador_principal.rect.colliderect(dinero_objetivo.rect):# si el jugador colisiona con el dinero, se incrementa el contador de dinero recolectado y se hace que el dinero reaparezca
                
                if sonido_moneda:
                    sonido_moneda.play() # Suena el sonido de recolectar dinero
                
                dinero_recolectado += 1
                score += 50
                dinero_objetivo.reaparecer(mapa)

            if jugador_principal.rect.colliderect(puerta.rect): #si el jugador colisiona con la puerta y ha recolectado suficiente dinero, se activa la victoria y se termina el juego
                if dinero_recolectado >= dinero_necesario:
                    victoria = True
                    game_over = True

            for vigilante in vigilantes:# Aqui se mueve cada vigilante usando su metodo mover, se le pasa el jugadr y el mapa para que se mueva inteligentemente persiguiendo al jugador y evitando las paredes, si el vigilante colisiona con una pared se devuelve a su posicion original para que no atraviese las paredes

                posicion_original = vigilante.rect.copy()

                vigilante.mover(jugador_principal, mapa)
                if mapa.colisiona_pared(vigilante.rect):
                    vigilante.rect = posicion_original

            for bala in balas:#aqui se mueve cada bala usando su metodo mover y ahora le paso el mapa para detectar las paredes
                bala.mover(mapa)

            for bala in balas[:]:
                for vigilante in vigilantes[:]:
                    if bala.rect.colliderect(vigilante.rect):
                        if sonido_muerte:
                            sonido_muerte.play() # suena el sonido de muerte al eliminar a un vigilante
                        if bala in balas:
                            balas.remove(bala)
                        if vigilante in vigilantes:
                            vigilantes.remove(vigilante)
                            score += 10 
                            vigilantes_muertos.append(tiempo_actual + 2000)
                        break

            for tiempo_muerte in vigilantes_muertos[:]:# Este es el ciclo que revisa si algun vigilante ha cumplido su tiempo de muerte para reaparecer
                if tiempo_actual > tiempo_muerte:

                    intentos = 0
                    while intentos < 100:
                        x = random.randint(mapa.rect.left + 50, mapa.rect.right - 50)
                        y = random.randint(mapa.rect.top + 50, mapa.rect.bottom - 50)
                        nuevo_vigilante = Vigilante(x, y)
                        if not mapa.colisiona_pared(nuevo_vigilante.rect):
                            vigilantes.append(nuevo_vigilante)
                            break
                        intentos += 1

                    vigilantes_muertos.remove(tiempo_muerte)

            for vigilante in vigilantes[:]:
                if vigilante.rect.colliderect(jugador_principal.rect):
                    if sonido_muerte:
                        sonido_muerte.play() # suena el sonido de muerte al ser golpeado por el vigilante

                    vigilantes.remove(vigilante)
                    jugador_principal.recibir_danio()
                    vigilantes_muertos.append(tiempo_actual + 2000)

                    if not jugador_principal.esta_vivo():
                        game_over = True

            # He corregido la limpieza de balas para que se eliminen si salen por cualquier lado de la pantalla o si chocan con una pared
            balas = [b for b in balas if 0 < b.rect.x < Ancho and 0 < b.rect.y < Alto and b.activa]

        # Aqui se dibuja todo en la pantalla
        # Dibujamos primero el fondo para que esté atrás de todo
        pantalla.blit(fondo_juego, (0, 0))

        mapa.dibujar(pantalla) # Dibujar el edificio del banco

        jugador_principal.dibujar(pantalla)
        dinero_objetivo.dibujar(pantalla)
        puerta.dibujar(pantalla) # Dibujar la puerta de entrada/salida

        for vigilante in vigilantes:
            vigilante.dibujar(pantalla)

        for bala in balas:
            bala.dibujar(pantalla)

        fuente = pygame.font.SysFont(None, 40)
        texto_vidas = fuente.render(f"Vidas: {jugador_principal.vidas}", True, (255, 255, 255))
        pantalla.blit(texto_vidas, (20, 20))

        texto_score = fuente.render(f"Puntos: {score}", True, (255, 255, 255))
        pantalla.blit(texto_score, (20, 60))

        texto_score = fuente.render(f"Puntos: {score}", True, (255, 255, 255))
        pantalla.blit(texto_score, (20, 60))

        texto_dinero = fuente.render(f"Dinero: {dinero_recolectado}/{dinero_necesario}", True, (0, 255, 0))
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
        # Se usa tiempo.tick porque asi se definio arriba en la funcion iniciar_juego
        tiempo.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    menu_principal() #este es el punto de entrada de mi juego, aqui se llama a la funcion menu_principal que muestra el menu del juego y desde ahi se puede iniciar el juego o salir completamente del programa