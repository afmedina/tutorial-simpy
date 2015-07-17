# Tutorial SimPy: solução do desafio 1

O código a seguir é uma possível solução para o desafio 1. Naturalmente é possível deixá-lo mais claro, eficiente, obscuro, elegante, rápido, lento, como todo código de programação.

O importante é que se você fez alguma que coisa que funcionou, acredito que está pronto para o SimPy.

```
# -*- coding: utf-8 -*-
from __future__ import print_function # para compatibilidade da função print com o Python 3
import random # gerador de números aleatórios


names = ['Chewbacca', 'R2D2']

def transfer(winner,looser,bankroll,tossCount):
    bankroll[winner] += 1
    bankroll[looser] -= 1
    print("Vencedor: %s. Agora %s possui: $%d e %s possui: $%d" % (names[winner], names[0], bankroll[0], names[1],bankroll[1]))
    
def coinToss(bankroll,tossCount):
    if random.uniform(0,1) < 0.5:
        transfer(1,0,bankroll,tossCount)
    else:
        transfer(0,1,bankroll,tossCount)

def run2Ruin(bankroll):
    tossCount = 0
    while bankroll[0] > 0 and bankroll[1] > 0:
        tossCount += 1
        coinToss(bankroll,tossCount)
    winner = bankroll[1] > bankroll[0]
    print("%s venceu depois de %d iterações, fim de jogo!" % (names[winner],tossCount))

bankroll = [5,5]
run2Ruin(bankroll)
```
