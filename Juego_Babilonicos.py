import pygame
import sys
import random
from Protagonista import Prota

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
clock = pygame.time.Clock()
musica_reproduciendo=False
musica_inicia= False
rectangulos_visibles= True
rectangulos_visibles1= False
points_visibles= False
Color_Cambia= False
font= pygame.font.Font(None,32)

while running:
    if Color_Cambia:
        screen.fill("blue")
        screen.blit(Music_text, (20,20))

    else:
        screen.fill(White if rectangulos_visibles else "red" if points_visibles else Green)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        elif event.type==pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    if musica_reproduciendo:
                        pygame.mixer.music.pause()
                        musica_reproduciendo=False
                    else:
                        pygame.mixer.music.unpause()
                        musica_reproduciendo=True
                  
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_clicked = True
            if rectangulos_visibles:
                if rectangulo1.collidepoint(event.pos):
                    rectangulos_visibles= False
                    points_visibles= True
                if rectangulo3.collidepoint(event.pos):
                    running= False
                if rectangulo2.collidepoint(event.pos):
                    Color_Cambia= True
                    rectangulos_visibles= False
            elif points_visibles:
                if point1.collidepoint(event.pos):
                    points_visibles= False
                    rectangulos_visibles1=True
                    
            
        

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
    
    if points_visibles:
        point1= pygame.draw.circle(screen, "purple", (150,150), 25)
        point2= pygame.draw.circle(screen, "purple", (400,450), 25)
        point3= pygame.draw.circle(screen, "purple", (650,150), 25)

    Music_text= font.render("Musica",True, Black)


    pygame.display.flip()
    clock.tick(40)

pygame.QUIT()
sys.exit()