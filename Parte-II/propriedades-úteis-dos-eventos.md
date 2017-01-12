## Propriedades úteis dos eventos
Um evento possui algumas propriedades que fazem a alegria de qualquer leitor:
* `Event.value:` o valor que foi passado para o evento no momento de sua criação;
* `Event.triggered:` `True,` caso o `Event` já tenha sido engatilhado, isto é, ele está na fila de eventos do SimPy e programado para ocorrer em determinado instante da simulação; `False,` caso contrário;
* `Event.processed:` `True,` caso o `Event` já tenha sido executado e `False,` caso contrário.

Existe uma dificuldade inicial que deve ser obrigatoriamente superada pelo programador: compreender a sequência de criação, disparo e execução de um evento em SimPy. 

No momento da sua criação, todo evento surge como um objeto na memória do SimPy e, inicialmente, ele encontra-se no estado *não engatilhado* (`Event.triggered = False`). Quando o evento é programado para ocorrer em determinado instante da simulação, ele passa ao estado *engatilhado* (`Event.triggered = True`). Quando o evento é finalmente executado no instante determinado, seu estado passa a processado: (`Event.processed = True`).
Por exemplo, quando você adiciona ao modelo uma linha:
```python
yield env.timeout(10)
```
O SimPy processa a linha na seguinte seqüência (figura):
1. Cria na memória um novo evento dentro do `Environment env`;
2. Engatilha o evento para ser processado dali a 10 unidades de tempo (minutos, por exemplo);
3. Quando a simulação atinge o instante de processamento esperado (10 minutos), o SimPy processa o evento e informa ao programa o sucesso da execução. Automaticamente, como o comando `yield` recebe o sinal de sucesso do processamento e o fluxo de execução do modelo retoma seu curso normal, processando a linha seguinte de código.

A figura ... elenca os diversos tipos de eventos que discutimos ao longo deste livro e sua sequência usual de criação->engatilhamento->processamento. Note como eles estão intrinsecamente ligados a questão do tempo de simulação.

Antes de avançar - e com o intuito de facilitar o aprendizagem do *lebrístico* leitor - vamos acrescentar ao código uma função para imprimir o status de cada evento dentro de uma lista e eventos. Basicamente ela recebe uma lista de eventos e imprime na tela as propriedades de cada evento da lista:
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

