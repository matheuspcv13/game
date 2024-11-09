import pygame
import sys
from database import Database
from jogo import jogo  # Importa a função `jogo` do arquivo jogo.py
from tela_inicial import tela_inicial

# Inicializar o Pygame
pygame.init()

# Configurações da Tela
LARGURA_TELA = 800
ALTURA_TELA = 600
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Jogo TAC")

def main():
    db = Database()  # Inicializa o banco de dados

    # Loop principal
    while True:
        escolha = tela_inicial(tela, db)
        
        if escolha == "jogar":
            vencedor = jogo(db)
            
            if vencedor == "tela_inicial":
                db.fechar_conexao()
                main()
        else:
            db.fechar_conexao()
            pygame.quit()
            sys.exit  

if __name__ == "__main__":
    main()
