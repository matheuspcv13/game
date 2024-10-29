import pygame

class Personagem(pygame.sprite.Sprite):
    def __init__(self, x, y, largura, altura, imagem, imagem_ataque):
        super().__init__()
        
        # Definir imagens e máscaras
        self.image_normal = pygame.transform.scale(imagem, (largura, altura))
        self.image_ataque = pygame.transform.scale(imagem_ataque, (largura, altura))
        self.image = self.image_normal  # Inicialmente, usa a imagem normal

        # Máscaras para detecção de colisão precisa
        self.mask_normal = pygame.mask.from_surface(self.image_normal)
        self.mask_ataque = pygame.mask.from_surface(self.image_ataque)
        self.mask = self.mask_normal  # Começa com a máscara normal

        # Definir retângulo e outras propriedades
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.velocidade = 5
        self.estado_atual = 0
        self.velocity_y = 0
        self.gravity = 0.5
        self.jump_speed = -13
        self.on_ground = False
        self.vida = 100
        self.atacando = False  # Estado de ataque

    def iniciar_ataque(self):
        """Ativa o estado de ataque e altera a imagem e máscara para o ataque."""
        self.atacando = True
        self.image = self.image_ataque
        self.mask = self.mask_ataque

    def finalizar_ataque(self):
        """Desativa o estado de ataque e retorna a imagem e máscara para o normal."""
        self.atacando = False
        self.image = self.image_normal
        self.mask = self.mask_normal

    def mover(self, teclas, parametro):
        """Controla o movimento e o estado do personagem com base nas teclas pressionadas."""
        # Movimento básico e controle de direção
        if parametro == "1":
            if teclas[pygame.K_a]:
                self.rect.x -= self.velocidade
                self.estado_atual = 1  # Estado de corrida
            
            if teclas[pygame.K_d]:
                self.rect.x += self.velocidade
                self.estado_atual = 1  # Estado de corrida
        
            if teclas[pygame.K_w] and self.on_ground:
                self.velocity_y = self.jump_speed
                self.on_ground = False
                self.estado_atual = 1  # Estado de pular

            # Inicia o ataque com a tecla 'espaco'
            if teclas[pygame.K_SPACE]:
                self.iniciar_ataque()
            else:
                self.finalizar_ataque()  # Finaliza o ataque ao soltar a tecla
        else:
            if teclas[pygame.K_LEFT]:
                self.rect.x -= self.velocidade
                self.estado_atual = 1  # Estado de corrida
            
            if teclas[pygame.K_RIGHT]:
                self.rect.x += self.velocidade
                self.estado_atual = 1  # Estado de corrida
        
            if teclas[pygame.K_UP] and self.on_ground:
                self.velocity_y = self.jump_speed
                self.on_ground = False
                self.estado_atual = 1  # Estado de pular

            # Inicia o ataque com a tecla 'p'
            if teclas[pygame.K_p]:
                self.iniciar_ataque()
            else:
                self.finalizar_ataque()  # Finaliza o ataque ao soltar a tecla

        # Aplica a gravidade
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # Impede o personagem de sair da tela
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > pygame.display.get_surface().get_width():
            self.rect.right = pygame.display.get_surface().get_width()
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > pygame.display.get_surface().get_height():
            self.rect.bottom = pygame.display.get_surface().get_height()
            self.velocity_y = 0
            self.on_ground = True  # Personagem está no chão

    def verificar_colisao(self, outro):
        """Verifica a colisão com outro personagem usando máscaras."""
        if pygame.sprite.collide_mask(self, outro):
            print("Colisão com máscara detectada!")
            # Ajustar posição com base na direção da colisão
            if self.rect.right > outro.rect.left and self.rect.left < outro.rect.left:
                self.rect.right = outro.rect.left
            elif self.rect.left < outro.rect.right and self.rect.right > outro.rect.right:
                self.rect.left = outro.rect.right
            if self.rect.bottom > outro.rect.top and self.rect.top < outro.rect.top:
                self.rect.bottom = outro.rect.top
                self.velocity_y = 0  # Zera a velocidade vertical ao colidir no topo
            elif self.rect.top < outro.rect.bottom and self.rect.bottom > outro.rect.bottom:
                self.rect.top = outro.rect.bottom
