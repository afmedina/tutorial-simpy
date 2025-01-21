# Solução dos desafios 4, 5 e 6

## Solução dos desafios 4, 5 e 6

> **Desafio 4**: imprima na tela o tempo de simulação e o números de clientes em fila. Quantos clientes existem em fila no instante 4.5?

Para solução do desafio, basta lembrarmos que a qualquer momento, o conjunto de entidades em fila pelo recurso é dado por `servidorRes.queue` e, portanto, o número de entidade em fila é facilmente obtido pela expressão:

```python
len(servidorRes.queue)
```

Foi acrescentada uma chamadas à função `print,` de modo a imprimir na tela o número de clientes em fila ao término do atendimento de cada cliente:

```python
def atendimentoServidor(env, nome, servidorRes):
    # função que ocupa o servidor e realiza o atendimento   
    # solicita o recurso servidorRes
    request = servidorRes.request()

    # aguarda em fila até a liberação do recurso e o ocupa
    yield request                       
    print('%.1f Servidor inicia o atendimento do %s' % (env.now, nome))

    # aguarda um tempo de atendimento exponencialmente distribuído
    yield env.timeout(random.expovariate(1.0/TEMPO_MEDIO_ATENDIMENTO))
    print('%.1f Servidor termina o atendimento do %s. Clientes em fila: %i' 
            % (env.now, nome, len(servidorRes.queue)))

    # libera o recurso servidorRes
    yield servidorRes.release(request)
```

Executado o código, descobrimos que no instante 5,5 min, temos 2 clientes em fila:

```python
0.5 Chegada do cliente 1
0.5 Servidor inicia o atendimento do cliente 1
1.4 Servidor termina o atendimento do cliente 1. Clientes em fila: 0
3.1 Chegada do cliente 2
3.1 Servidor inicia o atendimento do cliente 2
3.3 Chegada do cliente 3
4.1 Servidor termina o atendimento do cliente 2. Clientes em fila: 1
4.1 Servidor inicia o atendimento do cliente 3
4.1 Servidor termina o atendimento do cliente 3. Clientes em fila: 0
4.3 Chegada do cliente 4
4.3 Servidor inicia o atendimento do cliente 4
4.5 Servidor termina o atendimento do cliente 4. Clientes em fila: 0
```

Portanto, existem 0 cliente em fila no instante 4,5 minutos, nas condições simuladas (note a semente de geração de números aleatórios igual a 2).

> **Desafio 5**: calcule o tempo de permanência em fila de cada cliente e imprima o resultado na tela. Para isso, armazene o instante de chegada do cliente na fila em uma variável `chegada.`\
> Ao final do atendimento, armazene o tempo de fila, numa variável `tempoFila` e apresente o resultado na tela.

A ideia deste desafio é que você se acostume com esse cálculo tão trivial quanto importante dentro da simulação: o tempo de permanência de uma entidade em algum local. Neste caso, o local é uma fila por ocupação de um recurso.\
A lógica aqui é a de um cronometrista que deve disparar o cronômetro na chegada do cliente e pará-lo ao início do atendimento.\
Assim, ao chegar, criamos uma variável `chegada` que armazena o instante atual fornecido pelo comando `env.now` do SimPy:

```python
def atendimentoServidor(env, nome, servidorRes):
    # função que ocupa o servidor e realiza o atendimento
    # armazena o instante de chegada do cliente
    chegada = env.now    
    # solicita o recurso servidorRes
    request = servidorRes.request()
```

Agora, inciado o atendimento (logo após o `yield` que ocupa o recurso), a variável `tempoFila` armazena o tempo de permanência em fila. Como num cronômetro, o tempo em fila é calculado pelo instante atual do cronômetro menos o instante de disparo dele já armazenado na variável `chegada`:

```python
def atendimentoServidor(env, nome, servidorRes):
    # função que ocupa o servidor e realiza o atendimento
    # armazena o instante de chegada do cliente
    chegada = env.now    
    # solicita o recurso servidorRes
    request = servidorRes.request()

    # aguarda em fila até a liberação do recurso e o ocupa
    yield request
    # calcula o tempo em fila
    tempoFila = env.now - chegada
```

Para imprimir o resultado, basta simplesmente alterar a chamada à função `print` na linha seguinte, de modo que o código final da função `atendimentoServidor`\
fica:

