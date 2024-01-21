import pygame
import sys
import random

from game_obj.nave import Nave
from game_obj.meteoro import Meteoro

from utils.constantes import*
from acoes.checar_teclado import checarTeclado

pygame.font.init()
fonte = pygame.font.Font(None, 22)

# Inicialização do Pygamed
pygame.init()

# Configuração da tela
screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("KABUMMM")

# Variáveis do jogo
clock = pygame.time.Clock()
fechar_jogo = True

nave = Nave(screen)
meteoros = pygame.sprite.Group()

max_inimigos = 5
probabilidade_spaw = 0.01
pontos = 0

def criar_meteoro():
    meteoro = Meteoro(screen, nave.rect_nave.x, nave.rect_nave.y)
    meteoros.add(meteoro)

def desenhar():
    nave.desenha_nave()
    nave.desenhar_barra_boost()
    
    for meteoro in meteoros:
        meteoro.desenha_meteoro()

    posicao_texto = fonte.render(f'Velocidade: {nave.velocidade:.0f}', True, (255, 255, 255))
    screen.blit(posicao_texto, (10, 10))
    screen.blit(fonte.render(f'Inimigos: {len(meteoros)}', True, (255, 255, 255)), (10, 30))
    screen.blit(fonte.render(f'Pontos: {pontos * 10}', True, (255, 255, 255)), (10, 50))

def atualizaTudo():
    global pontos
    #Decide se ira criar novo meteoro
    if len(meteoros) < max_inimigos and random.random() < probabilidade_spaw:
        criar_meteoro()

    for meteoro in meteoros:
        pontos += meteoro.atualizar()

    nave.atualizar()

# Game Loop
while fechar_jogo:
    fechar_jogo = checarTeclado(fechar_jogo, nave)
    atualizaTudo()
    screen.fill((0, 0, 0))
    desenhar()
    pygame.display.flip()
    clock.tick(FPS)

# Encerramento do Pygame
pygame.quit()
sys.exit()

