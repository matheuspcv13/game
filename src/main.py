# jogo TAC
import pygame 
import sys
from personagens import Personagem
from utilidades import carregar_imagem

# Inicialização do Pygame
pygame.init()

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

# Carregar imagens do personagem e do ataque
imagem_personagem = carregar_imagem('assets/imagens/personagem.png')
imagem_personagem_ataque = carregar_imagem('assets/imagens/personagem_ataque.png')
imagem_personagem2 = carregar_imagem('assets/imagens/personagem2.png')
imagem_personagem2_ataque = carregar_imagem('assets/imagens/personagem2_ataque.png')

imagem_personagem2_ataque = pygame.transform.flip(carregar_imagem('assets/imagens/personagem2_ataque.png'), True, False)

# Carregar imagem de fundo
imagem_fundo = carregar_imagem('assets/imagens/fundo.png')
if imagem_fundo is not None:
    imagem_fundo = pygame.transform.scale(imagem_fundo, (LARGURA_TELA, ALTURA_TELA))
else:
    print("Erro ao carregar a imagem de fundo.")
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

def jogo():
    executar = True
    todos_sprites = pygame.sprite.Group()
    personagens = pygame.sprite.Group()

    jogador1 = Personagem(100, 300, 100, 155, imagem_personagem, imagem_personagem_ataque)
    jogador2 = Personagem(600, 300, 100, 155, imagem_personagem2, imagem_personagem2_ataque)
    personagens.add(jogador1, jogador2)
    todos_sprites.add(jogador1, jogador2)

    while executar:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        jogador1.mover(keys, '1')
        jogador2.mover(keys, '2')

        jogador1.update(ALTURA_TELA)
        jogador2.update(ALTURA_TELA)

        # Detectar colisão usando máscaras
        if pygame.sprite.collide_mask(jogador1, jogador2):
            if jogador1.atacando:
                jogador2.vida -= 10
                jogador1.finalizar_ataque()
            elif jogador2.atacando:
                jogador1.vida -= 10
                jogador2.finalizar_ataque()
            else:
                # Reverter posição para impedir sobreposição
                if jogador1.rect.right > jogador2.rect.left and jogador1.rect.left < jogador2.rect.left:
                    jogador1.rect.right = jogador2.rect.left
                elif jogador1.rect.left < jogador2.rect.right and jogador1.rect.right > jogador2.rect.right:
                    jogador1.rect.left = jogador2.rect.right

        # Limpar a tela
        tela.fill(PRETO)

        # Desenhar o fundo
        tela.blit(imagem_fundo, (0, 0))

        # Desenhar todos os sprites
        todos_sprites.draw(tela)
        
        # Desenhar barras de vida fixas no topo da tela
        draw_life_bar(tela, 50, 20, jogador1.vida)
        draw_life_bar(tela, LARGURA_TELA - 250, 20, jogador2.vida)

        # Atualizar a tela
        pygame.display.flip()
        
        # Manter a taxa de quadros
        relogio.tick(FPS)

if __name__ == "__main__":
    jogo()
