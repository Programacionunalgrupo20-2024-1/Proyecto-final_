import pygame
import sys
import random
from Protagonista import Prota

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("God save the princess")

# Definición de colores
Black = (0, 0, 0)
White = (255, 255, 255)
Green = (0, 255, 0)
Blue = (0, 0, 255)

pygame.mixer.music.load("sonido/Zoltraak.mp3")
pygame.mixer.music.play(-1)

# Variables de control
running = True
Prota = Prota(100, 250)
clock = pygame.time.Clock()
musica_reproduciendo = False
musica_inicia = False
rectangulos_visibles = True
rectangulos_visibles1 = False
points_visibles = False
Color_Cambia = False
font = pygame.font.Font(None, 32)

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
    # Configuración del color de fondo de la pantalla
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
                if rectangulo3.collidepoint(event.pos):
                    running = False
                if rectangulo2.collidepoint(event.pos):
                    Color_Cambia = True
                    rectangulos_visibles = False
            elif points_visibles:
                if point1.collidepoint(event.pos):
                    points_visibles = False
                    rectangulos_visibles1 = True
                # Verificar si se hizo clic dentro del área del botón "Regreso"
                elif (mouse_x - button_position_left[0])**2 + (mouse_y - button_position_left[1])**2 <= button_radius**2:
                    rectangulos_visibles = True
                    points_visibles = False
            elif rectangulos_visibles1:
                # Verificar si se hizo clic dentro del área del botón "Regreso"
                if (mouse_x - button_position_left[0])**2 + (mouse_y - button_position_left[1])**2 <= button_radius**2:
                    points_visibles = True
                    rectangulos_visibles1 = False
            elif Color_Cambia:
                # Botón de regreso desde la pantalla de música
                if (mouse_x - button_position_right[0])**2 + (mouse_y - button_position_right[1])**2 <= button_radius**2:
                    Color_Cambia = False
                    rectangulos_visibles = True

    # Dibujar elementos del juego
    if rectangulos_visibles:
        rectangulo3 = pygame.draw.rect(screen, Black, (300, 500, 200, 80))
        rectangulo2 = pygame.draw.rect(screen, Black, (300, 400, 200, 80))
        rectangulo1 = pygame.draw.rect(screen, Black, (300, 300, 200, 80))

    if rectangulos_visibles1:
        rectangulo4 = pygame.draw.rect(screen, Blue, (0, 400, 800, 200))
        rectangulo3 = pygame.draw.rect(screen, Black, (50, 450, 200, 80))
        rectangulo2 = pygame.draw.rect(screen, Black, (300, 450, 200, 80))
        rectangulo1 = pygame.draw.rect(screen, Black, (550, 450, 200, 80))
        Prota.dibujar(screen)
        # Dibujar el botón de regreso en la pantalla de nivel
        draw_return_button(button_position_left)

    if points_visibles:
        point1 = pygame.draw.circle(screen, "purple", (150, 150), 25)
        point2 = pygame.draw.circle(screen, "purple", (400, 450), 25)
        point3 = pygame.draw.circle(screen, "purple", (650, 150), 25)
        # Dibujar el botón de regreso en la selección de niveles
        draw_return_button(button_position_left)

    if Color_Cambia:
        # Dibujar el botón de regreso en la pantalla de música (esquina superior derecha)
        draw_return_button(button_position_right)

    Music_text = font.render("Musica", True, Black)

    pygame.display.flip()
    clock.tick(40)

pygame.quit()
sys.exit()
