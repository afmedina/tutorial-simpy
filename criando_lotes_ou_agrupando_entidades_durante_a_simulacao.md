# Criando lotes (ou agrupando) entidades durante a simulação

Uma situação bastante comum em modelos de simulação é o agrupamento de entidades em lotes ou o seu oposto: o desmembramento de um lote em diversas entidades separadas. É usual em softwares de simulação proprietários existir um comando (ou bloco) específico para isso. Por exemplo, o Arena possui o "Batch/Separate", o Simul8 o "Batching" etc.

Vamos partir de um exemplo simples, em que uma célula de produção deve realizar a tarefa de montagem de um certo componente a partir do encaixe de uma peça A com duas peças B. O operador da célula leva em média 5 minutos para montar o componente, segundo uma distribuição normal com desvio padrão de 1 minuto. Os processos de chegadas dos lotes A e B são distintos entre si, com tempos entre chegadas sucessivas uniformemente distribuidos no intervalo entre 40 a 60 minutos.

## Uma tática para agrupamento de lotes utilizando o `Container`

Uma maneira de resolver o problema é criar um `Container` de estoque temporário para cada peça. Assim, criamos dois estoques, respectivamente para as peças A e B, de modo que o componente só poderá iniciar sua montagem se cada estoque contiver ao menos o número de peças necessárias para sua montagem.

Comecemos criando uma possível máscara para o problema:
```python
import simpy
import random

TEMPO_CHEGADAS = [40, 50]       # intervalo entre chegadas de peças
TEMPO_MONTAGEM = [5, 1]         # tempo de montagem do componente
componentesProntos = 0          # variável para o total de componentes produzidos

def chegadaPecas(env, pecasContainerDict, tipo, tamLote):
    # gera lotes de pecas em intervalos uniformemente distribuídos
    # encaminha para o estoque
    pass
        
def montagem(env, pecasContainerDict, numA, numB):
    # montagem do componente
    global componentesProntos
    pass
    
random.seed(100)            
env = simpy.Environment()

# cria estoques de peças 
pecasContainerDict = {}
pecasContainerDict['A'] = simpy.Container(env)
pecasContainerDict['B'] = simpy.Container(env)

# inicia processos de chegadas de pecas
env.process(chegadaPecas(env, pecasContainerDict, 'A', 10))
env.process(chegadaPecas(env, pecasContainerDict, 'B', 10))

# inicia processo de montagem
env.process(montagem(env, pecasContainerDict, 1, 2))
env.run(until=80)   
```
Na máscara anterior, foram criadas duas funções: `chegaPecas`, que gera os lotes de peças A e B e armazena nos respectivos estoques e `montagem`, que retira as peças do estoque e montam o componente.

Note que criei um dicionário no Python: `pecasContainerDict`, para armazenar o `Container` de cada peça:
```python
# cria estoques de peças 
pecasContainerDict = {}
pecasContainerDict['A'] = simpy.Container(env)
pecasContainerDict['B'] = simpy.Container(env)
```
A função de geração de peças de fato, gera lotes e armazena dentro do Container o número de peças do lote:

```python
def chegadaPecas(env, pecasContainerDict, tipo, tamLote):
    # gera lotes de pecas em intervalos uniformemente distribuídos
    # encaminha para o estoque
    while True:
        pecasContainerDict[tipo].put(tamLote)
        print("%5.1f Chegada de lote\t%s\tPeças: %i"
                %(env.now, tipo, tamLote))
        yield env.timeout(random.uniform(*TEMPO_CHEGADAS))
```
Note que, diferentemente das funções de geração de entidades criadas nas seções anteriores deste livro, a função `chegadaPecas` não encaminha a entidade criada para uma nova função, iniciando um novo processo (de atendimento, por exemplo). A função apenas armazena uma certa quantidade de peças, `tamLote,` dentro do respectivo ```Container```  na linha:
```python
pecasContainerDict[tipo].put(tamLote)
```
O processo de montagem também recorre ao artifício de um laço infinito, pois, basicamente, representa uma operação que está sempre pronta para executar a montagem, desde que existam o número de peças mínimas à disposição nos respectivos estoques:

