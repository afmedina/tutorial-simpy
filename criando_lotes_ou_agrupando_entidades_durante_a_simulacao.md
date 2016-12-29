# Criando lotes (ou agrupando) entidades durante a simulação

Uma situação bastante comum em modelos de simulação é o agrupamento de entidades em lotes ou o seu oposto: o desmembramento de um lote em diversas entidades separadas. É usual em softwares de simulação proprietários existir um comando (ou bloco) específico para isso. Por exemplo, o Arena possui o "Batch/Separate", o Simul8 o "Batching" etc.

Vamos partir de um exemplo simples, em que uma célula de produção deve realizar a tarefa de montagem de um certo componente a partir do encaixe de 1 peça A com duas peças B. O operador da célula leva em média 5 minutos para montar o componente, segundo uma distribuição normal com desvio padrão de 1 minuto. Os processos de chegadas dos lotes A e B são distintos entre si, com tempos entre chegadas sucessivas uniformemente distribuidos no intervalo de 40 a 60 minutos.

## Uma tática para agrupamento de lotes: utilizar o `Container`

Uma maneira de resolver o problema é criar um `Container` de estoque temporário para cada peça. Assim, criamos dois estoques, para as peças A e B, de modo que o componente só poderá iniciar sua montagem se cada estoque contiver ao menos o número de peças necessárias para sua montagem.

Comecemos criando uma possível máscara para o problema:
```python
import simpy
import random

TEMPO_CHEGADAS = [40, 50]       # intervalo entre chegadas de peças
TEMPO_MONTAGEM = [5, 1]         # intervalo entre chegadas de peças
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

#cria estoques de peças 
pecasContainerDict = {}
pecasContainerDict['A'] = simpy.Container(env)
pecasContainerDict['B'] = simpy.Container(env)

# inicia processos de chegadas de pecas
env.process(chegadaPecas(env, pecasContainerDict, 'A', 10))
env.process(chegadaPecas(env, pecasContainerDict, 'B', 10))
# inicia processo de montagem
env.process(montagem(env, pecasContainerDict, 1, 2))
env.run(until = 80)   
```
Na máscara anterior, foram criadas duas funções: ```chegaPecas```, que gera os lotes de peças A e B e armazena nos respectivos estoques e ```montagem```, que retira as peças do estoque e montam o componente.

