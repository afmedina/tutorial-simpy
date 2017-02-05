# Interrupções de eventos

De modo semelhante ao que vimos com recursos, os eventos também podem ser interrompidos em SimPy. Como o SimPy aproveita-se dos comandos de interrupção já existentes no Python, pode-se utilizar lógicas do tipo `try... except` e assim capturar a interrupção em qualquer parte do modelo.

Considere um exemplo simples em que um jovem Jedi tem sua seção de meditação matinal interrompida por um cruel Lord Sith interessado em convertê-lo para o Lado Negro. 
Construir um modelo de simulação deste sistema, é tarefa simples: precisamos de uma função que representa o Jedi meditando e outra que interrompe o processo em determinado momento (lembre-se que um processo é também um evento para o SimPy).

O SimPy tem dois métodos diferentes para interroper um evento: `interrupt` ou `fail`.

## Interrompendo um evento com o método `interrupt`

Criaremos duas funções: `forca` que representa o processo de meditação e `ladoNegro` que representa o processo de interrupção da meditação. Inicialmente, interromperemos o processo `forca` por meio do método `interrupt`. Uma possível máscara para o modelo ficaria:

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
Para este exemplo, o processo de meditação é bem simples, pois estamos mais interessados em aprender sobre interrupções:

```python
def forca(env):
    # processo a ser interrompido
    while True:
        yield env.timeout(1)
        print('%d Eu estou com a Força e a Força está comigo.' % env.now)
``` 
Portanto, a cada 1 unidade de tempo, o Jedi fala um frase para manter-se concentrado. O processo de interrupção por sua vez, recebe como parâmetro de entrada o processo (ou evento) a ser interrompido. Apenas para ilustrar melhor o exemplo, vamos considerar que após 3 unidades de tempo, a função interrompe o processo (ou evento) de meditação:
```python
def ladoNegro(env, proc):
    # gerador de interrupção do processo proc
    yield env.timeout(3)
    print('%d Venha para o lado negro da força, nós temos CHURROS!' % env.now)
    # interrompe o processo proc
    proc.interrupt()
    print('%d Welcome, young Sith.' % env.now)
``` 
Portanto, a interrupção de um evento ou processo qualquer é invocada pelo método `.interrupt()`. Por exemplo, dado que processo ou evento `proc`, podemos interrompê-lo com a linha de código:
```python
# interrompe o processo proc
proc.interrupt()
``` 
Se você executar o modelo anterior, a coisa até começa bem, mas depois surge uma supresa desagradável:
```python
1 Eu estou com a Força e a Força está comigo.
2 Eu estou com a Força e a Força está comigo.
3 Venha para o lado negro da força, nós temos CHURROS!
3 Welcome, young Sith.
Traceback (most recent call last):

  File "<ipython-input-8-623c3bea2882>", line 1, in <module>
    runfile('C:/Book/Interruption/meditation.py', wdir='C:/Book/Interruption/')

  File "C:\Anaconda3\lib\site-packages\spyderlib\widgets\externalshell\sitecustomize.py", line 714, in runfile
    execfile(filename, namespace)

  File "C:\Anaconda3\lib\site-packages\spyderlib\widgets\externalshell\sitecustomize.py", line 89, in execfile
    exec(compile(f.read(), filename, 'exec'), namespace)

  File "C:/Book/Interruption/meditation.py", line 22, in <module>
    env.run()

  File "C:\Anaconda3\lib\site-packages\simpy\core.py", line 137, in run
    self.step()

  File "C:\Anaconda3\lib\site-packages\simpy\core.py", line 229, in step
    raise exc

Interrupt: Interrupt(None)
``` 
O que essa longa mensagem de erro nos faz lembrar é que o método `.interrupt()` vai além de interromper um mero evento do SimPy, ele interrompe o programa todo.

Mas, jovem leitor Jedi, tempo duas maneira de contornar o problema: com a lógica do tipo `try...except` ou com a propriedade `defused`, como veremos a seguir.

### Método de controle de interrupção 1: lógica de excessão `try... except`
Neste caso, a solução é razoavemente simples, basta acrecentarmos ao final do programa (ou em outra parte conveniente) uma lógica de excessão do SimPy, `simpy.Interrupt`, como no exemplo a seguir:

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
Quando executado, o modelo anterior fornece:
```python
1 Eu estou com a Força e a Força está comigo.
2 Eu estou com a Força e a Força está comigo.
3 Venha para o lado negro da força, nós temos CHURROS!
3 Welcome, young Sith.
3 Eu estou com a Força e a Força está comigo.
``` 
É importante notar que depois da interrupção `proc.interrupt()` o modelo ainda executa a última linha do processo `ladoNegro` (basicamente, imprime "Welcome, young Sith") para, a seguir, executar o comando dentro do `except simpy.Interrupt`.

### Método de controle de interrupção 2: atributo `defused`

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


