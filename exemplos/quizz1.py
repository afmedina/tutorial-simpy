# -*- coding: utf-8 -*-
from __future__ import print_function # para compatibilidade da função print com o Python 3
import random # gerador de números aleatórios


names = ['Chewbacca', 'R2D2']

def transfer(winner,looser,bankroll,tossCount):
    bankroll[winner] += 1
    bankroll[looser] -= 1
    print("Jogada %d vencedor: %s!" % (tossCount, names[winner]))
    print("    Agora %s possui: $%d e %s possui: $%d" % (names[0], bankroll[0], names[1],bankroll[1]))
    print()
    
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
    winner = bankroll[1]>bankroll[0]
    print("%s venceu depois de %d jogadas, fim de jogo!" % (names[winner],tossCount))

bankroll = [5,5]
run2Ruin(bankroll)