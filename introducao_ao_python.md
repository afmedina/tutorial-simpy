#Tutorial SimPy: Introdução ao Python
Antes de começarmos com o SimPy, preciso garantir que você tenha algum conhecimento mínimo de Python. Se você já tem algum conhecimento anterior, pule para a seção “Teste seus conhecimentos em Python” deste módulo.

<!---
acho que ficaria melhor inverter a ordem, como comentei anteriormente...
--->

Se você nunca teve contato com a linguagem, aviso que não pretendo construir uma introdução ou tutorial ao Python, simplesmente porque isso é o que mais existe disponível na internet. 

Procure um tutorial rápido (já vi um até de 10 minutos!) e mãos à obra! Nada mais fácil do que aprender o básico de Python.

Sugestões:
1.	Um curso muito bom no Udacity: [Programming Foundations with Python](https://www.udacity.com/course/programming-foundations-with-python--ud036) (clicando no botão azul “Access course materials”, você faz o curso de graça, mas sem receber o certificado). A vantagem do Udacity é que você pode começar o curso a hora que quiser.
2.	Um tutorial muito rápido (1 hora): [Python in One Easy Lesson](http://cs.stanford.edu/people/nick/python-in-one-easy-lesson/).
3.	Um tutorial completo: [Tutorial Python](http://wiki.python.org.br/Tutorial_Python).
4.	Outro curso muito bom, este no Coursera: [Introdução à Programação Interativa em Python (Parte 1)](https://pt.coursera.org/course/interactivepython1).
5.	Eu tenho na minha mesa um livro de Python muito bom: Summerfield, Mak. Programming in Python 3: a complete introduction. Addison-Wesley Professional. 2012.

<!---
eu gostei do CodeAcademy em 36 h...
e comprei um livro para a Renata - Python for Kids, legalzinho...
--->

Feito o tutorial, curso ou aprendido tudo sozinho, teste seus conhecimentos para verificar se você sabe o básico de Python e pode começar com o SimPy.
##Teste seus conhecimentos em Python: o problema da ruina do apostador
O [problema da ruina do apostador](http://en.wikipedia.org/wiki/Gambler%27s_ruin) é um problema clássico proposto por Pascal em uma carta para Fermat em 1656. A versão aqui apresentada é uma simplificação visando avaliar seus conhecimentos em Python.
> **Desafio**: dois apostadores iniciam um jogo de cara ou coroa em que cada um deles aposta $1 sempre em um mesmo lado da moeda. O vencedor leva aposta total ($2). Cada jogador tem incialmente $10 disponíveis para apostar. O jogo termina quando um dos jogadores atinge a ruina e não pode mais apostar.

Construa três funções:
* transfer(winner,looser,bankroll,tossCount): transfere o valor do jogador perdedor para o vencedor e imprime na tela o nome do vencedor;
* coinToss(bankroll,tossCount): sorteia o vencedor do cara ou coroa;
* run2Ruin(bankroll): mantém um loop permanente até que um dos jogadores entrem em ruina

Teste o programa com os parâmetros a seguir (você pode utilizar esse código como um template):
```
# -*- coding: utf-8 -*-
from __future__ import print_function # para compatibilidade da função print com o Python 3
import random # gerador de números aleatórios


names = ['Chewbacca', 'R2D2'] # nomes dos jogadores

def transfer(winner,looser,bankroll,tossCount):
# transfere o valor do jogador perdedor para o vencedor e imprime na tela o nome do vencedor

   
def coinToss(bankroll,tossCount):
# sorteia o vencedor do cara ou coroa

 
def run2Ruin(bankroll):
# mantém um loop permanente até que um dos jogadores entrem em ruina

bankroll = [5,5] # dinheiro disponível por cada jogador
run2Ruin(bankroll) # executa até a ruina de um dos jogadores
```

<!---
colocar algumas perguntas sobre o código, entrada e sáida para testar os conhecimentos do leitor (tipo quiz,depois de rodar o código)
--->

Quando sentir-se confortável com a linguagem, pule para a próxima seção, onde finalmente começa nossa aventura em SimPy.


