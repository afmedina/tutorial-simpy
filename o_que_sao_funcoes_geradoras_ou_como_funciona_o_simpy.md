# O que são funções geradoras? (Ou entendendo como funciona o SimPy) - Parte I

O comando `yield `é quem, como você já deve ter notado, dá o _ritmo_ do seu modelo em SimPy. Para melhor compreender como funciona um programa em SimPy, precisamos entender, além do próprio comando `yield`, outro conceito fundamental em programação: as funções geradoras.

Começaremos pelo conceito de Iterador.

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

1
2
3
```
No exemplo, ```lista``` é um *objeto* e o comando ```for``` é um **iterador** que permite vasculhar cada elemento dentro da lista, retornando sempre o elemento seguinte do objeto.

##Funções geradoras
Elas existem e [estão entre nós há tempos](https://en.wikipedia.org/wiki/Generator_(computer_programming), nós é que não sabíamos...

Uma **função geradora** é uma classe especial de funções que têm como característica retornar, cada vez que é chamada, valores em sequência. O que torna uma função qualquer uma *função geradora* é a presença do comando ```yield``` em seu corpo.

Por exemplo, cada vez que a função a seguir é chamada, ela retorna um novo número da sequência entre 0 e 10:
```python
def seqNum():
    n = 1
    while n <= 3:
        yield n
        n += 1

for i in seqNum():
    print(i)
```
Quando executado, o programa anterior retorna:
```
1
2
3
```

Note que a função retorna a sequência de números de 0 a 10 ```yield``` funciona como um ```return``` dentro da função, mas com o **superpoder** de aguardar o retorno do fluxo de controle do programa ali mesmo na linha do ```yield```, ou seja: a segunda chamada da função `seqNum `no loop `for`, **não** executa o corpo inteiro da função `seqNum`.
A primeira fez que o loop `for `chamou a função `seqNum()` o código é executado até a linha do `yield n`, que retona o valor `1` (afinal, n=1 neste momento).

A segunda fez que o loop `for `chama a função, ela não recomeça da primeira linha, de fato, ela é executada a partir da **linha seguinte ao comando `yield`** e retorna o valor `2`, pois `n` foi incrementado nessa segunda passagem.

Isto significa que, numa segunda chamada à função, a execução retoma a partir da linha seguinte ao ```yield``` e o próximo valor de *n* será o anterior incrementado de 1.

Uma função geradora é, de fato, um *iterador* e você normalmente vai utilizá-la dentro de algum *loop* ```for``` como no caso anterior. Outra possibilidade é você chamá-la diretamente pelo comando ```next``` do Python, como será visto no próximo exemplo.  

Exemplo: Que tal uma função que nos diga a posição atual de um Zumbi que só pode andar uma casa por fez no plano? A função geradora a seguir acompanha o andar cambeleante do zumbi:
```python
import random

def zombiePos():
    x, y, = 0, 0 # zombie initial position
    while True:
        yield x, y,  "Brains!"
        x += random.randint(-1, 1)
        y += random.randint(-1, 1)

zombie = zombiePos()

print(next(zombie))
print(next(zombie))
print(next(zombie))
```
Diferentemente do caso anterior, criamos um zumbi a partir da linha:
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
        
zombie1 = zombiePos()
zombie2 = zombiePos()
print(next(zombie1), next(zombie2))
print(next(zombie1), next(zombie2))
print(next(zombie1), next(zombie2))
```

