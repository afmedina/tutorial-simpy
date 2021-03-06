# Solução dos desafios 2 e 3

> **Desafio 2:** é comum que os comandos de criação de entidades nos softwares proprietários tenham a opção de limitar o número máximo de entidades geradas durante a simulação.  
> Modifique a função `geraChegadas` de modo que ela receba como parâmetro o `numeroMaxChegadas`e limite a criação de entidades a este número.

Neste caso, o _script_ em Python é autoexplicativo, apenas note que limitei o número de chegadas em 5 e fiz isso antes da chamada do processo gerado pela função `geraChegadas()`:

```python
import random     # gerador de números aleatórios
import simpy      # biblioteca de simulação

def geraChegadas(env, nome, taxa, numeroMaxChegadas):
    # função que cria chegadas de entidades no sistema
    contaChegada = 0
    while (contaChegada < numeroMaxChegadas:
        yield env.timeout(random.expovariate(1/taxa))
        contaChegada += 1
        print("%s %i chega em: %.1f " % (nome, contaChegada, env.now))

random.seed(1000)   # semente do gerador de números aleatórios
env = simpy.Environment() # cria o environment do modelo
# cria o processo de chegadas
env.process(geraChegadas(env, "Cliente", 2, 5)) 
env.run(until=10) # executa a simulação por 10 unidades de tempo
```

> **Desafio 3:** modifique a função `geraChegadas`de modo que as chegadas entre entidades sejam distribuídas segundo uma distribuição triangular de moda 1, menor valor 0,1 e maior valor 1,1.

Neste caso, precisamos verificar na documentação da biblioteca `random`, quais são nossas opções. A tabela a seguir, resume as distribuições disponíveis:

| **Função** | **Distribuição** |
| --- | --- |
| `random.random()` | gera números aleatórios no intervalo \[0.0, 1.0\) |
| `random.uniform(a, b)` | uniforme no intervalo \[a, b\] |
| `random.triangular(low, high, mode)` | triangular com menor valor _low_, maior valor _high_ e moda _mode_ |
| `random.betavariate(alpha, beta)` | beta com parâmetros _alpha_ e _beta_ |
| `random.expovariate(lambd)` | exponencial com média 1/_lambd_ |
| `random.gammavariate(alpha, beta)` | gamma com parâmetros _alpha_ e _beta_ |
| `random.gauss(mu, sigma)` | normal com média _mu_ e desvio padrão _sigma_ |
| `random.lognormvariate(mu, sigma)` | lognormal com média _mu_ e desvio padrão _sigma_ |
| `random.normalvariate(mu, sigma)` | equivalente à random.gauss, mas um pouco mais lenta |
| `random.vonmisesvariate(mu, kappa)` | [distribuição de von Mises](http://en.wikipedia.org/wiki/Von_Mises_distribution) com parâmetros _mu_ e _kappa_ |
| `random.paretovariate(alpha)` | pareto com parâmetro _alpha_ |
| `random.weibullvariate(alpha, beta)` | weibull com parâmetros _alpha_ e _beta_ |

A biblioteca NumPy, que veremos oportunamente, possui mais opções para distribuições estatísticas. Por enquanto, o desafio 3 pode ser solucionado de maneira literal:

```python
import random     # gerador de números aleatórios
import simpy      # biblioteca de simulação

def geraChegadas(env, nome, numeroMaxChegadas):
    # função que cria chegadas de entidades no sistema
    contaChegada = 0
    while (contaChegada < numeroMaxChegadas:
        yield env.timeout(random.triangular(0.1,1,1.1))
        contaChegada += 1
        print("%s %i chega em: %.1f " % (nome, contaChegada, env.now)))

random.seed(1000)         # semente do gerador de números aleatórios
env = simpy.Environment() # cria o environment do modelo
# cria o processo de chegadas
env.process(geraChegadas(env, "Cliente, 5))
env.run(until=10)
```

### Dica

Os modelos de simulação com muitos processos de chegadas e atendimento, tendem a utilizar diversas funções diferentes de distribuição de probabilidades, deixando as coisas meio confusas para o programador.

Uma dica bacana é criar uma função que armazene todas as distribuições do modelo em um único lugar, como uma prateleira de distribuições.

Por exemplo, imagine um modelo em SimPy que possui 3 processos: um exponencial com média 10 min, um triangular com parâmetros \(10, 20, 30\) min e um normal com média 0 e desvio 1 minuto. A função `distribution()` a seguir, armazena todos os geradores de números aleatórios em um único local:

```python
import random

def distributions(tipo):
    return {
        'arrival': random.expovariate(1/10.0),
        'singing': random.triangular(10, 20, 30),
        'applause': random.gauss(10, 1),
    }.get(tipo, 0.0)
```

O próximo exemplo testa como chamar a função:

```python
tipo = 'arrival'
print(tipo, distributions(tipo))

tipo = 'singing'
print(tipo, distributions(tipo))

tipo = 'applause'
print(tipo, distributions(tipo))
```

O qual produz a saída:

```python
arrival 6.231712146858156
singing 22.192356552471104
applause 10.411795571842426
```

Essa foi a nossa dica do dia!

> Fique a vontade para implementar funções de geração de números aleatórios ao seu gosto. Note, e isso é importante, que **praticamente todos os seus modelos de simulação em SimPy precisarão deste tipo de função!**

Uma última observação:

> Atenção à eficiência do código. Como a finalidade deste texto é prioritariamente didática, as chamadas às funções de geração de números aleatórios respeitam a lógica do aprendizado. Contudo, tais chamadas não são exatamente eficientes... Por exemplo, você consegue descobrir qual das duas chamadas a seguir é a mais eficiente e por quê?

```python
while True:
    yield env.timeout(random.expovariate(1.0/2.0))
```

Ou:

```python
while True:
    yield env.timeout(random.expovariate(0.5))
```

**Resposta: **note que, no primeiro caso, a cada novo número gerado é realizada uma operação de divisão. No segundo caso, isso não ocorre, deixando o tempo de processamento bem mais rápido.

## Teste seus conhecimentos:

1. Acrescente ao programa inicial, uma função `distribution` como a proposta na Dica do Dia e faça o tempo entre chegadas sucessivas de entidades chamar a função para obter o valor correto.
2. Considere que 50% das entidades geradas durante a simulação são do sexo feminino e 50% do sexo masculino. Modifique o programa para que ele sorteie o gênero dos clientes. Faça esse sorteio dentro da função `distribution` já criada.