Note que criei um dicionário no Python: ```pecasContainerDict```, para armazenar o ```Container``` de cada peça:
```python
#cria estoques de peças 
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
        print("%5.1f Chegada de lote tipo %s: +%i peças."
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
        print("%5.1f Inicia montagem.\tEstoque A: %i\tEstoque B: %i\tEspera: %4.1f"
                %(env.now, pecasContainerDict['A'].level, pecasContainerDict['B'].level, espera))
        yield env.timeout(random.normalvariate(*TEMPO_MONTAGEM))
        # acumula componente montado
        componentesProntos += 1
        print("%5.1f Fim da montagem.\tEstoque A: %i\tEstoque B: %i\tComponentes: %i\t"
            %(env.now, pecasContainerDict['A'].level, pecasContainerDict['B'].level,
              componentesProntos))
```
A parte central da função anterior é garantir que o processo só possa se iniciar caso existam peças suficientes para o componente final. Isto é garantido pelo comando ```get``` aplicado a cada ```Container``` de peças necessárias:
```python
        yield pecasContainerDict['A'].get(numA)
        yield pecasContainerDict['B'].get(numB)
```
O modelo completo em SimPy da nossa célula de montagem, fica:
```python
import simpy
import random

TEMPO_CHEGADAS = [40, 50]       # intervalo entre chegadas de peças
TEMPO_MONTAGEM = [5, 1]         # intervalo entre chegadas de peças
componentesProntos = 0          # variável para o total de componentes produzidos

def chegadaPecas(env, pecasContainerDict, tipo, tamLote):
    # gera lotes de pecas em intervalos uniformemente distribuídos
    # encaminha para o estoque
    while True:
        pecasContainerDict[tipo].put(tamLote)
        print("%5.1f Chegada de lote tipo %s: +%i peças."
                %(env.now, tipo, tamLote))
        yield env.timeout(random.uniform(*TEMPO_CHEGADAS))

        
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
        print("%5.1f Inicia montagem.\tEstoque A: %i\tEstoque B: %i\tEspera: %4.1f"
                %(env.now, pecasContainerDict['A'].level, pecasContainerDict['B'].level, espera))
        yield env.timeout(random.normalvariate(*TEMPO_MONTAGEM))
        # acumula componente montado
        componentesProntos += 1
        print("%5.1f Fim da montagem.\tEstoque A: %i\tEstoque B: %i\tComponentes: %i\t"
            %(env.now, pecasContainerDict['A'].level, pecasContainerDict['B'].level,
              componentesProntos))
    
random.seed(100)            
env = simpy.Environment()

#cria estoques de peças 
pecasContainerDict = {}
pecasContainerDict['A'] = simpy.Container(env)
pecasContainerDict['B'] = simpy.Container(env)

# inicia processos de chegadas de pecas
env.process(chegadaPecas(env, pecasContainerDict, 'A', 10))
env.process(chegadaPecas(env, pecasContainerDict, 'B', 10))
# inicia processo de montagem
env.process(montagem(env, pecasContainerDict, 1, 2))
env.run(until = 80)   
```
Quando executado, o modelo anterior fornece como saída:
```python
  0.0 Chegada de lote tipo A: +10 peças.
  0.0 Chegada de lote tipo B: +10 peças.
  0.0 Inicia montagem.  Estoque A: 9    Estoque B: 8    Espera:  0.0
  6.6 Fim da montagem.  Estoque A: 9    Estoque B: 8    Componentes: 1  
  6.6 Inicia montagem.  Estoque A: 8    Estoque B: 6    Espera:  0.0
 12.3 Fim da montagem.  Estoque A: 8    Estoque B: 6    Componentes: 2  
 12.3 Inicia montagem.  Estoque A: 7    Estoque B: 4    Espera:  0.0
 18.4 Fim da montagem.  Estoque A: 7    Estoque B: 4    Componentes: 3  
 18.4 Inicia montagem.  Estoque A: 6    Estoque B: 2    Espera:  0.0
 22.1 Fim da montagem.  Estoque A: 6    Estoque B: 2    Componentes: 4  
 22.1 Inicia montagem.  Estoque A: 5    Estoque B: 0    Espera:  0.0
 28.2 Fim da montagem.  Estoque A: 5    Estoque B: 0    Componentes: 5  
 41.5 Chegada de lote tipo A: +10 peças.
 44.5 Chegada de lote tipo B: +10 peças.
 44.5 Inicia montagem.  Estoque A: 14   Estoque B: 8    Espera: 16.3
 48.9 Fim da montagem.  Estoque A: 14   Estoque B: 8    Componentes: 6  
 48.9 Inicia montagem.  Estoque A: 13   Estoque B: 6    Espera:  0.0
 53.1 Fim da montagem.  Estoque A: 13   Estoque B: 6    Componentes: 7  
 53.1 Inicia montagem.  Estoque A: 12   Estoque B: 4    Espera:  0.0
 59.1 Fim da montagem.  Estoque A: 12   Estoque B: 4    Componentes: 8  
 59.1 Inicia montagem.  Estoque A: 11   Estoque B: 2    Espera:  0.0
 64.7 Fim da montagem.  Estoque A: 11   Estoque B: 2    Componentes: 9  
 64.7 Inicia montagem.  Estoque A: 10   Estoque B: 0    Espera:  0.0
 70.0 Fim da montagem.  Estoque A: 10   Estoque B: 0    Componentes: 10 
```
##Agrupando lotes por atributo da entidade

Outra situação bastante comum em modelos de simulação é quando precisamos agrupar entidades por atributo. Por exemplo, os componentes anteriores são de duas cores: brancos ou verdes, de modo que a célula de montagem agora deve pegar peças A e B com as cores corretas.

Como agora existe um atributo (no caso, cor) que diferencia uma peça da outra, precisaremos de um ```FilterStore```, para garantir a escolha certa da peça no estoque. Adicionalmente - e isso não é algo trivial de se compreender - a função ```montagem``` não pode ser mais *passiva*, no sentido que aguarda as peças no estoque, como no exemplo anterior. Precisamo criar processos para que cada peça A que chega ao estoque inicie a busca uma peça B que tenha a mesma cor.

Neste caso, a chegada de peças deve sortear uma cor. No exemplo seguinte, a cor é sorteada pelo comando ```[random.choice](https://docs.python.org/3/library/random.html#random.choice)```:
```python
def chegadaPecas(env, pecasFilterStoreDict, tipo):
    # gera lotes de pecas em intervalos uniformemente distribuídos
    # encaminha para o estoque
    while True:
        # sorteia a cor das peças
        cor = random.choice(("branco", "verde"))
        yield pecasFilterStoreDict[tipo].put(cor)
        print("%5.1f Chegada de peça tipo %s.\tCor: %s."
                %(env.now, tipo, cor))
        if tipo == 'A':
            # inicia processo de montagem
            env.process(montagem(env, cor, pecasFilterStoreDict))
        yield env.timeout(random.uniform(*TEMPO_CHEGADAS))
```
Note, na função anterior, que sempre que a peça por do tipo 'A', é iniciado um novo processo de montagem. Portanto, toda peça A que chega ao estoque inicia um processo de montagem.

