# O que são funções geradoras? (Ou entendendo como funciona o SimPy) - Parte I

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
    print (i)
```
Quando executado, o programa fornece a seguinte saída
```
1
2
3
```
No exemplo, ```lista``` é um *objeto* e o comando ```for``` é um **iterador** que permite vasculhar cada elemento dentro da lista, retornando sempre o elemento seguinte do objeto.

##Funções geradoras
Elas existem e [estão entre nós há tempos](https://en.wikipedia.org/wiki/Generator_(computer_programming), nós é que não sabíamos...

Uma **função geradora** é uma classe especial de funções que têm como característica retornar, cada vez que são chamadas, valores em sequência. O que torna uma função qualquer uma *função geradora* é a presença do comando ```yield``` em seu corpo. Por exemplo, cada vez que a função a seguir é chamada, ela retorna um novo número da sequência entre 0 e 10:
```python
def seqNum():
    n = 0
    while n <= 10:
        yield n
        n += 1

for i in seqNum():
```

Quando executado, o programa fornece a seguinte saída
```
0
1
2
3
4
5
6
7
8
9
10

```


Se você executou o programa anterior, deve ter notado que o ```yield``` funciona como um ```return``` dentro da função, mas com o **superpoder** de aguardar o retorno do fluxo de controle do programa ali mesmo na linha do ```yield```, ou seja: a segunda chamada da função **não** executa o corpo inteiro da função.

Isto significa que, numa segunda chamada à função, a execução retoma a partir da linha seguinte ao ```yield``` e o próximo valor de *n* será o anterior incrementado de 1.

Uma função geradora é, de fato, um *iterador* e você normalmente vai utilizá-la dentro de algum *loop* ```for``` como no caso anterior. Outra possibilidade é você chamá-la diretamente pelo comando ```next``` do Python, como será visto no próximo exemplo.  

Exemplo: Que tal uma função que nos diga a posição atual de um zumbi que só pode andar uma casa por fez no plano? A função geradora a seguir acompanha o andar cambeleante do morto-vivo:
```python
import random

def zombiePos():
    x, y, = 0, 0 # posição inicial do zumbi
    while True:
        yield x, y,  "Brains!"
        x += random.randint(-1, 1)
        y += random.randint(-1, 1)

zombie = zombiePos()

print(next(zombie))
print(next(zombie))
print(next(zombie))
```
Quando executado, vemos nosso zumbi caminhando uma posição por vez (algumas vezes ele fica no mesmo lugar...):
```
(0, 0, 'Brains!')
(1, 0, 'Brains!')
(2, 1, 'Brains!')

```
Neste programa, criamos um zumbi a partir da linha:
```python
zombie = zombiePos()
```
Cada novo passo do pobre infeliz é obtido pelo comando:
```python
next(zombie))
```

O bacana, no caso, é que podemos criar 2 zumbis passeando pela relva:

```python
import random

def zombiePos():
    x, y, = 0, 0 # zombie initial position
    while True:
        yield x, y, "Brains!"
        x += random.randint(-1, 1)
        y += random.randint(-1, 1)
        
zombie1, zumbie2  = zombiePos(), zombiePos()

print("zumbi 1", next(zombie1), "zumbi 2", next(zombie2))
print("zumbi 1", next(zombie1), "zumbi 2", next(zombie2))
print("zumbi 1", next(zombie1), "zumbi 2", next(zombie2))
```
Quando executado:
```
zumbi 1 (0, 0, 'Brains!') zumbi 2 (0, 0, 'Brains!')
zumbi 1 (0, 0, 'Brains!') zumbi 2 (0, 1, 'Brains!')
zumbi 1 (-1, 0, 'Brains!') zumbi 2 (1, 2, 'Brains!')


```
Obs: fica como exercício, construir uma lógica que impeça um zumbi de ocupar o mesmo espaço que outro.
