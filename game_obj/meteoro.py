import pygame
import random
from utils.constantes import LARGURA, ALTURA

class Meteoro(pygame.sprite.Sprite):
    imagem_meteoro = pygame.image.load("sprites/meteoro.png")
    def aleatorizar_x(self):
        x = 0
        if random.choice([-1, 1]) == -1 :
            x = random.randint(-200, 0)
        else:
            x = random.randint(LARGURA, LARGURA + 200)
        return float(x)

    def aleatorizar_y(self):
        y = 0
        if random.choice([-1, 1]) == -1 :
            y = random.randint(-200, 0)
        else:
            y = random.randint(ALTURA, ALTURA + 200)
        return float(y)

    def __init__(self, tela, x_nave, y_nave):
        super().__init__()
        tamanho_aleatorio = random.randint(25, 200)
        self.tela = tela
        self.tamanho = (tamanho_aleatorio, tamanho_aleatorio)
        self.velocidade = random.randint(1, 5)
        self.angulo = 0

        self.posicao = pygame.Vector2(self.aleatorizar_x(), self.aleatorizar_y())
        self.original_sprit_meteoro = Meteoro.imagem_meteoro
        self.original_sprit_meteoro = pygame.transform.scale(self.original_sprit_meteoro, self.tamanho)
        self.rect_meteoro = self.original_sprit_meteoro.get_rect(center=(self.posicao.x, self.posicao.y))

        self.x_nave = x_nave
        self.y_nave = y_nave

        self.vetor_direcao = pygame.Vector2(self.x_nave - self.posicao.x, self.y_nave - self.posicao.y)

    def desenha_meteoro(self):
        self.tela.blit(self.original_sprit_meteoro, self.rect_meteoro)

    def rotacao(self):
        self.angulo += 3
        if self.angulo >= 360:
            self.angulo = 0

        self.original_sprit_meteoro = Meteoro.imagem_meteoro
        self.original_sprit_meteoro = pygame.transform.scale(self.original_sprit_meteoro, self.tamanho)
        self.original_sprit_meteoro = pygame.transform.rotate(self.original_sprit_meteoro, self.angulo)
        self.rect_meteoro = self.original_sprit_meteoro.get_rect(center=self.rect_meteoro.center)

    def movimentar(self):
        self.vetor_direcao.normalize_ip()

        incremento_x, incremento_y = self.vetor_direcao * self.velocidade

        self.posicao.x += incremento_x
        self.posicao.y += incremento_y
        self.rect_meteoro.center = (self.posicao.x, self.posicao.y)

    def atualizar(self):
        self.rotacao()
        self.movimentar()
        if self.saiu_da_tela():
            self.kill()
            return 1
        return 0

    def saiu_da_tela(self):
        # Verifica se o objeto saiu pela esquerda ou pela direita
        saiu_pela_lateral = self.posicao.x + self.tamanho[0] < -200 or self.posicao.x > (LARGURA + 200)

        # Verifica se o objeto saiu pelo topo ou pela parte inferior
        saiu_pelo_topo_ou_base = self.posicao.y + self.tamanho[1] < -200 or self.posicao.y > (ALTURA + 200)

        return saiu_pela_lateral or saiu_pelo_topo_ou_base

