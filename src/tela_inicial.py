import pygame
import sys

# Configurações da Tela
LARGURA_TELA = 800
ALTURA_TELA = 600

# Função para mostrar a tela inicial com opções de Jogar ou Sair
def tela_inicial(tela, db):
    fonte_titulo = pygame.font.Font(None, 100)
    fonte_opcao = pygame.font.Font(None, 50)
    fonte_tabela_titulo = pygame.font.Font(None, 30)
    fonte_tabela_conteudo = pygame.font.Font(None, 24)

    titulo = fonte_titulo.render("Jogo TAC", True, (255, 255, 255))
    opcao_jogar = fonte_opcao.render("Jogar", True, (255, 255, 255))
    opcao_sair = fonte_opcao.render("Sair", True, (255, 255, 255))

    # Posições das opções
    jogar_rect = opcao_jogar.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 - 50))
    sair_rect = opcao_sair.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 + 50))

    # Chama a função para obter os maiores vencedores
    vencedores = db.select_nomes()

    while True:
        tela.fill((0, 0, 0))

        # Exibe o título e as opções
        tela.blit(titulo, (LARGURA_TELA // 2 - titulo.get_width() // 2, ALTURA_TELA // 4))
        tela.blit(opcao_jogar, (LARGURA_TELA // 2 - opcao_jogar.get_width() // 2, ALTURA_TELA // 2 - 50))
        tela.blit(opcao_sair, (LARGURA_TELA // 2 - opcao_sair.get_width() // 2, ALTURA_TELA // 2 + 50))

        # Posição da tabela
        tabela_largura = 200
        tabela_altura = 500
        tabela_x = LARGURA_TELA - tabela_largura - 20
        tabela_y = 20

        pygame.draw.rect(tela, (255, 255, 255), (tabela_x, tabela_y, tabela_largura, tabela_altura), 3)  # Borda branca de 3px

        titulo_nome = fonte_tabela_titulo.render("Nome", True, (255, 255, 255))
        titulo_wins = fonte_tabela_titulo.render("Wins", True, (255, 255, 255))

        tela.blit(titulo_nome, (tabela_x + 10, tabela_y + 10))  # Nome
        tela.blit(titulo_wins, (tabela_x + 100, tabela_y + 10))  # Wins

        # Exibe os dados dos vencedores dentro da tabela
        y_offset = tabela_y + 40
        for i, vencedor in enumerate(vencedores):
            nome = vencedor[1]
            vitorias = vencedor[2]

            texto_nome = fonte_tabela_conteudo.render(f"{nome}", True, (255, 255, 255))
            texto_vitorias = fonte_tabela_conteudo.render(f"{vitorias}", True, (255, 255, 255))

            # Exibe os dados na tela
            tela.blit(texto_nome, (tabela_x + 10, y_offset))  # Nome
            tela.blit(texto_vitorias, (tabela_x + 110, y_offset))  # Wins

            y_offset += 30  # Desloca para a próxima linha (30px de distância)

        # Exibe as opções de Jogar e Sair
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:  # Verifica se o mouse foi clicado
                if jogar_rect.collidepoint(evento.pos):  # Se clicou na opção "Jogar"
                    return "jogar"
                elif sair_rect.collidepoint(evento.pos):  # Se clicou na opção "Sair"
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
