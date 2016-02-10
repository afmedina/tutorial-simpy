# Environments: controlando a simulação

Em SimPy, o Environment é quem coordena a execução do seu programa. Ele avança o relógio de simulação, planeja a ordem de execução dos eventos e processa cada evento planejado no instante esperado pelo programa.

## Environment.run(): controle de execução

A maneira mais usual de controle de execução de um modelo de simulação é fornecendo o tempo de duração da simulação. O SimPy, contudo, vai além e permite que alguns outros modos de se controlar a simulação. 

Incialmente, vamos trabalhar com um modelo simples que gera chegadas de eventos em intervalos constantes entre si:

```python
import simpy

def geraChegada(env, p):
    while True:
        print("%s: ova chegada en %s" %(p, env.now))
        yield env.timeout(1)
        
env = simpy.Environment()
chegadas = env.process(geraChegada(env, "p1"))
env.run(until = 5)
```

Esta é a maneira mais usual, pois o tempo é um parâmetro de entrada

Quando não se fornece o tempo de simulação (ou ele não é conhecido a priori), podemos interromper a simulação pela própria extição do processo. No programa anterior, por exemplo, podemos substituir o comando while True por um laço for e gerar um número fixo de entidades:

```python
import simpy

def geraChegada(env, p, numEntidades):
    for i in range(0,numEntidades):
        print("%s: nova chegada en %s" %(p, env.now))
        yield env.timeout(1)
        
env = simpy.Environment()
chegadas = env.process(geraChegada(env, "p1", 5))
env.run()
```
Note, contudo, que se um modelo de simulação tem diversos processos ocorrendo ao mesmo tempo, o término da simulação só é garantido quando todos os processos terminarem. 

Ampliamos o exemplo anterior, de modo que dois processos são executados ao mesmo tempo, um com 3 entidades e outro com 5 entidades no máximo. Note armazenamos os processos em uma lista:


```python
import simpy

def geraChegada(env, p, numEntidades):
    for i in range(0,numEntidades):
        print("%s: nova chegada em %s" %(p, env.now))
        yield env.timeout(1)
        
env = simpy.Environment()
#chegadas é uma lista que armazena os processos em execução
chegadas = [env.process(geraChegada(env, "p1", 5)), env.process(geraChegada(env, "p2", 3))]
env.run()
```
Quando executado, o programa anterior fornece:
```
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

Uma terceira alterniva de controle de execução é pelo término do próprio processo de execução. Parindo do exemplo anterior, podemos parar a simulação quando o processo que gera 3 entidades termina. Isto é possível com a opção ```env.run(until=processo)```:

```
import simpy

def geraChegada(env, p, numEntidades):
    for i in range(0,numEntidades):
        print("%s: nova chegada em %s" %(p, env.now))
        yield env.timeout(1)
        
env = simpy.Environment()
chegadas = [env.process(geraChegada(env, "p1", 5)), env.process(geraChegada(env, "p2", 3))]
env.run(until=chegadas[1])
```

## Simulação passo a passo: ```peek``` & ```step```

O SimPy permite a simulação passo a passao por meio de dois comandos:
* peek(): retorna o instante de execução do próximo evento programado. Caso não existam mais eventos programados, retorna infinito (float('inf'));
* step(): processa o próximo evento. Caso não existam mais eventos, ele retorna um exceção interna EmptySchedule.

A maneira usual de realizar a simulação passo a passo é por meio de um laço ```while```, como no exemplo a seguir (derivado do primeiro exemplo desta seção):

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
**Desafio 6**: Considere que cada entidade gerada no primeiro exemplo desta seção tem um peso em gramas dado por uma distribuição normal de média 10 e desvio padrão igual a 5. Crie um critério de parada para quando a média dos pesos das entidades geradas esteja no intervalo entre 9,5 e 10,5.

**Desafio 7**: Modifique o critério anterior para que a parada ocorra quando a média for 10 com um intervalo de confiança de amplitude 0,5 e nível de significância igual a 95%. Dica: utilize a biblioteca ```numpy``` para isso (consulte o stackoverflow!).