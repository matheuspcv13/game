import pygame

class Personagem(pygame.sprite.Sprite):
    def __init__(self, x, y, cor, largura, altura, imagem, animações):
        super().__init__()
        self.animações = animações  # Lista de listas de animações
        self.estado_atual = 0  # Índice da animação atual (0 = idle, 1 = run, 2 = jump)
        self.frame_atual = 0
        self.frame_rate = 10
        self.contador_frames = 0
        
        self.image = pygame.transform.scale(imagem, (largura, altura))  # Redimensiona a imagem
        self.rect = self.image.get_rect(topleft=(x, y))
        self.largura = largura
        self.altura = altura

    def mover(self, teclas):
        if teclas[pygame.K_LEFT] or teclas[pygame.K_RIGHT]:
            self.estado_atual = 1  # Estado de corrida
        elif teclas[pygame.K_UP]:
            self.estado_atual = 2  # Estado de pular
        else:
            self.estado_atual = 0  # Estado de parado

        # Atualiza a animação
        self.atualizar_animacao()

    def atualizar_animacao(self):
        self.contador_frames += 1
        if self.contador_frames >= self.frame_rate:
            self.contador_frames = 0
            if self.estado_atual < len(self.animações):  # Verifica se o estado atual é válido
                frames = self.animações[self.estado_atual]
                if frames:  # Verifica se há frames para o estado atual
                    self.frame_atual = (self.frame_atual + 1) % len(frames)
                    self.image = frames[self.frame_atual]
                    self.rect = self.image.get_rect(topleft=self.rect.topleft)

    def atualizar(self):
        # Atualizar o estado do personagem
        pass
