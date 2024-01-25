import numpy as np
import time
from random import uniform

from utils.constantes import LARGURA, ALTURA
qtd_neuronios_oculta = 5
qtd_neuronios_saida = 3
class RedeNeural():
    def __init__(self,nave, meteoro, bias = -1):
        self.tempo_proximo_boost = (20 if int(nave.tempo_proximo_boost - time.time()) > 20 else int(nave.tempo_proximo_boost - time.time()) / nave.intervalo_entre_boosts)
        self.x_nave = (nave.rect_nave.x / LARGURA)
        self.y_nave = (nave.rect_nave.y / ALTURA)
        self.velocidade_nave = (nave.velocidade / nave.velocidade_max)
        self.x_meteoro = (meteoro.rect_meteoro.x / LARGURA)
        self.y_meteoro = (meteoro.rect_meteoro.y / ALTURA)
        self.velocidade_meteoro = (meteoro.velocidade / 5)
        self.bias = bias
        self.alpha = 0.1
        self.entradas = np.array([self.tempo_proximo_boost, self.x_nave, self.y_nave, self.velocidade_nave, self.x_meteoro, self.y_meteoro, self.velocidade_meteoro, self.bias])
        self.pesos_camada_oculta = self.aleatorizaPessosCamadaOculta()
        self.pesos_camada_saida = self.aleatorizaPessosCamadaSaida()

    def aleatorizaPessosCamadaOculta(self):
        global qtd_neuronios_oculta
        return np.array([[uniform(-1, 1) for _ in range(len(self.entradas))] for _ in range(qtd_neuronios_oculta)])

    def aleatorizaPessosCamadaSaida(self):
        global qtd_neuronios_saida, qtd_neuronios_oculta
        return np.array([[uniform(-1, 1) for _ in range(qtd_neuronios_oculta)] for _ in range(qtd_neuronios_saida)])

    def feedforward(self):
        global qtd_neuronios_oculta
        saida_neuronios = np.empty(qtd_neuronios_oculta)
        for i, pesos_neuronio_oculto in enumerate(self.pesos_camada_oculta):
            saida_neuronios[i] = self.tangenteHiperbolica(np.sum(self.entradas * pesos_neuronio_oculto))
        self.resultado = self.tangenteHiperbolica(np.sum(saida_neuronios * self.pesos_camada_saida))
        return self.resultado

    def tangenteHiperbolica(self, x):
        th = (np.exp(x) - np.exp(-x)) / (np.exp(x) + np.exp(-x))
        return th
    def atualizarPesos(self, erro):
        for i in range(len(self.pesos_camada_oculta)):
            self.pesos_camada_oculta[i] = self.pesos_camada_oculta[i] + (self.alpha * self.entradas[i] * erro)
        for i in range(len(self.pesos_camada_saida)):
            self.pesos_camada_saida[i] = self.pesos_camada_saida[i] + (self.alpha * self.entradas[i] * erro)

def evoluir_populacao(populacao, fitness):
    # Ordenar a população com base no fitness
    ordenados = np.argsort(fitness)
    # Selecionar os melhores indivíduos (maiores valores de fitness)
    melhores_indices = ordenados[-len(populacao):]
    # Criar nova população com base nos melhores indivíduos
    nova_populacao = [populacao[i] for i in melhores_indices]
    # Mutação: Adicionar variações aleatórias aos pesos dos indivíduos
    for individuo in nova_populacao:
        for i in range(len(individuo.pesos_camada_oculta)):
            for j in range(len(individuo.pesos_camada_oculta[i])):
                individuo.pesos_camada_oculta[i][j] += np.random.normal(0, 0.1)
        for i in range(len(individuo.pesos_camada_saida)):
            for j in range(len(individuo.pesos_camada_saida[i])):
                individuo.pesos_camada_saida[i][j] += np.random.normal(0, 0.1)

    return nova_populacao