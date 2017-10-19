# Solução do desafio 1

O código a seguir é uma possível solução para o desafio 1 da seção anterior. Naturalmente é possível deixá-lo mais claro, eficiente, obscuro, maligno, elegante, rápido ou lento, como todo código de programação.

O importante é que se você fez alguma que coisa que funcionou, acredito que é o suficiente para começar com o SimPy.

```python
import random                   # gerador de números aleatórios

names = ['Chewbacca', 'R2D2']   # jogadores

def transfer(winner, looser, bankroll, tossCount):
    # função que transfere o dinheiro do winner para o looser
    # imprime o vencedor do lançamento  e o bankroll de cada jogador
    bankroll[winner] += 1
    bankroll[looser] -= 1
    print("\nLançamento: %d\tVencedor: %s" % (tossCount, names[winner]))
    print("%s possui: $%d e %s possui: $%d"
            % (names[0], bankroll[0], names[1], bankroll[1]))

def coinToss(bankroll, tossCount):
    # função que sorteia a moeda e chama a transfer
    if random.uniform(0, 1) < 0.5:
        transfer(1, 0, bankroll, tossCount)
    else:
        transfer(0, 1, bankroll, tossCount)

def run2Ruin(bankroll):
    # função que executa o jogo até a ruina de um dos jogadores
    tossCount = 0               # contador de lançamentos
    while bankroll[0] > 0 and bankroll[1] > 0:
        tossCount += 1
        coinToss(bankroll,tossCount)
    winner = bankroll[1] > bankroll[0]
    print("\n%s venceu depois de %d lançamentos, fim de jogo!"
            % (names[winner], tossCount))

bankroll = [5, 5]               # dinheiro disponível para cada jogador
run2Ruin(bankroll)              # inicia o jogo
```

No meu computador, o problema anterior fornece o seguinte resultado:

```
Lançamento: 1   Vencedor: Chewbacca
Chewbacca possui: $6 e R2D2 possui: $4

Lançamento: 2   Vencedor: Chewbacca
Chewbacca possui: $7 e R2D2 possui: $3

Lançamento: 3   Vencedor: Chewbacca
Chewbacca possui: $8 e R2D2 possui: $2

Lançamento: 4   Vencedor: Chewbacca
Chewbacca possui: $9 e R2D2 possui: $1

Lançamento: 5   Vencedor: Chewbacca
Chewbacca possui: $10 e R2D2 possui: $0

Chewbacca venceu depois de 5 lançamentos, fim de jogo!
```

Note que o resultado fornecido deve ser diferente em seu computador, assim como ele se modifica a cada nova rodada no programa. Para que os resultados sejam semelhantes, precisamos utilizar o comando [`random.seed(semente)`](https://docs.python.org/3/library/random.html#random.seed\) com um mesmo valor inicial \(veja o item 1 na seção "Teste seus conhecimentos", na seção a seguir").

### Teste seus conhecimentos:

1. Cada vez que você executa o programa, a função `random.uniform(0, 1)` sorteia um novo número aleatório ente 0 e 1, tornando imprevisível o resultado do programa. Utilize a função `random.seed(semente)` para fazer com que a sequência gerada de números aleatórios seja sempre a mesma.
2. Acrescente um laço no programa principal de modo que o jogo possa ser repetido até um número pré definido de vezes. _Simule_ 100 partidas e verifique em quantas cada um dos jogadores venceu. 