```python
def montagem(env, pecasContainerDict, numA, numB):
    # montagem do componente
    global componentesProntos
    while True:
        # marca o instante em que a célula esta livre para a montagem
        chegada = env.now
        yield pecasContainerDict['A'].get(numA)
        yield pecasContainerDict['B'].get(numB)
        # armazena o tempo de espera por peças e inicia a montagem
        espera = env.now - chegada
        print("%5.1f Inicia montagem\tEstoque A: %i\tEstoque B: %i\tEspera: %4.1f"
                %(env.now, pecasContainerDict['A'].level, pecasContainerDict['B'].level, espera))
        yield env.timeout(random.normalvariate(*TEMPO_MONTAGEM))
        # acumula componente montado
        componentesProntos += 1
        print("%5.1f Fim da montagem\tEstoque A: %i\tEstoque B: %i\tComponentes: %i\t"
            %(env.now, pecasContainerDict['A'].level, pecasContainerDict['B'].level,
              componentesProntos))
```
A parte central da função anterior é garantir que o processo só possa se iniciar caso existam peças suficientes para o componente final. Isto é garantido pelo comando ```get``` aplicado a cada ```Container``` de peças necessárias:
```python
        yield pecasContainerDict['A'].get(numA)
        yield pecasContainerDict['B'].get(numB)
```
 Quando executado, o modelo completo fornece como saída:
```python
  0.0 Chegada de lote   tipo A: +10 peças
  0.0 Chegada de lote   tipo B: +10 peças
  0.0 Inicia montagem   Estoque A: 9    Estoque B: 8    Espera:  0.0
  6.6 Fim da montagem   Estoque A: 9    Estoque B: 8    Componentes: 1  
  6.6 Inicia montagem   Estoque A: 8    Estoque B: 6    Espera:  0.0
 12.3 Fim da montagem   Estoque A: 8    Estoque B: 6    Componentes: 2  
 12.3 Inicia montagem   Estoque A: 7    Estoque B: 4    Espera:  0.0
 18.4 Fim da montagem   Estoque A: 7    Estoque B: 4    Componentes: 3  
 18.4 Inicia montagem   Estoque A: 6    Estoque B: 2    Espera:  0.0
 22.1 Fim da montagem   Estoque A: 6    Estoque B: 2    Componentes: 4  
 22.1 Inicia montagem   Estoque A: 5    Estoque B: 0    Espera:  0.0
 28.2 Fim da montagem   Estoque A: 5    Estoque B: 0    Componentes: 5  
 41.5 Chegada de lote   tipo A: +10 peças
 44.5 Chegada de lote   tipo B: +10 peças
 44.5 Inicia montagem   Estoque A: 14   Estoque B: 8    Espera: 16.3
 48.9 Fim da montagem   Estoque A: 14   Estoque B: 8    Componentes: 6  
 48.9 Inicia montagem   Estoque A: 13   Estoque B: 6    Espera:  0.0
 53.1 Fim da montagem   Estoque A: 13   Estoque B: 6    Componentes: 7  
 53.1 Inicia montagem   Estoque A: 12   Estoque B: 4    Espera:  0.0
 59.1 Fim da montagem   Estoque A: 12   Estoque B: 4    Componentes: 8  
 59.1 Inicia montagem   Estoque A: 11   Estoque B: 2    Espera:  0.0
 64.7 Fim da montagem   Estoque A: 11   Estoque B: 2    Componentes: 9  
 64.7 Inicia montagem   Estoque A: 10   Estoque B: 0    Espera:  0.0
 70.0 Fim da montagem   Estoque A: 10   Estoque B: 0    Componentes: 10 
```
O que o leitor deve ter achado interessante é o modo passivo da função `montagem` que, por meio de um laço infinito `while True` aguarda o aparecimento de peças suficientes nos estoques para iniciar a montagem. Interessante também é notar que não alocamos recursos para a operação e isso significa que o modelo de simulação atual não permite a montagem simultânea de componentes (veja o tópico "Teste seus conhecimentos" na próxima seção).

##Agrupando lotes por atributo da entidade utilizando o `FilterStore`