```python
def atendimentoServidor(env, nome, servidorRes):
    # função que ocupa o servidor e realiza o atendimento
    # armazena o instante de chegada do cliente
    chegada = env.now    
    # solicita o recurso servidorRes
    request = servidorRes.request()

    # aguarda em fila até a liberação do recurso e o ocupa
    yield request
    # calcula o tempo em fila
    tempoFila = env.now - chegada                  
    print('%.1f Servidor inicia o atendimento do %s. Tempo em fila: %.1f'
            % (env.now, nome, tempoFila))

    # aguarda um tempo de atendimento exponencialmente distribuído
    yield env.timeout(random.expovariate(1.0/TEMPO_MEDIO_ATENDIMENTO))
    print('%.1f Servidor termina o atendimento do %s. Clientes em fila: %i' 
            % (env.now, nome, len(servidorRes.queue)))

    # libera o recurso servidorRes
    yield servidorRes.release(request)
```

Agora, a execução do programa mostra na tela o tempo de espera de cada cliente:

```python
0.5 Chegada do cliente 1
0.5 Servidor inicia o atendimento do cliente 1. Tempo em fila: 0.0
1.4 Servidor termina o atendimento do cliente 1. Clientes em fila: 0
3.1 Chegada do cliente 2
3.1 Servidor inicia o atendimento do cliente 2. Tempo em fila: 0.0
3.3 Chegada do cliente 3
4.1 Servidor termina o atendimento do cliente 2. Clientes em fila: 1
4.1 Servidor inicia o atendimento do cliente 3. Tempo em fila: 0.8
4.1 Servidor termina o atendimento do cliente 3. Clientes em fila: 0
4.3 Chegada do cliente 4
4.3 Servidor inicia o atendimento do cliente 4. Tempo em fila: 0.0
4.5 Servidor termina o atendimento do cliente 4. Clientes em fila: 0
```

> **Desafio 6:** um problema clássico de simulação envolve ocupar e desocupar recursos na seqüência correta. Considere uma lavanderia com 4 lavadoras, 3 secadoras e 5 cestos de roupas. Quando um cliente chega, ele coloca as roupas em uma máquina de lavar (ou aguarda em fila). A lavagem consome 20 minutos (constante). Ao terminar a lavagem, o cliente retira as roupas da máquina e coloca em um cesto e leva o cesto com suas roupas até a secadora, num processo que leva de 1 a 4 minutos distribuídos uniformemente. O cliente então descarrega as roupas do cesto diretamente para a secadora, espera a secagem e vai embora. Esse processo leva entre 9 e 12 minutos, uniformemente distribuídos. Construa um modelo que represente o sistema descrito.

A dificuldade do desafio da lavanderia é representar corretamente a sequência de ocupação e desocupação dos recursos necessários de cada cliente. Se você ocupá-los/desocupá-los na ordem errada, fatalmente seu programa apresentará resultados inesperados.

Como se trata de um modelo com vários processos e distribuições, vamos seguir a Dica da seção "Solução dos desafios 2 e 3" e construir uma função para armazenar as distribuições do problema, organizando nosso código:

```python
import random
import simpy

def distributions(tipo):
    # função que armazena as distribuições utilizadas no modelo
    return {
        'chegadas': random.expovariate(1.0/5.0),
        'lavar': 20,
        'carregar': random.uniform(1, 4),
        'descarregar': random.uniform(1, 2),
        'secar': random.uniform(9, 12),
    }.get(tipo, 0.0)
```

Como já destacado, a dificuldade é representar a sequência correta de processos do cliente: ele chega, ocupa uma lavadora, lava, ocupa um cesto, libera uma lavadora, ocupa uma secadora, libera o cesto, seca e libera a secadora. Se a sequência foi bem compreendida, a máscara a seguir será de fácil preenchimento:

```python
import random
import simpy

contaClientes = 0             # conta clientes que chegaram no sistema

def distributions(tipo):
    # função que armazena as distribuições utilizadas no modelo
    return {
        'chegadas': random.expovariate(1.0/5.0),
        'lavar': 20,
        'carregar': random.uniform(1, 4),
        'descarregar': random.uniform(1, 2),
        'secar': random.uniform(9, 12),
    }.get(tipo, 0.0)

def chegadaClientes(env, lavadoras, cestos, secadoras):
    # função que gera a chegada de clientes
    global contaClientes

    pass

    # chamada do processo de lavagem e secagem
    pass

def lavaSeca(env, cliente, lavadoras, cestos, secadoras):
    # função que processa a operação de cada cliente dentro da lavanderia

    # ocupa a lavadora
    pass

    # antes de retirar da lavadora, pega um cesto
    pass

    # libera a lavadora, mas não o cesto
    pass

    # ocupa a secadora antes de liberar o cesto
    pass

    # libera o cesto mas não a secadora
    pass

    # pode liberar a secadora
    pass

random.seed(10)
env = simpy.Environment()
lavadoras = simpy.Resource(env, capacity = 3)
cestos = simpy.Resource(env, capacity = 2)
secadoras = simpy.Resource(env, capacity = 1)
env.process(chegadaClientes(env, lavadoras, cestos, secadoras))

env.run(until = 40)
```

