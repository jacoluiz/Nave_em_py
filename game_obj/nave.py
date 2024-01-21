import pygame
import math
import time
from utils.constantes import LARGURA, ALTURA

class Nave:
    def __init__(self, tela):
        self.original_sprit_nave = pygame.image.load("sprites/nave.png")
        self.original_sprit_nave = pygame.transform.scale(self.original_sprit_nave, (32, 32))
        self.rect_nave = self.original_sprit_nave.get_rect()
        self.resetar_posicao()
        self.tela = tela

        self.velocidade = 0
        self.velocidade_max = 20
        self.aceleracao = 1
        self.angulo = 0
        self.sprit_nave = self.original_sprit_nave

        # Atributos relacionados ao boost
        self.boost_ativo = False
        self.tempo_boost_ativo = 0
        self.tempo_proximo_boost = 0
        self.duracao_boost = 3  # em segundos
        self.intervalo_entre_boosts = 20  # em segundos
        self.ultima_ativacao = 0
        self.valor_preenchido_boost = 10

    def desenhar_barra_boost(self):
        # Desenhe o contorno da barra de progresso
        pygame.draw.rect(self.tela, (255, 255, 255), ((LARGURA - 35), (ALTURA - 120), 25, 100), 2, 5)
        
        # Calcule o percentual da variável em relação ao máximo
        percentual = (((time.time() + self.intervalo_entre_boosts) - self.tempo_proximo_boost) / self.intervalo_entre_boosts) * 100

        # Calcule a largura proporcional com base no valor atual e máximo
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

        # Desenhe a barra de progresso preenchido
        if self.valor_preenchido_boost > 1 :
            pygame.draw.rect(self.tela, cor_boost, ((LARGURA - 34), (ALTURA - 21), 23, -(self.valor_preenchido_boost - 2)), 0, 5)

    def resetar_posicao(self):
        self.rect_nave.x = (LARGURA - self.rect_nave.width) // 2
        self.rect_nave.y = (ALTURA - self.rect_nave.height) // 2

    def colisoesBordas(self):
        # Lógica para verificar colisões com as bordas
        if self.rect_nave.x <= 0:
            self.rect_nave.x += 1
            return True

        elif self.rect_nave.x >= LARGURA - self.rect_nave.width:
            self.rect_nave.x -= 1
            return True

        elif self.rect_nave.y <= 0 :
            self.rect_nave.y += 1
            return True

        elif self.rect_nave.y >= ALTURA - self.rect_nave.height:
            self.rect_nave.y -= 1
            return True

        else:
            return False

    def diminuirVelocidade(self):
        if self.velocidade > 5 :
            self.velocidade -= 0.01
        elif self.velocidade <= 5 and self.velocidade > 2:
            self.velocidade -= 0.008
        elif self.velocidade <= 2 and self.velocidade > 0:
            self.velocidade -= 0.002

    def ativar_boost(self):
        # Verifica se o boost pode ser ativado
        tempo_atual = time.time()
        if tempo_atual > self.tempo_proximo_boost:
            print("Boost ativo")
            self.ultima_ativacao = tempo_atual
            self.boost_ativo = True
            self.tempo_boost_ativo = tempo_atual + self.duracao_boost
            self.tempo_proximo_boost = tempo_atual + self.intervalo_entre_boosts

    def acelerar(self):
        self.diminuirVelocidade()

        aceleracao_x = -self.aceleracao * math.sin(math.radians(self.angulo))
        aceleracao_y = -self.aceleracao * math.cos(math.radians(self.angulo))

        if self.velocidade < self.velocidade_max:
            if self.boost_ativo and (time.time() - self.ultima_ativacao) < 1 :
                self.velocidade += 0.05
            elif self.boost_ativo and (time.time() - self.ultima_ativacao) >= 1 :
                self.velocidade += 0.1

        if not self.colisoesBordas():
            self.rect_nave.x += self.velocidade * aceleracao_x
            self.rect_nave.y += self.velocidade * aceleracao_y

    def rotacionar(self, angulo):
        if self.velocidade >= 0.5 :
            self.angulo += angulo
            self.sprit_nave = pygame.transform.rotate(self.original_sprit_nave, self.angulo)
            self.rect_nave = self.sprit_nave.get_rect(center=self.rect_nave.center)

    def desenha_nave(self):
        self.tela.blit(self.sprit_nave, self.rect_nave)

    def atualizar(self):
        self.acelerar()
        # Verifica se o boost expirou
        if self.boost_ativo and time.time() > self.tempo_boost_ativo:
            self.boost_ativo = False
