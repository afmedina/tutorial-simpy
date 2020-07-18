# Solução do desafio 25

## Solução do desafio 25

> Desafio 25: modifique o modelo anterior para que ele aguarde até a chegada da lebre.

Para este desafio, basta alterarmos a parte do modelo que lida com a decisão de quem venceu:

```python
    # quem venceu?
    if lebreEvent not in resultado:
        print('%3.1f A tartaruga venceu em %3.1f minutos' %(env.now, tempo))
        printEventStatus(env, eventList)
        # aguarda o fim do evento da lebre
        yield lebreEvent
        printEventStatus(env, eventList)
        print('%3.1f A lebre chega em segundo...' %(env.now))
    elif tartarugaEvent not in resultado:
        print('%3.1f A lebre venceu em %3.1f minutos' %(env.now, tempo))
        printEventStatus(env, eventList)
        # aguarda o fim do evento da tartaruga
        yield tartarugaEvent
        printEventStatus(env, eventList)
        print('%3.1f A tartaruga chega em segundo...' %(env.now))
    else:
        print('%3.1f Houve um empate em %3.1f minutos' %(env.now, tempo))
        printEventStatus(env, eventList)
```

Quando simulado, o modelo anterior fornece:

```python
0.0 value: lebre         programado: True        processado: False
0.0 value: tartaruga     programado: True        processado: False
0.0 Iniciada a corrida!
5.3 A tartaruga venceu em 5.3 minutos
5.3 value: lebre         programado: True        processado: False
5.3 value: tartaruga     programado: True        processado: True
5.4 value: lebre         programado: True        processado: True
5.4 value: tartaruga     programado: True        processado: True
5.4 A lebre chega em segundo...
```

Nessa replicação a lebre perdeu por 0,1 minutos apenas. Um cochilada imperdoável da lebre, MEU AMIGO!

Na próxima seção, veremos uma tática mais interessante para resolver o mesmo problema a partir da novidade a ser apresentada, os `callbacks.`

## Teste seus conhecimentos

1. Crie um processo `chuva` que ocorre entre intervalos exponencialmente distribuídos com média de 5 minutos e dura, em média, 5 minutos exponencialmente distribuídos também. Quando a chuva começa, os corredores são 50% mais lentos durante o período. \(Dica: quando a chuva começar, construa novos eventos `timeout` e despreze os anteriores, mas calcule antes quais as velocidades dos corredores\).
2. Modifique o modelo para que ele execute um número configurável de replicações e forneça como resposta a porcentagem das vezes em que cada competidor venceu.

