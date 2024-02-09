import pygame
import sys
import random
from objetos.nave import Nave
from objetos.meteoro import Meteoro

from utils.constantes import*
from acoes.checar_teclado import checarTeclado

pygame.font.init()
fonte = pygame.font.Font(None, 22)
pygame.init()

# Configuração da tela
screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("KABUMMM")

# Variáveis do jogo
clock = pygame.time.Clock()
prox_movimento = 0
fechar_jogo = True
naves = pygame.sprite.Group()
meteoros = pygame.sprite.Group()

max_inimigos = 0
probabilidade_spaw = 0.01
rede_neural_jogando = False
#minimo 50
numero_de_naves = 1
contagem_geracao_atual = 0
contagem_geracao_anterior = 0

def criar_meteoro():
    if len(naves) != 0:
        meteoro = Meteoro(screen, random.choice(list(naves)).rect_nave)
        meteoros.add(meteoro)

def escrever_na_tela():
    screen.blit(fonte.render(f'Inimigos: {len(meteoros)}', True, (255, 255, 255)), (10, 30))

def desenhar():
    for nave in naves:
        nave.desenha_nave()
        if rede_neural_jogando == False :
            nave.desenhar_barra_boost()

    for meteoro in meteoros:
        meteoro.desenha_meteoro()
    escrever_na_tela()

def atualizaTudo():
    #Decide se ira criar novo meteoro
    if (len(meteoros) < max_inimigos and random.random() < probabilidade_spaw) or (len(meteoros) == 0):
        criar_meteoro()
    for meteoro in meteoros:
        meteoro.atualizar()
        for nave in naves :
            nave.atualizar()
            if nave.bateu_no_meteoro(meteoro.hitbox) and len(naves) <= 0:
                resetar_jogo()

def resetar_jogo():
    global meteoros, naves
    meteoros = pygame.sprite.Group()
    naves = pygame.sprite.Group()
    for i in range(numero_de_naves):
        naves.add(Nave(screen))

def player_joga():
    pass

def ia_joga():
    pass

resetar_jogo()
while fechar_jogo:
    if len(naves) != 0:
        fechar_jogo = checarTeclado(fechar_jogo, naves.sprites()[0], rede_neural_jogando)
        atualizaTudo()
    ia_joga()
    player_joga()
    screen.fill((3, 0, 20))
    desenhar()
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()

