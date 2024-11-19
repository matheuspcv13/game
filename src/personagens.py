import pygame

class Personagem(pygame.sprite.Sprite):
    def __init__(self, x, y, largura, altura, imagem, imagem_ataque):
        super().__init__()

        self.ataque_disponivel = True
        self.tempo_piscar = 0  # Tempo restante para piscar (em quadros)
        self.contador_piscar = 0  # Contador para alternar visibilidade
        self.visivel = True  # Determina se o sprite está visível

        
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
        self.gravity = 0.3  # Gravidade mais baixa para queda mais lenta
        self.jump_speed = -12  # Impulso maior para pular mais alto
        self.on_ground = False
        self.vida = 100
        self.atacando = False  # Estado de ataque

    def iniciar_ataque(self):
        """Ativa o estado de ataque e altera a imagem e máscara para o ataque."""
        if not self.atacando:  # Garante que só inicia o ataque se não estiver atacando
            self.atacando = True
            self.image = self.image_ataque
            self.mask = self.mask_ataque
            self.ataque_timer = 10  # Duração do ataque em quadros (ajuste conforme necessário)
    def finalizar_ataque(self):
        """Desativa o estado de ataque e retorna a imagem e máscara para o normal."""
        self.atacando = False
        self.image = self.image_normal
        self.mask = self.mask_normal


    def mover(self, teclas, parametro, outros_personagens):
        """Controla o movimento e o estado do personagem com base nas teclas pressionadas."""
        movimento_x = 0
        movimento_y = 0

        # Movimento básico e controle de direção
        if parametro == "1":
            if teclas[pygame.K_a]:
                movimento_x -= self.velocidade
            if teclas[pygame.K_d]:
                movimento_x += self.velocidade
            if teclas[pygame.K_w] and self.on_ground:
                self.velocity_y = self.jump_speed
                self.on_ground = False

            if teclas[pygame.K_SPACE] and self.ataque_disponivel:
                self.iniciar_ataque()
        else:
            if teclas[pygame.K_LEFT]:
                movimento_x -= self.velocidade
            if teclas[pygame.K_RIGHT]:
                movimento_x += self.velocidade
            if teclas[pygame.K_UP] and self.on_ground:
                self.velocity_y = self.jump_speed
                self.on_ground = False

            if teclas[pygame.K_p] and self.ataque_disponivel:
                self.iniciar_ataque()

        # Aplica movimento no eixo X e verifica colisões
        self.rect.x += movimento_x
        for outro in outros_personagens:
            if pygame.sprite.collide_mask(self, outro):
                # Reverte movimento em caso de colisão
                self.rect.x -= movimento_x

        # Aplica movimento no eixo Y (inclui gravidade) e verifica colisões
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y
        for outro in outros_personagens:
            if pygame.sprite.collide_mask(self, outro):
                # Reverte movimento em caso de colisão no eixo Y
                self.rect.y -= self.velocity_y
                self.velocity_y = 0
                self.on_ground = True


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


    def update(self, altura_tela, outros_personagens):
        # Aplica gravidade
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        if self.rect.bottom > altura_tela:
            self.rect.bottom = altura_tela
            self.velocity_y = 0
            self.on_ground = True

        # Verifica colisões com outros personagens
        for outro in outros_personagens:
            if outro != self:  # Evita verificar colisão consigo mesmo
                self.verificar_colisao(outro)

        # Impede o personagem de sair da tela
        if self.rect.bottom > altura_tela:
            self.rect.bottom = altura_tela
            self.velocity_y = 0
            self.on_ground = True

        # Controle do piscar
        if self.tempo_piscar > 0:
            self.contador_piscar += 1
            if self.contador_piscar % 5 == 0:  # Alterna visibilidade a cada 5 quadros
                self.visivel = not self.visivel
            self.tempo_piscar -= 1
        else:
            self.visivel = True  # Garante que fica visível ao terminar de piscar

        # Controle da animação de ataque
        if self.atacando:
            if self.ataque_timer > 0:
                self.ataque_timer -= 1
            else:
                self.finalizar_ataque()



    def verificar_colisao(self, outro):
        if pygame.sprite.collide_mask(self, outro):
            # Ajusta as posições para evitar sobreposição
            if self.rect.centerx < outro.rect.centerx:
                self.rect.right = outro.rect.left
            else:
                self.rect.left = outro.rect.right

            if self.rect.bottom <= outro.rect.top + 10:  # Colisão de cima
                self.rect.bottom = outro.rect.top  # Fixa a posição no topo do outro
                self.velocity_y = 0  # Anula a velocidade vertical
                self.on_ground = True  # Considera como se estivesse no chão
            else:
                # Colisão lateral
                deslocamento = 10  # Empurrão mínimo para evitar sobreposição
                if self.rect.x < outro.rect.x:
                    self.rect.right = outro.rect.left - deslocamento
                else:
                    self.rect.left = outro.rect.right + deslocamento

            # Lógica de ataque
            if self.atacando:
                outro.vida -= 10
                outro.tempo_piscar = 30
                outro.rect.x += 40 if self.rect.x < outro.rect.x else -40
                self.rect.x -= 20 if self.rect.x < outro.rect.x else 20
                self.finalizar_ataque()

    


