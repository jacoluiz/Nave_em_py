import pygame
import math
import time
import random
from utils.constantes import LARGURA, ALTURA
from objetos.explosao import AnimacaoExplosao
import os

caminho_pasta_sprites = "sprites/naves"
# Lista para armazenar as referências dos sprites
coletania_sprit_naves = []
# Iterar sobre os arquivos na pasta de sprites
for arquivo in os.listdir(caminho_pasta_sprites):
    # Verificar se o arquivo é uma imagem
    if arquivo.endswith(".png"):
        # Carregar o sprite e adicionar à lista
        sprite = pygame.image.load(os.path.join(caminho_pasta_sprites, arquivo))
        coletania_sprit_naves.append(sprite)

class Nave(pygame.sprite.Sprite):
    def __init__(self, tela):
        super().__init__()
        self.original_sprit_nave = random.choice(coletania_sprit_naves)
        self.original_sprit_nave = pygame.transform.scale(self.original_sprit_nave, (32, 32))
        self.rect_nave = self.original_sprit_nave.get_rect()
        self.resetar_posicao()
        self.tela = tela

        self.velocidade = 0
        self.velocidade_max = 5
        self.aceleracao = 1
        self.angulo = 0
        self.sprit_nave = self.original_sprit_nave

        self.boost_ativo = False
        self.tempo_boost_ativo = 0
        self.tempo_proximo_boost = time.time()
        self.duracao_boost = 3  # em segundos
        self.intervalo_entre_boosts = 10  # em segundos
        self.ultima_ativacao = 0
        self.valor_preenchido_boost = 10
        self.explosao = AnimacaoExplosao()

    def desenhar_barra_boost(self):
        pygame.draw.rect(self.tela, (255, 255, 255), ((LARGURA - 35), (ALTURA - 120), 25, 100), 2, 5)
        percentual = (((time.time() + self.intervalo_entre_boosts) - self.tempo_proximo_boost) / self.intervalo_entre_boosts) * 100
        self.valor_preenchido_boost = int(percentual)

        cor_boost = "#00BF0F"
        if self.valor_preenchido_boost > 100 :
            self.valor_preenchido_boost = 100
        elif self.valor_preenchido_boost < 30:
            cor_boost = "#920200"
        elif self.valor_preenchido_boost >= 30 and self.valor_preenchido_boost < 60:
            cor_boost = "#C55301"
        elif self.valor_preenchido_boost >= 60 and self.valor_preenchido_boost <=99:
            cor_boost = "#771B8F"

        if self.valor_preenchido_boost > 1 :
            pygame.draw.rect(self.tela, cor_boost, ((LARGURA - 34), (ALTURA - 21), 23, -(self.valor_preenchido_boost - 2)), 0, 5)

    def resetar_posicao(self):
        self.rect_nave.x = (LARGURA - self.rect_nave.width) // 2
        self.rect_nave.y = (ALTURA - self.rect_nave.height) // 2

    def colisoes_bordas(self):
        if self.rect_nave.x < 0:
            self.rect_nave.x = LARGURA - self.rect_nave.width
        elif self.rect_nave.x > LARGURA - self.rect_nave.width:
            self.rect_nave.x = 0

        if self.rect_nave.y < 0:
            self.rect_nave.y = ALTURA - self.rect_nave.height
        elif self.rect_nave.y > ALTURA - self.rect_nave.height:
            self.rect_nave.y = 0

    def diminuir_velocidade(self):
        if self.velocidade > 5 :
            self.velocidade -= 0.02
        elif self.velocidade <= 5 and self.velocidade > 2:
            self.velocidade -= 0.01
        elif self.velocidade <= 2 and self.velocidade > 0:
            self.velocidade -= 0.005

    def ativar_boost(self):
        tempo_atual = time.time()
        if tempo_atual > self.tempo_proximo_boost:
            self.ultima_ativacao = tempo_atual
            self.boost_ativo = True
            self.tempo_boost_ativo = tempo_atual + self.duracao_boost
            self.tempo_proximo_boost = tempo_atual + self.intervalo_entre_boosts

    def acelerar(self):
        self.diminuir_velocidade() if not  self.boost_ativo else None
        aceleracao_x = -self.aceleracao * math.sin(math.radians(self.angulo))
        aceleracao_y = -self.aceleracao * math.cos(math.radians(self.angulo))

        if self.velocidade < self.velocidade_max:
            if self.boost_ativo and (time.time() - self.ultima_ativacao) < 1 :
                self.velocidade += 0.05
            elif self.boost_ativo and (time.time() - self.ultima_ativacao) >= 1 :
                self.velocidade += 0.1

        self.rect_nave.x += self.velocidade * aceleracao_x
        self.rect_nave.y += self.velocidade * aceleracao_y

    def rotacionar(self, angulo):
        if self.velocidade >= 0.5:
            self.angulo += angulo
            self.sprit_nave = pygame.transform.rotate(self.original_sprit_nave, self.angulo)
            self.rect_nave = self.sprit_nave.get_rect(center=self.rect_nave.center)

    def desenha_nave(self):
        self.tela.blit(self.sprit_nave, self.rect_nave)

    def bateu_no_meteoro(self, hitbox):
        if self.rect_nave.colliderect(hitbox):
            self.explosao.executar_animacao(self.tela, (self.rect_nave.x, self.rect_nave.y))
            self.kill()
            return True
        return False

    def atualizar(self):
        self.acelerar()
        # Verifica se o boost expirou
        if self.boost_ativo and time.time() > self.tempo_boost_ativo:
            self.boost_ativo = False
