# Aguardando múltiplos eventos ao mesmo tempo com `AnyOf `e `AllOf`

Uma funcionalidade importante do SimPy é permitir que uma entidade aguarde até que dois ou mais eventos ocorram para então prosseguir com o processo. O SimPy possui duas opções muito interessantes para isso:

* `AnyOf(env, eventos):` aguarda até que um dos eventos tenham ocorrido - `AnyOf` é equivalente ao símbolo de "|" (ou `or`);
* `AllOf(env, eventos):` aguarda até que todos os eventos tenham ocorrido - `AllOf` é equivalente ao símbolo de "&" (ou `and`).

Para compreender o funcionamento dos comandos anteriores, partiremos de um exemplo baseado numa obscura fábula infantil: [a Lebre e a Tartaruga](https://en.wikipedia.org/wiki/The_Tortoise_and_the_Hare). 

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
Na função `corrida,` criamos os eventos `lebreEvent` e `tartarugaEvent`, que simulam, respectivamente, as corridas da lebre e da tartaruga. Mas, lembre-se: apesar de criados, os eventos ainda não foram *necessariamente* executados. Como não existe um `yield` aplicado aos eventos, eles foram criados na memória do Python, mas só serão considerados *processados* após o tempo de simulação avançar o suficiente para que os tempos de `timeout` tenham passado.

De outra forma, os eventos `lebreEvent` e `tartarugaEvent` foram *disparados*, mas não processados, pois a função `corrida` ainda não tem um comando que aguarda o término do processamento desses eventos. 

## Aguardando até que, ao menos, um evento termine com `AnyOf`
Para garantir que a função `corrida` aguarde até que, ao menos, um dos corredores termine a prova, uma opção é acrescentar um `yield AnyOf()` (que pode ser substituído por "|") após a criação dos eventos:
```python        
    # começou!
    start = env.now
    print('%3.1f Iniciada a corrida!' %(env.now))
    # simule até que o ao menos um dos eventos termine
    resultado = yield lebreEvent | tartarugaEvent
    tempo = env.now - start
```
O `yield` garante que a função aguardará até que um dos dois eventos - `lebreEvent` ou `tartarugaEvent` - termine e a variável `resultado` armazenará qual desses eventos terminou primeiro (ou mesmo os dois, em caso de empate). Assim, para sabermos quem venceu, basta explorarmos o valor contindo na variável `resultado`. 
O código a seguir completa o modelo, testando qual dos dois eventos está na variável `resultado`:
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
Quando o modelo anterior é executado, o bicho pega:
```python
0.0 Iniciada a corrida!
5.3 A tartaruga venceu em 5.3 minutos
```
>**Observação:** a linha:
```python
> resultado = yield lebreEvent | tartarugaEvent
```
> Poderia ter sido substituída, pela linha:
```python
> resultado = yield AnyOf(env, lebreEvent, tartarugaEvent)
```

## Aguardando todos os eventos com `AllOf`

Para não deixar ninguém triste, poderíamos forçar um empante na corrida, aguardando que a função `corrida` aguarde até que os dois eventos sejam concluídos para decretar o vencedor. Para isso, basta substituir a linha:
```python
resultado = yield lebreEvent | tartarugaEvent
```
por:
```python
resultado = yield lebreEvent & tartarugaEvent
```
Quando simulado, o novo modelo forncece como saída:
```python
0.0 Iniciada a corrida!
5.4 Houve um empate em 5.4 minutos
```
O que ocorreu? Neste caso, o comando `AllOf` (ou "&") aguardou até que os dois eventos terminassem para liberar o processamento da linha seguinte de código e nosso desvio de condição `if` identificou que a variável `resultado` possuia os dois eventos armazenados.

## Comprendendo melhor a saída dos comandos `AllOf` e `AnyOf`
Agora que já sabemos o que fazem os comandos `AllOf` e `AnyOf`, vamos explorar nessa seção um pouco mais sobre o que exatente esses comandos retornam.

Incialmente, imprima os valores dos eventos e da variável `resultado`, para descobrir seus conteúdos:
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
resultado =  <ConditionValue {<Timeout(5.33749212083634, value=tartaruga) object at 0xa5920f0>: 'tartaruga',
<Timeout(5.428964407135667, value=lebre) object at 0xa592470>: 'lebre'}>
5.4 Houve um empate em 5.4 minutos
```
Pela saída anterior, descobrimos, inicialmente, que os eventos são *objetos* do tipo `Timeout` e que armazenam tanto o tempo de espera, quanto o valor (ou `value`) fornecido na chamada da função `env.timeout.`

Um pouco mais abaixo, a saída revela que a variável `resultado` é um objeto da classe `ConditionValue` que, aparentemente, contém um dicionário de eventos em seu interior. Para acessar esse dicionário, o SimPy fornece o método `.todict():`
 ```python
 resutado.todict()
 ```
 Que retorna:
 ```python
 {<Timeout(5.428964407135667, value=lebre) object at 0xa18e30>: 'lebre',
 <Timeout(5.33749212083634, value=tartaruga) object at 0xa18eb0>: 'tartaruga'}
```
Que nada mais é do que um dicionário padrão do Python, onde as `keys` são os eventos e os `items` são os valores dos eventos.

## Conceitos desta seção
| Conteúdo | Descrição |
| -- | -- |
| `AnyOf(env, eventos)` | aguarda até que um dos eventos tenham ocorrido - `AnyOf` é equivalente ao símbolo de "\|" (ou `or`). |
| `AllOf(env, eventos)` | aguarda até que todos os eventos tenham ocorrido - `AllOf` é equivalente ao símbolo de "&" (ou `and`). |

## Desafios
>**Desafio 23:**