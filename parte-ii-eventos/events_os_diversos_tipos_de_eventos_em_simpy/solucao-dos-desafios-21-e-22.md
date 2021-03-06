# Solução dos desafios 21 e 22

> **Desafio 21:** crie um processo de geração de automóveis que desejam cruzar a ponte, durante o horário de pico que dura 4 horas. Os intervalos entre chegadas sucessivas de veículos para travessia são exponencialmente distribuídos com média de 10 segundos \(ou 6 veículos/min\), e a ponte permite a travessia de 10 veículos por minuto. Após 4 horas de operação, quantos veículos estão em espera por travessia da ponte?

Em relação ao modelo anterior, este novo sistema possui um processo de geração de chegadas de veículos e espera por abertura da ponte. Uma alternativa de implementação é utilizar um `Container` para armazenar os veículos em espera pela abertura da ponte, como no código a seguir:

```python
import simpy
import random

CAPACIDADE_TRAVESSIA = 10   # capacidade da ponte em por min

def chegadaVeiculos(env, filaTravessia):
    while True:
        # aguarda a chegada do próximo veículo
        yield env.timeout(random.expovariate(6.0))
        # acrescenta o veículo na fila de travessia
        yield filaTravessia.put(1)
```

No código anterior, `filaTravessia` é um `Container` que representa o conjunto de veículos em espera por travessia da ponte. Cada veículo gerado é imediatamente transferido para o `Container`.

A função `turno` é semelhante à anterior, apenas com a inclusão do tempo de abertura da ponte, como o parâmetro `tempo_ponte:`

```python
def turno(env, filaTravessia, tempo_ponte):
    # abre e fecha a ponte
    global abrePonte

    while True:
        # cria evento para abertura da ponte
        abrePonte = env.event()
        # inicia o processo da ponte elvatória
        env.process(ponteElevatoria(env, filaTravessia))
        # mantém a ponte fechada por 5 minutos
        yield env.timeout(5)
        # dispara o evento de abertura da ponte
        yield abrePonte.succeed(value=tempo_ponte)
        # mantém a ponte aberta por 5 minutos
        yield env.timeout(tempo_ponte)
```

Note que o parâmetro `tempo_ponte` é enviado como um valor para a função `ponteElevatória`, que agora deve lidar com a travessia dos veículos quando aberta. Neste caso, basta um comando `get` no `Container` que representa a fila de travessia dos veículos:

```python
def ponteElevatoria(env, filaTravessia, tempo_ponte):
    # opera a ponte elevatória
    global abrePonte, naoAtendidos

    print('%2.0f A ponte está fechada =(' %(env.now))
    # aguarda o evento para abertura da ponte
    tempoAberta = yield abrePonte
    print('%2.0f A ponte está  aberta =) e fecha em %2.0f minutos' 
            %(env.now, tempoAberta))

    # aguarda a chegada de mais veículos na fila de espera
    yield env.timeout(tempoAberta)

    # calcula quantos veículos podem atravessar a ponte
    numVeiculos = min(int(tempoAberta*CAPACIDADE_TRAVESSIA), filaTravessia.level)

    # retira os veículos da fila
    filaTravessia.get(numVeiculos)
    print('%2.0f Travessia de %i veículos\tFila atual: %i' 
            %(env.now, numVeiculos, filaTravessia.level))
```

Analisando o código anterior, assim que a ponte abre, a linha:

```python
# calcula quantos veículos podem atravessar a ponte
numVeiculos = min(int(tempoAberta*CAPACIDADE_TRAVESSIA), filaTravessia.level)
```

Estima quantos veículos, dentre aqueles que estão no `Container,` podem realizar a travessia. A seguir, os veículos são retirados do `Container` por meio de um comando `get` com parâmetro no número de veículos a serem retirados.

Ao final, deve-se criar o `Container`, realizar as chamadas dos processos e executar o modelo por 4 horas \(ou 240 minutos\):

```python
random.seed(100)
env = simpy.Environment()

# container para representar a fila de automóveis aguardando a travessia
filaTravessia = simpy.Container(env)

# inicia o processo de controle do turno
env.process(turno(env,filaTravessia, 5))
env.process(chegadaVeiculos(env,filaTravessia))

env.run(until=240)
```

Quando executado, o modelo completo fornece como saída \(resultados compactados\):

```python
 0 A ponte está fechada =(
 5 A ponte está  aberta =) e fecha em  5 minutos
10 A ponte está fechada =(
...
225 A ponte está  aberta =) e fecha em  5 minutos
230 A ponte está fechada =(
230 Travessia de 50 veículos    Fila atual: 170
235 A ponte está  aberta =) e fecha em  5 minutos
```

Portanto, considerando-se as condições simuladas, o modelo indica que 170 veículos ainda estão em espera em fila ao final da última abertura da ponte dentro do horário de pico. Portanto, o tempo de abertura da ponte parece ser insuficiente durante o horário de pico.

> **Desafio 22:** para o sistema anterior, construa um gráfico para o número de veículos em fila em função do tempo de abertura da ponte para travessia de automóveis. Qual o tempo mínimo que você recomendaria de abertura da ponte.

