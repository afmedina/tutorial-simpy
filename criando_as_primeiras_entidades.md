#Primeiro passo em SimPy: criando entidades

Algo elementar em qualquer pacote de simulação é uma função para criar entidades dentro do modelo. É o [“Alô mundo!”](http://pt.wikipedia.org/wiki/Programa_Ol%C3%A1_Mundo) dos pacotes de simulação. Nossa primeira missão será construir uma função que gere entidades  com intervalos entre chegadas sucessivas exponencialmente distribuídos, com média de 2 min.

<!---
sugiro incluir um módulo inicial com o básico de simulação
lá, definir entidades, recursos e processos
dar exemplos de entidades: clientes, peças, navios etc
recursos: posto de atendimento, máquina, berço etc
processos: atendimento, usinagem, carga/descarga etc

explicar dois processos básicos: geração (arrival) e extinção (dispose) de entidades

o primeiro exemplo pode ser determinínstico (uma chegada exatamente a cada 5 min), depois o aleatório (exercício)


R:
Se fosse um livro de simulação... Mas acho que a maioria vem aqui já sabendo esse básico e quer aprender logo a linguagem

Repare que, mesmo começando mais adiantado (pressupondo conhecimentos anteriores) a quantidade de informação é grande e longe de ser óbvia
--->
### Chamada das bibliotecas random e simpy

Inicialmente serão necessárias duas bibliotecas do Python: a ```random``` – biblioteca de geração de números aleatórios – e a ```simpy```, que é o próprio SimPy.

Começaremos nosso primeiro programa em SimPy chamando as bibliotecas de interesse:

<!---
não seria mais correto dizer que o programa é em Python? (ou Python / Simpy?)
SimPy é a biblioteca...

Não sei...
--->

```python
import random # gerador de números aleatórios
import simpy # biblioteca de simulação```

### Criando um evironment de simulação

Tudo no SimPy gira em torno de **processos** criandos por funções e todos os processos ocorrem num **environment**, ou um “ambiente” de simulação criando a partir da função ```simpy.Environment()```. 
Assim, o programa principal sempre começa com uma chamada ao SimPy, criando um *environment*  “env”:

```python
import random # gerador de números aleatórios
import simpy # biblioteca de simulação

env = simpy.Environment() # cria o environment do modelo
```
<!---
"env" é o nome do ambiente?
Poderia ser: "fab", "hosp", "porto"?

Isso ainda estou aprendendo. Nunca tentei um modelo com dois env ainda
--->

<!---
Sugestão: simular chegadas (e partidas) em uma praça pública
Pessoas chegam, ficam um tempo e vão embora
Quantas pessoas teremos na praça?

Ainda não. Limitei essa seção só ao processo de chegadas, porque a linguagem não é nada fácil

Mas aprimorar o exemplo, ok.
--->

Se você executar o programa anterior, nada acontece. No momento, você apenas criou um *environment*, mas não criou nenhum processo, portanto, não existe nenhum evento a ser simulado pelo SimPy.

### Criando um processo dentro do environment

Vamos escrever uma função ```
geraChegadas()```
 que cria entidades no sistema enquanto durar a simulação, a partir de três parâmetros de entrada: o *environment*, o nome da entidade (ou tipo) e a taxa de chegadas de entidades por unidade de tempo.
 
Assim, nosso código começa a ganhar corpo:
```python
import random # gerador de números aleatórios
import simpy # biblioteca de simulação

def geraChegadas(env, nome, lambda):
    #função que cria chegadas de entidades no sistema
    pass
    
env = simpy.Environment() # cria o environment do modelo
```

Inicialmente, precisamos gerar intervalos de tempos aleatórios, exponencialmente distribuídos, para representar os tempos entre chegadas sucessivas das entidades. Para gerar chegadas com intervalos exponenciais, utilizaremos a biblioteca ```random```, bem detalhada na sua [documentação](https://docs.python.org/2/library/random.html), e que possui a função:
```python
random.expovariate(lambd)```

Onde ```
lambd```
 é a taxa de ocorrência dos eventos ou, matematicamente, o inverso do tempo médio entre eventos sucessivos. No caso, se eu quero que as chegadas sejam entre intervalos médios de 2 min, a função ficaria:
```python
random.expovariate(lambd=1/2)```

A linha anterior é nosso gerador de números aleatórios de números exponencialmente distribuídos. O próximo passo é informar ao SimPy que queremos nossas entidades surgindo no sistema segundo a distribuição definida. Isso é feito pela chamada da palavra reservada ```
yield```
 com a função do SimPy ```
env.timeout(intervalo)```, que nada mais é do que uma função que causa um atraso de tempo, um *delay* no tempo dentro do *enviroment* ```
env```
 criado:

```python
yield env.timeout(random.expovariate(lambd=1/2))
```

Na linha de código anterior estamos executando ```
yield env.timeout()```
 para que o modelo retarde o processo num tempo aleatório gerado pela função ```
random.expovariate()```. Oportunamente, discutiremos mais a fundo qual o papel do palavra ```yield``` (*spoiler*: ela não é do SimPy, mas originalmente do próprio Python). Por hora, considere que ela é uma maneira de **criar eventos** dentro do ```
env```.

Colocando tudo junto na função ```
geraChegadas()```
e lembrando que temos de passar ```
env```
 como argumento da função, temos:
 


```python
import random # gerador de números aleatórios
import simpy  # biblioteca de simulação

def geraChegadas(env, nome, lambda):
    #função que cria chegadas de entidades no sistema
    contaChegada = 0
    while True:
        yield env.timeout(random.expovariate(lambda))
        contaChegada += 1
        print("%s %i chega em: %.1f " % (nome, contaChegada, env.now))

env = simpy.Environment() # cria o environment do modelo```

O código deve ser autoexplicativo: o laço ```
while```
 é **infinito** enquanto dure a simulação; um contador, ```
contaChegada```, armazena o total de entidades geradas e a função ```
print```, imprime na tela o instante de chegada de cada cliente. Note apenas que, dentro do ```print```, existe uma chamada para a **hora atual de simulação** ```
env.now()```.

Se você executar o codigo anterior, nada acontece novamente, pois falta chamarmos a função e informarmos ao SimPy qual o tempo de simulação. A chamada da função nos relembra que tudo em SimPy é gerar processos:

```python
import random # gerador de números aleatórios
import simpy  # biblioteca de simulação

def geraChegadas(env, nome, lambda):
    #função que cria chegadas de entidades no sistema
    contaChegada = 0
    while True:
        yield env.timeout(random.expovariate(lambda))
        contaChegada += 1
        print("%s %i chega em: %.1f " % (nome, contaChegada, env.now))

random.seed(1000)   # semente do gerador de números aleatórios
env = simpy.Environment() # cria o environment do modelo
env.process(geraChegadas(env, "Cliente", (1/2))) # cria o processo de chegadas
env.run(until=10) # roda a simulação por 10 unidades de tempo
```

Agora sim!

Note que ```
env.process(criaChegadas(env))```
 é um comando que **torna** a função ```criaChegadas()``` um processo dentro do environment ```
env```
. Esse processo só começa a ser executado na linha seguinte, quando ```
env.run(until=10)```
 informa ao SimPy para que todo processo pertencente ao ```
env```
 seja executado por um tempo de simulação igual a 10 minutos.

## Conceitos desta seção
| Conteúdo | Descrição |
| -- | -- |
| ```env = simpy.Environment()``` | cria um *environment* de simulação |
| ```random.expovariate(lambd)``` | gera números aleatórios exponencialmente distribuidos, com taxa *lambd* |
| ```yield env.timeout(time)``` | gera um atraso dado por *time* |
| ```random.seed(seed)``` | define o gerador de sementes aleatórias para um mesmo valor a cada nova simulação |
| ```env.process(geraChegadas(env))``` | inicia a função ```criaChegadas``` como um *processo* em ```env``` |
| ```env.run(until=tempoSim)``` | executa a simulação (executa todos os processos criandos em ```env```) pelo tempo *tempoSim* |
| ```env.now``` | retorna o instante atual da simulação |

<!---
Legal esta revisão (tabela)
--->

## Desafios (soluções na próxima seção)
**Desafio 2:** é comum que os comandos de criação de entidades nos [softwares proprietários](https://pt.wikipedia.org/wiki/Software_propriet%C3%A1rio) tenham a opção de limitar o número máximo de entidades geradas durante a simulação. 
Modifique a função ```
geraChegadas```
 de modo que ela receba como parâmetro ```
numeroMaxChegadas```
 e limite a criação de entidades a este número.

**Desafio 3:** modifique a função ```
geraChegadas```
 de modo que as chegadas entre entidades sejam distribuídas segundo uma distribuição triangular de moda 1, menor valor 0,1 e maior valor 1,1.
 





