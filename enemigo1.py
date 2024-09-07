import pygame

class Villano:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.Cargar = pygame.image.load("sprites/B_caballero_oscuro.png")
        self.altura_deseada = 300  # Aumentado de 100 a 150
        self.ajustar_imagen()
        self.vida = 100
        self.daño = 20
        self.critico = 30

    def ajustar_imagen(self):
        proporcion = self.altura_deseada / self.Cargar.get_height()
        nuevo_ancho = int(self.Cargar.get_width() * proporcion)
        self.imagen = pygame.transform.scale(self.Cargar, (nuevo_ancho, self.altura_deseada))
        self.ancho, self.alto = self.imagen.get_size()

    def dibujar(self, screen):
        screen.blit(self.imagen, (self.x, self.y))

    def dibujar_barra_vida(self, screen, font):
        barra_vida_ancho = 100  # Ancho de la barra
        barra_vida_alto = 10  # Alto de la barra
        color_borde = (0, 0, 0)  # Negro para el borde
        color_vida = (255, 0, 0)  # Rojo para la vida
        
        # Dibujar borde de la barra de vida
        pygame.draw.rect(screen, color_borde, (self.x, self.y - 20, barra_vida_ancho + 2, barra_vida_alto + 2))
        
        # Calcular el porcentaje de vida restante
        vida_porcentaje = self.vida / 100  # Suponiendo que la vida máxima es 100
        
        # Dibujar la parte llena de la barra de vida
        pygame.draw.rect(screen, color_vida, (self.x + 1, self.y - 19, int(barra_vida_ancho * vida_porcentaje), barra_vida_alto))
        
        # Dibujar la parte vacía (transparente)
        
        # Texto del porcentaje de vida (lo movemos más arriba de la barra)
        texto = font.render(f"{int(self.vida)}% HP", True, (0, 0, 0))  
        screen.blit(texto, (self.x + 1, self.y - 40))  # Mueve el texto más arriba (a -40 en lugar de -30)
