# Interrupções de eventos

De modo semelhante ao que vimos com recursos, os eventos também podem ser interrompidos em SimPy. Como o SimPy aproveita-se dos recursos de interrupção do Python, pode-se utilizar lógicas do tipo `try... except` e se capturar a interrupção em qualquer parte do modelo.

Considere um exemplo simples em que um jovem Jedi tem sua meditação matinal interrompida por um Lord Sith interessado em novas aquisições para o Lado Negro. Esse sistema pode ser interropido por, ao menos, dois métodos diferentes: `interrupt` ou `fail`.

## Interrompendo um evento com o método `interrupt`

Criaremos duas funções: `forca` que representa o processo de meditação do Jedi e `ladoNegro` que representa o processo de interrupção da meditação. Inicialmente, interromperemos o processo `forca` por meio do método `interrupt` aplicado ao processo força. Uma possível máscara para o modelo ficaria:

```python
import simpy

def forca(env):
    # processo a ser interrompido

def ladoNegro(env, proc):
    # gerador de interrupção do processo proc

env = simpy.Environment()

forcaProc = env.process(forca(env))
ladoNegroProc = env.process(ladoNegro(env, forcaProc))
``` 
O processo `for
```python

``` 

```python

``` 


```python

``` 


```python
import simpy

def forca(env):
    # processo a ser interrompido
    while True:
        yield env.timeout(1)
        print('%d Eu estou com a Força e a Força está comigo.' % env.now)


def ladoNegro(env, proc):
    # gerador de interrupção do processo proc
    yield env.timeout(3)
    print('%d Venha para o lado negro da força, nós temos CHURROS!' % env.now)
    # interrompe o processo proc
    proc.interrupt()
    print('%d Welcome, young Sith.' % env.now)

env = simpy.Environment()

forcaProc = env.process(forca(env))
ladoNegroProc = env.process(ladoNegro(env, forcaProc))

try:
    env.run()
except simpy.Interrupt:
    print('%d Eu estou com a Força e a Força está comigo.' % env.now)
``` 

```python

``` 

```python

``` 

```python

``` 

```python

``` 

```python

``` 

```python

``` 


