# Armazenagem e seleção de objetos específicos com  `Store() e FilterStore()`

O SimPy possui um ferramenta para armazenamento de objetos - como recursos, por exemplo - chamada `Store` e um comando de acesso a objetos específicos dentro do `Store` por meio de filtro, o `FilterStore`. O programador experiente vai notar a similaridade entre o `Store` e o [dicionário](http://www3.ifrn.edu.br/~jurandy/fdp/doc/aprenda-python/capitulo_10.html) do Python.

Vamos aprender sobre o `Store` a partir de um exemplo bem simples: uma barbearia com três barbeiros. Quando você chega a uma barbearia e tem uma ordem de preferência entre os barbeiros, isto é: barbeiro 1 vem antes do 2, que vem antes do 3, precisará selecionar seu _recurso_ barbeiro na ordem certa.

## Construindo um conjunto de objetos com `Store()`

Incialmente, vamos considerar que os clientes são atribuídos ao barbeiro que estiver livre, indistintamente. Se todos os barbeiros estiverem ocupados, o cliente aguarda em fila.

O comando que constrói um conjunto de objetos é o:

`meuStore = simpy.Store(env, capacity=capacidade)`

Para manipular a Store, temos três comandos:

* `meuStore.items:` adiciona objetos ao meuStore;
* `yield meuStore.get():` retira o primeiro objeto disponível de `meuStore` ou, caso o meuStore esteja vazio, aguarda até que algum objeto esteja disponível;
* `yield meuStore.put(umObjeto):` coloca um objeto no `meuStore`ou, caso o meuStore esteja cheio, aguarda um espaço vazio para colocar o objeto.

Assim, vamos criar um `Store`que armazenará o nome dos barbeiros: 0, 1, 2:

```python
env = simpy.Environment()

#cria 3 barbeiros diferentes
barbeirosList = [simpy.Resource(env, capacity=1) for i in range(3)]

#cria um Store para armazenar os barbeiros
barbeariaStore = simpy.Store(env, capacity=3)
barbeariaStore.items = [0, 1, 2]
```

No código anterior, criamos uma lista com três recursos que representarão os barbeiros. A seguir, criamos uma Store chamada barbeariaStore de capacidade 3 e adicionamos, na linha seguinte, um lista com três números.

Resumindo, nosso Store contém apenas os números 0, 1 e 2.

Vamos considerar que o intervalo entre chegadas sucessivas de clientes é exponenciamente distribuído com média de 5 minutos e que cada barbeiro leva um tempo normalmente distribuído com média 10 e desvio padão de minutos para cortar o cabelo.

Uma possível máscara para o problema seria:

```python
import simpy
import random

TEMPO_CHEGADAS = 5      # intervalo entre chegadas de clientes
TEMPO_CORTE = [10, 5]   # tempo médio de corte 

def chegadaClientes(env, barbeariaStore):
    # gera clientes exponencialmente distribuídos
    # encaminha para o processo de atendimento

def atendimento(env, cliente, barbeariaStore):
    #ocupa um barbeiro específico e realiza o corte

random.seed(100)            
env = simpy.Environment()

#cria 3 barbeiros diferentes
**barbeirosList = [simpy.Resource(env, capacity=1) for i in range(3)]**

#cria um Store para armazenar os barbeiros
**barbeariaStore = simpy.Store(env, capacity=3)
barbeariaStore.items = [0, 1, 2]**

# inicia processo de chegadas de clientes
env.process(chegadaClientes(env, barbeariaStore))
env.run(until = 20) 
```

A função para gerar clientes é semelhante a tantas outras que já fizemos neste livro:

```python
def chegadaClientes(env, barbeariaStore):
    # gera clientes exponencialmente distribuídos
    # encaminha para o processo de atendimento
    i = 0
    while True:
        yield env.timeout(random.expovariate(1/TEMPO_CHEGADAS))
        i += 1
        print("%5.1f Cliente %i chega." %(env.now, i))
        env.process(atendimento(env, i, barbeariaStore))
```

A função de atendimento, traz a novidade de que primeiro devemos _retirar_ um objeto do `Store`e, ao final do atendimento, devolvê-lo ao `Store`:

```python
def atendimento(env, cliente, barbeariaStore):
    #ocupa um barbeiro específico e realiza o corte
    chegada = env.now
    barbeiroNum = yield barbeariaStore.get()
    espera = env.now - chegada
    print("%5.1f Cliente %i inicia.\t\tBarbeiro %i ocupado.\tTempo de fila: %2.1f" 
            %(env.now, cliente, barbeiroNum, espera))
    with barbeirosList[barbeiroNum].request() as req:
        yield req
        yield env.timeout(random.normalvariate(*TEMPO_CORTE))
        print("%5.1f Cliente %i termina.\tBarbeiro %i liberado." %(env.now, cliente, barbeiroNum))
    barbeariaStore.put(barbeiroNum)
```

Quando estamos retirando um objeto do `barbeariaStore`, estamos apenas retirando o nome \(ou identificador\) do barbeiro disponível. Para ocuparmos o recurso \(ou barbeiro\) corretamente, utilizamos o identificador como índice da lista `barbeiroList`. Assim, temporariamente, o barbeiro retirado do Store fica indisponível para outros clientes, pois a linha:

```python
import simpy
import random

TEMPO_CHEGADAS = 5      # intervalo entre chegadas de clientes
TEMPO_CORTE = [10, 2]   # tempo médio de corte 

def chegadaClientes(env, barbeariaStore):
    # gera clientes exponencialmente distribuídos
    # encaminha para o processo de atendimento
    i = 0
    while True:
        yield env.timeout(random.expovariate(1/TEMPO_CHEGADAS))
        i += 1
        print("%5.1f Cliente %i chega." %(env.now, i))
        env.process(atendimento(env, i, barbeariaStore))

def atendimento(env, cliente, barbeariaStore):
    #ocupa um barbeiro específico e realiza o corte
    chegada = env.now
    barbeiroNum = yield barbeariaStore.get()
    espera = env.now - chegada
    print("%5.1f Cliente %i inicia.\t\tBarbeiro %i ocupado.\tTempo de fila: %2.1f" 
            %(env.now, cliente, barbeiroNum, espera))
    with barbeirosList[barbeiroNum].request() as req:
        yield req
        yield env.timeout(random.normalvariate(*TEMPO_CORTE))
        print("%5.1f Cliente %i termina.\tBarbeiro %i liberado." %(env.now, cliente, barbeiroNum))
    barbeariaStore.put(barbeiroNum)

random.seed(100)            
env = simpy.Environment()

#cria 3 barbeiros diferentes
barbeirosList = [simpy.Resource(env, capacity=1) for i in range(3)]

#cria um Store para armazenar os barbeiros
barbeariaStore = simpy.Store(env, capacity=3)
barbeariaStore.items = [0, 1, 2]

# inicia processo de chegadas de clientes
env.process(chegadaClientes(env, barbeariaStore))
env.run(until = 20)   
```

Como saída, o programa anterior fornece:

```python
  0.8 Cliente 1 chega.
  0.8 Cliente 1 inicia.         Barbeiro 0 ocupado.     Tempo de fila: 0.0
  3.8 Cliente 2 chega.
  3.8 Cliente 2 inicia.         Barbeiro 1 ocupado.     Tempo de fila: 0.0
 10.4 Cliente 3 chega.
 10.4 Cliente 3 inicia.         Barbeiro 2 ocupado.     Tempo de fila: 0.0
 12.7 Cliente 2 termina.        Barbeiro 1 liberado.
 13.9 Cliente 1 termina.        Barbeiro 0 liberado.
 14.2 Cliente 4 chega.
 14.2 Cliente 4 inicia.         Barbeiro 1 ocupado.     Tempo de fila: 0.0
 14.5 Cliente 5 chega.
 14.5 Cliente 5 inicia.         Barbeiro 0 ocupado.     Tempo de fila: 0.0
 17.8 Cliente 3 termina.        Barbeiro 2 liberado.
```

No caso do exemplo, o `Store`armazenou basicamente uma lista de números \[1,2,3\], que representam os nomes dos barbeiros. Poderíamos sofisticar um pouco mais o exemplo e criar um dicionário \(em Python\) para manipular os nomes reais dos barbeiros. Por exemplo, se os barbeiros se chamam João, José e Mário, poderíamos montar o `barberirosStore`com os próprios nomes:

```python
random.seed(100)            
env = simpy.Environment()

#cria 3 barbeiros diferentes e armazena em um dicionário
barbeirosList = [simpy.Resource(env, capacity=1) for i in range(3)]
barbeirosNomes = ['João', 'José', 'Mario']
barbeirosDict = dict(zip(barbeirosNomes, barbeirosList))

#cria um Store para armazenar os barbeiros
barbeariaStore = simpy.Store(env, capacity=3)
barbeariaStore.items = barbeirosNomes

# inicia processo de chegadas de clientes
env.process(chegadaClientes(env, barbeariaStore))
env.run(until = 20)  
```
O exemplo anterior apenas reforça que `Store` é um local para se armazenar objetos de qualquer tipo \(semelhante ao `dict` do Python\).
>Observação:`Store` opera segundo uma regra FIFO _(Firt-in-First-out_), ou seja: o primeiro objeto a entrar no Store por meio de um `.put()` será o primeiro objeto a sair dele com um `.get()`.

## Selecionando um objeto específico com `FilterStore()`

Considere agora o caso bastante comum em que precisamos selecionar um recurso específico \(segundo alguma regra\) dentro de um conjunto de recursos disponíveis. Por exemplo, na barbearia cada cliente tem um barbeiro preferido e, se ele não está disponível, o cliente prefere aguardar sua liberação.
Vamos assumir neste caso, que a preferência é uniformemente distribuída entre os barbeiros. 
Neste caso, o SimPy tem um comando específico para construir um conjunto de objetos filtrável:

```python
meuFilterStore = simpy.FilterStore(env, capacity=capacidade)
```

A grande diferença para o `Store` é que o podemos utilizar uma [função anônima do Python](http://pt.stackoverflow.com/questions/50422/como-declarar-uma-fun%C3%A7%C3%A3o-an%C3%B4nima-no-python) dentro do comando `.get()`. 
Incialmente, vamos criar um `FilterStore`de barbeiros:

```python
random.seed(150)            
env = simpy.Environment()

#cria 3 barbeiros diferentes
barbeirosList = [simpy.Resource(env, capacity=1) for i in range(3)]

#cria um Store para armazenar os barbeiros
barbeariaStore = simpy.FilterStore(env, capacity=3)
barbeariaStore.items = [0, 1, 2]

# inicia processo de chegadas de clientes
env.process(chegadaClientes(env, barbeariaStore))
env.run(until = 20)  
```

A função geradora de clientes tem uma ligeira modificação, pois agora temos de atribuir a cada cliente um barbeiro específico, segundo uma distribuição uniforme:

```python
import simpy
import random

TEMPO_CHEGADAS = 5          # intervalo entre chegadas de clientes
TEMPO_CORTE = [10, 5]       # tempo médio de corte 
PREF_BARBEIRO = [0, 2]      # preferência de barbeiros

def chegadaClientes(env, barbeariaStore):
    # gera clientes exponencialmente distribuídos
    # sorteia o barbeiro
    # inicia processo de atendimento
    i = 0
    while True:
        yield env.timeout(random.expovariate(1/TEMPO_CHEGADAS))
        i += 1
        barbeiroEscolhido = random.randint(*PREF_BARBEIRO)
        print("%5.1f Cliente %i chega.\t\tBarbeiro %i escolhido." %(env.now, i, barbeiroEscolhido))
        env.process(atendimento(env, i, barbeiroEscolhido, barbeariaStore))
```

Na função anterior, o _atributo_ `barbeiroEscolhido` armazena o número do barbeiro sorteado e envia a informação para a função que representa o processo de atendimento.
A função `atendimento` utilizará uma função anônima para buscar o barbeiro certo dentro do`FilterStore` criado:

```python
def atendimento(env, cliente, barbeiroEscolhido, barbeariaStore):
    #ocupa um barbeiro específico e realiza o corte
    chegada = env.now
    barbeiroNum = yield barbeariaStore.get(lambda barbeiro: barbeiro==barbeiroEscolhido)
    espera = env.now - chegada
    print("%5.1f Cliente %i incia.\t\tBarbeiro %i ocupado.\tTempo de fila: %2.1f" 
            %(env.now, cliente, barbeiroEscolhido, espera))
    with barbeirosList[barbeiroNum].request() as req:
        yield req
        yield env.timeout(random.normalvariate(*TEMPO_CORTE))
        print("%5.1f Cliente %i termina.\tBarbeiro %i liberado." %(env.now, cliente, barbeiroEscolhido))
    barbeariaStore.put(barbeiroNum)
```

Para selecionar o número certo do barbeiro, existe uma função `lambda` inserida dentro do `.get()`:

```python
barbeiroNum = yield barbeariaStore.get(lambda barbeiro: barbeiro==barbeiroEscolhido)
```

Esta função percorre os objetos dentro da `barbeariaStore`até encontrar um que tenha o número do respectivo barbeiro desejado pelo cliente.

