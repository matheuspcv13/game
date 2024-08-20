import pygame

class Arma(pygame.sprite.Sprite):
    def __init__(self, x, y, imagem):
        super().__init__()
        self.image = pygame.transform.scale(imagem, (30, 10))  # Ajuste o tamanho conforme necessário
        self.rect = self.image.get_rect(topleft=(x, y))

    def atualizar(self):
        # Adicione aqui a lógica para atualizar a arma, se necessário
        pass

    def desenhar(self, tela):
        tela.blit(self.image, self.rect)
