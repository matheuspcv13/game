import pygame

def carregar_imagem(caminho):
    try:
        imagem = pygame.image.load('../' + caminho)
        return imagem
    except pygame.error as e:
        print(f"Erro ao carregar imagem: {e}")
        return None

def carregar_som(caminho):
    try:
        som = pygame.mixer.Sound(caminho)
        return som
    except pygame.error as e:
        print(f"Erro ao carregar som: {e}")
        return None
    