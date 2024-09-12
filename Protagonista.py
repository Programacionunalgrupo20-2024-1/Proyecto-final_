import pygame

class Prota:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # Cargar las tres imágenes de animación
        self.sprites = [
            pygame.image.load("sprites/Beta_caballero.png"),
            pygame.image.load("sprites/caballero2.png"),
            pygame.image.load("sprites/caballero3.png")
        ]
        self.current_sprite = 0
        self.altura_deseada = 200  # Aumentado de 100 a 150, ahora 200
        self.ajustar_imagen()  # Ajustar tamaño de la imagen inicial
        self.vida = 100
        self.daño = 20
        self.critico = 30
        self.tiempo_animacion = 125  # Controla la velocidad de animación (125ms entre frames)
        self.ultimo_tiempo = pygame.time.get_ticks()  # Para el control del tiempo en la animación

    def ajustar_imagen(self):
        # Ajustar todas las imágenes al tamaño deseado
        for i in range(len(self.sprites)):
            proporcion = self.altura_deseada / self.sprites[i].get_height()
            nuevo_ancho = int(self.sprites[i].get_width() * proporcion)
            self.sprites[i] = pygame.transform.scale(self.sprites[i], (nuevo_ancho, self.altura_deseada))
        self.imagen = self.sprites[self.current_sprite]  # Imagen inicial

    def actualizar_animacion(self):
        # Verifica si ha pasado suficiente tiempo para cambiar de frame
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.ultimo_tiempo > self.tiempo_animacion:
            self.ultimo_tiempo = tiempo_actual
            # Cambiar al siguiente frame de la animación
            self.current_sprite = (self.current_sprite + 1) % len(self.sprites)
            self.imagen = self.sprites[self.current_sprite]  # Actualiza la imagen

    def dibujar(self, screen):
        # Llamar a actualizar_animacion para cambiar de sprite
        self.actualizar_animacion()
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
        
        # Texto del porcentaje de vida
        texto = font.render(f"{int(self.vida)}% HP", True, (0, 0, 0))  
        screen.blit(texto, (self.x + 1, self.y - 40))  # Mueve el texto más arriba (a -40 en lugar de -30)
    
    def modificar_vida(self, cantidad):
        self.vida += cantidad
        if self.vida < 0:
            self.vida = 0