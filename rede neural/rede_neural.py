import numpy as np

# Função de ativação ReLU
def relu(x):
    if x < 0:
        return 0
    elif x < 10000:
        return x
    else:
        return 10000

# Classe Neuronio
class Neuronio:
    def __init__(self, quantidade_ligacoes):
        self.peso = np.random.randint(-1000, 1000, quantidade_ligacoes).astype(float)
        self.erro = 0
        self.saida = 1
        self.quantidade_ligacoes = quantidade_ligacoes

# Classe Camada
class Camada:
    def __init__(self, quantidade_neuronios, quantidade_ligacoes):
        self.neuronios = [Neuronio(quantidade_ligacoes) for _ in range(quantidade_neuronios)]

# Classe RedeNeural
class RedeNeural:
    def __init__(self, quantidade_escondidas, qtd_neuronios_entrada, qtd_neuronios_escondida, qtd_neuronios_saida):
        self.camada_entrada = Camada(qtd_neuronios_entrada + 1, qtd_neuronios_entrada)
        self.camada_escondida = [Camada(qtd_neuronios_escondida + 1, qtd_neuronios_escondida) for _ in range(quantidade_escondidas)]
        self.camada_saida = Camada(qtd_neuronios_saida, qtd_neuronios_escondida)
        self.quantidade_escondidas = quantidade_escondidas

# Função de ativação da camada oculta
def ativacao_ocultas(x):
    return relu(x)

# Função de ativação da camada de saída
def ativacao_saida(x):
    return relu(x)

# Função para calcular a saída da rede neural
def calcular_saida(rede):
    somatorio = 0
    
    # Calculando saídas entre a camada de entrada e a primeira camada escondida
    for i in range(len(rede.camada_escondida[0].neuronios) - 1):
        somatorio = 0
        for j in range(len(rede.camada_entrada.neuronios)):
            somatorio += rede.camada_entrada.neuronios[j].saida * rede.camada_escondida[0].neuronios[i].peso[j]
        rede.camada_escondida[0].neuronios[i].saida = ativacao_ocultas(somatorio)
    
    # Calculando saídas entre as camadas escondidas
    for k in range(1, rede.quantidade_escondidas):
        for i in range(len(rede.camada_escondida[k].neuronios) - 1):
            somatorio = 0
            for j in range(len(rede.camada_escondida[k - 1].neuronios)):
                somatorio += rede.camada_escondida[k - 1].neuronios[j].saida * rede.camada_escondida[k].neuronios[i].peso[j]
            rede.camada_escondida[k].neuronios[i].saida = ativacao_ocultas(somatorio)
    
    # Calculando saídas entre a camada de saída e a última camada escondida
    for i in range(len(rede.camada_saida.neuronios)):
        somatorio = 0
        for j in range(len(rede.camada_escondida[-1].neuronios)):
            somatorio += rede.camada_escondida[-1].neuronios[j].saida * rede.camada_saida.neuronios[i].peso[j]
        rede.camada_saida.neuronios[i].saida = ativacao_saida(somatorio)

# Função para copiar vetor para as camadas
def copiar_vetor_para_camadas(rede, vetor):
    j = 0
    for i in range(rede.quantidade_escondidas):
        for k in range(len(rede.camada_escondida[i].neuronios)):
            for l in range(len(rede.camada_escondida[i].neuronios[k].peso)):
                rede.camada_escondida[i].neuronios[k].peso[l] = vetor[j]
                j += 1

    for k in range(len(rede.camada_saida.neuronios)):
        for l in range(len(rede.camada_saida.neuronios[k].peso)):
            rede.camada_saida.neuronios[k].peso[l] = vetor[j]
            j += 1

# Função para copiar camadas para vetor
def copiar_camadas_para_vetor(rede):
    vetor = []
    for i in range(rede.quantidade_escondidas):
        for k in range(len(rede.camada_escondida[i].neuronios)):
            for l in range(len(rede.camada_escondida[i].neuronios[k].peso)):
                vetor.append(rede.camada_escondida[i].neuronios[k].peso[l])

    for k in range(len(rede.camada_saida.neuronios)):
        for l in range(len(rede.camada_saida.neuronios[k].peso)):
            vetor.append(rede.camada_saida.neuronios[k].peso[l])

    return np.array(vetor)

# Função para copiar para a entrada
def copiar_para_entrada(rede, vetor_entrada):
    for i in range(len(rede.camada_entrada.neuronios) - 1):
        rede.camada_entrada.neuronios[i].saida = vetor_entrada[i]

# Função para obter a quantidade de pesos
def obter_quantidade_pesos(rede):
    soma = 0
    for i in range(rede.quantidade_escondidas):
        for j in range(len(rede.camada_escondida[i].neuronios)):
            soma += rede.camada_escondida[i].neuronios[j].quantidade_ligacoes

    for i in range(len(rede.camada_saida.neuronios)):
        soma += rede.camada_saida.neuronios[i].quantidade_ligacoes

    return soma

