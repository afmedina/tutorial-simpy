# Propriedades úteis dos eventos
Um evento qualquer tem 3 propriedades que fazem a alegria de qualquer leitor:
* `Event.value:` o valor que foi passado para o evento no momento de sua criação;
* `Event.triggered:` `True,` caso o `Event` já tenha sido programado e inserido na fila de eventos do SimPy e `False,` caso contrário;
* `Event.processed:` `True,` caso o `Event` já tenha sido executado e `False,` caso contrário;

Antes de avançar - e com o intuito de facilitar o aprendizagem do *lebrístico* leitor - vamos acrescentar ao código uma função para imprimir o status de cada evento dentro de uma lista e enventos:
```python
def printEventStatus(env, eventList):
    # imprime o status das entidades
    for event in eventList:
        print('%3.1f Evento (value): %s\t programado: %s\t processado: %s'
            %(env.now, event.value, event.triggered, event.processed))   
```
Vamos agora acrescentar a função ao nosso modelo original da lebre x tartaruga:
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

