# Armazenagem e seleção de objetos específicos com  `Store, FilterStore e PriorityStore`

O SimPy possui uma ferramenta para armazenamento de [objetos](http://wiki.python.org.br/ProgramacaoOrientadaObjetoPython#A2._Objetos_e_Tipos_de_dados) - como valores, recursos etc.  - chamada `Store;` um comando de acesso a objetos específicos dentro do `Store` por meio de filtro, o `FilterStore` e um comando de acesso de objetos por ordem de prioridade, o `PriorityStore.` O programador experiente vai notar certa similaridade da família `Store` com o [dicionário](http://www3.ifrn.edu.br/~jurandy/fdp/doc/aprenda-python/capitulo_10.html) do Python.

Vamos desvendar o funcionamento do `Store` a partir de um exemplo bem simples: simulando o processo de atendimento em uma barbearia com três barbeiros. Quando você chega a uma barbearia e tem uma ordem de preferência entre os barbeiros, isto é: barbeiro 1 vem antes do 2, que vem antes do 3, precisará selecionar o _recurso_ barbeiro na ordem certa de sua preferência, mas lembre-se: cada cliente tem seu gosto e gosto não se discute, simula-se!

## Construindo um conjunto de objetos com `Store`

Inicialmente, considere que os clientes são atribuídos ao primeiro barbeiro que encontrar-se livre, indistintamente. Se todos os barbeiros estiverem ocupados, o cliente aguarda em fila.

O comando que constrói um armazém de objetos é o `simpy.Store():`

`meuStore = simpy.Store(env, capacity=capacidade)`

Para manipular o `Store`criado, temos três comandos à disposição:

* `meuStore.items:` adiciona objetos ao `meuStore;`
* `yield meuStore.get():` retira o primeiro objeto disponível de `meuStore` ou, caso o `meuStore` esteja vazio, aguarda até que algum objeto sela colocado no `Store;`
* `yield meuStore.put(umObjeto):` coloca um objeto no `meuStore`ou, caso o `meuStore`esteja cheio, aguarda até que surja um espaço vazio para colocar o objeto.

  > Observação: se a capacidade não for fornecida, o SimPy assumirá que a capacidade do Store é ilimitada.

Para a nossa barbearia, criaremos um `Store`que armazenará o nome dos barbeiros, aqui denominados de 0, 1 e 2:

```python
env = simpy.Environment()

# cria 3 barbeiros diferentes
barbeirosList = [simpy.Resource(env, capacity=1) for i in range(3)]

# cria um Store para armazenar os barbeiros
barbeariaStore = simpy.Store(env, capacity=3)
barbeariaStore.items = [0, 1, 2]
```

No código anterior, criamos uma lista com três recursos que representarão os barbeiros. A seguir, criamos uma `Store,` chamada `barbeariaStore,` de capacidade 3 e adicionamos, na linha seguinte, um lista com os três números que representam os próprios barbeiros.

Em resumo, nosso `Store` contém apenas os números 0, 1 e 2.

Considere que o intervalo entre chegadas sucessivas de clientes é exponencialmente distribuído com média de 5 minutos e que cada barbeiro leva um tempo normalmente distribuído com média 10 e desvio padrão de 2 minutos para cortar o cabelo.

Uma possível máscara para o modelo de simulação seria:

```python
import simpy
import random

TEMPO_CHEGADAS = 5      # intervalo entre chegadas de clientes
TEMPO_CORTE = [10, 2]   # tempo médio de corte 

def chegadaClientes(env, barbeariaStore):
    # gera clientes exponencialmente distribuídos
    # encaminha para o processo de atendimento

def atendimento(env, cliente, barbeariaStore):
    # ocupa um barbeiro específico e realiza o corte

random.seed(100)            
env = simpy.Environment()

# cria 3 barbeiros diferentes
barbeirosList = [simpy.Resource(env, capacity=1) for i in range(3)]

# cria um Store para armazenar os barbeiros
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

A função de atendimento, traz a novidade de que primeiro devemos _retirar_ um objeto/barbeiro do `Store` e, ao final do atendimento, devolvê-lo ao `Store:`

```python
def atendimento(env, cliente, barbeariaStore):
    # ocupa um barbeiro específico e realiza o corte
    chegada = env.now
    # retira o barbeiro do Store
    barbeiroNum = yield barbeariaStore.get()
    espera = env.now - chegada
    print("%5.1f Cliente %i inicia.\t\tBarbeiro %i ocupado.\tTempo de fila: %2.1f" 
            %(env.now, cliente, barbeiroNum, espera))
    with barbeirosList[barbeiroNum].request() as req:
        yield req
        yield env.timeout(random.normalvariate(*TEMPO_CORTE))
        print("%5.1f Cliente %i termina.\tBarbeiro %i liberado."
                %(env.now, cliente, barbeiroNum))
    # devolve o barbeiro ao Store
    barbeariaStore.put(barbeiroNum)
```

Quando estamos retirando um objeto do `barbeariaStore,` estamos apenas retirando o nome \(ou identificador\) do barbeiro disponível. Algo como retirar um cartão com o nome do barbeiro de uma pilha de barbeiros disponíveis. Se o cartão é retirado, significa que, enquanto ele não for devolvido à pilha, nenhum cliente poderá ocupá-lo, pois ele não se encontra na pilha de barbeiros disponíveis.

Para ocuparmos o recurso \(ou barbeiro\) selecionado corretamente, utilizamos o identificador como índice da lista `barbeiroList`. Assim, temporariamente, o barbeiro retirado do Store fica indisponível para outros clientes, pois a linha:

```python
barbeiroNum = yield barbeariaStore.get()
```

Só retornará um barbeiro dentre aqueles que ainda estão à disposição.  
Ao ser executado por apenas 20 minutos, o modelo de simulação completo da barbeira fornece como saída:

```python
 11.8 Cliente 1 chega.
 11.8 Cliente 1 inicia.         Barbeiro 0 ocupado.     Tempo de fila: 0.0
 17.6 Cliente 2 chega.
 17.6 Cliente 2 inicia.         Barbeiro 1 ocupado.     Tempo de fila: 0.0
 19.5 Cliente 1 termina.        Barbeiro 0 liberado.
```

No caso do exemplo, o `Store` armazenou basicamente uma lista de números \[0,1,2\], que representam os nomes dos barbeiros. Poderíamos sofisticar um pouco mais o exemplo e criar um dicionário \(em Python\) para manipular os nomes reais dos barbeiros. Por exemplo, se os nomes dos barbeiros são: João, José e Mário, poderíamos montar o `barberirosStore`com seus respectivos nomes e evitar o uso de números:

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

> Observação:`Store` opera segundo uma regra FIFO _\(Firt-in-First-out_\), ou seja: o primeiro objeto a entrar no Store por meio de um `.put()` será o primeiro objeto a sair dele com um `.get()`.

## Selecionando um objeto específico com `FilterStore()`

Considere agora o caso bastante comum em que precisamos selecionar um recurso específico \(segundo alguma regra\) dentro de um conjunto de recursos disponíveis. Na barbearia, por exemplo, cada cliente agora tem um barbeiro preferido e, se ele não está disponível, o cliente prefere aguardar sua liberação.  
Neste caso, vamos assumir que a preferência de um cliente é uniformemente distribuída entre os três barbeiros.  
Precisamos, portanto, de um modo de selecionar um objeto específico dentro do `Store`. O SimPy tem um comando para construir um conjunto de objetos filtrável, o `FilterStore`:

```python
meuFilterStore = simpy.FilterStore(env, capacity=capacidade)
```

A grande diferença para o `Store` é que podemos utilizar uma [função anônima do Python](http://pt.stackoverflow.com/questions/50422/como-declarar-uma-função-anônima-no-python) dentro do comando `.get()` e assim puxar um objeto de dentro do `FilterStore` segundo alguma regra codificada por nós.  
Inicialmente, criaremos um `FilterStore`de barbeiros, que armazenará apenas os números 1, 2 e 3:

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

A função geradora de clientes terá uma ligeira modificação, pois temos de atribuir a cada cliente um barbeiro específico, respeitando o sorteio de uma distribuição uniforme:

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
        print("%5.1f Cliente %i chega.\t\tBarbeiro %i escolhido." 
                %(env.now, i, barbeiroEscolhido))
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
        print("%5.1f Cliente %i termina.\tBarbeiro %i liberado."
                %(env.now, cliente, barbeiroEscolhido))
    barbeariaStore.put(barbeiroNum)
```

Para selecionar o número certo do barbeiro, existe uma função `lambda` inserida dentro do `.get()`:

```python
barbeiroNum = yield barbeariaStore.get(lambda barbeiro: barbeiro==barbeiroEscolhido)
```

Esta função percorre os objetos dentro da `barbeariaStore`até encontrar um que tenha o número do respectivo barbeiro desejado pelo cliente. Note que também poderíamos ter optado por uma construção alternativa utilizando o nome dos barbeiros e não os números - neste caso, uma alternativa seria seguir o exemplo da seção anterior e utilizar um dicionário para associar o nome dos barbeiros aos respectivos recursos.  
Quando executado, o modelo anterior fornece:

```python
  8.7 Cliente 1 chega.          Barbeiro 1 escolhido.
  8.7 Cliente 1 inicia.         Barbeiro 1 ocupado.     Tempo de fila: 0.0
  9.7 Cliente 2 chega.          Barbeiro 0 escolhido.
  9.7 Cliente 2 inicia.         Barbeiro 0 ocupado.     Tempo de fila: 0.0
 12.4 Cliente 3 chega.          Barbeiro 1 escolhido.
 15.5 Cliente 1 termina.        Barbeiro 1 liberado.
 15.5 Cliente 3 inicia.         Barbeiro 1 ocupado.     Tempo de fila: 3.0
```

Repare que o cliente 3 chegou num instante em que o barbeiro 1 estava ocupado atendendo o cliente 1, assim ele foi obrigado a esperar em fila por 3 minutos, até que o cliente 1 liberasse o Barbeiro 1.

## Criando um `Store` com prioridade: `PriorityStore`

Como sabemos, um `Store` segue a regra FIFO, de modo que o primeiro objeto a entrar no `Store`será o primeiro a sair do `Store`. É possível quebrar essa regra por meio do `PriorityStore`:

```python
meuPriorityStore = simpy.PriorityStore(env, capacity=inf)
```

Para acrescentar um objeto qualquer ao `meuPriorityStore`já criado, a sequência de passos é primeiro criar um objeto `PriorityItem` - que representará o objeto a ser armazendo - para depois inseri-lo com um comando `put,` como representado no exemplo a seguir:

```python
# criar o PriorityItem
meuObjetoPriority = simpy.PriorityItem(priority=priority, item=meuObjeto)
# adicionar o PriorityItem ao PriorityStore
meuPriorityStore.put(meuObjetoPriority)
```

> Observação: como no caso do `PriorityResource`, quanto menor o valor de `priority`, maior a preferência pelo objeto.

No caso dos barbeiros: "João, José e Mário", considere que a ordem de prioridades é a própria ordem alfabética dos nomes. Assim, inicialmente, construiremos dois dicionários para armazenar essas informações sobre os barbeiros:

```python
random.seed(100)            
env = simpy.Environment()

# cria 3 barbeiros diferentes e armazena em um dicionário
barbeirosList = [simpy.Resource(env, capacity=1) for i in range(3)]
barbeirosNomes = ['João', 'José', 'Mario']
# lista com a ordem de prioridades dos barbeiros
barbeirosPrioList = ['0', '1', '2']

# dicionário de recursos e prioridades
barbeirosDict = dict(zip(barbeirosNomes, barbeirosList))
barbeirosPrioDict = dict(zip(barbeirosNomes, barbeirosPrioList))
```

A partir dos dicionários anteriores, podemos construir um `PriorityStore` que armazena os nomes dos barbeiros e suas prioridades:

```python
# cria um Store para armazenar os barbeiros
barbeariaStore = simpy.PriorityStore(env, capacity=3)
for nome in barbeirosNomes:
    barbeiro = simpy.PriorityItem(priority=barbeirosPrioDict[nome], item=nome)
    barbeariaStore.put(barbeiro)

# inicia processo de chegadas de clientes
env.process(chegadaClientes(env, barbeariaStore))
env.run(until = 20)
```

A função `atendimento` é muito semelhante às anteriores, basta notar que o comando `get` vai buscar não o nome, ma um _objeto_ `PriorityItem` dentro do `PriorityStore`. Este objeto possui dois atributos: `item` - no nosso caso, o nome do barbeiro - e `priority` - a prioridade do objeto.

A seguir, apresenta-se uma possível implementação da função `atendimento.` Note que o objeto `barbeiro` é um `PriorityItem` e que, para sabermos o seu nome, precisamos do comando `barbeiro.item:`

```python
def atendimento(env, cliente, barbeariaStore):
    #ocupa um barbeiro específico e realiza o corte
    chegada = env.now
    barbeiro = yield barbeariaStore.get()
    # extraí o nome do barbeiro
    barbeiroNome = barbeiro.item
    espera = env.now - chegada
    print("%5.1f Cliente %i inicia.\t\tBarbeiro %s ocupado.\tTempo de fila: %2.1f"
            %(env.now, cliente, barbeiroNome, espera))
    with barbeirosDict[barbeiroNome].request() as req:
        yield req
        yield env.timeout(random.normalvariate(*TEMPO_CORTE))
        print("%5.1f Cliente %i termina.\tBarbeiro %s liberado." 
                %(env.now, cliente, barbeiroNome))
    barbeariaStore.put(barbeiro)
```

O modelo de simulação completo, quando simulado por apenas 20 minutos, fornece como saída:

```python
  0.8 Cliente 1 chega.
  0.8 Cliente 1 inicia.         Barbeiro João ocupado.  Tempo de fila: 0.0
  3.8 Cliente 2 chega.
  3.8 Cliente 2 inicia.         Barbeiro José ocupado.  Tempo de fila: 0.0
 10.4 Cliente 3 chega.
 10.4 Cliente 3 inicia.         Barbeiro Mario ocupado. Tempo de fila: 0.0
 12.7 Cliente 2 termina.        Barbeiro José liberado.
 13.9 Cliente 1 termina.        Barbeiro João liberado.
 14.2 Cliente 4 chega.
 14.2 Cliente 4 inicia.         Barbeiro João ocupado.  Tempo de fila: 0.0
 14.5 Cliente 5 chega.
 14.5 Cliente 5 inicia.         Barbeiro José ocupado.  Tempo de fila: 0.0
 17.8 Cliente 3 termina.        Barbeiro Mario liberado.
```

> Observação 1: internamente, o SimPy trata a "família" `Store` como recursos com capacidade ilimitada de armazenamento de objetos.  
> Observação 2: uma implementação alternativa para o problema anterior, seria armazenar no `PriorityStore` não o nome do barbeiro, mas o próprio recurso criado. \(Veja o tópico: "Teste seus conhecimentos" na próxima seção.

## Conceitos desta seção

| Conteúdo | Descrição |
| --- | --- |
| `meuStore = simpy.Store(env, capacity=capacity` | cria um _Store_ `meuStore`: um armazém de objetos com capacidade `capacity`. Caso o parâmetro `capacity` não seja fornecido, o SimPy considera `capacity=inf`. |
| `yield meuStore.get()` | retira o primeiro objeto disponível de `meuStore` ou, caso o `meuStore` esteja vazio, aguarda até que algum objeto esteja disponível. |
| `yield meuStore.put(umObjeto)` | coloca um objeto no `meuStore`ou, caso o `meuStore`esteja cheio, aguarda até que surja um espaço vazio para colocar o objeto. |
| `meuFilterStore = simpy.FilterStore(env, capacity=capacity)` | cria um _Store_ `meuStore`: um armazém de objetos filtráveis com capacidade `capacity`. Caso o parâmetro `capacity` não seja fornecido, o SimPy considera `capacity=inf`. |
| `yield meuFilterStore.get(filter=<function <lambda>>)` | retira o 1° objeto do `meuFilterStore` que retorne True para a função anônima fornecida por filter. |
| `meuPriorityStore = simpy.PriorityStore(env, capacity=inf)` | cria um _PriorityStore_ `meuPriorityStore` - uma armazém de objetos com ordem de prioridade e capacidade `capacity`. Caso o parâmetro `capacity` não seja fornecido, o SimPy considera `capacity=inf`. |
| `meuObjetoPriority = simpy.PriorityItem(priority=priority, item=meuObjeto)` | cria um objeto `meuObjetoPriority` a partir de um objeto `meuObjeto` existente, com prioridade para ser armazenado em um `PriorityStore`. A `priority`deve ser um objeto ordenável. |
| `meuObjetoPriority.item` | retorna o atributo `item` do objeto `meuObjetoPriority`, definido no momento de criação do `PriorityItem.` |
| `meuObjetoPriority.priority` | retorna o atributo `priority` do objeto `meuObjetoPriority`, definido no momento de criação do `PriorityItem.` |
| `meuPriorityStore.put(meuObjetoPriority)` | coloca o objeto `meuObjetoPriority` no `PriorityStore` `meuPriorityStore` ou, caso o `meuPriorityStore`esteja cheio, aguarda até que surja um espaço vazio para colocar o objeto. |
| `yield meuPriorityStore.get()` | retorna o primeiro objeto disponível em `meuPriorityStore` respeitando a ordem de prioridade atribuída ao `PriorityItem` \(objetos com valor menor de prioridade são escolhidos primeiro\). Caso o `meuPriorityStore` esteja vazio, aguarda até que surja um espaço vazio para colocar o objeto. |

## Desafios

> **Desafio 15**: considere que na barbearia, 40% dos clientes escolhem seu barbeiro favorito, sendo que, 30% preferem o barbeiro A, 10% preferem o barbeiro B e nenhum prefere o barbeiro C \(o proprietário do salão\). Construa um modelo de simulação representativo deste sistema.
>
> **Desafio 16:** acrescente ao modelo da barbearia, a possibilidade de desistência e falta do barbeiro. Neste caso, existe 5% de chance de um barbeiro faltar em determinado dia. Neste caso, considere 3 novas situações:_ _
>
> * _Se o barbeiro favorito faltar, o respectivo cliente vai embora;_
> * O cliente que não possuir um barbeiro favorito olha a fila de clientes: se houver mais de 6 clientes em fila, ele desiste e vai embora;
> * O cliente que possui um barbeiro favorito, não esperará se houver mais de 3 clientes esperando seu barbeiro favorito.