# Função para copiar da saída
def copiar_da_saida(rede):
    vetor_saida = []
    for i in range(len(rede.camada_saida.neuronios)):
        vetor_saida.append(rede.camada_saida.neuronios[i].saida)
    return np.array(vetor_saida)

# Função para criar neurônio
def criar_neuronio(quantidade_ligacoes):
    return Neuronio(quantidade_ligacoes)

# Função para criar rede neural
def criar_rede_neural(quantidade_escondidas, qtd_neuronios_entrada, qtd_neuronios_escondida, qtd_neuronios_saida):
    qtd_neuronios_entrada += 1
    qtd_neuronios_escondida += 1

    rede = RedeNeural(quantidade_escondidas, qtd_neuronios_entrada, qtd_neuronios_escondida, qtd_neuronios_saida)

    for i in range(qtd_neuronios_entrada):
        rede.camada_entrada.neuronios[i].saida = 1.0

    for i in range(quantidade_escondidas):
        for j in range(qtd_neuronios_escondida):
            if i == 0:
                rede.camada_escondida[i].neuronios[j] = criar_neuronio(qtd_neuronios_entrada)
            else:
                rede.camada_escondida[i].neuronios[j] = criar_neuronio(qtd_neuronios_escondida)

    for j in range(qtd_neuronios_saida):
        rede.camada_saida.neuronios[j] = criar_neuronio(qtd_neuronios_escondida)

    return rede

# Função para destruir rede neural
def destruir_rede_neural(rede):
    for neuronio in rede.camada_entrada.neuronios:
        del neuronio.peso
    for camada in rede.camada_escondida:
        for neuronio in camada.neuronios:
            del neuronio.peso
        del camada.neuronios
    del rede.camada_escondida
    for neuronio in rede.camada_saida.neuronios:
        del neuronio.peso
    del rede.camada_saida

# Função para carregar rede neural
def carregar_rede(nome_arquivo):
    with open(nome_arquivo, 'rb') as f:
        quantidade_escondida = np.fromfile(f, dtype=np.int32, count=1)
        qtd_neuro_entrada = np.fromfile(f, dtype=np.int32, count=1)
        qtd_neuro_escondida = np.fromfile(f, dtype=np.int32, count=1)
        qtd_neuro_saida = np.fromfile(f, dtype=np.int32, count=1)

        rede = criar_rede_neural(quantidade_escondida[0], qtd_neuro_entrada[0], qtd_neuro_escondida[0], qtd_neuro_saida[0])

        for k in range(rede.quantidade_escondidas):
            for i in range(len(rede.camada_escondida[k].neuronios)):
                for j in range(len(rede.camada_escondida[k].neuronios[i].peso)):
                    rede.camada_escondida[k].neuronios[i].peso[j] = np.fromfile(f, dtype=np.float64, count=1)

        for i in range(len(rede.camada_saida.neuronios)):
            for j in range(len(rede.camada_saida.neuronios[i].peso)):
                rede.camada_saida.neuronios[i].peso[j] = np.fromfile(f, dtype=np.float64, count=1)

    return rede

# Função para salvar rede neural
def salvar_rede(rede, nome_arquivo):
    with open(nome_arquivo, 'wb') as f:
        np.array(rede.quantidade_escondidas, dtype=np.int32).tofile(f)
        np.array(rede.camada_entrada.quantidade_neuronios, dtype=np.int32).tofile(f)
        np.array(rede.camada_escondida[0].quantidade_neuronios, dtype=np.int32).tofile(f)
        np.array(rede.camada_saida.quantidade_neuronios, dtype=np.int32).tofile(f)

        for k in range(rede.quantidade_escondidas):
            for i in range(len(rede.camada_escondida[k].neuronios)):
                for j in range(len(rede.camada_escondida[k].neuronios[i].peso)):
                    np.array(rede.camada_escondida[k].neuronios[i].peso[j], dtype=np.float64).tofile(f)

        for i in range(len(rede.camada_saida.neuronios)):
            for j in range(len(rede.camada_saida.neuronios[i].peso)):
                np.array(rede.camada_saida.neuronios[i].peso[j], dtype=np.float64).tofile(f)

# Exemplo de uso:

# Criando uma rede neural
rede_neural = criar_rede_neural(2, 2, 3, 1)

# Copiando um vetor para as camadas
vetor_entrada = np.random.rand(obter_quantidade_pesos(rede_neural))
copiar_vetor_para_camadas(rede_neural, vetor_entrada)

# Copiando camadas para um vetor
vetor_saida = copiar_camadas_para_vetor(rede_neural)

# Copiando para a entrada
entrada = np.random.rand(rede_neural.camada_entrada.quantidade_neuronios - 1)
copiar_para_entrada(rede_neural, entrada)

# Calculando a saída
calcular_saida(rede_neural)

# Copiando da saída
saida = copiar_da_saida(rede_neural)

# Destruindo a rede neural
destruir_rede_neural(rede_neural)
