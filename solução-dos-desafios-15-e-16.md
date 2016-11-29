# Solução dos desafios 15 e 16

>**Desafio 15**: considere que na barbearia, 40% dos clientes escolhem seu barbeiro favorito, sendo que, 30% preferem o barbeiro A, 10% preferem o barbeiro B e nenhum prefere o barbeiro C (o proprietário do salão). Construa um modelo de simulação representativo deste sistema.

Como existe preferência pelo barbeiro, naturalmente a escolha mais simples é trabalharmos com o `FilterStore`. O código a seguir, cria uma lista de barbeiros com os nomes, outra com os respectivos Resources, um dicionário para localizarmos o barbeiro por seu nome e, por fim, um `FilterStore `com os nomes dos barbeiros:

```python
random.seed(50)            
env = simpy.Environment()

# cria 3 barbeiros diferentes e armazena em um dicionário
barbeirosNomes = ['Barbeiro A', 'Barbeiro B', 'Barbeiro C']
barbeirosList = [simpy.Resource(env, capacity=1) for i in range(3)]
barbeirosDict = dict(zip(barbeirosNomes, barbeirosList))

# cria um FilterStore para armazenar os barbeiros
barbeariaStore = simpy.FilterStore(env, capacity=3)
barbeariaStore.items = barbeirosNomes

# inicia processo de chegadas de clientes
env.process(chegadaClientes(env, barbeariaStore))
env.run(until = 20)  
```
Quando um cliente chega, existe 40% de chance dele preferir o barbeiro A e 10% de preferir o barbeiro B. O código a seguir atribui o barbeiro utilizando-se da função `random`:
```python
def chegadaClientes(env, barbeariaStore):
    # gera clientes exponencialmente distribuídos
    i = 0
    while True:
        yield env.timeout(random.expovariate(1/TEMPO_CHEGADAS))
        i += 1
        # tem preferência por barbeiro?
        r = random.random()
        if r <= 0.30:
            barbeiroEscolhido ='Barbeiro A'
        elif r <= 0.40:
            barbeiroEscolhido = 'Barbeiro B'
        else:
            barbeiroEscolhido = 'Sem preferência'
        print("%5.1f Cliente %i chega.\t\t%s." %(env.now, i, barbeiroEscolhido))
        # inicia processo de atendimento
        env.process(atendimento(env, i, barbeiroEscolhido, barbeariaStore))
```

Por fim, o processo de atendimento deve diferenciar os clientes que possuem um barbeiro favorito, pois neste caso temos que criar uma função anônima lambda para resgatar o barbeiro correto do FilterStore:
```python
def atendimento(env, cliente, barbeiroEscolhido, barbeariaStore):
    #ocupa um barbeiro específico e realiza o corte
    chegada = env.now
    if barbeiroEscolhido != 'Sem preferência':
        # retira do FilterStore o barbeiro escolhido no processo anterior
        barbeiro = yield barbeariaStore.get(lambda barbeiro: barbeiro==barbeiroEscolhido)
    else:
        # cliente sem preferência, retira o primeiro barbeiro do FilterStore
        barbeiro = yield barbeariaStore.get()
    espera = env.now - chegada
    print("%5.1f Cliente %i inicia.\t\t%s ocupado.\tTempo de fila: %2.1f" 
            %(env.now, cliente, barbeiro, espera))
    # ocupa o recurso barbeiro
    with barbeirosDict[barbeiro].request() as req:
        yield req
        tempoCorte = random.normalvariate(*TEMPO_CORTE)
        yield env.timeout(tempoCorte)
        print("%5.1f Cliente %i termina.\t%s liberado." %(env.now, cliente, barbeiro))
    # devolve o barbeiro para o FilterStore
    barbeariaStore.put(barbeiro)
```
Note, no código anterior, que, caso o cliente não tenha barbeiro preferido, o `get`do `FilterStore` é utilizado sem nenhuma função lambda dentro do parentesis. 
Por fim, o código completo:


