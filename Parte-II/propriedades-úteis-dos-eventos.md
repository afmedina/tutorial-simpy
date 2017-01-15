## Propriedades úteis dos eventos
Um evento possui algumas propriedades que fazem a alegria de qualquer leitor:
* `Event.value:` o valor que foi passado para o evento no momento de sua criação;
* `Event.triggered:` `True,` caso o `Event` já tenha sido engatilhado, isto é, ele está na fila de eventos do SimPy e programado para ocorrer em determinado instante da simulação; `False,` caso contrário;
* `Event.processed:` `True,` caso o `Event` já tenha sido executado e `False,` caso contrário.

Existe uma dificuldade inicial que deve ser obrigatoriamente superada pelo programador: compreender a sequência de criação, disparo e execução de um evento em SimPy. 

No momento da sua criação, todo evento surge como um objeto na memória do SimPy e, inicialmente, ele encontra-se no estado *não engatilhado* (`Event.triggered = False`). Quando o evento é programado para ocorrer em determinado instante da simulação, ele passa ao estado *engatilhado* (`Event.triggered = True`). Quando o evento é finalmente executado no instante determinado, seu estado passa a processado: (`Event.processed = True`).
Por exemplo, quando você adiciona ao modelo a linha de comando:
```python
yield env.timeout(10)
```
O SimPy processará a linha na seguinte sequência de passos (figura):

1. Cria na memória um novo evento dentro do `Environment env`;
2. Engatilha o evento para ser processado dali a 10 unidades de tempo (minutos, por exemplo);
3. Quando a simulação atinge o instante de processamento esperado (passados os 10 minutos), o evento é processado. Automaticamente, o comando `yield` recebe o sinal de sucesso do processamento e o fluxo de execução do modelo retoma seu curso normal, processando a linha seguinte do modelo.

A figura ... elenca os diversos tipos de eventos que discutimos ao longo deste livro e sua sequência usual de criação->engatilhamento->processamento. Note como eles estão intrinsecamente ligados à questão do tempo de simulação. 

