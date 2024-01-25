import pygame
import sys
import random
import numpy as np

from game_obj.nave import Nave
from game_obj.meteoro import Meteoro

from utils.constantes import*
from acoes.checar_teclado import checarTeclado
import rede_neural.rede_neural as ia

rede_neural_jogando = True
erro = 0

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

max_inimigos = 3
probabilidade_spaw = 0.01
pontos = 0

def meteoro_mais_proximo():
    posicao_nave = nave.rect_nave.center  # Posição central da nave
    # Verifica se há meteoros
    if not meteoros:
        return None
    # Inicializa a distância máxima com um valor grande
    distancia_minima = float('inf')
    meteoro_mais_proximo = None
    # Percorre todos os meteoros
    for meteoro in meteoros:
        posicao_meteoro = meteoro.rect_meteoro.center  # Posição central do meteoro
        # Calcula a distância entre a nave e o meteoro
        distancia = ((posicao_meteoro[0] - posicao_nave[0])**2 + (posicao_meteoro[1] - posicao_nave[1])**2)**0.5
        # Verifica se a distância é menor que a mínima encontrada até agora
        if distancia < distancia_minima:
            distancia_minima = distancia
            meteoro_mais_proximo = meteoro
    return meteoro_mais_proximo

def criar_meteoro():
    print("Criando meteoro")
    meteoro = Meteoro(screen, nave.rect_nave)
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
        if meteoro.atualizar(nave.rect_nave):
            pontos += 1

    nave.atualizar()

def comandoRedeNeural(comando):
    if comando >= -1 and comando < 0:
        nave.rotacionar(5)
    if comando <=1 and comando > 0:
        nave.rotacionar(-5)
    else :
        nave.ativar_boost()

# Game Loop
while fechar_jogo:
    fechar_jogo = checarTeclado(fechar_jogo, nave)
    if rede_neural_jogando and meteoro_mais_proximo() is not None:
        rede = ia.RedeNeural(nave, meteoro_mais_proximo())
        comandoRedeNeural(rede.feedforward())
        for meteoro in meteoros:
            nave.nave_se_aproximando(meteoro)
            if meteoro.bateu_na_nave() > 0 or nave.erro > 0:
                erro += meteoro.bateu_na_nave() + nave.erro
            #print('erro: ', erro)
        rede.atualizarPesos(erro)
        erro = 0

    atualizaTudo()
    screen.fill((0, 0, 0))
    desenhar()
    pygame.display.flip()
    clock.tick(FPS)

# Encerramento do Pygame
pygame.quit()
sys.exit()

