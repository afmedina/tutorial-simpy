# Criando, ocupando e desocupando recursos

## Criando

Em simulação, é usual representarmos processos que consomem recursos com alguma limitação de capacidade, tais como: máquinas de usinagem, operários em uma fábrica, empilhadeiras em um depósito etc. Quando um recurso é requisitado e não está disponível, há formação de uma fila de espera de entidades pela liberação do recurso.

Por exemplo, considere a simulação de uma fábrica, onde são necessários recursos "máquinas" que serão utilizados nos processos de fabricação.

No SimPy, a sintaxe para criar um recurso é:

```python
import simpy

env = simpy.Environment()
maquinas = simpy.Resource(env, capacity=2) # cria recurso maquinas com capacidadde 2
```

Se o parâmetro `capacity` não for fornecido, a função assume `capacity=1`. Note que  
`maquinas` foi criando dentro do Environment `env.`  
.

## Ocupando

Como comentado ao início da seção, muitos processos em simulação ocupam recursos. Assim, ocupar um recurso em um processo exige a codificação de uma função específica em que um dos argumentos deve ser o próprio recurso a ser utilizado. O trecho de código a seguir, exemplifica para o caso das máquinas já criadas:

```python
import simpy

def processo(env, entidade, maquinas):
    # função que ocupa o recurso e realiza o atendimento
    pass

env = simpy.Environment()
maquinas = simpy.Resource(env, capacity=2) # cria recurso maquinas com capacidade 2
```

É interessante notar que ocupar um recurso no SimPy é feito em duas etapas:  
1. **Requisitar** o recurso desejado com um `req = recurso.request()` \(o que é equivalente a entrar na fila para de acesso ao recurso\);  
1. **Ocupar** o recurso com um `yield req`

Assim, uma chamada ao recurso `maquinas`  
 ficaria:

```python
import simpy

def processo(env, entidade, maquinas):
    # função que ocupa o recurso e realiza o atendimento
    print("%s chega em %s" %(entidade, env.now))
    req = maquinas.request()                # solicita o recurso e ocupa a fila

    yield req                               # ocupa o recurso caso ele esteja livre ou aguarda sua liberação
    print("%s ocupa recurso em %s" %(entidade, env.now))

env = simpy.Environment()
maquinas = simpy.Resource(env, capacity=2)  # cria recurso com capacidade 2
```

> Enquanto a entidade estiver em fila aguardando a liberação do recurso, ela permanece na linha do comando `yield req`. Quando ela finalmente ocupa o recurso, a execução passa para a linha seguinte \(comando `print`, no caso do exemplo\).

Se pode parecer estranho que a ocupação de um recurso envolva duas linhas de código, o bom observador deve notar que isso pode dar flexibilidade em situação de lógica intrincada.

## Desocupando

Recurso criado e ocupado é liberado com a função `release(req)`. Considerando, por exemplo, que o processamento de peça leva 5 minutos em uma máquina, nossa função `processo` ficaria:

```python
import simpy

def processo(env, entidade, maquinas):
    # função que ocupa o recurso e realiza o atendimento
    print("%s chega em %s" %(entidade, env.now))
    req = maquinas.request()                # solicita o recurso e ocupa a fila

    yield req                               # ocupa o recurso caso ele esteja livre ou aguarda sua liberação
    print("%s ocupa recurso em %s" %(entidade, env.now))

    yield env.timeout(5)                    # executa o processo

    yield maquinas.release(req)             # libera o recurso
    print("%s libera o recurso em %s" %(entidade, env.now))

env = simpy.Environment()
maquinas = simpy.Resource(env, capacity=2)  # cria recurso com capacidade 2
```

Para testarmos nossa função, vamos executar o processo para apenas 4 peças e analisar o resultado. O código a seguir possui um laço `for` que chama a função `processo` 4 vezes no mesmo instante:

```python
import simpy

def processo(env, entidade, maquinas):
    # função que ocupa o recurso e realiza o atendimento
    print("%s chega em %s" %(entidade, env.now))
    req = maquinas.request()                # solicita o recurso e ocupa a fila

    yield req                               # ocupa o recurso caso ele esteja livre ou aguarda sua liberação
    print("%s ocupa recurso em %s" %(entidade, env.now))

    yield env.timeout(5)                    # executa o processo

    yield maquinas.release(req)             # libera o recurso
    print("%s libera o recurso em %s" %(entidade, env.now))

env = simpy.Environment()
maquinas = simpy.Resource(env, capacity=2)  # cria recurso com capacidade 2
for i in range(1,5):
    env.process(processo(env, "Peça %s" %i, maquinas))
env.run()
```

Quando executado, o programa retorna:

