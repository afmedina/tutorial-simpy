# Tutorial SimPy: solução dos desafios 2 e 3

##Desafio 2
É comum que os comandos de criação de entidades nos softwares proprietários tenham a opção de limitar o número máximo de entidades geradas durante a simulação. 
Modifique a função ```
geraChegadas```
 de modo que ela receba como parâmetro o ```
numeroMaxChegadas```
 e limite a criação de entidades a este número.
 
Neste caso, o *script* em Python é autoexplicativo (apenas note que limitei o número de chegadas em 5 e fiz isso antes, da chamada do processo):

<!---
pq vc define "tempo_medio_chegadas" e "numeroMaxChegadas" em lugares diferente do código?

no módulo anterior não tinha a constante "tempo_medio_chegadas"

sugestão: trocar o "while" por "for i=1 to n"

random.seed foi comentado?
--->

```python
# -*- coding: utf-8 -*-
from __future__ import print_function # para compatibilidade da função print com o Python 3
import random # gerador de números aleatórios
import simpy  # biblioteca de simulação

TEMPO_MEDIO_CHEGADAS = 1  #tempo entre chegadas sucessivas de clientes

def criaChegadas(env, numeroMaxChegadas):
    #função que cria chegadas de entidades no sistema
    contaChegada = 0
    while (contaChegada < numeroMaxChegadas):
        yield env.timeout(random.expovariate(1/TEMPO_MEDIO_CHEGADAS))
        contaChegada += 1
        print("Cliente %i chega em: %.1f " % (contaChegada, env.now))

random.seed(1000)   # semente do gerador de números aleatórios

numeroMaxChegadas = 5 # número máximo de chegadas

env = simpy.Environment() # cria o environment do modelo
env.process(criaChegadas(env, numeroMaxChegadas))
env.run(until=10)```




##Desafio 3
Modifique a função ```
geraChegadas```
 de modo que as chegadas entre entidades sejam distribuídas segundo uma triangular de moda 1, menor valor 0,1 e maior valor 1,1.

Neste caso, precisamos verificar na documentação da biblioteca random, quais são nossas opções. A tabela a seguir, resume as distribuições disponíveis:

| Função | Distribuição |
| -- | -- |
| random.random() | gera números aleatórios no intervalo [0.0, 1.0) |
| random.uniform(a, b) | uniforme no intervalo [a, b] |
| random.triangular(low, high, mode) | triangular com menor valor *low*, maior valor *high* e moda *mode* |
| random.betavariate(alpha, beta) | beta com parâmetros *alpha* e *beta* |
| random.expovariate(lambd) | exponencial com média 1/*lambd* |
| random.gammavariate(alpha, beta) | gamma com parâmetros *alpha* e *beta* |
| random.gauss(mu, sigma) | normal com média *mu* e desvio padrão *sigma* |
| random.lognormvariate(mu, sigma) | lognormal com média *mu* e desvio padrão *sigma* |
| random.normalvariate(mu, sigma) | equivalente à random.gauss, mas um pouco mais lenta |
| random.vonmisesvariate(mu, kappa) | [distribuição de von Mises](http://en.wikipedia.org/wiki/Von_Mises_distribution) com parâmetros *mu* e *kappa* |
| random.paretovariate(alpha) | pareto com parâmetro *alpha* |
| random.weibullvariate(alpha, beta) | weibull com parâmetros *alpha* e *beta* |

A biblioteca NumPy, que veremos oportunamente, possui mais opções para distribuições estatísticas. Por enquanto, o desafio 3 pode ser solucionado de maneira literal:

```python
# -*- coding: utf-8 -*-
from __future__ import print_function # para compatibilidade da função print com o Python 3
import random # gerador de números aleatórios
import simpy  # biblioteca de simulação

TEMPO_MEDIO_CHEGADAS = 1  #tempo entre chegadas sucessivas de clientes

def criaChegadas(env, numeroMaxChegadas):
    #função que cria chegadas de entidades no sistema
    contaChegada = 0
    while (contaChegada < numeroMaxChegadas):
        yield env.timeout(random.triangular(0.1,1,1.1))
        contaChegada += 1
        print("Cliente %i chega em: %.1f " % (contaChegada, env.now))

random.seed(1000)   # semente do gerador de números aleatórios

numeroMaxChegadas = 5 # número máximo de chegadas

env = simpy.Environment() # cria o environment do modelo
env.process(criaChegadas(env, numeroMaxChegadas))
env.run(until=10)```

>Fique a vontade para implementar as função ao seu gosto, note, e isso é importante, que **praticamente todos os seus modelos de simulação em SimPy precisarão desta função!**

