# Solução dos desafios 21 e 22
>**Desafio 21:** crie um processo de geração de automóveis que desejam cruzar a ponte, durante o horário de pico que dura 4 horas. O intervalo entre chegadas sucessivas de veículos para travessia é de 10 segundos (ou 6 veículos/min), exponencialmente distribuídos e a ponte permite a travessia de 5 veículos por minuto. Após 4 horas de operação, quantos veículos chegaram e não? 

Em relação ao modelo anterior, este novo sistema possui um processo de geração de chegadas de veículos e espera por abertura da ponte. Uma alternativa de implementação é utilizar um `Container` para amarzenar os veículos em espera pela abertura da ponte, como no codígo a seguir:
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
        abrePonte.succeed(value=tempo_ponte)
        # mantém a ponte aberta por 5 minutos
        yield env.timeout(tempo_ponte)
```
Note que o parâmetro `tempo_ponte` é enviado como um valor para a função `ponteElevatória`, que agora deve lidar com a travessia dos veículos quando aberta. Neste caso, basta um comando `get`  no `Container` que representa a fila de travessia dos veículos: 
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
    yield env.timeout(tempo_ponte)
    
    # calcula quantos veículos podem atravessar a ponte
    numVeiculos = min(int(tempoAberta*CAPACIDADE_TRAVESSIA), filaTravessia.level)
    
    # retira os veículos da fila
    filaTravessia.get(numVeiculos)
    print('%2.0f Travessia de %i veículos\tFila atual: %i' 
            %(env.now, numVeiculos, filaTravessia.level))
    # incrementa o número de veículos que estavam em fila e não foram atendidos nessa abertura
    naoAtendidos += filaTravessia.level
```
Analisando o código anterior, assim que a ponte abre, a linha:
```python
# calcula quantos veículos podem atravessar a ponte
numVeiculos = min(int(tempoAberta*CAPACIDADE_TRAVESSIA), filaTravessia.level)
```
Estima quantos veículos, dentre aqueles que estão no `Container,` podem realizar a travessia. A seguir, os veículos são retirados do `Container` por meio de um comando `get` com parâmetro no número de veículos a serem retirados.

Ao final, deve-se criar o `Container`, realizar as chamadas dos processos e executar o modelo por 4 horas (ou 240 minutos):
```python
env = simpy.Environment()

# número de veículos não atendidos durante a abertura da ponte)
naoAtendidos = 0

# container para representar a fila de automóveis aguardando a travessia
filaTravessia = simpy.Container(env)

# inicia o processo de controle do turno
env.process(turno(env,filaTravessia, 5))
env.process(chegadaVeiculos(env,filaTravessia))

env.run(until=240)
```
Quando executado, o modelo completo fornece como saída (resultados compactados):
```python
 0 A ponte está fechada =(
 5 A ponte está  aberta =) e fecha em  5 minutos
 5 Travessia de 25 veículos     Fila atual: 7
10 A ponte está fechada =(
...
225 A ponte está  aberta =) e fecha em  5 minutos
225 Travessia de 25 veículos    Fila atual: 795
230 A ponte está fechada =(
235 A ponte está  aberta =) e fecha em  5 minutos
235 Travessia de 25 veículos    Fila atual: 830

Número de veículos não atendidos no momento de abertura da ponte: 10149
```
Portanto, considerando-se as condições simuladas, o modelo indica que 830 veículos ainda estão em espera em fila ao final do período de pico e 10.149 veículos não foram atendidos na primeira abertura da ponte e tiveram (ou ainda terão) que aguardar 1 ou mais aberturas. Portanto, o tempo de abertura da ponte parece ser insuficiente no horário de pico.

>**Desafio 22:** Para o sistema anterior, construa um gráfico para o número de veículos em fila em função do tempo de abertura da ponte para travessia de automóveis. Qual o tempo mínimo que você recomendaria de abertura da ponte.

Como o desafio deseja 
```python

```

```python

```


```python

```


```python

```


```python

```
## Teste seus conhecimentos






