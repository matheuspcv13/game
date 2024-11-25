import pygame
import sys
import random
from utilidades import carregar_imagem


LARGURA_TELA = 800
ALTURA_TELA = 600


def aplicar_desfoque(imagem):
    
    return pygame.transform.smoothscale(imagem, (LARGURA_TELA // 2, ALTURA_TELA // 2))


class Gota:
    def __init__(self):
        self.x = random.randint(0, LARGURA_TELA)  
        self.y = random.randint(-50, -10)  
        self.velocidade = random.randint(1, 3)  

    def cair(self):
        self.y += self.velocidade  
        if self.y > ALTURA_TELA: 
            self.y = random.randint(-50, -10)
            self.x = random.randint(0, LARGURA_TELA)

    def desenhar(self, tela):
        pygame.draw.circle(tela, (0, 255, 255), (self.x, self.y), 5)

def tela_inicial(tela, db):
    # Fontes
    fonte_titulo = pygame.font.Font("../assets/fonts/PressStart2P-Regular.ttf", 25)
    fonte_opcao = pygame.font.Font("../assets/fonts/PressStart2P-Regular.ttf", 20)
    fonte_opcao_hover = pygame.font.Font("../assets/fonts/PressStart2P-Regular.ttf", 20)
    fonte_tabela_titulo = pygame.font.Font("../assets/fonts/PressStart2P-Regular.ttf", 10)
    fonte_tabela_conteudo = pygame.font.Font("../assets/fonts/PressStart2P-Regular.ttf", 14)

    # Títulos e opções
    titulo = fonte_titulo.render("GD FIGHTERS", True, (255, 255, 255))
    opcao_jogar = fonte_opcao.render("Jogar", True, (255, 255, 255))
    opcao_multijogador = fonte_opcao.render("Multijogador", True, (255, 255, 255))
    opcao_sair = fonte_opcao.render("Sair", True, (255, 255, 255))

    # Retângulos das opções
    jogar_rect = opcao_jogar.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 - 100))
    multijogador_rect = opcao_multijogador.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2))
    sair_rect = opcao_sair.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 + 100))

    # Animação de fundo
    gotas = [Gota() for _ in range(100)]
    fundo_imagem = carregar_imagem('assets/imagens/fundo.png')
    fundo_imagem = aplicar_desfoque(fundo_imagem)

    while True:
        tela.fill((0, 0, 0))
        tela.blit(fundo_imagem, (ALTURA_TELA, LARGURA_TELA))

        deslocamento_x = random.randint(-5, 5)  
        deslocamento_y = random.randint(-5, 5)  

        # Animação de título
        deslocamento_x = random.randint(-5, 5)
        deslocamento_y = random.randint(-5, 5)
        titulo_rect = titulo.get_rect(center=(LARGURA_TELA // 2 + deslocamento_x, ALTURA_TELA // 4 + deslocamento_y))

        # Atualizar as gotas
        for gota in gotas:
            gota.cair()
            gota.desenhar(tela)

        # Obter posição do mouse
        mouse_pos = pygame.mouse.get_pos()

        # Alterar cor das opções ao passar o mouse
        if jogar_rect.collidepoint(mouse_pos):
            opcao_jogar = fonte_opcao_hover.render("JOGAR", True, (0, 255, 0))
        else:
            opcao_jogar = fonte_opcao.render("JOGAR", True, (255, 255, 255))

        if multijogador_rect.collidepoint(mouse_pos):
            opcao_multijogador = fonte_opcao_hover.render("MULTIJOGADOR", True, (0, 255, 0))
        else:
            opcao_multijogador = fonte_opcao.render("MULTIJOGADOR", True, (255, 255, 255))

        if sair_rect.collidepoint(mouse_pos):
            opcao_sair = fonte_opcao_hover.render("SAIR", True, (255, 0, 0))
        else:
            opcao_sair = fonte_opcao.render("SAIR", True, (255, 255, 255))

        tabela_largura = 230
        tabela_altura = 500
        tabela_x = LARGURA_TELA - tabela_largura - 20
        tabela_y = 20

        pygame.draw.rect(tela, (255, 255, 255), (tabela_x, tabela_y, tabela_largura, tabela_altura), 3)  

        titulo_nome = fonte_tabela_titulo.render("Nome", True, (255, 255, 255))
        titulo_wins = fonte_tabela_titulo.render("Wins", True, (255, 255, 255))

        tela.blit(titulo_nome, (tabela_x + 10, tabela_y + 10))  
        tela.blit(titulo_wins, (tabela_x + 180, tabela_y + 10))  
        vencedores = db.select_nomes()
    
        y_offset = tabela_y + 40
        for i, vencedor in enumerate(vencedores):
            nome = vencedor[1]
            vitorias = vencedor[2]

            if (i == 0) :
                texto_nome = fonte_tabela_conteudo.render(f"{nome}", True, (255, 255, 0))
                texto_vitorias = fonte_tabela_conteudo.render(f"{vitorias}", True, (255, 255, 0))
            else:
                texto_nome = fonte_tabela_conteudo.render(f"{nome}", True, (255, 255, 255))
                texto_vitorias = fonte_tabela_conteudo.render(f"{vitorias}", True, (255, 255, 255))
            
        
            tela.blit(texto_nome, (tabela_x + 10, y_offset))  
            tela.blit(texto_vitorias, (tabela_x + 180, y_offset))  

            y_offset += 30  


        # Desenhar na tela
        tela.blit(titulo, titulo_rect)
        tela.blit(opcao_jogar, (LARGURA_TELA // 2 - opcao_jogar.get_width() // 2, ALTURA_TELA // 2 - 100))
        tela.blit(opcao_multijogador, (LARGURA_TELA // 2 - opcao_multijogador.get_width() // 2, ALTURA_TELA // 2))
        tela.blit(opcao_sair, (LARGURA_TELA // 2 - opcao_sair.get_width() // 2, ALTURA_TELA // 2 + 100))

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if jogar_rect.collidepoint(evento.pos):
                    return "jogar"
                elif multijogador_rect.collidepoint(evento.pos):
                    return "multijogador"
                elif sair_rect.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