Antes de avançar - e com o intuito de facilitar o aprendizagem do *lebrístico* leitor - acrecentaremos ao modelo da Lebre e da Tartaruga uma função para imprimir as propriedade dos eventos. Basicamente ela recebe uma lista de eventos e imprime na tela as propriedades de cada evento da lista:
```python
def printEventStatus(env, eventList):
    # imprime o status das entidades
    for event in eventList:
        print('%3.1f value: %s\t programado: %s\t processado: %s'
            %(env.now, event.value, event.triggered, event.processed))     
```
Basicamente, devemos criar uma lista a partir dos eventos de corrida da Lebre e da Tartaruga, para fornecer a lista para nossa função de impressão de propriedades dos eventos:
```python
# cria os eventos de corrida de cada animal
lebreEvent = env.timeout(lebreTempo, value='lebre')
tartarugaEvent = env.timeout(tartarugaTempo, value='tartaruga')

# cria lista de eventos
eventList = [lebreEvent, tartarugaEvent]
printEventStatus(env, eventList)
```
O modelo completo, com a impressão das propriedades dos eventos, ficaria:
```python
import simpy
import random

def corrida(env):
    # a lebre x tartaruga!
    # sorteia aleatoriamente os tempos dos animais
    lebreTempo = random.normalvariate(5,2)
    tartarugaTempo = random.normalvariate(5,2)
    
    # cria os eventos de corrida de cada animal
    lebreEvent = env.timeout(lebreTempo, value='lebre')
    tartarugaEvent = env.timeout(tartarugaTempo, value='tartaruga')
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
        print('%3.1f A tartaruga venceu em %3.1f minutos' %(env.now, tempo))       
    elif tartarugaEvent not in resultado:
        print('%3.1f A lebre venceu em %3.1f minutos' %(env.now, tempo))
    else:
        print('%3.1f Houve um empate em %3.1f minutos' %(env.now, tempo))
    printEventStatus(env, eventList)

def printEventStatus(env, eventList):
    # imprime o status das entidades
    for event in eventList:
        print('%3.1f value: %s\t programado: %s\t processado: %s'
            %(env.now, event.value, event.triggered, event.processed))          

random.seed(10)
env = simpy.Environment()
env.process(corrida(env))
env.run(until=10)
```
Quando simulado, o modelo fornece como resultado:
```python
0.0 value: lebre         programado: True        processado: False
0.0 value: tartaruga     programado: True        processado: False
0.0 Iniciada a corrida!
5.3 A tartaruga venceu em 5.3 minutos
5.3 value: lebre         programado: True        processado: False
5.3 value: tartaruga     programado: True        processado: True
```
Repare no instante 0.0, que os eventos do tipo `timeout` são programados imediatamente após sua criação. Quando a tartaruga vence, o seus evento é considerado processado e a lebre não, algo esperado. Contudo, o que aconteceria se simulassemos o modelo por mais tempo? Ou seja, se deixássemos o modelo processando por mais tempo, a lebre apareceria na linha de chegada?
No modelo a seguir, acrescentamos à função corrida um evento `timeout,` logo após a chegada, que representaria a comemoração da tartaruga por 4 minutos:
```python
def corrida(env):
    # a lebre x tartaruga!
    # sorteia aleatoriamente os tempos dos animais
    lebreTempo = random.normalvariate(5,2)
    tartarugaTempo = random.normalvariate(5,2)
    
    # cria os eventos de corrida de cada animal
    lebreEvent = env.timeout(lebreTempo, value='lebre')
    tartarugaEvent = env.timeout(tartarugaTempo, value='tartaruga')
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
        print('%3.1f A tartaruga venceu em %3.1f minutos' %(env.now, tempo))       
    elif tartarugaEvent not in resultado:
        print('%3.1f A lebre venceu em %3.1f minutos' %(env.now, tempo))
    else:
        print('%3.1f Houve um empate em %3.1f minutos' %(env.now, tempo))
    printEventStatus(env, eventList)
    
    # a tartaruga inicia a comemoração!
    yield env.timeout(4)
    printEventStatus(env, eventList)
```
Como resultado, agora o modelo fornece como saída:
```python
0.0 value: lebre         programado: True        processado: False
0.0 value: tartaruga     programado: True        processado: False
0.0 Iniciada a corrida!
5.3 A tartaruga venceu em 5.3 minutos
5.3 value: lebre         programado: True        processado: False
5.3 value: tartaruga     programado: True        processado: True
9.3 value: lebre         programado: True        processado: True
9.3 value: tartaruga     programado: True        processado: True
```
Repare que no instante 9.3 minutos o evento da lebre está processado. Isto é importantíssimo e não avance sem compreender o que está acontecendo: quando a linha:
```python
# simule até que alguém chegue primeiro
resultado = yield lebreEvent | tartarugaEvent
```
Aguardou até que um dos eventos tivesse terminado, ela **não cancelou** o outro evento que, por ser um `timeout`, continuou na fila de eventos até que o SimPy pudesse processá-lo. (Note que o instante 9.3 não representa o instante de processamento do processo, provavelmente a lebre cruzou a linha de chegada após isso).
> Observação: até a presente versão do SimPy, não existe a possíbilidade de se cancelar um evento já programado.

## Conceitos desta seção
| Conteúdo | Descrição |
| -- | -- |
| `Event.value` | o valor que foi passado para o evento no momento de sua criação. |
| `Event.triggered` | `True,` caso o `Event` já tenha sido engatilhado, isto é, ele está na fila de eventos do SimPy e programado para ocorrer em determinado instante da simulação; `False,` caso contrário. |
| `Event.processed` | `True,` caso o `Event` já tenha sido executado e `False,` caso contrário. |

## Desafio
> Desafio 25: modifique o modelo anterior para que ele aguarde até a chegada da lebre.