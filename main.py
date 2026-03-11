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
from scripts.dinero import Dinero #aqui se importa la clase dinero para crear el dinero que el jugador debe recolectar para ganar el juego 

from scripts.puerta import Puerta # importe la clase puerta para colocarlo en la esquina inferior derecha de la pantalla

from scripts.mapa import MapaBanco #Aqui se importa la clase mapa banco para crear el mapa del banco donde se desarrolla el juego, el mapa tiene paredes y pasillos tipo laberinto

# Menu principal del juego
def menu_principal():

    pygame.init() #inicie todos los modulos de pygame correctamente sin esto no funciona nada 
    pygame.mixer.init() # Inicializamos el audio para la musica de inicio
    
    #INICIALIZAR CONTROL de videojuego 
    pygame.joystick.init()
    control = None
    if pygame.joystick.get_count() > 0:
        control = pygame.joystick.Joystick(0)
        control.init()

    info = pygame.display.Info()# utilice pygame.display.Info() para obtener el tamaño real de la pantalla
    Ancho = info.current_w
    Alto = info.current_h

    pantalla = pygame.display.set_mode((Ancho, Alto))#Cree la pantalla usando el ancho y alto de la pantalla obtenida con pygame.display.Info()
    pygame.display.set_caption("Mision Roja")

    # --- MUSICA DE INICIO ---
    ruta_script = os.path.dirname(os.path.abspath(__file__))
    ruta_inicio = os.path.join(ruta_script, "assets", "music", "musica inicio.mp3")
    try:
        pygame.mixer.music.load(ruta_inicio)
        pygame.mixer.music.play(-1) # Suena en bucle en el menu
        pygame.mixer.music.set_volume(1.0) 
    except:
        print("Aviso: No se pudo cargar musica inicio.mp3")

    reloj = pygame.time.Clock() #cree un reloj para controlar la velocidad del menu y que no consuma muchos recursos de la computadora 
    en_menu = True
    
    # aqui cree una lista de gotas de sangre para el efecto de lluvia de sangre del menu 
    gotas_sangre = []
    for i in range(100): 
        x = random.randint(0, Ancho)
        y = random.randint(-Alto, 0) 
        velocidad = random.randint(3, 8) 
        tamano = random.randint(3, 6) 
        gotas_sangre.append([x, y, velocidad, tamano])

    # Variables para el efecto profesional de parpadeo
    contador_alpha = 0
    subiendo = True

    #Cree los rectangulos para los botones de empezar el juego y salir del juego y les asigne una fuente para el texto de los botones 
    rect_empezar = pygame.Rect(Ancho//2 - 200, Alto//2 + 20, 400, 70)
    rect_salir = pygame.Rect(Ancho//2 - 200, Alto//2 + 110, 400, 70)
    fuente_botones = pygame.font.SysFont("Arial", 40, bold=True)

    while en_menu: #Este es el bucle del menu principal que se ejecuta constantemente hasta que se presiona la tecla Enter para iniciar el juego o Esc para salir completamente del programa

        pantalla.fill((20, 0, 0))#Fondo oscuro profesional (con un toque de rojo muy oscuro)
        pos_mouse = pygame.mouse.get_pos()

        for gota in gotas_sangre:#Aqui se actualiza la posicion de cada gota de sangre para crear el efecto de lluvia de sangre del menu x
            gota[1] += gota[2] 
            if gota[1] > Alto:
                gota[1] = random.randint(-100, 0)
                gota[0] = random.randint(0, Ancho)
            pygame.draw.rect(pantalla, (138, 0, 0), (gota[0], gota[1], gota[3]//2, gota[3]*2))
            
        fuente_titulo = pygame.font.SysFont("Impact", 150) 
        texto_sombra = fuente_titulo.render("MISION ROJA", True, (0, 0, 0))
        pantalla.blit(texto_sombra, (Ancho//2 - 395, Alto//2 - 245))
        texto_titulo = fuente_titulo.render("MISION ROJA", True, (255, 0, 0))
        pantalla.blit(texto_titulo, (Ancho//2 - 400, Alto//2 - 250))

        pygame.draw.rect(pantalla, (255, 0, 0), (Ancho//2 - 300, Alto//2 - 100, 600, 5)) # linea decorativa roja arriba del titulo 

        if subiendo:
            contador_alpha += 5
            if contador_alpha >= 255: subiendo = False
        else:
            contador_alpha -= 5
            if contador_alpha <= 50: subiendo = True

        # Boton Enter para Jugar
        col_e = (200, 0, 0) if rect_empezar.collidepoint(pos_mouse) else (138, 0, 0)
        pygame.draw.rect(pantalla, col_e, rect_empezar, border_radius=10)
        txt_e = fuente_botones.render("ENTER PARA JUGAR", True, (255, 255, 255))
        txt_e.set_alpha(contador_alpha)
        pantalla.blit(txt_e, (rect_empezar.x + 35, rect_empezar.y + 12))

        # Boton para Salir del Juego
        col_s = (200, 0, 0) if rect_salir.collidepoint(pos_mouse) else (138, 0, 0)
        pygame.draw.rect(pantalla, col_s, rect_salir, border_radius=10)
        txt_s = fuente_botones.render("SALIR DEL JUEGO", True, (255, 255, 255))
        txt_s.set_alpha(contador_alpha)
        pantalla.blit(txt_s, (rect_salir.x + 55, rect_salir.y + 12))

        fuente_creditos = pygame.font.SysFont("Arial", 20)
        texto_autor = fuente_creditos.render("Desarrollado por: Jesus Ariel Santos", True, (100, 100, 100))
        pantalla.blit(texto_autor, (20, Alto - 40))

        for evento in pygame.event.get(): 
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1: 
                    if rect_empezar.collidepoint(evento.pos):
                        pygame.mixer.music.stop()
                        en_menu = False
                        iniciar_juego()
                    if rect_salir.collidepoint(evento.pos):
                        pygame.quit()
                        sys.exit()
            if evento.type == pygame.KEYDOWN: 
                if evento.key == pygame.K_RETURN:
                    pygame.mixer.music.stop() 
                    en_menu = False
                    iniciar_juego()
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            
            # DETECCION DE BOTON START O X EN EL CONTROL PARA EMPEZAR 
            if evento.type == pygame.JOYBUTTONDOWN:
                if evento.button in [0, 9]: # 0 es X, 9 suele ser Start
                    pygame.mixer.music.stop()
                    en_menu = False
                    iniciar_juego()

        pygame.display.flip()
        reloj.tick(60) #Este es l contador de el reloj que controla la velocidad del menu,

def iniciar_juego():

    # Aquí iniciamos todos los modulos de pygame correctamente sin esto no funciona el teclado no funciona la ventana, no funcionaria nada
    pygame.init()

    # Utilice pygame.display.Info() para obtener el tamaño real de la pantalla
    info = pygame.display.Info()
    Ancho = info.current_w
    Alto = info.current_h

    # Re-detectar control en el juego
    pygame.joystick.init()
    control = None
    if pygame.joystick.get_count() > 0:
        control = pygame.joystick.Joystick(0)
        control.init()

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
    dir_sonidos = os.path.join(ruta_script, "assets", "sonidos") # Ruta corregida a assets/sonidos
    ruta_fondo = os.path.join(ruta_script, "assets", "images", "fondo.png")
    
    # Rutas para las musicas del juego 
    ruta_musica_fondo = os.path.join(ruta_script, "assets", "music", "musica fondo.mp3")
    ruta_musica_perdiste = os.path.join(ruta_script, "assets", "music", "musica perdiste.mp3")
    ruta_musica_victoria = os.path.join(ruta_script, "assets", "music", "musica victoria.mp3")
    
    try:
        pygame.mixer.music.load(ruta_musica_fondo)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.4)
    except:
        pass

    # Intentamos cargar la imagen de fondo.png
    try:
        fondo_img = pygame.image.load(ruta_fondo).convert()
        fondo_juego = pygame.transform.scale(fondo_img, (Ancho, Alto))
    except:
        # Si no la encuentra, creamos una superficie de color sólido para que el juego no falle
        fondo_juego = pygame.Surface((Ancho, Alto))
        fondo_juego.fill((60, 0, 0))

    # CARGA DE SONIDOS INDIVIDUAL PARA EVITAR FALLOS
    try:
        sonido_disparo = pygame.mixer.Sound(os.path.join(dir_sonidos, "sonido_disparar.wav"))
    except: print("No se encontró sonido_disparar.wav")

    try:
        sonido_moneda = pygame.mixer.Sound(os.path.join(dir_sonidos, "sonido_dinero.mp3"))
    except: print("No se encontró sonido_dinero.wav")

    try:
        sonido_muerte = pygame.mixer.Sound(os.path.join(dir_sonidos, "sonido_muerte.mp3"))
    except: print("No se encontró sonido_muerte.wav")

    #Esto permite colocar el nombre del juego arriba en la ventana 
    pygame.display.set_caption("Mision Roja")

    # El jugador empieza FUERA del banco (a la izquierda) 
    jugador_principal = Jugador(mapa.rect.left - 100, mapa.rect.centery)

    # El objeto dinero se crea pasando el objeto mapa para que aparezca dentro 
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

    for i in range(7): # Esto es para que el ciclo se ejecute (7) veces 
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
    musica_perdiste_activa = False # Variable para controlar que la música de muerte no se cargue repetidamente
    musica_victoria_activa = False # Variable para controlar que la musica de victoria no se cargue repetidamente

    score = 0 #Este es el sistema de puntos 

    balas = []

    # configuracion del efecto de lluvia de sangre para la pantalla de game over 
    gotas_sangre_go = [[random.randint(0, Ancho), random.randint(-Alto, 0), random.randint(4, 10), random.randint(3, 7)] for _ in range(150)]
    alpha_perdiste = 0
    subiendo_perdiste = True
    rect_reintentar = pygame.Rect(Ancho//2 - 200, Alto//2 + 50, 400, 70)
    rect_volver_inicio = pygame.Rect(Ancho//2 - 200, Alto//2 + 140, 400, 70) 

    # CONFIGURACIÓN DE EFECTO DE LLUVIA DE DINERO PARA la VICTORIA 
    lluvia_dinero = []
    for i in range(200): # Muchas gotas para la victoria
        x = random.randint(0, Ancho)
        y = random.randint(-Alto, 0)
        velocidad = random.randint(3, 9) 
        tamano = random.randint(10, 20) # Más grandes
        color = random.choice([(0, 150, 0), (255, 215, 0)]) # Verde billete o Oro
        lluvia_dinero.append([x, y, velocidad, tamano, color])

    # Variables de parpadeo para Victoria
    alpha_victoria = 0
    subiendo_victoria = True

    # Este es el Bucle principal se ejecuta constantemente, si se detiene se cierra el juego
    while corriendo:

        tiempo_actual = pygame.time.get_ticks() #Esta variable obtiene el tiempo actual 
        pos_mouse = pygame.mouse.get_pos()

        for evento in pygame.event.get():#este es el bucle de eventos que detecta las teclas presionadas por el usuario

            if evento.type == pygame.QUIT:#si la ventana del juego es cerrada por el usuario se cierra completamente el programa
                corriendo = False

            # DETECCION DE DISPARO CON L1 (Botón 4) o R1 (Botón 5)
            if evento.type == pygame.JOYBUTTONDOWN:
                if (evento.button == 4 or evento.button == 5) and not game_over and not victoria:
                    if sonido_disparo:
                        sonido_disparo.play()
                    nueva_bala = Bala(
                        jugador_principal.rect.centerx - 4,
                        jugador_principal.rect.centery - 4,
                        jugador_principal.direccion
                    )
                    balas.append(nueva_bala)
                
                # REINICIAR CON X (Botón 0)
                if evento.button == 0 and (game_over or victoria):
                    # Lógica de reinicio (copiada de la tecla R)
                    musica_perdiste_activa = False
                    musica_victoria_activa = False
                    try:
                        pygame.mixer.music.load(ruta_musica_fondo)
                        pygame.mixer.music.play(-1)
                    except: pass
                    jugador_principal.vidas = 3
                    jugador_principal.rect.x = mapa.rect.left - 100 
                    jugador_principal.rect.y = mapa.rect.centery
                    vigilantes.clear()
                    vigilantes_muertos.clear()
                    balas.clear()
                    for i in range(7):
                        intentos = 0
                        while intentos < 100:
                            x = random.randint(mapa.rect.left + 50, mapa.rect.right - 50)
                            y = random.randint(mapa.rect.top + 50, mapa.rect.bottom - 50)
                            enemigo = Vigilante(x, y)
                            if not mapa.colisiona_pared(enemigo.rect):
                                vigilantes.append(enemigo)
                                break
                            intentos += 1
                    score = 0 
                    game_over = False
                    victoria = False
                    dinero_recolectado = 0
                    dinero_objetivo.reaparecer(mapa)

                # VOLVER AL INICIO CON TRIÁNGULO (Botón 3)
                if evento.button == 3 and (game_over or victoria):
                    pygame.mixer.music.stop()
                    corriendo = False 
                    menu_principal()

            if evento.type == pygame.KEYDOWN:# si el usuario presiona una tecla se verifica cual es la tecla presionada para tomar la accion correspondiente 

                if evento.key == pygame.K_ESCAPE:# si el usuario presiona la tecla ESC se cierra completamente el programa 
                    corriendo = False

                if evento.key == pygame.K_SPACE and not game_over and not victoria:# si el usuario presiona la tecla espacio y el juego no ha terminado, se crea una nueva bala
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

                if evento.key == pygame.K_r and (game_over or victoria):#si el usuario presina la tecla R y el juaego ha terminado se reinicia el juego, se restablecen las vidas del jugador 
                    #REINICIO COMPLETO
                    musica_perdiste_activa = False
                    musica_victoria_activa = False
                    try:
                        pygame.mixer.music.load(ruta_musica_fondo)
                        pygame.mixer.music.play(-1)
                    except: pass
                    jugador_principal.vidas = 3
                    jugador_principal.rect.x = mapa.rect.left - 100 
                    jugador_principal.rect.y = mapa.rect.centery
                    vigilantes.clear()
                    vigilantes_muertos.clear()
                    balas.clear()
                    for i in range(7):
                        intentos = 0
                        while intentos < 100:
                            x = random.randint(mapa.rect.left + 50, mapa.rect.right - 50)
                            y = random.randint(mapa.rect.top + 50, mapa.rect.bottom - 50)
                            enemigo = Vigilante(x, y)
                            if not mapa.colisiona_pared(enemigo.rect):
                                vigilantes.append(enemigo)
                                break
                            intentos += 1
                    score = 0 
                    game_over = False
                    victoria = False
                    dinero_recolectado = 0
                    dinero_objetivo.reaparecer(mapa)

            if evento.type == pygame.MOUSEBUTTONDOWN and (game_over or victoria):
                if evento.button == 1:
                    if rect_reintentar.collidepoint(evento.pos):
                        # Reinicio por clic
                        musica_perdiste_activa = False
                        musica_victoria_activa = False
                        try:
                            pygame.mixer.music.load(ruta_musica_fondo)
                            pygame.mixer.music.play(-1)
                        except: pass
                        jugador_principal.vidas = 3
                        jugador_principal.rect.x = mapa.rect.left - 100 
                        jugador_principal.rect.y = mapa.rect.centery
                        vigilantes.clear()
                        vigilantes_muertos.clear()
                        balas.clear()
                        for i in range(7): 
                            intentos = 0
                            while intentos < 100:
                                x = random.randint(mapa.rect.left + 50, mapa.rect.right - 50)
                                y = random.randint(mapa.rect.top + 50, mapa.rect.bottom - 50)
                                enemigo = Vigilante(x, y)
                                if not mapa.colisiona_pared(enemigo.rect):
                                    vigilantes.append(enemigo)
                                    break
                                intentos += 1
                        score = 0
                        game_over = False
                        victoria = False
                        dinero_recolectado = 0
                        dinero_objetivo.reaparecer(mapa)
                    
                    if rect_volver_inicio.collidepoint(evento.pos):
                        pygame.mixer.music.stop()
                        corriendo = False 
                        menu_principal()

        if not game_over and not victoria: # si el juego no ha terminado se ejecuta la logica del juego, si el juego ha terminado se detiene toda la logica y solo se muestra el mensaje de victoria o game over y la opcion de reiniciar el juego 

            teclas = pygame.key.get_pressed()
            
            #LOGICA DE MOVIMIENTO PARA CONTROL (Stick y Cruceta)
            # Se crea un diccionario similar a 'teclas' para que el metodo .mover del jugador lo entienda
            teclas_control = {
                pygame.K_LEFT: teclas[pygame.K_LEFT],
                pygame.K_RIGHT: teclas[pygame.K_RIGHT],
                pygame.K_UP: teclas[pygame.K_UP],
                pygame.K_DOWN: teclas[pygame.K_DOWN]
            }

            if control:
                # Ejes del stick izquierdo (Eje 0 horizontal, Eje 1 vertical)
                eje_x = control.get_axis(0)
                eje_y = control.get_axis(1)
                # Cruceta (Hat)
                hat = control.get_hat(0)

                if eje_x < -0.5 or hat[0] == -1: teclas_control[pygame.K_LEFT] = True
                if eje_x > 0.5 or hat[0] == 1: teclas_control[pygame.K_RIGHT] = True
                if eje_y < -0.5 or hat[1] == 1: teclas_control[pygame.K_UP] = True
                if eje_y > 0.5 or hat[1] == -1: teclas_control[pygame.K_DOWN] = True

            rect_original = jugador_principal.rect.copy()

            # Se le pasa el mapa y el estado de las teclas (combinado con control)
            jugador_principal.mover(teclas_control, mapa)

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
                    # DETENEMOS LA MUSICA Y CARGAMOS LA DE VICTORIA INMEDIATAMENTE
                    pygame.mixer.music.stop()
                    try:
                        pygame.mixer.music.load(ruta_musica_victoria)
                        pygame.mixer.music.play(-1)
                        pygame.mixer.music.set_volume(0.6)
                    except:
                        print("No se encontró: musica victoria.mp3")
                    victoria = True
                    musica_victoria_activa = True

            for vigilante in vigilantes:# Aqui se mueve cada vigilante usando su metodo mover, se le pasa el jugadr y el mapa para que se mueva inteligentemente persiguiendo al jugador y evitando las paredes, si el vigilante colisiona con una pared se devuelve a su posicion original para que no atraviese las paredes

                posicion_original = vigilante.rect.copy()

                vigilante.mover(jugador_principal, mapa)

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
                        # DETENEMOS LA MUSICA Y CARGAMOS LA DE PERDISTE
                        pygame.mixer.music.stop()
                        try:
                            pygame.mixer.music.load(ruta_musica_perdiste)
                            pygame.mixer.music.play(-1)
                        except: pass
                        game_over = True
                        musica_perdiste_activa = True

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

        texto_dinero = fuente.render(f"Dinero: {dinero_recolectado}/{dinero_necesario}", True, (0, 255, 0))
        pantalla.blit(texto_dinero, (20, 100))

        if game_over or victoria:
            # Fuentes compartidas
            f_grande = pygame.font.SysFont("Impact", 150)
            f_btn = pygame.font.SysFont("Arial", 40, bold=True)

            if victoria:
                # PORTADA DE VICTORIA 
                # Fondo especial de victoria (Verde dinero)
                pantalla.fill((0, 30, 0))

                # DIBUJAR LLUVIA DE DINERO/CONFECI
                for billete in lluvia_dinero:
                    billete[1] += billete[2] # Caen
                    if billete[1] > Alto: billete[1] = random.randint(-200, 0)
                    pygame.draw.rect(pantalla, billete[4], (billete[0], billete[1], billete[3], billete[3]//2), border_radius=3)

                # Titulo gigante "VICTORIA"
                txt_p = f_grande.render("VICTORIA", True, (255, 255, 255))
                pantalla.blit(txt_p, (Ancho//2 - 275, Alto//2 - 255))

                # Mensaje personalizado
                f_mensaje = pygame.font.SysFont("Arial", 70, bold=True)
                txt_m = f_mensaje.render("¡ERES UN DURO!", True, (255, 215, 0)) # Dorado
                pantalla.blit(txt_m, (Ancho//2 - 240, Alto//2 - 90))

                # Lógica de parpadeo compartida
                if subiendo_victoria:
                    alpha_victoria += 8
                    if alpha_victoria >= 255: subiendo_victoria = False
                else:
                    alpha_victoria -= 8
                    if alpha_victoria <= 50: subiendo_victoria = True

                #BOTONES DE VICTORIA
                col_r = (200, 0, 0) if rect_reintentar.collidepoint(pos_mouse) else (138, 0, 0)
                pygame.draw.rect(pantalla, col_r, rect_reintentar, border_radius=10)
                txt_r = f_btn.render("X PARA REINTENTAR", True, (255, 255, 255)) # Texto cambiado para control
                txt_r.set_alpha(alpha_victoria)
                pantalla.blit(txt_r, (Ancho//2 - 165, Alto//2 + 58))

                col_v = (200, 0, 0) if rect_volver_inicio.collidepoint(pos_mouse) else (138, 0, 0)
                pygame.draw.rect(pantalla, col_v, rect_volver_inicio, border_radius=10)
                txt_v = f_btn.render("TRIANGULO INICIO", True, (255, 255, 255)) # Texto cambiado para control
                txt_v.set_alpha(alpha_victoria)
                pantalla.blit(txt_v, (Ancho//2 - 150, Alto//2 + 148))

            elif game_over:
                pantalla.fill((10, 0, 0))
                for g in gotas_sangre_go:
                    g[1] += g[2]
                    if g[1] > Alto: g[1] = random.randint(-100, 0)
                    pygame.draw.rect(pantalla, (100, 0, 0), (g[0], g[1], g[3]//2, g[3]*2))
                
                txt_p = f_grande.render("PERDISTE", True, (255, 0, 0))
                pantalla.blit(txt_p, (Ancho//2 - 250, Alto//2 - 205))

                if subiendo_perdiste:
                    alpha_perdiste += 8
                    if alpha_perdiste >= 255: subiendo_perdiste = False
                else:
                    alpha_perdiste -= 8
                    if alpha_perdiste <= 50: subiendo_perdiste = True

                #BOTONES DE DERROTA 
                col_r = (200, 0, 0) if rect_reintentar.collidepoint(pos_mouse) else (138, 0, 0)
                pygame.draw.rect(pantalla, col_r, rect_reintentar, border_radius=10)
                txt_r = f_btn.render("X PARA REINTENTAR", True, (255, 255, 255))
                txt_r.set_alpha(alpha_perdiste)
                pantalla.blit(txt_r, (Ancho//2 - 165, Alto//2 + 58))

                col_v = (200, 0, 0) if rect_volver_inicio.collidepoint(pos_mouse) else (138, 0, 0)
                pygame.draw.rect(pantalla, col_v, rect_volver_inicio, border_radius=10)
                txt_v = f_btn.render("TRIANGULO INICIO", True, (255, 255, 255))
                txt_v.set_alpha(alpha_perdiste)
                pantalla.blit(txt_v, (Ancho//2 - 150, Alto//2 + 148))

        pygame.display.flip()
        # Se usa tiempo.tick porque asi se definio arriba en la funcion iniciar_juego
        tiempo.tick(60)

    pygame.quit() #si la ventana del juego es cerrada por el usuario se cierra completamente el programa
    sys.exit() # si el usuario presiona la tecla ESC se cierra completamente el programa 


if __name__ == "__main__":
    menu_principal() #este es el punto de entrada de mi juego, aqui se llama a la funcion menu_principal que muestra el menu del juego y desde ahi se puede iniciar el juego o salir completamente del programa