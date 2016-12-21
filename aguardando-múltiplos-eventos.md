# Aguardando múltiplos eventos ao mesmo tempo com `AnyOf `e `AllOf`

Uma funcionalidade importante do SimPy é permitir que uma entidade aguarde até que dois ou mais eventos ocorram para então continuar algum processo. O SimPy possui duas opções muito interessantes para isso:

* `AnyOf(env, eventos)`: aguarda até que um dos eventos tenham ocorrido - `AnyOf` é equivalente ao símbolo de "|" (ou `or`);
* `AllOf(env, eventos)`: aguarda até que todos os eventos tenham ocorrido - `AllOf` é equivalente ao símbolo de "&" (ou `and`).

Para compreender o funcionamento dos comandos anteriores, vamos partir de um exemplo baseado numa obscura fábula infantil: [a Lebre e a Tartaruga](https://en.wikipedia.org/wiki/The_Tortoise_and_the_Hare). 

Neste exemplo, sortearemos um tempo de corrida para cada bicho e identificaremos quem foi o vencedor. Para tanto, além do sorteio, criaremos dois eventos que representam a corrida de cada bicho:
```python
def corrida(env):
    # a lebre x tartaruga!
    # sorteia aleatoriamente os tempos dos animais
    # cria os eventos que disparam as corridas
    lebreTempo = random.normalvariate(5,2)
    tartarugaTempo = random.normalvariate(5,2)
    # cria os eventos de corrida de cada animal
    lebreEvent = env.timeout(lebreTempo, value='lebre')
    tartarugaEvent = env.timeout(tartarugaTempo, value='tartaruga')
```
Na função anterior, `corrida`, criamos os eventos `lebreEvent` e `tartarugaEvent`, que simulam, respectivamente, as corridas da lebre e da tartaruga. Mas, atenção: os eventos foram criados, mas não foram *necessariamente* executados. Como não existe um `yield` aplicado aos eventos, eles foram criados na memória do Python, e aguardam a sua exesperando o momento de serem executados no SimPy.

Agora, vamos acrescentar um `yield` com condição de que ele aguarde até que, _ao menos_, um dos bichos tenha terminado a corrida:
```python        
    # começou!
    start = env.now
    print('%3.1f Iniciada a corrida!' %(env.now))
    # simule até que alguém chegue primeiro
    resultado = yield lebreEvent | tartarugaEvent
    tempo = env.now - start
```
A variável resultado armazena nesse instante o evento que terminou primeiro. Assim, a função precisa apenas de uma lógica de comparação e impressão do bicho vencedor. O código a seguir completa o modelo e já o deixa pronto para a execução:
```python
import simpy
import random

def corrida(env):
    # a lebre x tartaruga!
    # sorteia aleatoriamente os tempos dos animais
    # cria os eventos que disparam as corridas
    lebreTempo = random.normalvariate(5,2)
    tartarugaTempo = random.normalvariate(5,2)
    # cria os eventos de corrida de cada animal
    lebreEvent = env.timeout(lebreTempo, value='lebre')
    tartarugaEvent = env.timeout(tartarugaTempo, value='tartaruga')
           
    # começou!
    start = env.now
    print('%3.1f Iniciada a corrida!' %(env.now))
    # simule até que alguém chegue primeiro
    resultado = yield lebreEvent | tartarugaEvent
    tempo = env.now - start
    
    # quem venceu?
    if lebreEvent not in resultado:
        print('%3.1f A tartaruga venceu em %3.1f minutos' %(tempo, env.now))
    elif tartarugaEvent not in resultado:
        print('%3.1f A lebre venceu em %3.1f minutos' %(tempo, env.now))
    else:
        print('%3.1f Houve um empate em %3.1f minutos' %(tempo, env.now))

random.seed(10)
env = simpy.Environment()
proc = env.process(corrida(env))
env.run(until=10)
```
Quando executado, o bicho pega:
```python
0.0 Iniciada a corrida!
5.3 A tartaruga venceu em 5.3 minutos
```
>**Observação:** a linha:
```python
> resultado = yield lebreEvent | tartarugaEvent
```
> poderia ter sido substituída, pela linha:
```python
> resultado = yield AnyOf(env, lebreEvent, tartarugaEvent)
```

## Propriedades úteis dos eventos
Um evento qualquer tem 3 propriedades que fazem a alegria de qualquer leitor:
* `Event.value`: o valor que foi passado para o evento no momento de sua criação;
* `Event.triggered`: `True`, caso o `Event` já tenha sido programado e inserido na fila de eventos do SimPy e `False`, caso contrário;
* `Event.processed`: `True`, caso o `Event` já tenha sido executado e `False`, caso contrário;

Antes de avançar - e com o intuito de facilitar o aprendizagem do *lebrístico* leitor - vamos acrescentar ao código uma função para imprimir o status de cada evento dentro de uma lista e enventos:
```python
def printEventStatus(env, eventList):
    # imprime o status das entidades
    for event in eventList:
        print('%3.1f Evento (value): %s\t programado: %s\t processado: %s'
            %(env.now, event.value, event.triggered, event.processed))   
```
Vamos agora acrescentar a função ao nosso modelo da lebre x tartaruga:
```python
import simpy
import random

def corrida(env):
    # a lebre x tartaruga!
    # sorteia aleatoriamente os tempos dos animais
    lebreTempo = random.normalvariate(50,2)
    tartarugaTempo = random.normalvariate(5,2)
    # cria os eventos de corrida de cada animal
    lebreEvent = env.timeout(lebreTempo, value='lebre')
    tartarugaEvent = env.timeout(tartarugaTempo, value='tartaruga')

    # cria lista de eventos
    eventList = [lebreEvent, tartarugaEvent]
    printEventStatus(env, eventList)
            
    # começou!
    start = env.now
    print('%3.1f Iniciada a corrida!' %(env.now))
    # simule até que alguém chegue primeiro
    resultado = yield lebreEvent | tartarugaEvent
    tempo = env.now - start
    
    # quem venceu?
    if lebreEvent not in resultado:
        print('%3.1f A tartaruga venceu em %3.1f minutos' %(tempo, env.now))
    elif tartarugaEvent not in resultado:
        print('%3.1f A lebre venceu em %3.1f minutos' %(tempo, env.now))
    else:
        print('%3.1f Houve um empate em %3.1f minutos' %(tempo, env.now))
    printEventStatus(env, eventList)

def printEventStatus(env, eventList):
    # imprime o status das entidades
    for event in eventList:
        print('%3.1f Evento (value): %s\t programado: %s\t processado: %s'
            %(env.now, event.value, event.triggered, event.processed))        
    
random.seed(10)
env = simpy.Environment()
proc = env.process(corrida(env))
env.run(until=10)
```

## Aguardando um evento ocorrer para disparar outro  `(wait_event = env.event())`

