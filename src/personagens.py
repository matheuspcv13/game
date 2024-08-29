import pygame

class Personagem(pygame.sprite.Sprite):
    def __init__(self, x, y, largura, altura, imagem):
        super().__init__()
        self.image = pygame.transform.scale(imagem, (largura, altura))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.velocidade = 5
        self.estado_atual = 0 
    
    def mover(self, teclas, parametro):
        
        if(parametro == "1"):
            if teclas[pygame.K_a]:
                self.rect.x -= self.velocidade
                self.estado_atual = 1  # Estado de corrida
            
            if teclas[pygame.K_d]:
                self.rect.x += self.velocidade
                self.estado_atual = 1  # Estado de corrida
        
            if teclas[pygame.K_w]:
                self.rect.y -= self.velocidade
                self.estado_atual = 1  # Estado de pular
            if teclas[pygame.K_s]:
                self.estado_atual = 1  # Estado de parado
                self.rect.y += self.velocidade
        else:
            if teclas[pygame.K_LEFT]:
                self.rect.x -= self.velocidade
                self.estado_atual = 1  # Estado de corrida
            
            if teclas[pygame.K_RIGHT]:
                self.rect.x += self.velocidade
                self.estado_atual = 1  # Estado de corrida
        
            if teclas[pygame.K_UP]:
                self.rect.y -= self.velocidade
                self.estado_atual = 1  # Estado de pular
            if teclas[pygame.K_DOWN]:
                self.estado_atual = 1  # Estado de parado
                self.rect.y += self.velocidade
        pass

        # Impede o personagem de sair da tela
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > pygame.display.get_surface().get_width():
            self.rect.right = pygame.display.get_surface().get_width()
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > pygame.display.get_surface().get_height():
            self.rect.bottom = pygame.display.get_surface().get_height()

            

