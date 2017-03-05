# Começando pelo Python

Antes de começarmos com o SimPy, precisamos garantir que você tenha algum conhecimento mínimo de Python. Se você julga que seus conhecimentos na linguagem são razoáveis, a recomendação é que você pule para a seção seguinte,  “Teste seus conhecimentos em Python”.

Se você nunca teve contato com a linguagem, aviso que não pretendemos construir uma "introdução" ou "tutorial" para o Python, simplesmente porque isso é o que mais existe à disposição na internet.

Procure um tutorial rápido \(existem tutoriais de até 10 minutos!\) e mãos à obra! Nada mais fácil do que aprender o básico de Python.

Sugestões:

1. Um curso muito bom no Udacity \(20 horas\): [Programming Foundations with Python](https://www.udacity.com/course/programming-foundations-with-python--ud036\) \(clicando no botão azul “Access course materials”, você faz o curso de graça, mas sem receber o certificado). A vantagem do Udacity é que você pode começar o curso a hora que quiser;
2. Outro curso muito bom é o da CodeAcademy \(13 horas\): [Python](https://www.codecademy.com/pt-BR/learn/python);
3. Outro curso muito bom, este no Coursera: [Introdução à Programação Interativa em Python \(Parte 1\)](https://pt.coursera.org/course/interactivepython1).
4. Eu tenho sempre na minha mesa um ótimo livro de Python: _Summerfield, Mak. Programming in Python 3: a complete introduction. Addison-Wesley Professional. 2012_. Este livro já foi traduzido para o Português e pode ser encontrado na [amazon](http://www.amazon.com.br/Programa%C3%A7%C3%A3o-Em-Python-Mark-Summerfield/dp/8576083841/ref=sr_1_7?s=books&ie=UTF8&qid=1448738880&sr=1-7&keywords=python).

Feito o tutorial, curso ou aprendido mesmo tudo sozinho, teste seus conhecimentos para verificar se você sabe o _básico_ _necessário_ de Python para começar com o SimPy.

## Teste seus conhecimentos em Python: o problema da ruina do apostador

O [problema da ruína do apostador](http://en.wikipedia.org/wiki/Gambler%27s_ruin) é um problema clássico proposto por Pascal em uma carta para Fermat em 1656. A versão aqui apresentada é uma simplificação visando avaliar seus conhecimentos em Python.

> **Desafio 1**: dois apostadores iniciam um jogo de cara ou coroa em que cada um deles aposta $1 sempre em um mesmo lado da moeda. O vencedor leva a aposta total \($2\). Cada jogador tem inicialmente $10 disponíveis para apostar. O jogo termina quando um dos jogadores atinge a ruína e não tem mais dinheiro para apostar.

Construa três funções:

1. `transfer(winner, looser, bankroll, tossCount):` transfere o valor do jogador perdedor para o vencedor e imprime na tela o nome do vencedor;

2. `coinToss(bankroll, tossCount):` sorteia o vencedor do cara ou coroa;

3. `run2Ruin(bankroll):` mantém um laço permanente até que um dos jogadores entrem em ruína

Teste o programa com os parâmetros a seguir \(você pode utilizar esse código como uma máscara para iniciar o seu programa\):

```python
import random                   # gerador de números aleatórios

names = ['Chewbacca', 'R2D2']   # jogadores

def transfer(winner, looser, bankroll, tossCount):
    # função que transfere o dinheiro do winner para o looser
    # imprime o vencedor do lançamento  e o bankroll de cada jogador
    pass

def coinToss(bankroll, tossCount):
    # função que sorteia a moeda e chama a transfer
    pass

def run2Ruin(bankroll):
    # função que executa o jogo até a ruina de um dos jogadores
    pass

bankroll = [5, 5]               # dinheiro disponível para cada jogador
run2Ruin(bankroll)              # inicia o jogo
```

Agora é com você: complete o código anterior e descubra se você está pronto para inciar com o SimPy!  
\(A próxima seção apresenta uma possível resposta para o desafio e, na sequência, tudo enfim, começa.\)