```python
import simpy
import random

TEMPO_CHEGADAS = 5          # intervalo entre chegadas de clientes
TEMPO_CORTE = [10, 2]       # tempo médio de corte 

def chegadaClientes(env, barbeariaStore):
    # gera clientes exponencialmente distribuídos
    i = 0
    while True:
        yield env.timeout(random.expovariate(1/TEMPO_CHEGADAS))
        i += 1
        # tem preferência por barbeiro?
        r = random.random()
        if r <= 0.30:
            barbeiroEscolhido ='Barbeiro A'
        elif r <= 0.40:
            barbeiroEscolhido = 'Barbeiro B'
        else:
            barbeiroEscolhido = 'Sem preferência'
        print("%5.1f Cliente %i chega.\t\t%s." %(env.now, i, barbeiroEscolhido))
        # inicia processo de atendimento
        env.process(atendimento(env, i, barbeiroEscolhido, barbeariaStore))

def atendimento(env, cliente, barbeiroEscolhido, barbeariaStore):
    #ocupa um barbeiro específico e realiza o corte
    chegada = env.now
    if barbeiroEscolhido != 'Sem preferência':
        # retira do FilterStore o barbeiro escolhido no processo anterior
        barbeiro = yield barbeariaStore.get(lambda barbeiro: barbeiro==barbeiroEscolhido)
    else:
        # cliente sem preferência, retira o primeiro barbeiro do FilterStore
        barbeiro = yield barbeariaStore.get()
    espera = env.now - chegada
    print("%5.1f Cliente %i inicia.\t\t%s ocupado.\tTempo de fila: %2.1f" 
            %(env.now, cliente, barbeiro, espera))
    # ocupa o recurso barbeiro
    with barbeirosDict[barbeiro].request() as req:
        yield req
        tempoCorte = random.normalvariate(*TEMPO_CORTE)
        yield env.timeout(tempoCorte)
        print("%5.1f Cliente %i termina.\t%s liberado." %(env.now, cliente, barbeiro))
    # devolve o barbeiro para o FilterStore
    barbeariaStore.put(barbeiro)
    
    
random.seed(50)            
env = simpy.Environment()

# cria 3 barbeiros diferentes e armazena em um dicionário
barbeirosNomes = ['Barbeiro A', 'Barbeiro B', 'Barbeiro C']
barbeirosList = [simpy.Resource(env, capacity=1) for i in range(3)]
barbeirosDict = dict(zip(barbeirosNomes, barbeirosList))

# cria um FilterStore para armazenar os barbeiros
barbeariaStore = simpy.FilterStore(env, capacity=3)
barbeariaStore.items = barbeirosNomes

# inicia processo de chegadas de clientes
env.process(chegadaClientes(env, barbeariaStore))
env.run(until = 20)
```
Quando executado, o código anterior fornece:

```python
  3.4 Cliente 1 chega.          Barbeiro A.
  3.4 Cliente 1 inicia.         Barbeiro A ocupado.     Tempo de fila: 0.0
  8.5 Cliente 2 chega.          Sem preferência.
  8.5 Cliente 2 inicia.         Barbeiro B ocupado.     Tempo de fila: 0.0
  9.0 Cliente 3 chega.          Barbeiro A.
  9.2 Cliente 1 termina.        Barbeiro A liberado.
  9.2 Cliente 3 inicia.         Barbeiro A ocupado.     Tempo de fila: 0.3
  9.8 Cliente 4 chega.          Sem preferência.
  9.8 Cliente 4 inicia.         Barbeiro C ocupado.     Tempo de fila: 0.0
 11.8 Cliente 5 chega.          Sem preferência.
 13.7 Cliente 2 termina.        Barbeiro B liberado.
 13.7 Cliente 5 inicia.         Barbeiro B ocupado.     Tempo de fila: 1.9
 17.3 Cliente 3 termina.        Barbeiro A liberado.

```
> **Desafio 16:** acrescente ao modelo da barbearia, a possibilidade de desistência e falta do barbeiro. Neste caso, existe 5% de chance de um barbeiro faltar em determinado dia. Neste caso, considere 3 novas situações:
* Se o barbeiro favorito faltar, o respectivo cliente vai embora;
* O cliente que não possuir um barbeiro favorito olha a fila de clientes: se houver mais de 6 clientes em fila, ele desiste e vai embora;
* O cliente que possui um barbeiro favorito, não esperará se houver mais de 3 clientes esperando seu barbeiro favorito.

Como, neste caso, temos que identificar quantos clientes estão aguardando o respectivo barbeiro favorito, uma saída seria utilizar um dicionário para armazenar o número de clientes em fila (outra possibilidade seria um `Store` específico para a fila):

