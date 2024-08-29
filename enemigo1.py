import pygame

class Villano:
    def __init__(self,x,y):
        self.x =x 
        self.y= y
        self.alto = 200
        self.ancho=100
        self.Cargar = pygame.image.load("sprites/B_caballero_oscuro.png")
        self.imagen=pygame.transform.scale(self.Cargar,(self.alto,self.ancho))
        self.vida=100
        self.daño=20
        self.critico=30
    
    def dibujar(self,screen):
        screen.blit(self.imagen,(self.x,self.y))