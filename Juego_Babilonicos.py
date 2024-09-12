import pygame
import sys
import random
from Protagonista import Prota
from enemigo1 import Villano

pygame.init()
pygame.mixer.init()

pygame.display.set_caption("God save the princess")

# Colores
Black = (0, 0, 0)
White = (255, 255, 255)
Green = (0, 255, 0)
Blue = (0, 0, 255)

pygame.mixer.music.load("sonido/Zoltraak.mp3")
pygame.mixer.music.play(-1)
# Cargar y ajustar imagen de fondo
fondo_nivel1 = pygame.image.load(r"sprites\fondo_Encantado.jpg")
if not fondo_nivel1:
    print("Error al cargar la imagen de fondo")
    exit()
fondo_inicio = pygame.transform.scale(fondo_nivel1, (800, 600))

fondo_inicio= pygame.image.load(r"sprites\fondo_1.png")
if not fondo_inicio:
    print("Error al cargar la imagen de fondo")
    exit()
fondo_inicio = pygame.transform.scale(fondo_inicio, (800, 600))

screen = pygame.display.set_mode((800, 600), 0, 32)
# Crear instancias de personajes
protagonista = Prota(100, 200)
enemigo1 = Villano(400, 100)
imagen_rectangulo3 = pygame.image.load(r"sprites/star_logo.png")
imagen_rectangulo1 = pygame.image.load(r"sprites/quit_logo.png")
# Configuración del reloj
clock = pygame.time.Clock()
imagen_musica_on = pygame.image.load(r"sprites/musica_on.png")
imagen_musica_on = pygame.transform.scale(imagen_musica_on, (85, 80))
imagen_musica_off = pygame.image.load(r"sprites/musica_off.png")
imagen_musica_off = pygame.transform.scale(imagen_musica_off, (85, 80))
imagen_musica_actual = imagen_musica_on
# Cargar imágenes de los botones
imagen_piedra = pygame.image.load("sprites/piedra.jpeg")
imagen_piedra = pygame.transform.scale(imagen_piedra, (120, 170))  # Ajustar tamaño si es necesario
imagen_papel = pygame.image.load("sprites/papel.jpeg")
imagen_papel = pygame.transform.scale(imagen_papel, (120, 170))
imagen_tijera = pygame.image.load("sprites/tijera.jpeg")
imagen_tijera = pygame.transform.scale(imagen_tijera, (120, 170))

