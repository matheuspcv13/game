import pygame
import sys
from personagens import Personagem
from armas import Arma
from mapas import Mapa
from utilidades import carregar_imagem, carregar_som

# Inicialização do Pygame
pygame.init()

# Configurações da Tela
LARGURA_TELA = 800
ALTURA_TELA = 600
FPS = 60

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

# Configuração da Tela
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Jogo de Plataforma 2D")

# Relógio para controlar a taxa de quadros
relogio = pygame.time.Clock()

# Carregar recursos
imagem_fundo = carregar_imagem('assets/imagens/fundo.png')  # Imagem de fundo

# Carregar imagens e animações para o primeiro personagem
imagem_personagem = carregar_imagem('assets/imagens/personagem.png')
imagem_idle = carregar_imagem('assets/imagens/idle.png')
imagem_jump = carregar_imagem('assets/imagens/jump.png')
imagem_run = carregar_imagem('assets/imagens/run.png')

# Carregar imagens e animações para o segundo personagem
imagem_personagem2 = carregar_imagem('assets/imagens/personagem2.png')
imagem_idle2 = carregar_imagem('assets/imagens/idle2.png')
imagem_jump2 = carregar_imagem('assets/imagens/jump2.png')
imagem_run2 = carregar_imagem('assets/imagens/run2.png')

# Redimensionar a imagem de fundo para caber na tela
if imagem_fundo is not None:
    imagem_fundo = pygame.transform.scale(imagem_fundo, (LARGURA_TELA, ALTURA_TELA))
else:
    print("Erro ao carregar a imagem de fundo.")

# Função principal do jogo
def jogo():
    fonte = pygame.font.Font(None, 36)
    executar = True

    # Criar grupos de sprites
    todos_sprites = pygame.sprite.Group()
    personagens = pygame.sprite.Group()
    armas = pygame.sprite.Group()

    # Adicionar personagens
    animações_jogador1 = [
        [imagem_idle],  # Idle
        [imagem_run],   # Run
        [imagem_jump]   # Jump
    ]
    jogador1 = Personagem(100, 100, (255, 0, 0), 100, 100, imagem_personagem, animações_jogador1)

    animações_jogador2 = [
        [imagem_idle2],  # Idle
        [imagem_run2],   # Run
        [imagem_jump2]   # Jump
    ]
    jogador2 = Personagem(300, 100, (0, 0, 255), 100, 100, imagem_personagem2, animações_jogador2)

    personagens.add(jogador1, jogador2)
    todos_sprites.add(jogador1, jogador2)

    # Adicionar armas
    # espada = Arma(200, 200, imagem_arma)
    # armas.add(espada)
    # todos_sprites.add(espada)

    while executar:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Atualizar
        keys = pygame.key.get_pressed()
        jogador1.mover(keys)
        jogador2.mover(keys)

        # Atualizar armas
        for arma in armas:
            arma.atualizar()

        # Limpar a tela
        tela.fill(PRETO)  # Opcional, pode ser removido se usar fundo

        # Desenhar o fundo
        if imagem_fundo is not None:
            tela.blit(imagem_fundo, (0, 0))  # Desenha a imagem de fundo no canto superior esquerdo

        # Desenhar todos os sprites
        todos_sprites.draw(tela)
        
        # Desenhar texto
        desenhar_texto("Bem-vindo ao Jogo!", fonte, BRANCO, tela, LARGURA_TELA // 2, ALTURA_TELA // 2)
        
        # Atualizar a tela
        pygame.display.flip()
        
        # Manter a taxa de quadros
        relogio.tick(FPS)

# Função para desenhar o texto na tela
def desenhar_texto(texto, fonte, cor, superficie, x, y):
    texto_surface = fonte.render(texto, True, cor)
    texto_rect = texto_surface.get_rect()
    texto_rect.center = (x, y)
    superficie.blit(texto_surface, texto_rect)

# Rodar o jogo
if __name__ == "__main__":
    jogo()