A função montagem, a seguir, faz uma busca pelas peças A e B da mesma cor:
```python
def montagem(env, cor, pecasFilterStoreDict):
    # montagem do componente
    global componentesProntos
    while True:
        # marca o instante em que a célula está livre para a montagem
        chegada = env.now
        yield pecasFilterStoreDict['A'].get(lambda c: c==cor)
        yield pecasFilterStoreDict['B'].get(lambda c: c==cor)
        # armazena o tempo de espera por peças e inicia a montagem
        espera = env.now - chegada
        print("%5.1f Inicia montagem.\t\tCor: %s\tEspera: %4.1f"
                %(env.now, cor, espera))
        yield env.timeout(random.normalvariate(*TEMPO_MONTAGEM))
        # acumula componente montado
        componentesProntos += 1
        print("%5.1f Fim da montagem.\t\tCor: %s\tComponentes: %i\t"
            %(env.now, cor, componentesProntos))
```
Finalizando, precisamos criar o Environment, um FilterStore para cada tipo de peça e chamar a execução do modelo:
```python
random.seed(100)            
env = simpy.Environment()

#cria estoques de peças 
pecasFilterStoreDict = {}
pecasFilterStoreDict['A'] = simpy.FilterStore(env)
pecasFilterStoreDict['B'] = simpy.FilterStore(env)

# inicia processos de chegadas de pecas
env.process(chegadaPecas(env, pecasFilterStoreDict, 'A'))
env.process(chegadaPecas(env, pecasFilterStoreDict, 'B'))

env.run(until = 80) 
```
O modelo completo ficaria:
```python
import simpy
import random

TEMPO_CHEGADAS = [40, 50]       # intervalo entre chegadas de peças
TEMPO_MONTAGEM = [5, 1]         # intervalo entre chegadas de peças

componentesProntos = 0          # variável para o total de componentes produzidos

def chegadaPecas(env, pecasFilterStoreDict, tipo):
    # gera lotes de pecas em intervalos uniformemente distribuídos
    # encaminha para o estoque
    while True:
        # sorteia a cor das peças
        cor = random.choice(("branco", "verde"))
        yield pecasFilterStoreDict[tipo].put(cor)
        print("%5.1f Chegada de peça tipo %s.\tCor: %s."
                %(env.now, tipo, cor))
        if tipo == 'A':
            # inicia processo de montagem
            env.process(montagem(env, cor, pecasFilterStoreDict))
        yield env.timeout(random.uniform(*TEMPO_CHEGADAS))

        
def montagem(env, cor, pecasFilterStoreDict):
    # montagem do componente
    global componentesProntos
    while True:
        # marca o instante em que a célula está livre para a montagem
        chegada = env.now
        yield pecasFilterStoreDict['A'].get(lambda c: c==cor)
        yield pecasFilterStoreDict['B'].get(lambda c: c==cor)
        # armazena o tempo de espera por peças e inicia a montagem
        espera = env.now - chegada
        print("%5.1f Inicia montagem.\t\tCor: %s\tEspera: %4.1f"
                %(env.now, cor, espera))
        yield env.timeout(random.normalvariate(*TEMPO_MONTAGEM))
        # acumula componente montado
        componentesProntos += 1
        print("%5.1f Fim da montagem.\t\tCor: %s\tComponentes: %i\t"
            %(env.now, cor, componentesProntos))
    
random.seed(100)            
env = simpy.Environment()

#cria estoques de peças 
pecasFilterStoreDict = {}
pecasFilterStoreDict['A'] = simpy.FilterStore(env)
pecasFilterStoreDict['B'] = simpy.FilterStore(env)

# inicia processos de chegadas de pecas
env.process(chegadaPecas(env, pecasFilterStoreDict, 'A'))
env.process(chegadaPecas(env, pecasFilterStoreDict, 'B'))

env.run(until = 80) 
```
Quando executado, o programa anterior fornece como saída:
```python
  0.0 Chegada de peça tipo A.   Cor: branco.
  0.0 Chegada de peça tipo B.   Cor: verde.
 44.5 Chegada de peça tipo A.   Cor: verde.
 44.5 Inicia montagem.          Cor: verde      Espera:  0.0
 47.7 Chegada de peça tipo B.   Cor: branco.
 47.7 Inicia montagem.          Cor: branco     Espera: 47.7
 49.0 Fim da montagem.          Cor: verde      Componentes: 1  
 52.6 Fim da montagem.          Cor: branco     Componentes: 2  
```
>**Desafio 19**: