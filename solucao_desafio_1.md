# Tutorial SimPy: solução do desafio 1

O código a seguir é uma possível solução para o desafio 1 da seção anterior. Naturalmente é possível deixá-lo mais claro, eficiente, obscuro, elegante, rápido ou lento, como todo código de programação.

O importante é que se você fez alguma que coisa que funcionou, acredito que é o suficiente para começar com o SimPy.

```python
# -*- coding: utf-8 -*-
import random # gerador de números aleatórios


names = ['Chewbacca', 'R2D2']

def transfer(winner, looser, bankroll, tossCount):
    bankroll[winner] += 1
    bankroll[looser] -= 1
    print("Vencedor: %s. Agora %s possui: $%d e %s possui: $%d" % (names[winner], names[0], bankroll[0], names[1],bankroll[1]))
    
def coinToss(bankroll, tossCount):
    if random.uniform(0,1) < 0.5:
        transfer(1, 0, bankroll, tossCount)
    else:
        transfer(0, 1, bankroll, tossCount)

def run2Ruin(bankroll):
    tossCount = 0
    while bankroll[0] > 0 and bankroll[1] > 0:
        tossCount += 1
        coinToss(bankroll,tossCount)
    winner = bankroll[1] > bankroll[0]
    print("%s venceu depois de %d iterações, fim de jogo!" % (names[winner], tossCount))

bankroll = [5, 5]
run2Ruin(bankroll)
```

### Teste seus conhecimentos:
1. Cada vez que você executa o programa, a função `random.uniform(0, 1)` sorteia novos números aleatórios, tornando imprevisível o resultado do programam a cada rodada. Utilize a função `random.seed()` para fazer com que a sequência gerada de números aleatórios seja sempre a mesma.
2. Acrescente um laço no programa principal de modo que o jogo possa ser repetido até um número pré definido de vezes. *Simule* 100 partidas e verifique em quantas cada um dos jogadores venceu. 