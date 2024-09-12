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
        texto_avance = font2.render("AVANZASTE AL NIVEL 2 CAMPEÓN", True, Black)
        screen.blit(texto_avance, (30, 200))
        pygame.display.flip()
        pygame.time.delay(2000)
        nivel_iniciado = False
        rectangulos_visibles = True
        points_visibles = False
        rectangulos_visibles1 = False
        ronda_actual = 1
        fondo_nive2 = pygame.image.load(r"sprites\B_fondo2.png")

    if protagonista.vida <= 0 and not muerte_activada:
        tiempo_muerte = pygame.time.get_ticks()
        muerte_activada = True

    if muerte_activada:
        GameOver_text = font2.render("HAS MUERTO INUTIL", True, Black)
        screen.blit(GameOver_text, (600 // 3, 200 // 2))

        if pygame.time.get_ticks() - tiempo_muerte > 1000:
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
                elif (mouse_x - button_position_left[0])**2 + (mouse_y - button_position_left[1])**2 <= button_radius**2:
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
        pygame.draw.rect(screen,White, (0, 400, 800, 200))
        BotonPiedra = pygame.draw.circle(screen, Black, (130, 500),60)
        BotonPapel = pygame.draw.circle(screen, Black, (400, 500),60)
        Botontijera = pygame.draw.circle(screen, Black, (660, 500),60)
        
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
        Nivel_1 = pygame.draw.circle(screen, "black", (400, 500), 55)
        draw_return_button(button_position_left)

    if mostrar_piedra:
        screen.blit(piedra, (300, 300))
        if pygame.time.get_ticks() - piedra_en_pantalla > 250:
            mostrar_piedra = False
    if mostrar_papel:
        screen.blit(papel, (300, 300))
        if pygame.time.get_ticks() - papel_en_pantalla > 250:
            mostrar_papel = False
    if mostrar_tijera:
        screen.blit(tijera, (300, 300))
        if pygame.time.get_ticks() - tijera_en_pantalla > 250:
            mostrar_tijera = False
    
    # Solo se muestra el texto de la ronda si el nivel ha comenzado y no estamos en las pantallas de menú o música

    pygame.display.flip()
    clock.tick(30)
   
    if Color_Cambia:
        draw_return_button(button_position_right)

pygame.quit()
sys.exit()