```python
random.seed(25)            
env = simpy.Environment()

# cria 3 barbeiros diferentes e armazena em um dicionário
barbeirosNomes = ['Barbeiro A', 'Barbeiro B', 'Barbeiro C']
barbeirosList = [simpy.Resource(env, capacity=1) for i in range(3)]
barbeirosDict = dict(zip(barbeirosNomes, barbeirosList))

# dicionário para armazenar o número de clientes em fila de favoritos 
filaDict = dict(zip(barbeirosNomes, [0,0,0]))

# falta de um barbeiro
if random.random() <= 0.05:
    barbeirosNomes.remove(random.choice((barbeirosNomes)))

# cria um FilterStore para armazenar os barbeiros
barbeariaStore = simpy.FilterStore(env, capacity=3)
barbeariaStore.items = barbeirosNomes

# inicia processo de chegadas de clientes
env.process(chegadaClientes(env, barbeariaStore))
env.run(until = 20)   
```
Para garantir a falta de um barbeiro em 5% das simulações, foi novamente utilizado o comando `random.random` e adicionalmente o comando `[random.choice](https://docs.python.org/dev/library/random.html#random.choice)` que selecionada uniformemente um elemento da lista `barbeirosNomes`:
```python
if random.random() <= 0.05:
    barbeirosNomes.remove(random.choice((barbeirosNomes)))
```
Na linha anterior, além de sortearmos um dos barbeiros, ele é removido da lista de barbeiros, o que facilita o processo de desistência do cliente.
O processo de chegadas de clientes não precisa ser modificado em relação ao código anterior, contudo, o processo de atendimento precisa armazenar o número de clientes em fila por barbeiro - para isso criamos um dicionário - e o número de clientes em fila total. Assim, criamos uma variável global que armazena o número total de clientes em fila. Uma possível codificação para a função de atendimento seria:
```python
def atendimento(env, cliente, barbeiroEscolhido, barbeariaStore):
    #ocupa um barbeiro específico e realiza o corte
    global filaAtual     # número de clientes em fila
    
    chegada = env.now
    if barbeiroEscolhido != 'Sem preferência':
        if barbeiroEscolhido not in barbeirosDict:
            # caso o barbeiro tenha faltado, desiste do atendimento
            print("%5.1f Cliente %i desiste.\t%s ausente." 
                %(env.now, cliente, barbeiroEscolhido))
            env.exit()
        if filaDict[barbeiroEscolhido] > 3:
            # caso a fila seja maior do que 6, desiste do atendimento
            print("%5.1f Cliente %i desiste.\t%s com mais de 3 clientes em fila." 
                %(env.now, cliente, barbeiroEscolhido))
            env.exit()
        # cliente atual entra em fila e incrementa a fila do barbeiro favorito
        filaAtual += 1
        filaDict[barbeiroEscolhido] = filaDict[barbeiroEscolhido] + 1
        barbeiro = yield barbeariaStore.get(lambda barbeiro: barbeiro==barbeiroEscolhido)
        filaDict[barbeiroEscolhido] = filaDict[barbeiroEscolhido] - 1
    else:
        # cliente sem preferência, verifica o tamanho total da fila
        if filaAtual > 6:
            # caso a fila seja maior do que 6, desiste do atendimento
            print("%5.1f Cliente %i desiste.\tFila com mais de 6 clientes em fila." 
                %(env.now, cliente))
            env.exit()  
        else:
            # cliente entra em fila e pega o primeiro barbeiro livre
            filaAtual += 1
            barbeiro = yield barbeariaStore.get()
            
    # cliente já tem barbeiro, então sai da fila 
    filaAtual -= 1  

    espera = env.now - chegada
    print("%5.1f Cliente %i inicia.\t\t%s ocupado.\tTempo de fila: %2.1f" 
            %(env.now, cliente, barbeiro, espera))
    # ocupa o recurso barbeiro
    with barbeirosDict[barbeiro].request() as req:
        yield req
        tempoCorte = random.normalvariate(*TEMPO_CORTE)
        yield env.timeout(tempoCorte)
        print("%5.1f Cliente %i termina.\t%s liberado." %(env.now, cliente, barbeiro))
    # devolve o barbeiro para o FilterStore
    barbeariaStore.put(barbeiro)```



```python

```

```python

```

## Teste seus conhecimentos

1. Considere que a barbearia opera 6 horas por dia. Acrescente ao seu modelo às estatíticas de clientes atendidos, clientes que desistiram (e por qual razão), ocupação dos barbeiros e tempo médio de espera em fila por barbeiro.
2. Dada a presente demanda da barbearia, quantos barbeiros devem estar trabalhando, caso o proprietário pretenda que o tempo médio de espera em fila seja inferior a 15 minutos?

