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
Na função anterior, `corrida`, criamos os eventos `lebreEvent` e `tartarugaEvent`, que simulam, respectivamente, as corridas da lebre e da tartaruga. Mas, atenção: apesar de criados, os eventos não foram *necessariamente* executados. Como não existe um `yield` aplicado aos eventos, eles foram criados na memória do Python, mas a função corrida não vai aguardar o término de sua execução. 

## Aguardando até que, ao menos, um evento termine com AnyOf
Para garantir que a função `corrida` aguarde até que, ao menos, um dos corredores termine a prova, devemos acrescentar um `yield AnyOf()` (que pode ser substituído por "|"):
```python        
    # começou!
    start = env.now
    print('%3.1f Iniciada a corrida!' %(env.now))
    # simule até que alguém chegue primeiro
    resultado = yield lebreEvent | tartarugaEvent
    tempo = env.now - start
```
O `yield` garante que a função aguardará até que um dos dois eventos, lebreEvent ou tartarugaEvent, termine e a variável `resultado` armazenará qual evento terminou primeiro. Assim, para sabermos que venceu, basta explorarmos o valor contindo na variável `resultado`. 
O código a seguir completa o modelo, testando qual dos dois eventos está na variável `resultado`:
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

## Aguardando todos os eventos com `AllOf`

Neste caso, podemos forçar um empante na corrida, aguardando que os dois corredores cruzem a linha de chegada. Para isso, basta substituir a linha:
```python
resultado = yield lebreEvent | tartarugaEvent
```
por:
```python
resultado = yield lebreEvent & tartarugaEvent
```
Quando simulado, o novo programa forncece como saída:
```python
0.0 Iniciada a corrida!
5.4 Houve um empate em 5.4 minutos
```
O que ocorreu? Neste caso, o comando `AllOf` (ou "&") aguardou até que os dois eventos terminassem para liberar o processamento da linha seguinte de código.

## Comprendendo o resultado dos comandos `AllOf` e `AnyOf`
Agora que já sabemos o que fazem os comandos `AllOf` e `AnyOf`, vamos discutir nessa seção um pouco mais sobre o que exatente esses comandos retornam.
Incialmente, imprima os valores dos eventos e da variável `resultado`, para descobrir seus conteúdos:
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
    print('lebreEvent= ', lebreEvent)
    print('tartarugaEvent= ', tartarugaEvent)
    # começou!
    start = env.now
    print('%3.1f Iniciada a corrida!' %(env.now))
    # simule até que alguém chegue primeiro
    resultado = yield lebreEvent & tartarugaEvent
    print('resultado = ', resultado)
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
Quando executado, o programa fornecce:
```python
lebreEvent=  <Timeout(5.428964407135667, value=lebre) object at 0xa592470>
tartarugaEvent=  <Timeout(5.33749212083634, value=tartaruga) object at 0xa5920f0>
0.0 Iniciada a corrida!
resultado =  <ConditionValue {<Timeout(5.33749212083634, value=tartaruga) object at 0xa5920f0>: 'tartaruga', <Timeout(5.428964407135667, value=lebre) object at 0xa592470>: 'lebre'}>
5.4 Houve um empate em 5.4 minutos
```
Pela saída anterior, descobrimos, inicialmente, que os eventos são *objetos* do tipo `Timeout` e que armazenam tanto o tempo de espera, quanto o valor (ou `value`) fornecido na função.
 Um pouco mais abaixo, a saída revela que a variável `resultado` é um objeto da classe `ConditionValue` que, aparentemente, contém um dicionário de eventos em seu interior. Para acessar esse dicionário, o SimPy fornece o método `.todict()`, assim:
 ```python
 resutado.todict()
 ```
 fornece:
 ```python
 {<Timeout(5.428964407135667, value=lebre) object at 0xa18e30>: 'lebre', <Timeout(5.33749212083634, value=tartaruga) object at 0xa18eb0>: 'tartaruga'}
```
Que nada mais é do que um dicionário padrão do Python.