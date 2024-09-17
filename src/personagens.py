import pygame

class Personagem(pygame.sprite.Sprite):
    def __init__(self, x, y, largura, altura, imagem, imagens_ataque, imagens_ataque2):
        super().__init__()
        self.imagem_padrao = pygame.transform.scale(imagem, (largura, altura))
        self.image = self.imagem_padrao
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.velocidade = 5
        self.estado_atual = 0
        
        self.mask = pygame.mask.from_surface(self.image)  # Cria a máscara a partir da imagem
        
        self.imagens_ataque = [pygame.transform.scale(img, (largura, altura)) for img in imagens_ataque]
        self.index_ataque = 0
        self.atacando = False
        
        self.imagens_ataque2 = [pygame.transform.scale(img, (largura, altura)) for img in imagens_ataque2]
        self.index_ataque2 = 0
        self.atacando2 = False

    def mover(self, teclas, parametro):
        if parametro == "1":
            if teclas[pygame.K_a]:
                self.rect.x -= self.velocidade
                self.estado_atual = 1 
            if teclas[pygame.K_d]:
                self.rect.x += self.velocidade
                self.estado_atual = 1 
            if teclas[pygame.K_w]:
                self.rect.y -= self.velocidade
                self.estado_atual = 1 
            if teclas[pygame.K_s]:
                self.estado_atual = 1  
                self.rect.y += self.velocidade
            if teclas[pygame.K_SPACE]:
                self.atacando = True
                self.index_ataque = 0
            if teclas[pygame.K_m]:
                self.atacando2 = True
                self.index_ataque = 0
        else:
            if teclas[pygame.K_LEFT]:
                self.rect.x -= self.velocidade
                self.estado_atual = 1  
            if teclas[pygame.K_RIGHT]:
                self.rect.x += self.velocidade
                self.estado_atual = 1 
            if teclas[pygame.K_UP]:
                self.rect.y -= self.velocidade
                self.estado_atual = 1 
            if teclas[pygame.K_DOWN]:
                self.estado_atual = 1
                self.rect.y += self.velocidade
            if teclas[pygame.K_END]:
                self.atacando = True
                self.index_ataque = 0
            if teclas[pygame.K_DELETE]:
                self.atacando2 = True
                self.index_ataque = 0

    def atacar(self):
        if self.atacando:
            self.image = self.imagens_ataque[self.index_ataque]
            self.index_ataque = (self.index_ataque + 1) % len(self.imagens_ataque)
            if self.index_ataque == 0:
                self.atacando = False
                self.image = self.imagem_padrao
    
    def atacar2(self):
        if self.atacando2:
            self.image = self.imagens_ataque2[self.index_ataque2]
            self.index_ataque2 = (self.index_ataque2 + 1) % len(self.imagens_ataque2)
            if self.index_ataque2 == 0:
                self.atacando2 = False
                self.image = self.imagem_padrao
    
    def verificar_colisao(self, outro):
        if self.rect.colliderect(outro.rect):
            if self.rect.right > outro.rect.left and self.rect.left < outro.rect.left:
                self.rect.right = outro.rect.left
            elif self.rect.left < outro.rect.right and self.rect.right > outro.rect.right:
                self.rect.left = outro.rect.right
            if self.rect.bottom > outro.rect.top and self.rect.top < outro.rect.top:
                self.rect.bottom = outro.rect.top
            elif self.rect.top < outro.rect.bottom and self.rect.bottom > outro.rect.bottom:
                self.rect.top = outro.rect.bottom

        # Impede o personagem de sair da tela 
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > pygame.display.get_surface().get_width():
            self.rect.right = pygame.display.get_surface().get_width()
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > pygame.display.get_surface().get_height():
            self.rect.bottom = pygame.display.get_surface().get_height()

            

