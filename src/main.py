import pygame
import sys
from database import Database
from jogo import jogo  # Importa o jogo local
from tela_inicial import tela_inicial
from servidor import iniciar_servidor  # Importa a lógica do servidor
from cliente import cliente  # Importa a lógica do cliente
import threading

# Inicializar o Pygame
pygame.init()

# Configurações da Tela
LARGURA_TELA = 800
ALTURA_TELA = 600
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("GD Fighters")

def tela_multijogador(tela):
    """
    Mostra uma tela para o jogador escolher entre criar ou entrar em uma partida.
    """
    # Configura fontes e textos
    fonte_titulo = pygame.font.Font(None, 48)
    fonte_opcao = pygame.font.Font(None, 36)

    titulo = fonte_titulo.render("Multijogador", True, (255, 255, 255))
    opcao_criar = fonte_opcao.render("Criar Partida", True, (255, 255, 255))
    opcao_entrar = fonte_opcao.render("Entrar na Partida", True, (255, 255, 255))

    # Define retângulos para as opções
    criar_rect = opcao_criar.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 - 50))
    entrar_rect = opcao_entrar.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 + 50))

    while True:
        tela.fill((0, 0, 0))  # Limpa a tela com cor preta
        
        # Desenha os textos
        titulo_rect = titulo.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 4))
        tela.blit(titulo, titulo_rect)
        tela.blit(opcao_criar, criar_rect)
        tela.blit(opcao_entrar, entrar_rect)

        # Detecta a posição do mouse para destacar botões
        mouse_pos = pygame.mouse.get_pos()
        if criar_rect.collidepoint(mouse_pos):
            opcao_criar = fonte_opcao.render("Criar Partida", True, (0, 255, 0))  # Verde
        else:
            opcao_criar = fonte_opcao.render("Criar Partida", True, (255, 255, 255))  # Branco

        if entrar_rect.collidepoint(mouse_pos):
            opcao_entrar = fonte_opcao.render("Entrar na Partida", True, (0, 255, 0))  # Verde
        else:
            opcao_entrar = fonte_opcao.render("Entrar na Partida", True, (255, 255, 255))  # Branco

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if criar_rect.collidepoint(evento.pos):
                    return "criar"
                elif entrar_rect.collidepoint(evento.pos):
                    return "entrar"

        pygame.display.flip()

def main():
    """
    Controla o fluxo principal do jogo.
    """
    db = Database()  # Inicializa o banco de dados

    while True:
        escolha = tela_inicial(tela, db)
        
        if escolha == "jogar":
            # Modo de jogo local
            vencedor = jogo(db)
            if vencedor == "tela_inicial":
                db.fechar_conexao()
                main()
        elif escolha == "multijogador":
            # Modo multijogador
            escolha_multijogador = tela_multijogador(tela)

            if escolha_multijogador == "criar":
                print("Iniciando o servidor...")
                threading.Thread(target=iniciar_servidor).start()
                vencedor = jogo(db, True)
            elif escolha_multijogador == "entrar":
                print("Conectando ao servidor...")
                threading.Thread(target=cliente).start()
                jogo(db, True, True)
        else:
            # Encerrar o jogo
            db.fechar_conexao()
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()
