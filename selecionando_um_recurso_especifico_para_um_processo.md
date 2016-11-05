# Armazenagem e seleção de objetos específicos com  `Store() e FilterStore()`

O SimPy possui um ferramenta para armazenamento de objetos - como recursos, por exemplo - chamada `Store` e um comando de acesso a objetos específicos dentro do `Store` por meio de filtro, o `FilterStore`. O programador experiente vai notar a similaridade entre o `Store` e o [dicionário](http://www3.ifrn.edu.br/~jurandy/fdp/doc/aprenda-python/capitulo_10.html) do Python.

Vamos aprender sobre o `Store` a partir de um exemplo bem simples: uma barbearia com três barbeiros. Quando você chega a uma barbearia e tem uma ordem de preferência entre os barbeiros, isto é: barbeiro 1 vem antes do 2, que vem antes do 3, precisará selecionar seu _recurso_ barbeiro na ordem certa. 

## Construindo um conjunto de barbeiros com `Store()`

Incialmente, vamos considerar que os clientes são atribuídos ao barbeiro que estiver livre, indistintamente. Se todos os barbeiros estiverem ocupados, o cliente aguarda em fila. 

O comando que constrói um conjunto de objetos é o:

`meuStore = simpy.Store(env, capacity=capacidade)`

Para manipular a Store, temos três comandos:
* `meuStore.items:` adiciona objetos ao meuStore;
* `meuStore.get():` retira o primeiro objeto disponível de meuStore;
* `meuStore.put(umObjeto):` coloca um objeto no meuStore.

Assim, vamos criar um `Store `que armazenará o nome dos barbeiros: 0, 1, 2:
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
barbeirosList = [simpy.Resource(env, capacity=1) for i in range(3)]

#cria um Store para armazenar os barbeiros
barbeariaStore = simpy.Store(env, capacity=3)
barbeariaStore.items = [0, 1, 2]

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
A função de atendimento, traz a novidade de que primeiro devemos *retirar* um objeto do `Store `e, ao final do atendimento, devolvê-lo ao `Store`:

```python
def atendimento(env, cliente, barbeariaStore):
    #ocupa um barbeiro específico e realiza o corte
    chegada = env.now
    barbeiroNum = yield barbeariaStore.get()
    espera = env.now - chegada
    print("%5.1f Cliente %i incia.\t\tBarbeiro %i ocupado.\tTempo de fila: %2.1f" %(env.now, cliente, barbeiroNum, espera))
    with barbeirosList[barbeiroNum].request() as req:
        yield req
        yield env.timeout(random.normalvariate(*TEMPO_CORTE))
        print("%5.1f Cliente %i termina.\tBarbeiro %i liberado." %(env.now, cliente, barbeiroNum))
    barbeariaStore.put(barbeiroNum)
```
Quando estamos retirando um objeto do `barbeariaStore`, estamos apenas retirando o nome (ou identificador) do barbeiro disponível. Para ocuparmos o recurso (ou barbeiro) corretamente, utilizamos o identificador como índice da lista `barbeiroList`. Assim, temporariamente, o barbeiro retirado do Store fica indisponível para outros clientes, pois a linha:


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
    print("%5.1f Cliente %i incia.\t\tBarbeiro %i ocupado.\tTempo de fila: %2.1f" %(env.now, cliente, barbeiroNum, espera))
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
  0.8 Cliente 1 incia.          Barbeiro 0 ocupado.     Tempo de fila: 0.0
  3.8 Cliente 2 chega.
  3.8 Cliente 2 incia.          Barbeiro 1 ocupado.     Tempo de fila: 0.0
 10.4 Cliente 3 chega.
 10.4 Cliente 3 incia.          Barbeiro 2 ocupado.     Tempo de fila: 0.0
 12.7 Cliente 2 termina.        Barbeiro 1 liberado.
 13.9 Cliente 1 termina.        Barbeiro 0 liberado.
 14.2 Cliente 4 chega.
 14.2 Cliente 4 incia.          Barbeiro 1 ocupado.     Tempo de fila: 0.0
 14.5 Cliente 5 chega.
 14.5 Cliente 5 incia.          Barbeiro 0 ocupado.     Tempo de fila: 0.0
 17.8 Cliente 3 termina.        Barbeiro 2 liberado.
```


