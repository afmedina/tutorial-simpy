``````# O que são funções geradoras? (Ou entendendo como funciona o SimPy)

##Iterador
Na programação voltada ao objeto, *iteradores* são métodos que permitem ao programador observar os valores dentro de um dado objeto.

<!---
esta seção está bem confusa, rever

Só joguei uns conceitos. AInda não sei como apresentar isso de modo didático
--->

Quando você percorre uma lista com o comando ```
for,```
 por exemplo, está intrinsecamente utilizando um iterador:
```python
 lista = [1, 2, 3]
 for i in lista:
    print (i)```
No exemplo, o comando ```for``` permite vasculhar cada elemento dentro da lista.

##Funções geradoras
Elas existem e [estão entre nós há tempos](https://en.wikipedia.org/wiki/Generator_(computer_programming), nós é que não sabíamos...

Uma função geradora é uma classe especial de funções que tem como característica retornar, cada vez que são chamadas, valores em sequência. O que torna uma função qualquer uma *função geradora* é a presença do comando ```yield``` em seu corpo. Por exemplo, cada vez que a função a seguir é chamada, ela retorna um novo número da sequência entre 0 e 10:
```python
def seqNum():
    n = 0
    while n <= 10:
        yield n
        n += 1

for i in seqNum():
    print(i)```


Se você executou o programa anterior, deve ter notado que o ```yield``` funciona como um ```return``` dentro da função, mas com o **superpoder** de aguardar o retorno do fluxo de controle do programa ali mesmo na linha do ```yield```, ou seja: a segunda chamada da função **não** executa o corpo inteiro da função! Isto significa que, numa segunda chamada à função, a execução retoma a partir da linha seguinte ao ```yield``` e o próximo valor de *n* será o anterior incrementado de 1.

Uma função geradora é, de fato, um *iterador* e você normalmente vai utilizá-la dentro de algum *loop* ```for``` como no caso anterior ou, você pode chamá-la diretamente pelo comando ```next``` do Python, como será visto no próximo exemplo.  

Que tal uma função que nos diga a posição atual de um Zumbi que só pode andar uma casa por fez no plano? A função geradora a seguir acompanha o andar cambeleante do zumbi pelo plano:
```python
import random

def zombiePos():
    x, y, = 0, 0 # zombie initial position
    while True:
        yield x, y
        x += random.randint(-1, 1)
        y += random.randint(-1, 1)

zombie = zombiePos()

print(next(zombie))
print(next(zombie))
print(next(zombie))
```
Diferentemente do caso anterior, criamos um zumbi a partir da linha:
```python
zombie = zombiePos()```
Cada novo passo do pobre infeliz é obtido pelo comando:
```python
next(zombie))```

O bacana, no caso, é que podemos criar 2 zumbis passeando pela relva:

```python
import random

def zombiePos():
    x, y, = 0, 0 # zombie initial position
    while True:
        yield x, y, "Brains!"
        x += random.randint(-1, 1)
        y += random.randint(-1, 1)
        
zombie1 = zombiePos()
zombie2 = zombiePos()
print(next(zombie1), next(zombie2))
print(next(zombie1), next(zombie2))
print(next(zombie1), next(zombie2))```

## SimPy x funções geradoras

Já sabemos que as entidades e eventos em SimPy são modeladas como **processos** dentro de um **environment**. Cada processo é basicamente uma função como qualquer outra construída em Python, mas que contém a palavrinha mágica ```yield```. Assim, como descrito no item anterior, todo processo em SimPy é também uma **função geradora**.

Um evento típico do SimPy é o timeout() ou, mas usual: env.timeout(tempo).

Para compreendermos a mecânica do SimPy (e da maioria dos softwares de simulação) é só questão de se reconhecer que os processos de um modelo de simulação nada mais são que eventos (ou atividades ou ações) que interagem entre si de diversas maneiras, tais como: congelando outro evento por tempo determinado, disparando novos eventos ou mesmo interrompendo certo evento já em execução.

Quando um processo encontra um ```yield```, o processo é suspenso até que o instante em que o evento deve ocorrer. O SimPy então *dispara* o evento no momento correto.
    
