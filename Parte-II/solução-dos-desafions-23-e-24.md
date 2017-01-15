## Desafios
>**Desafio 23:** Considere que existe uma probabilidade de que a Lebre, por alguma razão mal explicada (eu realizaria um teste antidoping nos competidores), resolva que é uma boa idéia tirar uma soneca de 5 mintos em algum instante entre 2 e 10 minutos do início da corrida. Modele esta nova situação (dica: crie um função `soneca` que gera um evento que pode ocasionar a parada da Lebre ainda durante a corrida).

Para este desafio será criada uma função para gerar a soneca e uma função adicional para identificar o vencedor, pois agora a tartaruga pode (ou não) vencer enquanto a lebre estiver dormindo.

Començando pela função que determina o vencedor:
```python
def imprimeVencedor(start, resultado, lebreEvent, tartarugaEvent):
    # determina o vencedor da corrida
    tempo = env.now - start
    # quem venceu?
    if lebreEvent not in resultado:
        print('%3.1f A tartaruga venceu em %3.1f minutos' %(env.now, tempo))
    elif tartarugaEvent not in resultado:
        print('%3.1f A lebre venceu em %3.1f minutos' %(env.now, tempo))
    else:
        print('%3.1f Houve um empate em %3.1f minutos' %(env.now, tempo))
```
A função `soneca` a seguir, cria um evento sonecaEvent, sorteia o instante da soneca e processa o evento no instante correto:
```python
def soneca(env):
    global sonecaEvent

    # cria o evento da soneca
    sonecaEvent = env.event()
    # sorteia o instante da soneca
    inicioSoneca = random.uniform(2, 10)
    # aguarda instante da soneca
    yield env.timeout(inicioSoneca)
    # durma!
    sonecaEvent.succeed()
```
A função corrida, agora deve lidar com as diversas situações possiveis: uma soneca da lebre durante a corrida, a lebre acordando, a tartaruga ou a lebre vencendo. Essas diversas situações podem ser facilmente modeladas por um conjunto de lógicas de desvio condicional `if` concatenadas com operções do tipo `AnyOf`:
```python
def corrida(env):
    # a lebre x tartaruga!
    global sonecaEvent

    # sorteia aleatoriamente os tempos dos animais
    lebreTempo = random.normalvariate(5,2)
    tartarugaTempo = random.normalvariate(5,2)
    # cria os eventos de corrida de cada animal
    lebreEvent = env.timeout(lebreTempo, value='lebre')
    tartarugaEvent = env.timeout(tartarugaTempo, value='tartaruga')

    # começou!
    start = env.now
    print('%3.1f Iniciada a corrida!' %(env.now))
    # simule até que alguém chegue primeiro ou alguém pegue no sono...
    resultado = yield lebreEvent | tartarugaEvent | sonecaEvent

    if sonecaEvent in resultado:
        # a lebre dormiu!
        lebreTempo -= env.now - start
        print('%3.1f A lebre capotou de sono?!?!' %(env.now))
        lebreAcorda = env.timeout(5, value='lebre')
        resultado = yield lebreAcorda | tartarugaEvent

        if tartarugaEvent in resultado:
            # a tartaruga venceu durante o sono da lebre
            imprimeVencedor(start, resultado, None, tartarugaEvent)
            env.exit()
        else:
            # a lebre acordou antes da corrida terminar
            print('%3.1f A lebre acordou, amigo!' %(env.now))
            lebreEvent2 = env.timeout(lebreTempo, value='lebre')
            resultado = yield lebreEvent2 | tartarugaEvent
            # alguém venceu!
            imprimeVencedor(start, resultado, lebreEvent2, tartarugaEvent)
    else:
        # alguém venceu, antes da lebre pegar no sono!
        imprimeVencedor(start, resultado, lebreEvent, tartarugaEvent)
```
Não devemos esquecer de inciar o processo da soneca:
```python
random.seed(100)
env = simpy.Environment()
# inicia processo da soneca
env.process(soneca(env))
# inicia a corrida
env.process(corrida(env))

env.run(until=10)
```
Note, na função `corrida,`que quando a tartaruga vence enquanto a lebre está dormindo, a função `imprimeVencedor` é chamada com o parâmetro `lebreEvent=None`, já informando à função que a lebre perdeu.

Quando o modelo anterior é simulado, fornece como resultado:
```python
0.0 Iniciada a corrida!
3.2 A lebre capotou de sono?!?!
7.6 A tartaruga venceu em 7.6 minutos
```
Você pode alterar o valor da semente geradora de números aleatórios - na linha `random.seed(...)` - e apostar com os amigos quem vencerá a próxima corrida!

