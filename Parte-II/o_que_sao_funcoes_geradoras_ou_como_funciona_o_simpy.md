# O que são funções geradoras? \(Ou entendendo como funciona o SimPy\) - Parte I

O comando `yield`é quem, como você já deve ter notado, dá o _ritmo_ do seu modelo em SimPy. Para melhor compreender como funciona um programa em SimPy, precisamos entender, além do próprio comando `yield,`outro conceito fundamental em programação: as funções geradoras.

Começaremos pelo conceito de Iterador.

## Iterador

Na programação voltada ao objeto, _iteradores_ são _métodos_ que permitem ao programa observar os valores dentro de um dado objeto.

Quando você percorre uma lista com o comando `for,`  
 por exemplo, está intrinsecamente utilizando um iterador:

```python
 lista = [10, 20, 30]
 for i in lista:
    print (i)

10
20
30
```

No exemplo, `lista` é um _objeto_ e o comando `for` é um **iterador** que permite vasculhar cada elemento dentro da lista, retornando sempre o elemento seguinte do objeto.

## Funções geradoras

Elas existem e \([estão entre nós há tempos...](https://en.wikipedia.org/wiki/Generator_%28computer_programming)\)

Uma **função geradora** é uma classe especial de função que tem como característica retornar, cada vez que é chamada, valores em sequência. O que torna uma função qualquer uma _função geradora_ é a presença do comando `yield` em seu corpo.

O comando `yield`funciona, a primeira vez que a função é chamada, algo semelhante a um `return,` mas com um **superpoder:** toda vez que a função é chamada novamente, a execução começa a partir da linha seguinte ao `yield`.

Por exemplo, podemos imprimir os mesmo números da lista anterior, chamando 3 vezes a função `seqNum(),`definida a seguir:

```python
def seqNum():
    n = 10
    yield n
    n += 10
    yield n
    n += 10
    yield n

for i in seqNum():
 print(i)

10
20
30
```

Note que a _função geradora_ `seqNum`é um _objeto_ e que o loop `for` permite acessar os elementos retornados por cada `yield`.

A primeira fez que o loop `for`chamou a função `seqNum()` o código é executado até a linha do `yield n,` que retorna o valor `10` \(afinal, n=10 neste momento\).

A segunda fez que o loop `for`chama a função, ela não recomeça da primeira linha, de fato, ela é executada a partir da **linha seguinte ao comando **`yield` e retorna o valor `20`, pois `n` foi incrementado nessa segunda passagem.

Na terceira chamada à função, a execução retoma a partir da linha seguinte ao segundo `yield` e o próximo valor de _n_ será o anterior incrementado de 10.

Uma função geradora é, de fato, um _iterador_ e você normalmente vai utilizá-la dentro de algum _loop_ `for` como no caso anterior. Outra possibilidade é você chamá-la diretamente pelo comando `next` do Python, como será visto no próximo exemplo.

Exemplo: Que tal uma função que nos diga a posição atual de um Zumbi que só pode andar uma casa por fez no plano? A função geradora a seguir acompanha o andar cambaleante do zumbi:

```python
import random

def zombiePos():
    x, y, = 0, 0 # posição inicial do zumbie
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

Na seção a seguir discutiremos o papel da função geradora em um modelo de simulação. Por ora, sugerimos as seguintes fontes de consulta caso você procure um maior aprofundamento sobre o `yield` e as funções geradoras:

* [PEP 225 - Descritivo técnico do yield no Python](https://www.python.org/dev/peps/pep-0255/ "PEP 255")

* [Utilizando Geradores na Python Brasil](http://wiki.python.org.br/UsandoGenerators)

* Uma boa explicação na StackOverflow: [What does the yield keyword do?](http://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do)



