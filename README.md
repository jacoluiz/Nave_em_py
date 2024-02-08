# Base para interpretação de uma rede Neural

## Neurônio
Um neurônio é uma unidade fundamental em uma rede neural, inspirado no neurônio biológico. Ele recebe entradas, realiza uma soma ponderada dessas entradas multiplicadas pelos pesos associados, adiciona um viés (bias) e aplica uma função de ativação para produzir uma saída.

## Pesos
Os pesos em um neurônio representam a força ou a importância associada a cada entrada. Durante o treinamento da rede neural, esses pesos são ajustados para minimizar o erro entre a saída prevista e a saída desejada.

## Camada
Uma camada é um conjunto de neurônios que funcionam em paralelo. Em uma rede neural, geralmente temos três tipos principais de camadas:

### Camada de Entrada:
Recebe as entradas originais para o modelo. Cada neurônio na camada de entrada representa uma característica ou atributo dos dados.

### Camadas Ocultas:
Essas camadas são intermediárias entre a camada de entrada e a camada de saída. Cada neurônio nas camadas ocultas recebe entradas da camada anterior, realiza cálculos com pesos e produz uma saída. Essas camadas são chamadas "ocultas" porque suas saídas não são diretamente observáveis no contexto do problema.

### Camada de Saída:
Produz a saída final da rede neural. Cada neurônio na camada de saída representa uma classe ou uma previsão relacionada ao problema em questão.

## Função de Ativação
Uma função de ativação é aplicada à soma ponderada das entradas e pesos de um neurônio, determinando se o neurônio deve ser ativado (produzir uma saída significativa) ou não. A função ReLU (Rectified Linear Unit) é uma escolha comum, pois é simples e eficaz.

## Treinamento da Rede Neural
O treinamento de uma rede neural envolve apresentar um conjunto de dados de treinamento à rede, ajustar os pesos iterativamente para minimizar a diferença entre as saídas previstas e as saídas reais (rótulos) associadas a esses dados. Isso é feito usando algoritmos de otimização, como o Gradiente Descendente.

## Viés (BIAS)
O viés é um termo adicional adicionado à soma ponderada nas camadas de neurônios. Ele permite que o modelo aprenda a melhor representação dos dados, mesmo quando todas as entradas são zero.

## Estrutura da Rede Neural no Código
O código implementa uma rede neural com uma camada de entrada, várias camadas ocultas e uma camada de saída. Os pesos dos neurônios são inicializados aleatoriamente, e a função ReLU é usada como função de ativação.

Espero que essas explicações ajudem a compreender os conceitos básicos por trás do código.

PS: Não olhe o codigo, esta mais bagunçado que minha vida ;)