```
Peça 1 chega em 0
Peça 2 chega em 0
Peça 3 chega em 0
Peça 4 chega em 0
Peça 1 ocupa recurso em 0
Peça 2 ocupa recurso em 0
Peça 1 libera o recurso em 5
Peça 2 libera o recurso em 5
Peça 3 ocupa recurso em 5
Peça 4 ocupa recurso em 5
Peça 3 libera o recurso em 10
Peça 4 libera o recurso em 10
```

A saída da simulação permite concluir que as quatro peças chegaram no instante 0, mas como a capacidade do recurso era para apenas 2 peças simultâneas, as peças 3 e 4 tiveram que aguardar em fila até a liberação das máquinas no instante 5.

## Status do recurso

O SimPy fornece alguns parâmetros para você acompanhar o status do recursos criados no modelo. Para um recurso `res` definido no programa, podem ser extraídos os seguintes parâmetros durante a simulação:

* `res.capacity`: capacidade do recurso;
* `res.count`: quantas unidades de capacidade do recurso estão ocupadas no momento;
* `res.queue`: lista de objetos \(no caso, requisições\) que estão em fila no momento. Como res.queue é uma lista, o **número** de entidades em fila do recurso é obtido diretamente com o comando `len(res.queue)`;
* `res.users`: lista de objetos \(no caso, requisições\) que estão ocupando o recurso no momento. Como res.users é uma lista, o **número** de entidades em processo no recurso é obtido diretamente com o comando `len(res.users)`.

Ao exemplo anterior acrescentamos uma pequena função - `printStatus` - que imprime na tela todos os parâmetros anteriores de um recurso:

```python
import simpy

def processoRecurso(env, entidade, maquinas):
    # função que ocupa o recurso e realiza o atendimento
    print("%s chega em %s" %(entidade, env.now))
    req = maquinas.request()                # solicita o recurso e ocupa a fila

    yield req                               # sai da fila e ocupa o recurso
    print("%s ocupa recurso em %s" %(entidade, env.now))

    yield env.timeout(5)                    # executa o processo

    yield maquinas.release(req)             # libera o recurso
    print("%s libera o recurso em %s" %(entidade, env.now))
    printStatus(maquinas)

def printStatus(res):
    # imprime status do recurso
    print ("\tCapacidade: %i \tQuantidade ocupada: %i" %(res.capacity,  res.count))
    print ("\tEntidades (request) aguardando fila: ", res.queue)
    print ("\tEntidades em processamento: ", res.users)
    print ("\tNúmero de entidades em fila: %i e em processamento: %i"
    % (len(res.queue), len(res.queue)))


env = simpy.Environment()
maquinas = simpy.Resource(env, capacity=2)  # cria recurso com capacidade 2
for i in range(1,5):
    env.process(processoRecurso(env, "Peça %s" %i, maquinas))
env.run()
```

Quando executado, o programa anterior fornece como saída:

```
Peça 1 chega em 0
Peça 2 chega em 0
Peça 3 chega em 0
Peça 4 chega em 0
Peça 1 ocupa recurso em 0
Peça 2 ocupa recurso em 0
Peça 1 libera o recurso em 5
        Capacidade: 2   Quantidade ocupada: 1
        Entidades (request) aguardando fila:  [<Request() object at 0xeffd530>]
        Entidades em processamento:  [<Request() object at 0xeffd5f0>]
        Número de entidades em fila: 1 e em processamento: 1
Peça 2 libera o recurso em 5
        Capacidade: 2   Quantidade ocupada: 2
        Entidades (request) aguardando fila:  []
        Entidades em processamento:  [<Request() object at 0xeffd5f0>, <Request() object at 0xeffd530>]
        Número de entidades em fila: 0 e em processamento: 0
Peça 3 ocupa recurso em 5
Peça 4 ocupa recurso em 5
Peça 3 libera o recurso em 10
        Capacidade: 2   Quantidade ocupada: 0
        Entidades (request) aguardando fila:  []
        Entidades em processamento:  []
        Número de entidades em fila: 0 e em processamento: 0
Peça 4 libera o recurso em 10
        Capacidade: 2   Quantidade ocupada: 0
        Entidades (request) aguardando fila:  []
        Entidades em processamento:  []
        Número de entidades em fila: 0 e em processamento: 0
```

Esta seção para por aqui. Na continuação, construiremos um exemplo completo com geração de entidades e ocupação de recursos, de modo a cruzar tudo o que vimos até agora sobre o SimPy.

## Conteúdos desta seção

| **Conteúdo** | **Descrição** |
| --- | --- |
| `meuRecurso = simpy.Resource(env, capacity=1)` | cria um recurso em `env` com capacidade = 1 |
| `meuRequest = meuRecurso.request()` | solicita o recurso meuRecurso \(note que ele ainda não ocupa o recurso\) |
| `yield meuRequest` | aguarda em fila a liberação do recurso |
| `meuRecurso.release(meuResquest)` | libera `meuRecurso` a partir do `meuResquest` realizado |
| `env.process(função_geradora)` | inicia o processo implementado na `função_geradora` |