O programa a seguir apresenta uma possível solução para o desafio, já com diversos comandos de impressão:

```python
import random
import simpy

contaClientes = 0           # conta clientes que chegaram no sistema

def distributions(tipo):
    # função que armazena as distribuições utilizadas no modelo
    return {
        'chegadas': random.expovariate(1.0/5.0),
        'lavar': 20,
        'carregar': random.uniform(1, 4),
        'descarregar': random.uniform(1, 2),
        'secar': random.uniform(9, 12),
    }.get(tipo, 0.0)

def chegadaClientes(env, lavadoras, cestos, secadoras):
    # função que gera a chegada de clientes
    global contaClientes

    contaClientes = 0
    while True:
        contaClientes += 1
        yield env.timeout(distributions('chegadas'))
        print("%.1f chegada do cliente %s" %(env.now, contaClientes))
         # chamada do processo de lavagem e secagem
        env.process(lavaSeca(env, "Cliente %s" % contaClientes, lavadoras, cestos, secadoras))

def lavaSeca(env, cliente, lavadoras, cestos, secadoras):
    # função que processa a operação de cada cliente dentro da lavanderia
    global utilLavadora, tempoEsperaLavadora, contaLavadora

    # ocupa a lavadora
    req1 = lavadoras.request()
    yield req1
    print("%.1f %s ocupa lavadora" %(env.now, cliente))
    yield env.timeout(distributions('lavar'))

    # antes de retirar da lavadora, pega um cesto
    req2 = cestos.request()
    yield req2
    print("%.1f %s ocupa cesto" %(env.now, cliente))
    yield env.timeout(distributions('carregar'))

    # libera a lavadora, mas não o cesto
    lavadoras.release(req1)
    print("%.1f %s desocupa lavadora" %(env.now, cliente))

    # ocupa a secadora antes de liberar o cesto
    req3 = secadoras.request()
    yield req3
    print("%.1f %s ocupa secadora" %(env.now, cliente))
    yield env.timeout(distributions('descarregar'))

    # libera o cesto mas não a secadora
    cestos.release(req2)
    print("%.1f %s desocupa cesto" %(env.now, cliente))
    yield env.timeout(distributions('secar'))

    # pode liberar a secadora
    print("%.1f %s desocupa secadora" %(env.now, cliente))
    secadoras.release(req3)



random.seed(10)
env = simpy.Environment()
lavadoras = simpy.Resource(env, capacity=3)
cestos = simpy.Resource(env, capacity=2)
secadoras = simpy.Resource(env, capacity=1)
env.process(chegadaClientes(env, lavadoras, cestos, secadoras))

env.run(until=40)
```

A execução do programa anterior fornece como saída:

```python
4.2 chegada do cliente 1
4.2 Cliente 1 ocupa lavadora
12.6 chegada do cliente 2
12.6 Cliente 2 ocupa lavadora
24.2 Cliente 1 ocupa cesto
27.2 Cliente 1 desocupa lavadora
27.2 Cliente 1 ocupa secadora
28.8 Cliente 1 desocupa cesto
32.6 Cliente 2 ocupa cesto
36.3 Cliente 2 desocupa lavadora
38.7 Cliente 1 desocupa secadora
38.7 Cliente 2 ocupa secadora
```

## Teste seus conhecimentos:

1. A fila M/M/1 possui expressões analíticas conhecidas. Por exemplo, o tempo médio de permanência no sistema é dado pela expressão: $$W = \frac{1} {\mu - \lambda}$$. Valide seu modelo, ou seja, calcule o resultado esperado para a expressão e compare com o resultado obtido pelo seu programa.
2. Utilizando a função [`plot`da bilbioteca `matplotlib,`](http://matplotlib.org/users/pyplot_tutorial.html#pyplot-tutorial%29%20construa%20um%20gr%C3%A1fico%20que%20represente%20a%20evolu%C3%A7%C3%A3o%20do%20n%C3%BAmero%20de%20entidades%20em%20fila%20%28dica:%20voc%C3%AA%20precisar%C3%A1%20armazenar%20o%20tempo%20de%20espera%20em%20uma%20lista%20e%20plotar%20a%20lista%20em%20um%20gr%C3%A1fico%20ao%20final%20da%20simula%C3%A7%C3%A3o%5C).
3. No problema da lavanderia, crie uma situação de desistência, isto é: caso a fila de espera por lavadoras seja de 5 clientes, o próximo cliente a chegar no sistema desiste imediatamente de entrar na lavanderia.