>**Desafio 24:** É interessante notar, que mesmo quando um dos competidores *perde* a corrida, de fato, o respectivo evento **não é** cancelado. Altere o modelo anterior para marcar o horário de chegada dos dois competidores, garantindo que os eventos `lebreEvent` e `tartarugaEvent` sejam executados até o fim.

Uma possível solução para o desafio é transformar o a função `imprimeVencedor` em um processo que, após informar o vencedor, continua até que o outro competidor passe pela linha de chegada. Por exemplo, podemos uma alternativa seria:

```python
def imprimeVencedor(env, start, resultado, lebreEvent, tartarugaEvent):
    # determina o vencedor da corrida
    tempo = env.now - start
    # quem venceu?
    if lebreEvent not in resultado:
        print('%3.1f A tartaruga venceu em %3.1f minutos' %(env.now, tempo))
        if lebreEvent:
            yield lebreEvent
            print('%3.1f A lebre chega em 2º lugar' %(env.now))
    elif tartarugaEvent not in resultado:
        print('%3.1f A lebre venceu em %3.1f minutos' %(env.now, tempo))
        yield tartarugaEvent
        print('%3.1f A tartaruga chega em 2º lugar' %(env.now))
    else:
        print('%3.1f Houve um empate em %3.1f minutos' %(env.now, tempo))
```

A função `corrida` deve agora utilizar comandos do tipo `env.process(imprimeVencedor)` para inciar o processo que determina quem venceu e continua a corrida até que o outro competidor chegue. Note, no código a seguir, que apenas no caso da lebre ser pega ainda dormindo, a modificação do código é um pouco mais trabalhosa:
```python
def corrida(env):
    # a lebre x tartaruga!
    global sonecaEvent

    # sorteia aleatoriamente os tempos dos animais
    lebreTempo = random.normalvariate(5,2)
    tartarugaTempo = random.normalvariate(5,2)
    # cria os eventos de corrida de cada animal
    lebreEvent = env.timeout(lebreTempo, value='lebre')
    tartarugaEvent = env.timeout(tartarugaTempo, value='tartaruga')

    # começou!
    start = env.now
    print('%3.1f Iniciada a corrida!' %(env.now))
    # simule até que alguém chegue primeiro ou alguém pegue no sono...
    resultado = yield lebreEvent | tartarugaEvent | sonecaEvent

    if sonecaEvent in resultado:
        # a lebre dormiu!
        lebreTempo -= env.now - start
        print('%3.1f A lebre capotou de sono?!?!' %(env.now))
        lebreAcorda = env.timeout(lebreTempo, value='acorda')
        resultado = yield lebreAcorda | tartarugaEvent

        if tartarugaEvent in resultado:
            # a tartaruga venceu durante o sono da lebre
            env.process(imprimeVencedor(env, start, resultado, None, tartarugaEvent))
            yield lebreAcorda
            print('%3.1f A lebre acordou, amigo!' %(env.now))
            yield env.timeout(lebreTempo, value='lebre')
            print('%3.1f A lebre chega em 2º lugar' %(env.now))
            # termina o processo
            env.exit()
        else:
            # a lebre acordou antes da corrida terminar
            print('%3.1f A lebre acordou, amigo!' %(env.now))
            lebreEvent2 = env.timeout(lebreTempo, value='lebre')
            resultado = yield lebreEvent2 | tartarugaEvent
            # alguém venceu!
            env.process(imprimeVencedor(env, start, resultado, lebreEvent2, tartarugaEvent))
    else:
        # alguém venceu, antes da lebre pegar no sono!
        env.process(imprimeVencedor(env, start, resultado, lebreEvent, tartarugaEvent))
```
Quando executado, o modelo completo fornece como saída:
```python
0.0 Iniciada a corrida!
3.2 A lebre capotou de sono?!?!
7.6 A tartaruga venceu em 7.6 minutos
8.2 A lebre acordou, amigo!
9.3 A lebre chega em 2º lugar
```
O que é importante destacar é que o comando `AnyOf` **não** paraliza um evento que ainda não foi processado. No saída exemplo, a tartaruga venceu e o processamento da linha:
```python
yield lebreAcorda
```
Fez o modelo aguardar até que o evento da lebre acordar fosse processado (no instante determinado quando o evento foi criado). Não houve, portanto, um novo evento criado para a lebre, apenas aguardamos a conclusão do evento já engatilhado na memória, mas não concluído. 

## Teste seus conhecimentos
1. Generalize a função `corrida` para um número qualquer de competidores utilizando o operador `**kwargs` visto no Desafio 19. 
1. Construa um gráfico com a evolução da prova, isto é, a distância percorrida por cada competidor x tempo de prova.
