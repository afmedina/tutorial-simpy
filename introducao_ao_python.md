#Tutorial SimPy: Introdução ao Python
Antes de começarmos com o SimPy, precisamos garantir que você tenha algum conhecimento mínimo de Python. Se você julga que seus conhecimentos na linguagem são razoáveis, a recomendação é que você pule para a seção seguinte,  “Teste seus conhecimentos em Python”.

<!---
acho que ficaria melhor inverter a ordem, como comentei anteriormente...

Não, pq precisa instalar antes.
--->

Se você nunca teve contato com a linguagem, aviso que não pretendemos construir uma "introdução" ou "tutorial" para o Python, simplesmente porque isso é o que mais existe disponível na internet. 

Procure um tutorial rápido (já vi um até de 10 minutos!) e mãos à obra! Nada mais fácil do que aprender o básico de Python.

Sugestões:

1. Um curso muito bom no Udacity (20 horas): [Programming Foundations with Python](https://www.udacity.com/course/programming-foundations-with-python--ud036) (clicando no botão azul “Access course materials”, você faz o curso de graça, mas sem receber o certificado). A vantagem do Udacity é que você pode começar o curso a hora que quiser.
2. Outro curso muito bom é o da CodeAcademy (13 horas): [Python](https://www.codecademy.com/pt-BR/learn/python)
2.	Um tutorial muito rápido (1 hora): [Python in One Easy Lesson](http://cs.stanford.edu/people/nick/python-in-one-easy-lesson/).
3.	Um tutorial completo: [Tutorial Python](http://wiki.python.org.br/Tutorial_Python).
4.	Outro curso muito bom, este no Coursera: [Introdução à Programação Interativa em Python (Parte 1)](https://pt.coursera.org/course/interactivepython1).
5.	Eu tenho sempre na minha mesa um ótimo livro de Python: Summerfield, Mak. Programming in Python 3: a complete introduction. Addison-Wesley Professional. 2012. Este livro já foi traduzido para o Português e pode ser encontrado na [amazon](http://www.amazon.com.br/Programa%C3%A7%C3%A3o-Em-Python-Mark-Summerfield/dp/8576083841/ref=sr_1_7?s=books&ie=UTF8&qid=1448738880&sr=1-7&keywords=python).

<!---
e comprei um livro para a Renata - Python for Kids, legalzinho...
--->

Feito o tutorial, curso ou aprendido mesmo tudo sozinho, teste seus conhecimentos para verificar se você sabe o básico *necessário* de Python para começar com o SimPy.
##Teste seus conhecimentos em Python: o problema da ruina do apostador
O [problema da ruina do apostador](http://en.wikipedia.org/wiki/Gambler%27s_ruin) é um problema clássico proposto por Pascal em uma carta para Fermat em 1656. A versão aqui apresentada é uma simplificação visando avaliar seus conhecimentos em Python.
> **Desafio**: dois apostadores iniciam um jogo de cara ou coroa em que cada um deles aposta $1 sempre em um mesmo lado da moeda. O vencedor leva a aposta total ($2). Cada jogador tem incialmente $10 disponíveis para apostar. O jogo termina quando um dos jogadores atinge a ruina e não tem mais dinheiro para apostar.

Construa três funções:

1. ` transfer(winner, looser, bankroll, tossCount)`: transfere o valor do jogador perdedor para o vencedor e imprime na tela o nome do vencedor.;

2. `coinToss(bankroll, tossCount):` sorteia o vencedor do cara ou coroa;

3. ` run2Ruin(bankroll)`: mantém um loop permanente até que um dos jogadores entrem em ruina


Teste o programa com os parâmetros a seguir (você pode utilizar esse código como um template):

```# Tutorial SimPy: solução do desafio 1

O código a seguir é uma possível solução para o desafio 1 da seção anterior. Naturalmente é possível deixá-lo mais claro, eficiente, obscuro, elegante, rápido, lento, como todo código de programação.

O importante é que se você fez alguma que coisa que funcionou, acredito que está pronto para o SimPy.

```python
# -*- coding: utf-8 -*-
from __future__ import print_function # para compatibilidade da função print com o Python 3
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
from __future__ import print_function # para compatibilidade da função print com o Python 3
import random # gerador de números aleatórios


names = ['Chewbacca', 'R2D2'] # nomes dos jogadores
def transfer(winner, looser, bankroll, tossCount):
# transfere o valor do jogador perdedor para o vencedor e imprime na tela o nome do vencedor

   
def coinToss(bankroll, tossCount):
# sorteia o vencedor do cara ou coroa

 
def run2Ruin(bankroll):
# mantém um loop permanente até que um dos jogadores entrem em ruina

bankroll = [5,5] # dinheiro disponível por cada jogador
run2Ruin(bankroll) # executa até a ruina de um dos jogadores```

A próxima seção apresenta uma possível resposta para o desafio e, na sequência, tudo enfim começa.
