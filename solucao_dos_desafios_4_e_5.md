# Solução dos desafios 4, 5 e 6

> **Desafio 4**: imprima na tela o tempo de simulação e o números de clientes em fila. Quantos clientes existem em fila no instante 5.5?

Para solução do desafio, precisamos inicialmente de uma variável que armazene o número de clientes em fila. A variável global `clientesFila` armazenará este valor, como mostra o ínicio do código alterado da seção anterior:

```python
import random # gerador de números aleatórios
import simpy  # biblioteca de simulação

TEMPO_MEDIO_CHEGADAS = 1.0    # tempo entre chegadas sucessivas de clientes
TEMPO_MEDIO_ATENDIMENTO = 0.5 # tempo médio de atendimento no servidor

clientesFila = 0
```

O próximo passo é incrementar essa variável quando um novo cliente entra em fila e, de modo similar, decrementá-la quando um cliente sai da fila para iniciar seu atendimento. Etapas relativamente fáceis de programar se você entendeu a função `atendimentoServidor`
 da seção anterior:

```python
def atendimentoServidor(env, nome, servidorRes):
    global clientesFila

    request = servidorRes.request() # solicita o recurso servidorRes

    clientesFila += 1 # incrementa contador de novo cliente em fila
    print('%.2f: chegada de novo cliente em fila. Clientes em fila: %d' 
    %(env.now, clientesFila))

    yield request # aguarda em fila até o acesso

    print('%s inicia o atendimento em: %.1f ' % (nome, env.now()))
    clientesFila -= 1 # decrementa contador de novo cliente em fila
```

Repare que foram acrescentadas duas chamadas à função `print`, de modo a imprimir na tela o número de clientes em fila em cada instante de mudança do valor da variável `clientesFila.`
Executado o código, descobrimos que no istante 5,5 min, temos 2 clientes em fila:

```
Cliente 1 chega em: 1.5 
1.50: chegada de novo cliente em fila. Clientes em fila: 1
Cliente 1 inicia o atendimento em: 1.5 
Cliente 1 termina o atendimento em: 1.6.
Cliente 2 chega em: 2.6 
2.61: chegada de novo cliente em fila. Clientes em fila: 1
Cliente 2 inicia o atendimento em: 2.6 
Cliente 2 termina o atendimento em: 2.9.
Cliente 3 chega em: 3.0 
3.05: chegada de novo cliente em fila. Clientes em fila: 1
Cliente 3 inicia o atendimento em: 3.0 
Cliente 4 chega em: 3.8 
3.81: chegada de novo cliente em fila. Clientes em fila: 1
Cliente 5 chega em: 4.0 
3.95: chegada de novo cliente em fila. Clientes em fila: 2
Cliente 3 termina o atendimento em: 5.0.
Cliente 4 inicia o atendimento em: 5.0 
Cliente 6 chega em: 5.1 
5.06: chegada de novo cliente em fila. Clientes em fila: 2
Cliente 4 termina o atendimento em: 5.2.
Cliente 5 inicia o atendimento em: 5.2 
Cliente 5 termina o atendimento em: 5.3.
Cliente 6 inicia o atendimento em: 5.3 
Cliente 7 chega em: 5.7 
5.73: chegada de novo cliente em fila. Clientes em fila: 1
Cliente 6 termina o atendimento em: 5.8.
Cliente 7 inicia o atendimento em: 5.8 
Cliente 8 chega em: 6.0 
5.99: chegada de novo cliente em fila. Clientes em fila: 1
Cliente 9 chega em: 6.0 
6.03: chegada de novo cliente em fila. Clientes em fila: 2
Cliente 7 termina o atendimento em: 6.2.
Cliente 8 inicia o atendimento em: 6.2 
Cliente 8 termina o atendimento em: 6.5.
Cliente 9 inicia o atendimento em: 6.5 
Cliente 9 termina o atendimento em: 6.8.
Cliente 10 chega em: 9.7 
9.69: chegada de novo cliente em fila. Clientes em fila: 1
Cliente 10 inicia o atendimento em: 9.7 
```

> **Desafio 5**: calcule o tempo de permanência em fila de cada cliente e imprima o resultado na tela. Para isso, armazene o instante de chegada do cliente na fila em uma variável `chegada.`
>  Ao final do atendimento, armazene o tempo de fila, numa variável `tempoFila`
>  e apresente o resultado na tela.

A ideia deste desafio é que você se acostume com esse cálculo tão trivial mas tão importante dentro da simulação: o tempo de permanência de uma entidade em algum local. Neste caso, o local é a fila.
A lógica aqui é a de um cronometrista que deve disparar o cronômetro na chegada do cliente e pará-lo ao início do antendimento.
Assim, ao chegar, criamos uma variável `chegada`
 que armazena o instante atual fornecido pelo comando `env.now`
 do
