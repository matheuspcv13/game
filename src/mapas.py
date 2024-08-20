import pygame

class Mapa (pygame.sprite.Sprite):
    def __init__(self, imagem):
        super().__init__()
        self.image = imagem
        self.rect = self.image.get_rect(topleft=(0, 0))

    def desenhar(self, tela):
        tela.blit(self.image, self.rect)
