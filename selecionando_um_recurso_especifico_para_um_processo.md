# Armazenagem e seleção de objetos específicos com  `Store() e FilterStore()`

O SimPy possui um ferramenta para armazenamento de objetos - como recursos, por exemplo - chamada `Store` e um comando de acesso a objetos específicos dentro do `Store` por meio de filtro, o `FilterStore`. O programador experiente vai notar a similaridade entre o `Store` e o [dicionário](http://www3.ifrn.edu.br/~jurandy/fdp/doc/aprenda-python/capitulo_10.html) do Python.

Vamos aprender sobre o `Store` a partir de um exemplo bem simples: uma barbearia com três barbeiros. Quando você chega a uma barbearia e tem uma ordem de preferência entre os barbeiros, isto é: barbeiro 1 vem antes do 2, que vem antes do 3, precisará selecionar seu _recurso_ barbeiro na ordem certa. 

# Construindo um conjunto de barbeiros

Incialmente, vamos considerar que os clientes são atribuídos ao barbeiro que estiver livre, indistintamente. Se todos os barbeiros estiverem ocupados, o cliente aguarda em fila. 

O comando que constrói um conjunto de objetos é o:
meuStore = simpy.Store(env, capacity=capacidade)
Para manipular a Store, temos três comandos:
meuStore.items: adiciona objetos ao meuStore;
meuStore.get(): retira o primeiro objeto disponível de meuStore;
meuStore.put(umObjeto): coloca um objeto no meuStore.

Assim, vamos criar um Store que armazenará o nome dos barbeiros: 0, 1, 2:
env = simpy.Environment()
#cria 3 barbeiros diferentes
barbeirosList = [simpy.Resource(env, capacity=1) for i in range(3)]

#cria um Store para armazenar os barbeiros
barbeariaStore = simpy.Store(env, capacity=3)
barbeariaStore.items = [0, 1, 2]

No código anterior, criamos uma lista com três recursos que representarão os barbeiros. A seguir, criamos uma Store chamada barbeariaStore de capacidade 3 e adicionamos, na linha seguinte, um lista com trÊs números.

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



