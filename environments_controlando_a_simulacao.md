# Environments: controlando a simulação

Em SimPy, o `Environment`é quem coordena a execução do seu programa. Ele avança o relógio de simulação, planeja a ordem de execução dos eventos e processa cada evento planejado pelo progrma no instante correto.

## `Environment.run():` controle de execução

A maneira mais usual de controle de execução de um modelo de simulação é fornecendo o tempo de duração da simulação. O SimPy, contudo, vai além e permite alguns outros modos de se controlar a simulação.

Incialmente, vamos trabalhar com um modelo simples que gera chegadas de eventos em intervalos constantes entre si:

```python
import simpy

def geraChegada(env, p):
    while True:
        print("%s: Nova chegada en %s" %(p, env.now))
        yield env.timeout(1)

env = simpy.Environment()
chegadas = env.process(geraChegada(env, "p1"))
env.run(until = 5)        # execute até o instante 5
```

Quando executado, o programa anterior fornece:

```python
p1: nova chegada en 0
p1: nova chegada en 1
p1: nova chegada en 2
p1: nova chegada en 3
p1: nova chegada en 4
```

No programa anterior, a última linha informa ao SimPy que a simulação deve ser executada até o instante 5 \(implicitamente o SimPy assume que o instante inicial é 0\). Esta é a maneira mais usual: o tempo de simulação é um parâmetro de entrada.

Quando não se fornece o tempo de simulação \(ou ele não é conhecido a priori\), podemos interromper a simulação pela própria extição do processo. No programa anterior, por exemplo, podemos substituir o comando `while True` por um laço `for`e executar a simulação com um número fixo de entidades pré estabelecido:

```python
import simpy

def geraChegada(env, p, numEntidades):
    for i in range(0,numEntidades):
        print("%s: nova chegada en %s" %(p, env.now))
        yield env.timeout(1)

env = simpy.Environment()
chegadas = env.process(geraChegada(env, "p1", 5)) # gere apenas 5 entidades
env.run()
```

Contudo, que se um modelo de simulação tem diversos processos ocorrendo ao mesmo tempo, o término da simulação só é garantido quando todos os processos terminarem.

O próximo programa, amplia o exemplo anterior, de modo que dois processos são executados ao mesmo tempo, um com 3 entidades e outro com 5 entidades no máximo. Note como os processos foram armazendos em uma lista:

```python
import simpy

def geraChegada(env, p, numEntidades):
    for i in range(0,numEntidades):
        print("%s: nova chegada em %s" %(p, env.now))
        yield env.timeout(1)

env = simpy.Environment()
# chegadas é uma lista que armazena os processos em execução
chegadas = [env.process(geraChegada(env, "p1", 5)), env.process(geraChegada(env, "p2", 3))]
env.run()
```

Quando executado, o programa anterior fornece:

```py
p1: nova chegada em 0
p2: nova chegada em 0
p1: nova chegada em 1
p2: nova chegada em 1
p1: nova chegada em 2
p2: nova chegada em 2
p1: nova chegada em 3
p1: nova chegada em 4
```

Repare que a simulação apenas termina quando o processo de 5 entidades termina.

Uma quarta alternativa de controle de execução é pelo término do próprio processo de execução. Partindo do exemplo anterior, podemos parar a simulação quando o processo que gera 3 entidades termina. Isto é possível com a opção `env.run(until=processo)`:

```python
import simpy

def geraChegada(env, p, numEntidades):
    for i in range(0,numEntidades):
        print("%s: nova chegada em %s" %(p, env.now))
        yield env.timeout(1)

env = simpy.Environment()
chegadas = [env.process(geraChegada(env, "p1", 5)), env.process(geraChegada(env, "p2", 3))]
env.run(until=chegadas[1])
```

Quando executado, o programa anterior fornece:

```python
p1: nova chegada em 0
p2: nova chegada em 0
p1: nova chegada em 1
p2: nova chegada em 1
p1: nova chegada em 2
p2: nova chegada em 2
p1: nova chegada em 3
```

No programa anterior, a linha `env.run(until=chegadas[1])` determina que o programa seja executado até que o processo `chegadas[1]` esteja concluído. Note que na lista:

```python
chegadas = [env.process(geraChegada(env, "p1", 5)), env.process(geraChegada(env, "p2", 3))]
```

`chegadas[1]`é o processo `env.process(geraChegadas(env, "p2", 3))` que deve terminar após 3 entidades criadas. Verifique na saída do programa que neste caso, de fato o programa parou após 3 entidades do tipo "p2" geradas.

## Simulação passo a passo: `peek` & `step`

O SimPy permite a simulação passo a passo por meio de dois comandos:

* `peek()`: retorna o instante de execução do próximo evento programado. Caso não existam mais eventos programados, retorna infinito `(float('inf'))`;
* `step()`: processa o próximo evento. Caso não existam mais eventos, ele retorna um exceção interna `EmptySchedule`.

A maneira usual de realizar a simulação passo a passo é por meio de um laço `while`, como no exemplo a seguir \(derivado do primeiro exemplo desta seção\):

```python
import simpy

def geraChegada(env, p):
    while True:
        print("%s: nova chegada em %s" %(p, env.now))
        yield env.timeout(1)

env = simpy.Environment()
chegadas = env.process(geraChegada(env, "p1"))
until = 5
while env.peek() < until:
    env.step()
```

## Desafios

**Desafio 9**: Considere que cada entidade gerada no primeiro exemplo desta seção tem um peso em gramas dado por uma distribuição normal de média 10 e desvio padrão igual a 5. Crie um critério de parada para quando a média dos pesos das entidades geradas esteja no intervalo entre 9,5 e 10,5.

**Desafio 10**: Modifique o critério anterior para que a parada ocorra quando a média for 10 com um intervalo de confiança de amplitude 0,5 e nível de significância igual a 95%. Dica: utilize a biblioteca `numpy` para isso \(consulte o stackoverflow!\).