Outra situação bastante comum em modelos de simulação é quando precisamos agrupar entidades por atributo. Por exemplo, os componentes anteriores são de duas cores: brancos ou verdes, de modo que a célula de montagem agora deve pegar peças A e B com as cores corretas.

Como agora existe um atributo (no caso, cor) que diferencia uma peça da outra, precisaremos de um ```FilterStore```, para garantir a escolha certa da peça no estoque. Contudo, devemos lembrar que o `FilterStore`, diferentemente do `Container`, não permite que se armazene ou retire múltiplos objetos ao mesmo tempo. O comando `put` (ou mesmo o `get),` é limitado a um objeto por vez. Por fim, a montagem do componente agora é pelo atributo "cor", o que significa que a função `montagem` deve ser chamada uma vez para cada valor do atributo (no caso duas vezes: "branco" ou "verde").
De modo semelhante ao exemplo anterior, uma máscara para o problema seria:
```python
import simpy
import random

TEMPO_CHEGADAS = [40, 50]       # intervalo entre chegadas de peças
TEMPO_MONTAGEM = [5, 1]         # tempo de montagem do componente
componentesProntos = 0          # variável para o total de componentes produzidos

def chegadaPecas(env, pecasFilterStoreDict, tipo, tamLote):
    # gera lotes de pecas em intervalos uniformemente distribuídos
    # sorteia a cor das peças
    # coloca um número tamLote de peças dentro do FilterStore
    pass
        
def montagem(env, pecasFilterStoreDict, numA, numB, cor):
    # montagem do componente
    global componentesProntos
    pass
    
random.seed(100)            
env = simpy.Environment()

# cria um dicionário para armazenar os FilterStore
pecasFilterStoreDict = {}
pecasFilterStoreDict['A'] = simpy.FilterStore(env)
pecasFilterStoreDict['B'] = simpy.FilterStore(env)

# inicia processos de chegadas de pecas
env.process(chegadaPecas(env, pecasFilterStoreDict, 'A', 10))
env.process(chegadaPecas(env, pecasFilterStoreDict, 'B', 10))

# inicia processos de montagem de pecas
env.process(montagem(env, pecasFilterStoreDict, 1, 2, 'branco'))
env.process(montagem(env, pecasFilterStoreDict, 1, 2, 'verde'))

env.run(until=80) 
```
Note que foi criado um dicionário `pecasFilterStore` armazena um `FilterStore` para cada tipo de peça. 
Vamos agora construir a função `chegadaPecas`, considerando que ela deve sortear a cor do lote de peças e enviar todas as peças do lote (uma por vez) para o respectivo `FilterStore.`
Para sortear a cor do lote, uma opção é utilizar o comando [random.choice](https://docs.python.org/3/library/random.html#random.choice), enquanto o envio de múltiplas peças para o `FilterStore` pode ser feito por um laço `for,` como mostra o código a seguir:
```python
def chegadaPecas(env, pecasFilterStoreDict, tipo, tamLote):
    # gera lotes de pecas em intervalos uniformemente distribuídos
    while True:
        # sorteia a cor das peças
        cor = random.choice(("branco", "verde"))
        # coloca um número tamLote de peças dentro do FilterStore
        for i in range(tamLote):
            yield pecasFilterStoreDict[tipo].put(cor)
        print("%5.1f Chegada de lote\ttipo: %s\t\tCor: %s"
                %(env.now, tipo, cor))
        yield env.timeout(random.uniform(*TEMPO_CHEGADAS))
```

A função `montagem,` de modo semelhante a função anterior, é formada por um laço infinito do tipo `while True`, mas deve retirar múltiplas peças de cada estoque, respeitando o atributo "cor". O código a seguir, soluciona este problema novamente com laços do tipo `for` e uma função anônima para buscar a cor correta da peça dentro do `FilterStore:`
```python
def montagem(env, pecasFilterStoreDict, numA, numB, cor):
    # montagem do componente
    global componentesProntos
    
    while True:
        # marca o instante em que a célula está livre para a montagem
        chegada = env.now
        for i in range(numA):
            yield pecasFilterStoreDict['A'].get(lambda c: c==cor)
        for i in range(numB):
            yield pecasFilterStoreDict['B'].get(lambda c: c==cor)
        # armazena o tempo de espera por peças e inicia a montagem
        espera = env.now - chegada
        print("%5.1f Inicia montagem\tCor: %s\tEspera: %4.1f"
                %(env.now, cor, espera))
        yield env.timeout(random.normalvariate(*TEMPO_MONTAGEM))
        # acumula componente montado
        componentesProntos += 1
        print("%5.1f Fim da montagem\tCor: %s\tComponentes: %i\tEstoque A: %i\tEstoque B: %i"
            %(env.now, cor, componentesProntos,  len(pecasFilterStoreDict['A'].items), 
              len(pecasFilterStoreDict['B'].items)))
```
Dois pontos merecem destaque na função anterior:
1. A função `montagem`, deve ser chamada duas vezes na inicialização da simulação, uma para cada cor. Isto significa que nossa implementação permite a montagem simultânea de peças de cores diferentes. Caso seja necessário contornar este problema, basta a criação de um recurso "montador" (veja o tópico "Teste seus conhecimentos" na próxima seção";
2. Na última linha, para contabilizar o total de peças ainda em estoque, como o `FilterStore` não possui um método `.level,` utilizou-se a função `len()` aplicada a todos os `items` do `FilterStore.`

Quando executado por apenas 80 minutos, o programa anterior fornece como saída:
```python
  0.0 Chegada de lote   tipo: A         Cor: branco
  0.0 Chegada de lote   tipo: B         Cor: verde
 44.5 Inicia montagem   Cor: verde      Espera: 44.5
 44.5 Chegada de lote   tipo: A         Cor: verde
 47.7 Inicia montagem   Cor: branco     Espera: 47.7
 47.7 Chegada de lote   tipo: B         Cor: branco
 50.3 Fim da montagem   Cor: verde      Componentes: 1  Estoque A: 18   Estoque B: 16
 50.3 Inicia montagem   Cor: verde      Espera:  0.0
 51.4 Fim da montagem   Cor: branco     Componentes: 2  Estoque A: 17   Estoque B: 14
 51.4 Inicia montagem   Cor: branco     Espera:  0.0
 54.8 Fim da montagem   Cor: verde      Componentes: 3  Estoque A: 16   Estoque B: 12
 54.8 Inicia montagem   Cor: verde      Espera:  0.0
 57.0 Fim da montagem   Cor: branco     Componentes: 4  Estoque A: 15   Estoque B: 10
 57.0 Inicia montagem   Cor: branco     Espera:  0.0
 59.2 Fim da montagem   Cor: verde      Componentes: 5  Estoque A: 14   Estoque B: 8
 59.2 Inicia montagem   Cor: verde      Espera:  0.0
 61.3 Fim da montagem   Cor: branco     Componentes: 6  Estoque A: 13   Estoque B: 6
 61.3 Inicia montagem   Cor: branco     Espera:  0.0
 64.6 Fim da montagem   Cor: branco     Componentes: 7  Estoque A: 12   Estoque B: 4
 64.6 Inicia montagem   Cor: branco     Espera:  0.0
 65.9 Fim da montagem   Cor: verde      Componentes: 8  Estoque A: 11   Estoque B: 2
 65.9 Inicia montagem   Cor: verde      Espera:  0.0
 68.8 Fim da montagem   Cor: branco     Componentes: 9  Estoque A: 10   Estoque B: 0
 71.1 Fim da montagem   Cor: verde      Componentes: 10 Estoque A: 9    Estoque B: 0   
```
Naturalmente, existem outras soluções, mas optei por um caminho que mostrasse algumas limitações para um problema bastante comum em modelos de simulação. 

>**Desafio 19**: Considere, no primeiro exemplo, que o componente possui mais duas partes, C e D que devem ser previamente montadas entre si para, a seguir, serem encaixadas nas peças A e B. Os tempos de montagem são todos semlhantes. (Dica: generalize a função `montagem` apresentada no exemplo).  

>**Desafio 20**: Nos exemplos anteriores, os processos de montagem são paralelos. Considere que existe apenas um montador compartilhado para todos processos. Generalize a função montagem do desafio anterior, de modo que ela receba como parâmetro o respectivo recurso utilizado no processo.