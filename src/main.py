import pygame
import sys
from personagens import Personagem
from utilidades import carregar_imagem, carregar_som

pygame.init()
pygame.mixer.init()

LARGURA_TELA = 800
ALTURA_TELA = 600
FPS = 60

PRETO = (0, 0, 0)

tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Mostrar Personagem")

relogio = pygame.time.Clock()

imagem_personagem = carregar_imagem('assets/imagens/personagem.png')
imagem_personagem2 = carregar_imagem('assets/imagens/personagem2.png')

imagens_ataque1 = [carregar_imagem(f'assets/imagens/Attack_1.png') for i in range(1, 6)]
imagens_ataque2 = [pygame.transform.flip(carregar_imagem(f'assets/imagens/Attack_2.png'), True, False) for i in range(1, 6)]
imagens_ataque3 = [carregar_imagem(f'assets/imagens/Attack_3.png') for i in range(1, 6)]
imagens_ataque4 = [pygame.transform.flip(carregar_imagem(f'assets/imagens/Attack_4.png'), True, False) for i in range(1, 6)]


imagem_fundo = carregar_imagem('assets/imagens/fundo.png')
if imagem_fundo is not None:
    imagem_fundo = pygame.transform.scale(imagem_fundo, (LARGURA_TELA, ALTURA_TELA))
else:
    print("Erro ao carregar a imagem de fundo.")
    pygame.quit()
    sys.exit()

caminho_do_som = "../assets/sounds/musica_fundo.mp3"
som = carregar_som(caminho_do_som)
if som:
    som.play()

chao_invisivel = pygame.Rect(0, 500, LARGURA_TELA, 100)

def jogo():
    executar = True

    todos_sprites = pygame.sprite.Group()
    personagens = pygame.sprite.Group()

    jogador1 = Personagem(100, 300, 100, 155, imagem_personagem, imagens_ataque1, imagens_ataque3)
    jogador2 = Personagem(600, 300, 100, 155, imagem_personagem2, imagens_ataque2, imagens_ataque4)
    personagens.add(jogador1, jogador2)
    todos_sprites.add(jogador1, jogador2)

    while executar:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Atualizar
        keys = pygame.key.get_pressed()
        jogador1.mover(keys, '1')
        jogador2.mover(keys, '2')
        jogador1.atacar()  
        jogador2.atacar()
        jogador1.atacar2()
        jogador2.atacar2()
        jogador1.verificar_colisao(jogador2)
        jogador2.verificar_colisao(jogador1)

        # Verificar colisão usando máscaras
        if pygame.sprite.collide_mask(jogador1, jogador2):
            print("Colisão detectada!")
        
        for personagem in personagens:
            if personagem.rect.colliderect(chao_invisivel):
                personagem.rect.y = chao_invisivel.top - personagem.rect.height

        # Desenhar
        tela.fill(PRETO)
        if imagem_fundo:
            tela.blit(imagem_fundo, (0, 0))
        todos_sprites.draw(tela)

        # Atualizar a tela
        pygame.display.flip()
        relogio.tick(FPS)

# Iniciar o jogo
jogo()
