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


> **Desafio 16:** acrescente ao modelo da barbearia, a possibilidade de desistência e falta do barbeiro. Neste caso, existe 5% de chance de um barbeiro faltar em determinado dia. Neste caso, considere 3 novas situações:
* Se o barbeiro favorito faltar, o respectivo cliente vai embora;
* O cliente que não possuir um barbeiro favorito olha a fila de clientes: se houver mais de 6 clientes em fila, ele desiste e vai embora;
* O cliente que possui um barbeiro favorito, não esperará se houver mais de 3 clientes esperando seu barbeiro favorito.

```python

```
## Teste seus conhecimentos

1. Dada a presente demanda da barbearia, quantos barbeiros devem estar trabalhando, caso o proprietário pretenda que o tempo médio de espera em fila seja inferior a 5 minutos?

