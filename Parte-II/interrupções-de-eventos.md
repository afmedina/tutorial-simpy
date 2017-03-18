# Interrupções de eventos

De modo semelhante ao que vimos com recursos, os eventos também podem ser interrompidos em SimPy. Como o SimPy aproveita-se dos comandos de interrupção já existentes no Python, pode-se utilizar o [bloco `try... except`](https://docs.python.org/3.5/tutorial/errors.html) e assim capturar a interrupção em qualquer parte do modelo.

Considere um exemplo simples em que um jovem [Jedi](https://pt.wikipedia.org/wiki/Jedi) tem sua seção de meditação matinal interrompida por um cruel [Lord Sith](https://pt.wikipedia.org/wiki/Sith) interessado em convertê-lo para o Lado Negro. 

Construir um modelo de simulação deste sistema, é tarefa simples: precisamos de uma função que representa o Jedi meditando e outra que interrompe o processo em determinado momento \(lembre-se que um processo é também um evento para o SimPy\).

O SimPy tem dois métodos diferentes para interroper um evento: `interrupt` ou `fail.`

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

Portanto, a cada 1 unidade de tempo, o Jedi fala um frase para manter-se concentrado. O processo de interrupção por sua vez, recebe como parâmetro de entrada o processo \(ou evento\) a ser interrompido. Apenas para ilustrar melhor o exemplo, vamos considerar que após 3 unidades de tempo, a função interrompe o processo \(ou evento\) de meditação:

```python
def ladoNegro(env, proc):
    # gerador de interrupção do processo proc
    yield env.timeout(3)
    print('%d Venha para o lado negro da força, nós temos CHURROS!' % env.now)
    # interrompe o processo proc
    proc.interrupt()
    print('%d Welcome, young Sith.' % env.now)
```

Portanto, a interrupção de um evento ou processo qualquer é invocada pelo método `.interrupt().` Por exemplo, dado que processo ou evento `proc`, podemos interrompê-lo com a linha de código:

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

Mas, jovem leitor Jedi, temos duas maneiras de contornar o problema: com a lógica de controle de exceção do Python`try...except` ou com a propriedade `.defused,` como veremos a seguir.

### Método de controle de interrupção 1: lógica de exceção `try... except`

Neste caso, a solução é razoavelmente simples, basta acrescentarmos ao final do programa \(ou em outra parte conveniente\) uma lógica de exceção do SimPy, `simpy.Interrupt,`como no exemplo a seguir:

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

É importante notar que depois da interrupção `proc.interrupt()` o modelo ainda executa a última linha do processo `ladoNegro` \(basicamente, imprime "Welcome, young Sith"\) para, a seguir, executar o comando dentro do `except simpy.Interrupt.`

### Método de controle de interrupção 2: alterando o atributo `defused`

No caso anterior, o leitor deve ter notado que, ao interromper o processo, interrompemos a simulação por completo, pois nossa lógica de exceção está ao final do código.

E se quisésemos apenas paralizar o processo \(ou evento\) sem que isso impactasse em toda a simulação? Neste caso, SimPy fornece um atributo `defused` para cada evento que, quando alterado para `True`, faz com que a  interrupção seja "desarmada".

Vamos alterar o atributo `defused` do processo interrompido no exemplo anterior:

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
    # defused no processo para evitar a interrupção da simulação
    proc.defused = True
    print('%d Welcome, young Sith.' % env.now)

env = simpy.Environment()

forcaProc = env.process(forca(env))
ladoNegroProc = env.process(ladoNegro(env, forcaProc))

env.run()
```

Quando executado, o modelo anterior fornece:

```python
1 Eu estou com a Força e a Força está comigo.
2 Eu estou com a Força e a Força está comigo.
3 Venha para o lado negro da força, nós temos CHURROS!
3 Welcome, young Sith.
```

Novamente a execução do processo de interrupção vai até o fim e a interrupção que poderia causar a paralização de todo o modelo é desarmada.

Portanto, se o objetivo é _desarmar_ a interrupção, basta tornar `True` o atributo `defused` do evento.

## Interrompendo um evento com o método `fail`

De modo semelhante a provocar um interrupção, podemos provocar uma _falha_ no evento. O interessante, neste caso, é que podemos informar a falha

