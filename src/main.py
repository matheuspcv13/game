# jogo TAC
import pygame 
import sys
from personagens import Personagem
from utilidades import carregar_imagem
from database import Database

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

# Função para exibir a tela de nome do vencedor
def tela_nome_vencedor():
    nome = ""
    fonte = pygame.font.Font(None, 74)
    input_box = pygame.Rect(LARGURA_TELA // 2 - 100, ALTURA_TELA // 2, 200, 50)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and nome:
                    db.salvar_vencedor(nome)
                    return
                elif evento.key == pygame.K_BACKSPACE:
                    nome = nome[:-1]
                else:
                    nome += evento.unicode

        # Atualizar tela
        tela.fill(PRETO)
        txt_surface = fonte.render(nome, True, BRANCO)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        tela.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(tela, BRANCO, input_box, 2)

        # Mensagem
        msg_surface = fonte.render("Digite seu nome:", True, BRANCO)
        tela.blit(msg_surface, (LARGURA_TELA // 2 - 100, ALTURA_TELA // 2 - 50))

        pygame.display.flip()
        relogio.tick(FPS)

# Função para mostrar a tela de Game Over
def mostrar_game_over(screen, vencedor):
    fonte = pygame.font.Font(None, 74)
    texto_game_over = fonte.render("GAME OVER", True, BRANCO)
    texto_vencedor = fonte.render(f"Vencedor: {vencedor}", True, BRANCO)
    texto_rect = texto_game_over.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 - 40))
    vencedor_rect = texto_vencedor.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 + 40))

    screen.blit(texto_game_over, texto_rect)
    screen.blit(texto_vencedor, vencedor_rect)
    pygame.display.flip()
    pygame.time.wait(2000)  # Espera 2 segundos antes de chamar a tela de nome

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

def jogo(db):

    db.select_nomes()
    executar = True
    todos_sprites = pygame.sprite.Group()
    personagens = pygame.sprite.Group()

    # Inicializar personagens
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
        jogador1.mover(keys, '1')
        jogador2.mover(keys, '2')

        # Atualizar personagens (gravidade e limites da tela)
        jogador1.update(ALTURA_TELA)
        jogador2.update(ALTURA_TELA)

        # Detectar colisão usando máscaras
        if pygame.sprite.collide_mask(jogador1, jogador2):
            print("Colisão com máscara detectada!")  # Debug de console
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

        # Debug visual: desenhar retângulos de colisão e contornos das máscaras
        for personagem in personagens:
            # Desenhar o retângulo da imagem
            pygame.draw.rect(tela, (0, 255, 0), personagem.rect, 1)  # Verde para o rect da imagem

            # Desenhar o contorno da máscara
            if personagem.mask:
                offset = (personagem.rect.left, personagem.rect.top)
                for point in personagem.mask.outline():
                    pygame.draw.circle(tela, (255, 0, 0), (point[0] + offset[0], point[1] + offset[1]), 1)  # Pontos da máscara em vermelho

        draw_life_bar(tela, 50, 20, jogador1.vida)
        draw_life_bar(tela, LARGURA_TELA - 250, 20, jogador2.vida)

        # Verificar se algum jogador perdeu
        if jogador1.vida <= 0:
            print("Jogador 1 perdeu!")
            mostrar_game_over(tela, "Jogador 2")
            tela_nome_vencedor()  # Chama a tela para digitar o nome
            executar = False

        if jogador2.vida <= 0:
            print("Jogador 2 perdeu!")
            mostrar_game_over(tela, "Jogador 1")
            tela_nome_vencedor()
            executar = False

        # Atualizar a tela
        pygame.display.flip()
        
        # Manter a taxa de quadros
        relogio.tick(FPS)

if __name__ == "__main__":
    db = Database()
    try:
        jogo(db)
    finally:
        # Fechar conexão com o banco de dados ao final do jogo
        db.fechar_conexao()
