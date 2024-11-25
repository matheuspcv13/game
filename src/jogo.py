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

def jogo(db, mult = False, jogador2_mult = False):
    # Variáveis de controle para piscar
    piscar_jogador1 = False
    piscar_jogador2 = False
    tempo_piscar_jogador1 = 0
    tempo_piscar_jogador2 = 0
    duracao_piscar = 500  # Duração do efeito em milissegundos

    db.select_nomes()
    executar = True
    todos_sprites = pygame.sprite.Group()
    personagens = pygame.sprite.Group()

    if mult:
        # Cliente - Conectar ao servidor e receber dados para o personagem
        if jogador2_mult:
            jogador = Personagem(600, 300, 100, 155, imagem_personagem2, imagem_personagem2_ataque)
            personagens.add(jogador)
            todos_sprites.add(jogador)
        else:
            jogador = Personagem(100, 300, 100, 155, imagem_personagem, imagem_personagem_ataque)
            personagens.add(jogador)
            todos_sprites.add(jogador)

        # Inicializando o socket para o cliente
        # server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # server.bind(('127.0.0.1', 5000))
        # server.listen(1)
        # print("Aguardando conexão do cliente...")
        # client_socket, client_address = server.accept()
        # print(f"Cliente {client_address} conectado!")

        while executar:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Captura de teclas
            keys = pygame.key.get_pressed()

            jogador.mover(keys, '1', [jogador])  # Movimento do jogador 1
            jogador.update(ALTURA_TELA, [jogador])

            # Limpar a tela
            tela.fill(PRETO)

            # Desenhar o fundo
            tela.blit(imagem_fundo, (0, 0))

            # Desenhar ambos os jogadores
            for personagem in personagens:
                if personagem.visivel:
                    tela.blit(personagem.image, personagem.rect.topleft)

            # Atualizar a tela
            pygame.display.flip()

            # Manter a taxa de quadros
            relogio.tick(FPS)

    else:

        jogador1 = Personagem(100, 300, 100, 155, imagem_personagem, imagem_personagem_ataque)
        jogador2 = Personagem(600, 300, 100, 155, imagem_personagem2, imagem_personagem2_ataque)
        personagens.add(jogador1, jogador2)
        todos_sprites.add(jogador1, jogador2)

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
                if jogador1.atacando:
                    jogador2.vida -= 10
                    jogador2.rect.x += 40  # Recuar para a direita
                    jogador2.velocity_y -= 5  # Pequeno empurrão para cima
                    piscar_jogador2 = True
                    tempo_piscar_jogador2 = pygame.time.get_ticks()
                elif jogador2.atacando:
                    jogador1.vida -= 10
                    jogador1.rect.x -= 40  # Recuar para a esquerda
                    jogador1.velocity_y -= 5  # Pequeno empurrão para cima
                    piscar_jogador1 = True
                    tempo_piscar_jogador1 = pygame.time.get_ticks()

            # Limpar a tela
            tela.fill(PRETO)

            # Desenhar o fundo
            tela.blit(imagem_fundo, (0, 0))

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

            
            for personagem in personagens:
                if personagem.visivel:  # Apenas desenha se estiver visível
                    tela.blit(personagem.image, personagem.rect.topleft)


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