fondo_win = pygame.image.load('sprites/fondowin.jpeg')
win_img = pygame.image.load('sprites/win.png')
win_img = pygame.transform.scale(pygame.image.load('sprites/win.png'), (300, 200))
fondo_win = pygame.transform.scale(pygame.image.load('sprites/fondowin.jpeg'), (800, 600))
pergamino_image = pygame.image.load(r"sprites\B_pergamino.png")
pergamino_image = pygame.transform.scale(pergamino_image, (800, 600))
pergamino1 = pergamino_image
# Variables para el efecto de escritura
texto_mostrado = ""
indice_letra = 0
velocidad_texto = 23  # Milisegundos entre cada letra
ultimo_tiempo = pygame.time.get_ticks()
historia = "\n¡Ah, bienvenido, Caballero! \nLa reina ha sido secuestrada \npor un inmigrant... eh, \nquiero decir, por un malechor, \n¡sí, un malechor! Todos\nen el reino te necesitamos"
# Crear rectángulos de colisión para las imágenes
BotonPiedra = pygame.Rect(130 - imagen_piedra.get_width() // 2, 500 - imagen_piedra.get_height() // 2, imagen_piedra.get_width(), imagen_piedra.get_height())
BotonPapel = pygame.Rect(400 - imagen_papel.get_width() // 2, 500 - imagen_papel.get_height() // 2, imagen_papel.get_width(), imagen_papel.get_height())
Botontijera = pygame.Rect(660 - imagen_tijera.get_width() // 2, 500 - imagen_tijera.get_height() // 2, imagen_tijera.get_width(), imagen_tijera.get_height())

boton_musica_radius = 30
boton_musica_position = (730, 550)
boton_musica_color = (0, 0, 0)

# Variables de estado
running = True
musica_reproduciendo = False
musica_inicia = False
rectangulos_visibles = True
rectangulos_visibles1 = False
points_visibles = False
Color_Cambia = False
font = pygame.font.Font(None, 32)
font2 = pygame.font.Font(None, 64)
tiempo_muerte = None
mostrar_muerte = False
ronda_actual = 1
resultado_ronda = ""
texto_ronda = ""
texto_ronda_timer = 0
enemigo_eleccion = None
juego_iniciado = False
nivel_seleccionado = False
nivel_iniciado = False
muerte_activada = False
mostrar_contador_rondas = False

# Cargar imágenes para piedra, papel o tijera
Cpiedra = pygame.image.load("sprites/piedra-beta.png")
piedra = pygame.transform.scale(Cpiedra, (200, 150))
Ctijera = pygame.image.load("sprites/tijera-beta.png")
tijera = pygame.transform.scale(Ctijera, (200, 150))
Cpapel = pygame.image.load("sprites/papel-beta.png")
papel = pygame.transform.scale(Cpapel, (200, 150))
imagen_rectangulo3 = pygame.transform.scale(imagen_rectangulo3, (200, 80))
imagen_rectangulo1 = pygame.transform.scale(imagen_rectangulo1, (200, 80))

# Obtener rectángulos de las imágenes para detectar colisiones
rectangulo1 = imagen_rectangulo1.get_rect(topleft=(300, 400))
rectangulo3 = imagen_rectangulo3.get_rect(topleft=(300, 500))
# Variables para el tiempo de las imágenes en pantalla
mostrar_piedra = False
piedra_en_pantalla = 0
mostrar_papel = False
papel_en_pantalla = 0
mostrar_tijera = False
tijera_en_pantalla = 0

# Variables para el botón de regreso
button_color = (0, 0, 0)
button_position_left = (50, 50)
button_position_right = (750, 50)
button_radius = 30

def determinar_resultado(jugador_ataque, enemigo_ataque):
    if jugador_ataque == enemigo_ataque:
        return "Empate"
    elif (jugador_ataque == "piedra" and enemigo_ataque == "tijera") or \
         (jugador_ataque == "papel" and enemigo_ataque == "piedra") or \
         (jugador_ataque == "tijera" and enemigo_ataque == "papel"):
        return "Ganaste"
    else:
        return "Perdiste"

def draw_return_button(position):
    pygame.draw.circle(screen, button_color, position, button_radius)
    arrow_color = White
    arrow_points = [
        (position[0] - 10, position[1]),
        (position[0] + 10, position[1] - 10),
        (position[0] + 10, position[1] + 10)
    ]
    pygame.draw.polygon(screen, arrow_color, arrow_points)


def combate(Prota, enemigo1, seleccion_prota, seleccion_enemigo):
    global ronda_actual, resultado_ronda
    resultado = determinar_resultado(seleccion_prota, seleccion_enemigo)
    if seleccion_prota == seleccion_enemigo:
        Prota.modificar_vida(-Prota.vida * 0.10)
        enemigo1.modificar_vida(-enemigo1.vida * 0.10)
    elif (seleccion_prota == "piedra" and seleccion_enemigo == "tijera") or \
         (seleccion_prota == "papel" and seleccion_enemigo == "piedra") or \
         (seleccion_prota == "tijera" and seleccion_enemigo == "papel"):
        enemigo1.modificar_vida(-Prota.daño)
    else:
        Prota.modificar_vida(-enemigo1.daño)
    ronda_actual += 1
    resultado_ronda = resultado
    return resultado

def dibujar_texto_con_efecto(texto, posicion, color, velocidad):
    global texto_mostrado, indice_letra, ultimo_tiempo
    ahora = pygame.time.get_ticks()

    if indice_letra < len(texto) and ahora - ultimo_tiempo >= velocidad:
        texto_mostrado += texto[indice_letra]
        indice_letra += 1
        ultimo_tiempo = ahora
    
    # Renderizar y dividir el texto en líneas
    for i, linea in enumerate(texto_mostrado.split('\n')):
        texto_renderizado = font.render(linea, True, color)
        screen.blit(texto_renderizado, (posicion[0], posicion[1] + i * 40))  # Espaciado entre líneas
def mostrar_victoria(screen):
    # Mostrar las imágenes
    screen.blit(fondo_win, (0, 0))
    screen.blit(win_img, (0, 0)) 
    pygame.display.flip()
    pygame.time.wait(5000) #tempo que sale 
    # Cerrar el juego después de que se desvanece el fondo
    pygame.quit()
    sys.exit()


# Bucle principal del juego
while running:
    screen.blit(fondo_inicio, (0, 0))
    if Color_Cambia:
        Music_text = font.render("Musica", True, Black)
        screen.blit(Music_text, (20, 20))
        draw_return_button(button_position_right)
    else:
        if not Color_Cambia and not rectangulos_visibles:
            if points_visibles:
                screen.fill(White)
            else:
                screen.blit(fondo_nivel1, (0, 0))
    
    if resultado_ronda == "Ganaste":
        enemigo1.vida -= 25
    elif resultado_ronda == "Perdiste":
        protagonista.vida -= 25
    elif resultado_ronda == "Empate":
        protagonista.vida -= 10
        enemigo1.vida -= 10

    if enemigo1.vida <= 0:
            mostrar_victoria(screen)

    if protagonista.vida <= 0 and not muerte_activada:
        tiempo_muerte = pygame.time.get_ticks()
        muerte_activada = True

    if muerte_activada:
        # Renderizar el texto con un color de fondo blanco y un color de borde negro
        GameOver_text = font2.render("HAS MUERTO INUTIL", True, White, Black)
        screen.blit(GameOver_text, (90, 100))
        if pygame.time.get_ticks() - tiempo_muerte > 2000:
            muerte_activada = False
            rectangulos_visibles = True
            nivel_iniciado = False
            points_visibles = False
            rectangulos_visibles1 = False
            ronda_actual = 1
            resultado_ronda = ""
            enemigo_eleccion = None

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                if musica_reproduciendo:
                    pygame.mixer.music.pause()
                    musica_reproduciendo = False
                else:
                    pygame.mixer.music.unpause()
                    musica_reproduciendo = True
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if rectangulos_visibles:
                if (mouse_x - boton_musica_position[0])**2 + (mouse_y - boton_musica_position[1])**2 <= boton_musica_radius**2:
                    if musica_reproduciendo:
                        pygame.mixer.music.pause()
                        musica_reproduciendo = False
                        imagen_musica_actual = imagen_musica_off
                    else:
                        pygame.mixer.music.unpause()
                        musica_reproduciendo = True
                        imagen_musica_actual = imagen_musica_on
                if rectangulo1.collidepoint(event.pos):
                    nivel_iniciado = True
                    rectangulos_visibles = False
                    points_visibles = True
                    ronda_actual = 1
                    resultado_ronda = ""
                    enemigo_eleccion = None
                elif rectangulo3.collidepoint(event.pos):
                    running = False
            elif points_visibles:
                if Nivel_1.collidepoint(event.pos):
                    points_visibles = False
                    rectangulos_visibles1 = True
                elif (mouse_x - button_position_left[0])**2 + (mouse_y - button_position_left[1])**1 <= button_radius**2:
                    rectangulos_visibles = True
                    points_visibles = False
            
            elif rectangulos_visibles1:
                if BotonPiedra.collidepoint(event.pos):
                    seleccion_prota = "piedra"
                    seleccion_enemigo = random.choice(["piedra", "papel", "tijera"])
                    mostrar_piedra = True
                    piedra_en_pantalla = pygame.time.get_ticks()
                    combate(protagonista, enemigo1, seleccion_prota, seleccion_enemigo)
                    mostrar_contador_rondas = True
                elif BotonPapel.collidepoint(event.pos):
                    seleccion_prota = "papel"
                    seleccion_enemigo = random.choice(["piedra", "papel", "tijera"])
                    mostrar_papel = True
                    papel_en_pantalla = pygame.time.get_ticks()
                    combate(protagonista, enemigo1, seleccion_prota, seleccion_enemigo)
                    mostrar_contador_rondas = True
                elif Botontijera.collidepoint(event.pos):
                    seleccion_prota = "tijera"
                    seleccion_enemigo = random.choice(["piedra", "papel", "tijera"])  
                    mostrar_tijera = True
                    tijera_en_pantalla = pygame.time.get_ticks()
                    combate(protagonista, enemigo1, seleccion_prota, seleccion_enemigo)
                    mostrar_contador_rondas = True
                elif (mouse_x - button_position_left[0])**2 + (mouse_y - button_position_left[1])**2 <= button_radius**2:
                    points_visibles = True
                    rectangulos_visibles1 = False
                    mostrar_contador_rondas = False
            elif Color_Cambia:
                if (mouse_x - button_position_right[0])**2 + (mouse_y - button_position_right[1])**2 <= button_radius**2:
                    Color_Cambia = False
                    rectangulos_visibles = True
            if Color_Cambia:
                if (mouse_x - button_position_right[0])**2 + (mouse_y - button_position_right[1])**2 <= button_radius**2:
                    Color_Cambia = False
                    rectangulos_visibles = True
    if not nivel_iniciado:
        nivel_iniciado = True
        ronda_actual = 1
        protagonista.vida = 100
        enemigo1.vida = 100
        resultado_ronda = ""
        enemigo_eleccion = None
    # Solo se muestra el texto de la ronda si el nivel ha comenzado y no estamos en las pantallas de menú o música
    if resultado_ronda != "":
        pygame.time.delay(200)
        resultado_ronda = ""
        enemigo_eleccion = None
    if rectangulos_visibles:
        screen.blit(imagen_rectangulo1, (300, 500))
        screen.blit(imagen_rectangulo3, (300, 400))
        pygame.draw.circle(screen, boton_musica_color, boton_musica_position, boton_musica_radius)
        screen.blit(imagen_musica_actual, (boton_musica_position[0] - imagen_musica_on.get_width() // 2, boton_musica_position[1] - imagen_musica_on.get_height() // 2))
    if rectangulos_visibles1:
        pygame.draw.rect(screen, White, (0, 400, 800, 200))  # Fondo para los botones
        
        # Dibujar imágenes de los botones
        screen.blit(imagen_piedra, (130 - imagen_piedra.get_width() // 2, 500 - imagen_piedra.get_height() // 2))
        screen.blit(imagen_papel, (400 - imagen_papel.get_width() // 2, 500 - imagen_papel.get_height() // 2))
        screen.blit(imagen_tijera, (660 - imagen_tijera.get_width() // 2, 500 - imagen_tijera.get_height() // 2))
        
        protagonista.dibujar(screen)
        protagonista.dibujar_barra_vida(screen, font)
        enemigo1.dibujar(screen)
        enemigo1.dibujar_barra_vida(screen, font)
        draw_return_button(button_position_left)
    
    if mostrar_contador_rondas:
        ronda_text = font.render(f"Ronda {ronda_actual}", True, Black)
        screen.blit(ronda_text, (700, 20))
        resultado_text = font.render(resultado_ronda, True, Black)
        screen.blit(resultado_text, (350, 20))      

    if points_visibles:
        screen.blit(pergamino_image, (0, 0))  # Draw the pergamino image as the background
        Nivel_1 = pygame.draw.circle(screen, "black", (405, 500), 55)
        draw_return_button(button_position_left)
        iniciar_text = font.render("Iniciar", True, White)
        screen.blit(iniciar_text, (372, 490))
        # Llamar a la función para dibujar el texto con efecto
        dibujar_texto_con_efecto(historia, (260, 165), Black, velocidad_texto)

    if mostrar_piedra:
        screen.blit(piedra, (300, 300))
        if pygame.time.get_ticks() - piedra_en_pantalla > 350:
            mostrar_piedra = False
    if mostrar_papel:
        screen.blit(papel, (300, 300))
        if pygame.time.get_ticks() - papel_en_pantalla > 350:
            mostrar_papel = False
    if mostrar_tijera:
        screen.blit(tijera, (300, 300))
        if pygame.time.get_ticks() - tijera_en_pantalla > 350:
            mostrar_tijera = False
    
    # Solo se muestra el texto de la ronda si el nivel ha comenzado y no estamos en las pantallas de menú o música

    pygame.display.flip()
    clock.tick(30)
   
    if Color_Cambia:
        draw_return_button(button_position_right)

pygame.quit()
sys.exit()