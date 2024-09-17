import pygame, random
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

# Configuração da Tela
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Mostrar Personagem")

# Relógio para controlar a taxa de quadros
relogio = pygame.time.Clock()

# Carregar imagem do personagem
imagem_personagem = carregar_imagem('assets/imagens/personagem.png')
imagem_personagem2 = carregar_imagem('assets/imagens/personagem2.png')
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

# Função principal do jogo
def jogo():
    executar = True

    # Criar grupos de sprites
    todos_sprites = pygame.sprite.Group()
    personagens = pygame.sprite.Group()

    # Adicionar personagem
    jogador1 = Personagem(100, 300, 100, 155, imagem_personagem)
    personagens.add(jogador1)
    todos_sprites.add(jogador1)

    # Adicionar personagem
    jogador2 = Personagem(600, 300, 100, 155, imagem_personagem2)
    personagens.add(jogador2)
    todos_sprites.add(jogador2)

    while executar:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Atualizar
        keys = pygame.key.get_pressed()
        jogador1.mover(keys, '1')

        eys = pygame.key.get_pressed()
        jogador2.mover(keys, '2')


        if pygame.sprite.collide_rect(jogador1, jogador2):
            print("Colisão detectada!")
            # Reverter movimento para evitar sobreposição
            if jogador1.rect.colliderect(jogador2.rect):
                # Colisão pela direita do jogador1
                if jogador1.rect.right > jogador2.rect.left and jogador1.rect.left < jogador2.rect.left:
                    jogador1.rect.right = jogador2.rect.left
                # Colisão pela esquerda do jogador1
                elif jogador1.rect.left < jogador2.rect.right and jogador1.rect.right > jogador2.rect.right:
                    jogador1.rect.left = jogador2.rect.right
                # Colisão por baixo do jogador1
                elif jogador1.rect.bottom > jogador2.rect.top and jogador1.rect.top < jogador2.rect.top:
                    jogador1.rect.bottom = jogador2.rect.top
                # Colisão por cima do jogador1
                elif jogador1.rect.top < jogador2.rect.bottom and jogador1.rect.bottom > jogador2.rect.bottom:
                    jogador1.rect.top = jogador2.rect.bottom

        if pygame.sprite.collide_rect(jogador2, jogador1):
            print("Colisão 2 detectada!")
            if jogador2.rect.colliderect(jogador1.rect):
                if jogador2.rect.right > jogador1.rect.left and jogador2.rect.left < jogador1.rect.left:
                    jogador2.rect.right = jogador1.rect.left
                elif jogador2.rect.left < jogador1.rect.right and jogador2.rect.right > jogador1.rect.right:
                    jogador2.rect.left = jogador1.rect.right
                elif jogador2.rect.bottom > jogador1.rect.top and jogador2.rect.top < jogador1.rect.top:
                    jogador2.rect.bottom = jogador1.rect.top
                elif jogador2.rect.top < jogador1.rect.bottom and jogador2.rect.bottom > jogador1.rect.bottom:
                    jogador2.rect.top = jogador1.rect.bottom

        # Limpar a tela
        tela.fill(PRETO)

        # Desenhar o fundo
        tela.blit(imagem_fundo, (0, 0))

        # Desenhar todos os sprites
        todos_sprites.draw(tela)
        
        # Atualizar a tela
        pygame.display.flip()
        
        # Manter a taxa de quadros
        relogio.tick(FPS)

# Rodar o jogo
if __name__ == "__main__":
    jogo()