Como o desafio deseja uma avaliação da fila ao final do horário de pico para diferentes valores de abertura da ponte, o primeiro passo é construir um laço para que o modelo possa ser executado para diferentes valores do tempo de abertura da ponte:

```python
# lista para armazenar o resultado do cenário simulado
resultado = []

for tempo_ponte in range(5, 10):
    random.seed(100)   
    env = simpy.Environment()

    # número de veículos não atendidos ao final da simulação    
    naoAtendidos = 0 

    # container para representar a fila de automóveis aguardando a travessia
    filaTravessia = simpy.Container(env)

    # inicia o processo de controle do turno
    env.process(turno(env,filaTravessia, tempo_ponte))
    env.process(chegadaVeiculos(env,filaTravessia))

    env.run(until=240)

    # arnazena o número de veículos do cenário atual em uma lista
    resultado.append((tempo_ponte, naoAtendidos))
```

Note, no código anterior, que foi criada uma lista, `resultado,` para armazenar o `tuple` com o tempo de abertura da ponte simulado e o resultado do número de veículos não atendidos ao final da simulação.

A função `ponteElevatoria` precisa de apenas de uma pequena modificação para assegurar que a variável global `naoAtendidos` receba corretamente o número de veículos não atendidos imediatamente após ao fechamento da ponte:

```python
def ponteElevatoria(env, filaTravessia):
    # opera a ponte elevatória
    global abrePonte, naoAtendidos

    print('%2.0f A ponte está fechada =(' %(env.now))
    # aguarda o evento para abertura da ponte
    tempoAberta = yield abrePonte
    print('%2.0f A ponte está  aberta =) e fecha em %2.0f minutos' 
            %(env.now, tempoAberta))

    # aguarda a chegada de mais veículos na fila de espera
    yield env.timeout(tempoAberta)    
    # calcula quantos veículos podem atravessar a ponte
    numVeiculos = min(int(tempoAberta*CAPACIDADE_TRAVESSIA), filaTravessia.level)
    # retira os veículos da fila
    filaTravessia.get(numVeiculos)
    # armazena o número de veículos não atendidos ao final da abertura da ponte
    naoAtendidos = filaTravessia.level
    print('%2.0f Travessia de %i veículos\tFila atual: %i' 
                %(env.now, numVeiculos, filaTravessia.level))
```

O próximo passo é acrescentar, ao final da simulação, um gráfico do número de veículos em função do tempo de abertura da ponte. Essa operação é facilitada pelo uso da biblioteca **matplotlib** no conjunto de dados armazenado na lista `resultado:`

```python
# lista para armazenar o resultado do cenário simulado
resultado = []

for tempo_ponte in range(5, 11):
    random.seed(100)

    env = simpy.Environment()

    # número de veículos não atendidos ao final da simulação
    naoAtendidos = 0

    # container para representar a fila de automóveis aguardando a travessia
    filaTravessia = simpy.Container(env)

    # inicia o processo de controle do turno
    env.process(turno(env,filaTravessia, tempo_ponte))
    env.process(chegadaVeiculos(env,filaTravessia))

    env.run(until=240)

    # arnazena o número de veículos do cenário atual em uma lista
    resultado.append((tempo_ponte, naoAtendidos))

import matplotlib.pyplot as plt

# descompacta os valores armazenados na lista resultado e plota em um gráfico de barras
plt.bar(*zip(*resultado), align='center')
plt.xlabel('Tempo de abertura da ponte (min)')
plt.ylabel('Número de veículos em espera ao final\nda última abertura da ponte')
plt.xlim(4.5,10.5)
plt.grid(True)
plt.show()
```

Quando executado, o modelo anterior fornece como resultado o seguinte gráfico:

![](../../.gitbook/assets/ponte_elevatoria.png)

Em uma primeira análise, portanto, o tempo de abertura de 7 minutos seria suficiente para atender aos veículos durante o horário de pico. Contudo, nossa análise está limitada a uma replicação apenas, o que torna a conclusão, eventualmente, precipitada \(veja o item 2 do tópico "Teste seus conhecimentos" a seguir\).

## Teste seus conhecimentos

1. Por que utilizamos na função `ponteElevatoria` a variável global `naoAtendidos?` Não seria suficiente armazenar na fila `resultados` diretamente o número de veículos no `Container` `filaTravessia,` pelo comando `filaTravessia.level?`
2. Como nos lembram Chiwf e Medina \(2014\): "nunca se deve tomar decisões baseadas em apenas uma replicação de um modelo de simulação". Afinal, basta modificar a semente geradora de número aleatórios, para que o resultado do gráfico seja outro \(teste no seu modelo!\). Modifique o modelo para que ele simule um número de replicações configurável para cada tempo de abertura da ponte. Adicionalmente, garanta que tempos de abertura diferentes utilizem a mesma sequencia de números aleatórios. \(Dica: para esta segunda parte, armazene as sementes geradoras em uma lista\).

 Chwif, L., and A. C. Medina. 2014. [Modelagem e Simulacão de Eventos Discretos: Teoria e Aplicacões](http://livrosimulacao.eng.br/msed-agora-no-formato-ebook/). 4ª ed. São Paulo: Elsevier Brasil.