SimPy:

```python
def atendimentoServidor(env, nome, servidorRes):
    global clientesFila

    chegada = env.now               # armazena o instante de chegada do cliente
    request = servidorRes.request() # solicita o recurso servidorRes
```

Agora, inciado o atendimento \(logo após o `yield`
 que ocupa o recurso\), a variável `tempoFila` armazena o tempo de permanência em fila. Como num cronômetro, o tempo em fila é calculado pelo instante atual do cronômetro menos o instante de disparo dele já armazenado na variável `chegada`:

```python
def atendimentoServidor(env, nome, servidorRes):
    global clientesFila

    chegada = env.now               # armazena o instante de chegada do cliente
    request = servidorRes.request() # solicita o recurso servidorRes

    clientesFila += 1 # incrementa contador de novo cliente em fila
    print('%.2f: chegada de novo cliente em fila. Clientes em fila: %d' 
    %(env.now, clientesFila))

    yield request # aguarda em fila até o acesso

    tempoFila = env.now - chegada
```

Para imprimir o resultado, basta simplesmente alterar a chamada à função `print` na linha seguinte, de modo que o código final da função `atendimentoServidor`
 fica:

```python
def atendimentoServidor(env, nome, servidorRes):
    global clientesFila

    chegada = env.now() # armazena o instante de chegada do cliente
    request = servidorRes.request() # solicita o recurso servidorRes

    clientesFila += 1 # incrementa contador de novo cliente em fila
    print('%.2f: chegada de novo cliente em fila. Clientes em fila: %d'
    %(env.now(), clientesFila))

    yield request # aguarda em fila até o acesso

    tempoFila = env.now()-chegada
    print('%s inicia o atendimento em: %.1f. Tempo em fila: %.1f min ' 
    % (nome, env.now(), tempoFila))
    clientesFila -= 1 # decrementa contador de novo cliente em fila

    # tempo de atendimento exponencial
    yield env.timeout(random.expovariate(1.0/TEMPO_MEDIO_ATENDIMENTO))

    print('%s termina o atendimento em: %.1f.' % (nome, env.now())) 

    yield servidorRes.release(request) # libera o recurso servidorRes
```

Agora, a execução do programa mostra na tela o tempo de espera de cada cliente:

```
Cliente 1 chega em: 1.5 
1.50: chegada de novo cliente em fila. Clientes em fila: 1
Cliente 1 inicia o atendimento em: 1.5. Tempo em fila: 0.0 
Cliente 1 termina o atendimento em: 1.6.
Cliente 2 chega em: 2.6 
2.61: chegada de novo cliente em fila. Clientes em fila: 1
Cliente 2 inicia o atendimento em: 2.6. Tempo em fila: 0.0 
Cliente 2 termina o atendimento em: 2.9.
Cliente 3 chega em: 3.0 
3.05: chegada de novo cliente em fila. Clientes em fila: 1
Cliente 3 inicia o atendimento em: 3.0. Tempo em fila: 0.0 
Cliente 4 chega em: 3.8 
3.81: chegada de novo cliente em fila. Clientes em fila: 1
Cliente 5 chega em: 4.0 
3.95: chegada de novo cliente em fila. Clientes em fila: 2
Cliente 3 termina o atendimento em: 5.0.
Cliente 4 inicia o atendimento em: 5.0. Tempo em fila: 1.2 
Cliente 6 chega em: 5.1 
5.06: chegada de novo cliente em fila. Clientes em fila: 2
Cliente 4 termina o atendimento em: 5.2.
Cliente 5 inicia o atendimento em: 5.2. Tempo em fila: 1.2 
Cliente 5 termina o atendimento em: 5.3.
Cliente 6 inicia o atendimento em: 5.3. Tempo em fila: 0.2 
Cliente 7 chega em: 5.7 
5.73: chegada de novo cliente em fila. Clientes em fila: 1
Cliente 6 termina o atendimento em: 5.8.
Cliente 7 inicia o atendimento em: 5.8. Tempo em fila: 0.1 
Cliente 8 chega em: 6.0 
5.99: chegada de novo cliente em fila. Clientes em fila: 1
Cliente 9 chega em: 6.0 
6.03: chegada de novo cliente em fila. Clientes em fila: 2
Cliente 7 termina o atendimento em: 6.2.
Cliente 8 inicia o atendimento em: 6.2. Tempo em fila: 0.2 
Cliente 8 termina o atendimento em: 6.5.
Cliente 9 inicia o atendimento em: 6.5. Tempo em fila: 0.5 
Cliente 9 termina o atendimento em: 6.8.
Cliente 10 chega em: 9.7 
9.69: chegada de novo cliente em fila. Clientes em fila: 1
Cliente 10 inicia o atendimento em: 9.7. Tempo em fila: 0.0
```

