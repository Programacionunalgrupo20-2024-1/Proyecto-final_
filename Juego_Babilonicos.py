import pygame
import sys
import random
from Protagonista import Prota
from enemigo1 import Villano

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("God save the princess")

Black = (0,0,0)
White= (255,255,255)
Green= (0,255,0)
Blue=(0,0,255)

pygame.mixer.music.load("sonido/Zoltraak.mp3")
pygame.mixer.music.play(-1)

running= True
Prota= Prota(100,250)
enemigo1= Villano(420,50)
clock = pygame.time.Clock()
musica_reproduciendo=False
musica_inicia= False
rectangulos_visibles= True
rectangulos_visibles1= False
points_visibles= False
Color_Cambia= False
font= pygame.font.Font(None,32)

# variables para el piedra, papel o tijeras
Cpiedra=pygame.image.load("sprites/piedra-beta.png")
piedra= pygame.transform.scale(Cpiedra,(200,150))
Ctijera=pygame.image.load("sprites/tijera-beta.png")
tijera= pygame.transform.scale(Ctijera,(200,150))
Cpapel=pygame.image.load("sprites/papel-beta.png")
papel= pygame.transform.scale(Cpapel,(200,150))
#variables para el tiempo de las imagenes en pantalla
mostrar_piedra=False
piedra_en_pantalla=0
mostrar_papel=False
papel_en_pantalla=0
mostrar_tijera=False
tijera_en_pantalla=0

# Variables para el botón de regreso
button_color = (200, 0, 0)
button_position_left = (50, 50)   # Posición para la mayoría de las pantallas (esquina superior izquierda)
button_position_right = (750, 50) # Posición para la pantalla de música (esquina superior derecha)
button_radius = 30


def draw_return_button(position):
    """Dibuja un botón de regreso en la pantalla en la posición especificada."""
    pygame.draw.circle(screen, button_color, position, button_radius)
    arrow_color = White
    arrow_points = [
        (position[0] - 10, position[1]),  # Punta de la flecha
        (position[0] + 10, position[1] - 10),  # Parte superior de la base de la flecha
        (position[0] + 10, position[1] + 10)   # Parte inferior de la base de la flecha
    ]
    pygame.draw.polygon(screen, arrow_color, arrow_points)



while running:
    if Color_Cambia:
        screen.fill("blue")
        screen.blit(Music_text, (20, 20))
    else:
        screen.fill(White if rectangulos_visibles else "red" if points_visibles else Green)
    
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
                if rectangulo1.collidepoint(event.pos):
                    rectangulos_visibles = False
                    points_visibles = True
                elif rectangulo3.collidepoint(event.pos):
                    running = False
                elif rectangulo2.collidepoint(event.pos):
                    Color_Cambia = True
                    rectangulos_visibles = False
            elif points_visibles:
                if point1.collidepoint(event.pos):
                    points_visibles = False
                    rectangulos_visibles1 = True
                elif (mouse_x - button_position_left[0])**2 + (mouse_y - button_position_left[1])**2 <= button_radius**2:
                    rectangulos_visibles = True
                    points_visibles = False
            elif rectangulos_visibles1:
                if rectangulo3.collidepoint(event.pos):
                    mostrar_piedra = True
                    piedra_en_pantalla = pygame.time.get_ticks()
                elif rectangulo2.collidepoint(event.pos):
                    mostrar_papel = True
                    papel_en_pantalla = pygame.time.get_ticks()
                elif rectangulo1.collidepoint(event.pos):
                    mostrar_tijera = True
                    tijera_en_pantalla = pygame.time.get_ticks()
                elif (mouse_x - button_position_left[0])**2 + (mouse_y - button_position_left[1])**2 <= button_radius**2:
                    points_visibles = True
                    rectangulos_visibles1 = False
            elif Color_Cambia:
                if (mouse_x - button_position_right[0])**2 + (mouse_y - button_position_right[1])**2 <= button_radius**2:
                    Color_Cambia = False
                    rectangulos_visibles = True

    if rectangulos_visibles:
        rectangulo3=pygame.draw.rect(screen, Black,(300,500,200,80))
        rectangulo2=pygame.draw.rect(screen, Black,(300,400,200,80))
        rectangulo1=pygame.draw.rect(screen, Black,(300,300,200,80))

    if rectangulos_visibles1:
        rectangulo4=pygame.draw.rect(screen, Blue,(0,400,800,200))
        rectangulo3=pygame.draw.rect(screen, Black,(50,450,200,80))
        rectangulo2=pygame.draw.rect(screen, Black,(300,450,200,80))
        rectangulo1=pygame.draw.rect(screen, Black,(550,450,200,80))
        Prota.dibujar(screen)
        enemigo1.dibujar(screen)
        draw_return_button(button_position_left)
    
    if points_visibles:
        point1= pygame.draw.circle(screen, "purple", (150,150), 25)
        point2= pygame.draw.circle(screen, "purple", (400,450), 25)
        point3= pygame.draw.circle(screen, "purple", (650,150), 25)
        draw_return_button(button_position_left)
    
    if mostrar_piedra:
        screen.blit(piedra, (300, 300))
        if pygame.time.get_ticks() - piedra_en_pantalla>500:
            mostrar_piedra=False
    if mostrar_papel:
        screen.blit(papel, (300, 300))
        if pygame.time.get_ticks() - papel_en_pantalla>500:
            mostrar_papel=False
    if mostrar_tijera:
        screen.blit(tijera, (300, 300))
        if pygame.time.get_ticks() - tijera_en_pantalla>500:
            mostrar_tijera=False
    

    Music_text= font.render("Musica",True, Black)

     # Dibujar el botón de regreso
    

    if Color_Cambia:
        draw_return_button(button_position_right)
    

    pygame.display.flip()
    clock.tick(40)

pygame.QUIT()
sys.exit()

