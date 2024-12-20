# jogo TAC
import pygame 
import sys
from personagens import Personagem
from utilidades import carregar_imagem
from database import Database
import socket
import pickle
import pygame
import threading
import random


# Inicialização do Pygame
pygame.init()

info_tela = pygame.display.Info()

# Configurações da Tela
LARGURA_TELA = 800
ALTURA_TELA = 600
FPS = 60

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255) 
VERDE = (0, 255, 0) 
VERMELHO = (255, 0, 0)

# Configuração da Tela
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Mostrar Personagem")

# Relógio para controlar a taxa de quadros
relogio = pygame.time.Clock()

def tela_digitar_nome(screen, vencedor, db):
    fonte = pygame.font.Font(None, 50)
    input_box = pygame.Rect(LARGURA_TELA // 2 - 150, ALTURA_TELA // 2, 300, 50)
    color_inactive = pygame.Color('white')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = True
    text = ''
    txt_surface = fonte.render(text, True, color)
    screen.fill(PRETO)

    # Título
    titulo = fonte.render(f"Parabéns, {vencedor}!", True, BRANCO)
    screen.blit(titulo, (LARGURA_TELA // 2 - titulo.get_width() // 2, ALTURA_TELA // 4))

    # Texto de Instrução
    instrucao = fonte.render("", True, BRANCO)
    screen.blit(instrucao, (LARGURA_TELA // 2 - instrucao.get_width() // 2, ALTURA_TELA // 3 + 100))

    # Desenha a caixa de texto
    pygame.draw.rect(screen, color, input_box, 2)
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))

    pygame.display.flip()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(evento.pos):
                    active = True
                    color = color_active
                else:
                    active = False
                    color = color_inactive

            if evento.type == pygame.KEYDOWN:
                if active:
                    if evento.key == pygame.K_RETURN:  # Quando pressionar Enter, salva o nome
                        # Chama a função de salvar ou atualizar o vencedor
                        db.salvar_vencedor(vencedor, text)
                        return "tela_inicial"
                    elif evento.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += evento.unicode

                txt_surface = fonte.render(text, True, color)
                screen.fill(PRETO)
                screen.blit(titulo, (LARGURA_TELA // 2 - titulo.get_width() // 2, ALTURA_TELA // 4))
                screen.blit(instrucao, (LARGURA_TELA // 2 - instrucao.get_width() // 2, ALTURA_TELA // 3 + 100))
                pygame.draw.rect(screen, color, input_box, 2)
                screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))

                pygame.display.flip()

# Carregar imagens do personagem e do ataque
imagem_personagem = carregar_imagem('assets/imagens/personagem.png')
imagem_personagem_ataque = carregar_imagem('assets/imagens/personagem_ataque.png')
imagem_personagem2 = carregar_imagem('assets/imagens/personagem2.png')
imagem_personagem2_ataque = pygame.transform.flip(carregar_imagem('assets/imagens/personagem2_ataque.png'), True, False)

# Carregar imagem de fundo
imagem_fundo = carregar_imagem('assets/imagens/fundo.png')
if imagem_fundo is not None:
    imagem_fundo = pygame.transform.scale(imagem_fundo, (LARGURA_TELA, ALTURA_TELA))
else:
    pygame.quit()
    sys.exit()

pygame.mixer.music.load('../assets/sounds/musica_fundo.mp3')
pygame.mixer.music.play(loops=-1)

def draw_life_bar(screen, x, y, vida):
    largura_barra = 200
    altura_barra = 15
    fill_width = (vida / 100) * largura_barra
    border_rect = pygame.Rect(x - 2, y - 2, largura_barra + 4, altura_barra + 4)
    pygame.draw.rect(screen, PRETO, border_rect)
    fill_rect = pygame.Rect(x, y, fill_width, altura_barra)
    pygame.draw.rect(screen, VERDE if vida > 30 else VERMELHO, fill_rect)
    border_inner = pygame.Rect(x, y, largura_barra, altura_barra)
    pygame.draw.rect(screen, BRANCO, border_inner, 2)

def escutar_servidor(client):
    global jogador2_posicao, jogador2_ativo
    while True:
        try:
            # Recebe a mensagem do servidor
            mensagem = client.recv(1024).decode('utf-8')
            if mensagem:
                print(f"Mensagem recebida do servidor: {mensagem}")

                # Exemplo de mensagem que pode atualizar o estado do jogo
                if mensagem.startswith("posicao"):
                    _, pos_x, pos_y = mensagem.split(",")
                    jogador2_posicao = (int(pos_x), int(pos_y))
                    jogador2_ativo = True  # Marca que o jogador 2 está ativo

        except:
            print("Erro ao receber mensagem do servidor.")
            break

def jogo(db, mult=False, jogador2_mult=False):
    global jogador2_posicao, jogador2_ativo

    pygame.init()
    tela = pygame.display.set_mode((800, 600))
    relogio = pygame.time.Clock()
    
    jogador2_posicao = (0, 0)  # Posição inicial do jogador 2
    jogador2_ativo = False  # Flag para o jogador 2

    # Conectar ao servidor (se for multiplayer)
    if mult:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('127.0.0.1', 5000))
        print("Conectado ao servidor.")

        # Inicia o thread para escutar mensagens do servidor
        threading.Thread(target=escutar_servidor, args=(client,), daemon=True).start()

    # Lógica do personagem
        jogador = Personagem(100, 300, 100, 155, imagem_personagem, imagem_personagem_ataque)
        todos_sprites = pygame.sprite.Group(jogador)
        
        if jogador2_mult:
            jogador2 = Personagem(600, 300, 100, 155, imagem_personagem2, imagem_personagem2_ataque)
            todos_sprites.add(jogador2)
        
        # Loop principal do jogo
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Captura de teclas
            keys = pygame.key.get_pressed()

            # Mover o jogador 1
            jogador.mover(keys, '1', [jogador])  
            jogador.update(800, [jogador])

            # Atualizar o jogador 2 (caso esteja ativo)
            if jogador2_ativo:
                jogador2.update(800, [jogador2])

            # Limpar a tela
            tela.fill(PRETO)

            # Desenhar o fundo
            tela.blit(imagem_fundo, (0, 0))

            # Desenhar os jogadores
            for personagem in todos_sprites:
                if personagem.visivel:
                    tela.blit(personagem.image, personagem.rect.topleft)

            # Atualizar a tela
            pygame.display.flip()

            # Manter a taxa de quadros
            relogio.tick(60)
    else:
        piscar_jogador1 = False
        piscar_jogador2 = False
        tempo_piscar_jogador1 = 0
        tempo_piscar_jogador2 = 0
        duracao_piscar = 500  # Duração do efeito em milissegundos

        db.select_nomes()
        executar = True
        todos_sprites = pygame.sprite.Group()

        personagens = pygame.sprite.Group()
        jogador1 = Personagem(100, 300, 100, 155, imagem_personagem, imagem_personagem_ataque)
        jogador2 = Personagem(600, 300, 100, 155, imagem_personagem2, imagem_personagem2_ataque)
        personagens.add(jogador1, jogador2)
        todos_sprites.add(jogador1, jogador2)

        class Particula:
            def __init__(self, x, y, cor, duracao):
                self.x = x
                self.y = y
                self.cor = cor
                self.duracao = duracao
                self.tamanho = random.randint(2, 6)
                self.velocidade_x = random.uniform(-2, 2)
                self.velocidade_y = random.uniform(-2, 2)

            def atualizar(self):
                # Atualiza a posição da partícula
                self.x += self.velocidade_x
                self.y += self.velocidade_y
                # Reduz a duração
                self.duracao -= 1

            def desenhar(self, tela):
                # Desenha a partícula
                if self.duracao > 0:
                    pygame.draw.circle(tela, self.cor, (int(self.x), int(self.y)), self.tamanho)
                    print(f"Desenhando partícula em ({self.x}, {self.y})")

        particulas = []

    while executar:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Captura de teclas
        keys = pygame.key.get_pressed()

        # Atualizar movimentos dos personagens
        jogador1.mover(keys, '1', [jogador2])  # Passa o outro jogador como referência
        jogador2.mover(keys, '2', [jogador1])  # Passa o outro jogador como referência

        # Atualizar personagens (gravidade e limites da tela)
        jogador1.update(ALTURA_TELA, [jogador2])
        jogador2.update(ALTURA_TELA, [jogador1])

        # Verificar colisão entre os jogadores
        jogador1.verificar_colisao(jogador2)
        jogador2.verificar_colisao(jogador1)

        # Detectar colisão usando máscaras
        if pygame.sprite.collide_mask(jogador1, jogador2):
            print("Colisão detectada!")  # Verifica se a colisão está acontecendo
            if jogador1.atacando:
                print("Jogador 1 atacando jogador 2!")  # Verifica se o jogador 1 está atacando
                jogador2.vida -= 10
                jogador2.rect.x += 40
                jogador2.velocity_y -= 5
                piscar_jogador2 = True
                tempo_piscar_jogador2 = pygame.time.get_ticks()
                
                # Geração de partículas
                for _ in range(20):
                    particulas.append(Particula(jogador2.rect.centerx, jogador2.rect.centery, VERMELHO, 30))
                    print(f"Partículas criadas: {len(particulas)}")
            elif jogador2.atacando:
                print("Jogador 2 atacando jogador 1!")  # Verifica se o jogador 2 está atacando
                jogador1.vida -= 10
                jogador1.rect.x -= 40
                jogador1.velocity_y -= 5
                piscar_jogador1 = True
                tempo_piscar_jogador1 = pygame.time.get_ticks()
                
                # Geração de partículas
                for _ in range(20):
                    particulas.append(Particula(jogador1.rect.centerx, jogador1.rect.centery, VERMELHO, 100))


        # Atualizar partículas
        for particula in particulas[:]:
            particula.atualizar()
            if particula.duracao <= 0:
                particulas.remove(particula)
            print(f"Partículas ativas: {len(particulas)}")
            print(f"Atualizando partículas. Restantes: {len(particulas)}")

        # Limpar a tela
        tela.fill(PRETO)

        # Desenhar o fundo
        tela.blit(imagem_fundo, (0, 0))


        # Desenhar personagens
        for personagem in personagens:
            if personagem.visivel:  # Apenas desenha se estiver visível
                tela.blit(personagem.image, personagem.rect.topleft)

        # Controlar o piscar dos jogadores
        tempo_atual = pygame.time.get_ticks()
        if piscar_jogador1 and tempo_atual - tempo_piscar_jogador1 < duracao_piscar:
            pygame.draw.rect(tela, VERMELHO, jogador1.rect)  # Pisca em vermelho
        else:
            piscar_jogador1 = False

        if piscar_jogador2 and tempo_atual - tempo_piscar_jogador2 < duracao_piscar:
            pygame.draw.rect(tela, VERMELHO, jogador2.rect)  # Pisca em vermelho
        else:
            piscar_jogador2 = False

        draw_life_bar(tela, 50, 20, jogador1.vida)
        draw_life_bar(tela, LARGURA_TELA - 250, 20, jogador2.vida)

        # Verificar se algum jogador perdeu
        if jogador1.vida <= 0:
            resultado = tela_digitar_nome(tela, "Jogador 2", db)
            if resultado == "tela_inicial":
                return "tela_inicial"

        if jogador2.vida <= 0:
            resultado = tela_digitar_nome(tela, "Jogador 1", db)
            if resultado == "tela_inicial":
                return "tela_inicial"

        # Atualizar a tela
        pygame.display.flip()

        # Manter a taxa de quadros
        relogio.tick(FPS)