> **Desafio 6:** um problema clássico de simulação envolve ocupar e desocupar recursos na seqüência correta. Considere uma lavanderia com 4 lavadoras, 3 secadoras e 5 cestos de roupas. Quando um cliente chega, ele coloca as roupas em uma máquina de lavar \(ou aguarda em fila\). A lavagem consome 20 minutos \(constante\). Ao terminar a lavagem, o cliente retira as roupas da máquina e coloca em um cesto e leva o cesto com suas roupas até a secadora, num processo que leva de 1 a 4 minutos distribuídos uniformemente. O cliente então descarrega as roupas do cesto diretamente para a secadora, espera a secagem e vai embora. Esse processo leva entre 9 e 12 minutos, uniformemente distribuídos. Construa um modelo que represente o sistema descrito.

A dificuldade do desafio da lavanderia é representar corretamente a sequência de ocupação e desocupação dos recursos necessários de cada cliente. Se você ocupá-los\/desocupá-los na ordem errada, fatalmente seu programa apresentará resultados inesperados.

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

contaClientes = 0 # conta clientes que chegaram no sistema

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

O programa a seguir apresenta uma possível solução, já com diversos comandos de impressão:

```python
import random
import simpy

contaClientes = 0 # conta clientes que chegaram no sistema

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
        print("Cliente %s chega em %.1f" %(contaClientes, env.now))
        #chamada do processo de lavagem e secagem
        env.process(lavaSeca(env, "Cliente %s" %contaClientes, lavadoras, cestos, secadoras))

def lavaSeca(env, cliente, lavadoras, cestos, secadoras):
    # função que processa a operação de cada cliente dentro da lavanderia

    # ocupa a lavadora
    req1 = lavadoras.request()
    yield req1
    print("%s ocupa lavadora em %.1f" %(cliente, env.now))
    yield env.timeout(distributions('lavar'))

    # antes de retirar da lavadora, pega um cesto
    req2 = cestos.request()
    yield req2
    print("%s ocupa cesto em %.1f" %(cliente, env.now))
    yield env.timeout(distributions('carregar'))

    # libera a lavadora, mas não o cesto
    lavadoras.release(req1)
    print("%s desocupa lavadora em %.1f" %(cliente, env.now))

    # ocupa a secadora antes de liberar o cesto
    req3 = secadoras.request()
    yield req3
    print("%s ocupa secadora em %.1f" %(cliente, env.now))
    yield env.timeout(distributions('descarregar'))

    # libera o cesto mas não a secadora
    cestos.release(req2)
    print("%s desocupa cesto em %.1f" %(cliente, env.now))
    yield env.timeout(distributions('secar'))

    # pode liberar a secadora
    print("%s desocupa secadora em %.1f" %(cliente, env.now))
    secadoras.release(req3)

random.seed(10)
env = simpy.Environment()
lavadoras = simpy.Resource(env, capacity = 3)
cestos = simpy.Resource(env, capacity = 2)
secadoras = simpy.Resource(env, capacity = 1)
env.process(chegadaClientes(env, lavadoras, cestos, secadoras))
env.run(until = 40)
```

A execução do programa fornece como saída:

```
Cliente 1 chega em 4.2
Cliente 1 ocupa lavadora em 4.2
Cliente 2 chega em 12.6
Cliente 2 ocupa lavadora em 12.6
Cliente 1 ocupa cesto em 24.2
Cliente 1 desocupa lavadora em 27.2
Cliente 1 ocupa secadora em 27.2
Cliente 1 desocupa cesto em 28.8
Cliente 2 ocupa cesto em 32.6
Cliente 2 desocupa lavadora em 36.3
Cliente 1 desocupa secadora em 38.7
Cliente 2 ocupa secadora em 38.7
```

# Teste seus conhecimentos:

1. A fila M\/M\/1 possui expressões analíticas conhecidas. Por exemplo, o tempo médio de permanência no sistema é dado pela expressão: $$W = \frac{1} {\mu - \lambda}$$. Valide seu modelo, ou seja, calcule o resultado esperado para a expressão e compare com o resultado obtido pelo seu programa.

2. No problema da lavanderia, crie uma situação de desistência, isto é: caso a fila de espera por lavadoras seja de 5 clientes, o próximo cliente a chegar no sistema desiste imediatamente de entrar na lavanderia.


