# Solução dos desafios 19 e 20

> **Desafio 19**: Considere, no primeiro exemplo, que o componente possui mais duas partes, C e D que devem ser previamente montadas entre si para, a seguir, serem encaixadas nas peças A e B. Os tempos de montagem são todos semlhantes. \(Dica: generalize a função `montagem` apresentada no exemplo\).

Para este desafio, não precisamos alterar o processo de chegadas, apenas vamos chamá-lo mais vezes, para as peças tipo A, B, C e D.   
Inicialmente, portanto, precisamos criar um `Container` para cada etapa da montagem, bem como chamar a função de geração de lotes para as 4 partes iniciais do componente:

```python
random.seed(100)            
env = simpy.Environment()

# cria estoques de peças
tipoList = ['A', 'B', 'C', 'D', 'AB', 'CD', 'ABCD']
pecasContainerDict = {}
for tipo in tipoList:
    pecasContainerDict[tipo] = simpy.Container(env)

# inicia processos de chegadas de pecas
for i in "ABCD":
    env.process(chegadaPecas(env, pecasContainerDict, i, 10))
```

O bacana desse desafio é explorar o potencial de _generalidade_ do SimPy, afinal, os processos de montagem são semelhantes, o que muda apenas é o quais as peças estão sendo unidas.  
Imagine por um momento, que podemos querer unir 3 ou mais peças. A lógica em si não é muito diferente daquela feita na seção anterior, muda apenas a necessidade de se lidar com um número de peças diferentes. Assim, para _generalizar_  a função `montagem`, proponho utilizar o operador [`**kwargs`](http://stackoverflow.com/questions/3394835/args-and-kwargs/3394898#3394898) que envia um conjunto de parâmetros para uma função como um dicionário.  
A ideia aqui é chamar o processo de montagem de maneira flexível, por exemplo:

```python
# inicia processos de montagem
env.process(montagem(env, pecasContainerDict, 'AB', A=1, B=2))
env.process(montagem(env, pecasContainerDict, 'CD', C=1, D=2))
env.process(montagem(env, pecasContainerDict, 'ABCD', AB=1, CD=1))
```

Estamos chamando a função montagem para diferentes configurações de peças a serem montadas. Por exemplo, a primeira linha representa uma montagem de uma peça A com duas B; a segunda uma peça C e duas D e a terceira linha representa uma peça do tipo AB com uma do tipo CB, formando o componente ABCD.

O código a seguir, apresenta uma solução que dá razoável generalidade para a função `montagem`:

```python
def montagem(env, pecasContainerDict, keyOut, **kwargs):
    # montagem do componente

    while True:
        # marca o instante em que a célula esta livre para a montagem
        chegada = env.now

        # pega uma peça de cada um dos items do dicionário kwargs
        for key, value in kwargs.items():
            yield pecasContainerDict[key].get(value)

        # armazena o tempo de espera por peças e inicia a montagem
        espera = env.now - chegada
        print("%5.1f Inicia montagem\t%s\tEspera: %4.1f" %(env.now, keyOut, espera))
        yield env.timeout(random.normalvariate(*TEMPO_MONTAGEM))
        # acumula componente montado no Container de saída keyOut
        yield pecasContainerDict[keyOut].put(1)
        print("%5.1f Fim da montagem\t%s\tEstoque: %i"
                %(env.now, keyOut, pecasContainerDict[keyOut].level))
```

No código anterior, os componentes montados são colocados no `Container` definido no parâmetro `keyOut` e, note como a parte relativa ao parâmetro `**kwargs` é tratada como um mero dicionário pelo Python.

O modelo de simulação completo do desafio 19 fica:

```python
import simpy
import random

TEMPO_CHEGADAS = [40, 50]       # intervalo entre chegadas de peças
TEMPO_MONTAGEM = [5, 1]         # tempo de montagem do componente

def chegadaPecas(env, pecasContainerDict, tipo, tamLote):
    # gera lotes de pecas em intervalos uniformemente distribuídos
    # encaminha para o estoque
    while True:
        pecasContainerDict[tipo].put(tamLote)
        print("%5.1f Chegada de lote\t%s\tPeças: %i"
                %(env.now, tipo, tamLote))
        yield env.timeout(random.uniform(*TEMPO_CHEGADAS))


def montagem(env, pecasContainerDict, keyOut, **kwargs):
    # montagem do componente

    while True:
        # marca o instante em que a célula esta livre para a montagem
        chegada = env.now

        # pega uma peça de cada um dos items do dicionário kwargs
        for key, value in kwargs.items():
            yield pecasContainerDict[key].get(value)

        # armazena o tempo de espera por peças e inicia a montagem
        espera = env.now - chegada
        print("%5.1f Inicia montagem\t%s\tEspera: %4.1f" %(env.now, keyOut, espera))
        yield env.timeout(random.normalvariate(*TEMPO_MONTAGEM))
        # acumula componente montado no Container de saída keyOut
        yield pecasContainerDict[keyOut].put(1)
        print("%5.1f Fim da montagem\t%s\tEstoque: %i"
                %(env.now, keyOut, pecasContainerDict[keyOut].level))

random.seed(100)            
env = simpy.Environment()

# cria estoques de peças
tipoList = ['A', 'B', 'C', 'D', 'AB', 'CD', 'ABCD']
pecasContainerDict = {}
for tipo in tipoList:
    pecasContainerDict[tipo] = simpy.Container(env)

# inicia processos de chegadas de pecas
for i in "ABCD":
    env.process(chegadaPecas(env, pecasContainerDict, i, 10))

# inicia processos de montagem
env.process(montagem(env, pecasContainerDict, 'AB', A=1, B=2))
env.process(montagem(env, pecasContainerDict, 'CD', C=1, D=2))
env.process(montagem(env, pecasContainerDict, 'ABCD', AB=1, CD=1))

env.run(until=40)
```

Quando executado por apenas 40 minutos, o modelo anterior fornece como saída:

```python
  0.0 Chegada de lote   A       Peças: 10
  0.0 Chegada de lote   B       Peças: 10
  0.0 Chegada de lote   C       Peças: 10
  0.0 Chegada de lote   D       Peças: 10
  0.0 Inicia montagem   AB      Espera:  0.0
  0.0 Inicia montagem   CD      Espera:  0.0
  5.7 Fim da montagem   AB      Estoque: 1
  5.7 Inicia montagem   AB      Espera:  0.0
  6.1 Fim da montagem   CD      Estoque: 0
  6.1 Inicia montagem   ABCD    Espera:  6.1
  6.1 Inicia montagem   CD      Espera:  0.0
  9.4 Fim da montagem   AB      Estoque: 1
  9.4 Inicia montagem   AB      Espera:  0.0
  9.7 Fim da montagem   CD      Estoque: 1
  9.7 Inicia montagem   CD      Espera:  0.0
 12.3 Fim da montagem   ABCD    Estoque: 1
 12.3 Inicia montagem   ABCD    Espera:  0.0
 13.8 Fim da montagem   AB      Estoque: 1
 13.8 Inicia montagem   AB      Espera:  0.0
 13.9 Fim da montagem   CD      Estoque: 1
 13.9 Inicia montagem   CD      Espera:  0.0
 18.2 Fim da montagem   ABCD    Estoque: 2
 18.2 Inicia montagem   ABCD    Espera:  0.0
 19.2 Fim da montagem   CD      Estoque: 1
 19.2 Inicia montagem   CD      Espera:  0.0
 19.4 Fim da montagem   AB      Estoque: 1
 19.4 Inicia montagem   AB      Espera:  0.0
 21.8 Fim da montagem   ABCD    Estoque: 3
 21.8 Inicia montagem   ABCD    Espera:  0.0
 25.2 Fim da montagem   CD      Estoque: 1
 25.3 Fim da montagem   AB      Estoque: 1
 26.6 Fim da montagem   ABCD    Estoque: 4
 26.6 Inicia montagem   ABCD    Espera:  0.0
 34.5 Fim da montagem   ABCD    Estoque: 5
```

> **Desafio 20**: Nos exemplos anteriores, os processos de montagem são paralelos. Considere que existe apenas um montador compartilhado para todos processos. Generalize a função montagem do desafio anterior, de modo que ela receba como parâmetro o respectivo recurso utilizado no processo.  
> Neste desafio precisamos apenas garantir que a função `montagem` receba como parâmetro o respectivo recurso a ser utilizado no processo:

```python
def montagem(env, pecasContainerDict, montador, keyOut, **kwargs):
    # montagem do componente

    while True:
        # marca o instante em que a célula esta livre para a montagem
        with montador.request() as req:
            # ocupa o recurso montador
            yield req
            chegada = env.now
            # pega uma peça de cada um dos items do dicionário kwargs
            for key, value in kwargs.items():
                yield pecasContainerDict[key].get(value)

            # armazena o tempo de espera por peças e inicia a montagem
            espera = env.now - chegada
            print("%5.1f Inicia montagem\t%s\tEspera: %4.1f"
                    %(env.now, keyOut, espera))
            yield env.timeout(random.normalvariate(*TEMPO_MONTAGEM))
            # acumula componente montado no Container de saída keyOut
            yield pecasContainerDict[keyOut].put(1)
            print("%5.1f Fim da montagem\t%s\tEstoque: %i"
                    %(env.now, keyOut, pecasContainerDict[keyOut].level))
```

Repare que a saída de tempo de espera que a função fornece é, na verdade, o tempo de espera do _montador_ e não o tempo de espera em fila pelo recurso \(veja o tópico "Teste seus conhecimentos" a seguir\).

A chamada de execução do modelo não é muito diferente do desafio anterior, apenas precisamos criar um recurso único que realiza todos os processos:

```python
random.seed(100)            
env = simpy.Environment()

# cria estoques de peças
tipoList = ['A', 'B', 'C', 'D', 'AB', 'CD', 'ABCD']
pecasContainerDict = {}
for tipo in tipoList:
    pecasContainerDict[tipo] = simpy.Container(env)


# inicia processos de chegadas de pecas
for i in "ABCD":
    env.process(chegadaPecas(env, pecasContainerDict, i, 10))

# cria os recursos de montagem
montador = simpy.Resource(env, capacity=1)

# inicia processos de montagem
env.process(montagem(env, pecasContainerDict, montador, 'AB', A=1, B=2))
env.process(montagem(env, pecasContainerDict, montador,'CD', C=1, D=2))
env.process(montagem(env, pecasContainerDict, montador,'ABCD', AB=1, CD=1))

env.run(until=40)
```

Quando o modelo anterior é executado por apenas 40 minutos, temos como saída:

```python
  0.0 Chegada de lote   A       Peças: 10
  0.0 Chegada de lote   B       Peças: 10
  0.0 Chegada de lote   C       Peças: 10
  0.0 Chegada de lote   D       Peças: 10
  0.0 Inicia montagem   AB      Espera:  0.0
  5.7 Fim da montagem   AB      Estoque: 1
  5.7 Inicia montagem   CD      Espera:  0.0
 11.8 Fim da montagem   CD      Estoque: 1
 11.8 Inicia montagem   ABCD    Espera:  0.0
 15.5 Fim da montagem   ABCD    Estoque: 1
 15.5 Inicia montagem   AB      Espera:  0.0
 21.6 Fim da montagem   AB      Estoque: 1
 21.6 Inicia montagem   CD      Espera:  0.0
 25.2 Fim da montagem   CD      Estoque: 1
 25.2 Inicia montagem   ABCD    Espera:  0.0
 29.6 Fim da montagem   ABCD    Estoque: 2
 29.6 Inicia montagem   AB      Espera:  0.0
 33.8 Fim da montagem   AB      Estoque: 1
 33.8 Inicia montagem   CD      Espera:  0.0
 39.7 Fim da montagem   CD      Estoque: 1
 39.7 Inicia montagem   ABCD    Espera:  0.0
```

Note como a produção de componentes ABCD caiu de 5 peças no peças no desafio 19, para apenas 2 neste desafio. Isso é naturalmente explicado, pois agora os processos não são mais paralelos e devem ser executados por um único montador.

## Teste seus conhecimentos

1. Acrescente o cálculo do tempo médio em espera por fila de montador ao modelo do desafio 20;
2. Acrescente o cálculo do WIP - _Work In Progress_ do processo ou o _trabalho em andamento_, isto é, quantas peças estão em produção ao longo do tempo de simulação;
3. Utilize a biblioteca [matplotlib](http://matplotlib.org/) e construa um gráfico para evolução do estoque de cada peça ao longo da simulação, bem como do WIP.



