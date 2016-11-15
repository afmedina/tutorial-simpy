#Primeiro passo em SimPy: criando entidades

Algo elementar em qualquer pacote de simulação é uma função para criar entidades dentro do modelo. É o [“Alô mundo!”](http://pt.wikipedia.org/wiki/Programa_Ol%C3%A1_Mundo) dos pacotes de simulação. Nossa primeira missão será construir uma função que gere entidades  com intervalos entre chegadas sucessivas exponencialmente distribuídos, com média de 2 min. Vamos simular o sistema por 10 minutos apenas.

### Chamada das bibliotecas ```random``` e ```simpy```

Inicialmente serão necessárias duas bibliotecas do Python: a ```random``` – biblioteca de geração de números aleatórios – e a ```simpy```, que é o próprio SimPy.

Começaremos nosso primeiro programa em SimPy chamando as bibliotecas de interesse:

<!---
não seria mais correto dizer que o programa é em Python? (ou Python / Simpy?)
SimPy é a biblioteca...

Não sei...
--->

```python
import random             # gerador de números aleatórios
import simpy              # biblioteca de simulação

random.seed(1000)         # semente do gerador de números aleatórios
```
Note a linha final``` random.seed(1000)```, ela garante que a geração de números aleatórios sempre começará pela mesma semente. Na prática,a sequência de números aleatórios gerados será sempre a mesma, facilitando o processo de verificação do programa.


### Criando um ```evironment``` de simulação

Tudo no SimPy gira em torno de **eventos** criandos por funções e todos os eventos ocorrem num **environment**, ou um “ambiente” de simulação criando a partir da função ```simpy.Environment()```. 
Assim, todo programa principal sempre começa com uma chamada ao SimPy, criando um *environment*  “env”:

```python
import random             # gerador de números aleatórios
import simpy              # biblioteca de simulação

random.seed(1000)         # semente do gerador de números aleatórios
env = simpy.Environment() # cria o environment do modelo na variável env
```

Se você executar o programa anterior, nada acontece. No momento, você apenas criou um *environment*, mas não criou nenhum processo, portanto, não existe ainda nenhum evento a ser simulado pelo SimPy.

### Criando um gerador de chegadas dentro do ```environment```

Vamos escrever uma função ```
geraChegadas()```
 que cria entidades no sistema enquanto durar a simulação, a partir de três parâmetros de entrada: o *environment*, o nome da entidade (ou tipo) e a taxa de chegadas de entidades por unidade de tempo. Para o SimPy, equivale dizer que você vai construir uma *função geradora de eventos* dentro do *environment* criado. No caso, os eventos gerados serão as chegadas de entidades no sistema.
 
Assim, nosso código começa a ganhar corpo:
```python
import random             # gerador de números aleatórios
import simpy              # biblioteca de simulação

def geraChegadas(env, nome, taxa):
    # função que cria chegadas de entidades no sistema
    pass

random.seed(1000)         # semente do gerador de números aleatórios
env = simpy.Environment() # cria o environment do modelo
```
Precisamos informar ao SimPy que a função ```geraChegadas()``` é, de fato, um processo que deve ser executado ao longo de toda a simulação. Um processo é criado dentro do ```environment```, pelo comando:
```python
env.process(função_que_gera_o_processo)
```
A chamada ao processo é sempre feita após a criação do env, então basta acrescentar uma nova linha ao nosso código:
```python
import random             # gerador de números aleatórios
import simpy              # biblioteca de simulação

def geraChegadas(env, nome, taxa):
    # função que cria chegadas de entidades no sistema
    pass
    
random.seed(1000)         # semente do gerador de números aleatórios
env = simpy.Environment() # cria o environment do modelo
# cria o processo de chegadas
env.process(geraChegadas(env, "Cliente", 2)))
```
### Criando intervalos de tempo de espera com ```env.timeout(tempo_de_espera)```
Inicialmente, precisamos gerar intervalos de tempos aleatórios, exponencialmente distribuídos, para representar os tempos entre chegadas sucessivas das entidades. Para gerar chegadas com intervalos exponenciais, utilizaremos a biblioteca ```random```, bem detalhada na sua [documentação](https://docs.python.org/2/library/random.html), e que possui a função:
```python
random.expovariate(lambd)
```

Onde `lambd` é a taxa de ocorrência dos eventos ou, matematicamente, o inverso do tempo médio entre eventos sucessivos. No caso, se queremos que as chegadas ocorram entre intervalos médios de 2 min, a função ficaria:
```python
random.expovariate(lambd=1.0/2.0)
```
A linha anterior é basicamente nosso gerador de números aleatórios exponencialmente distribuídos. O passo seguinte será informar ao SimPy que queremos nossas entidades surgindo no sistema segundo a distribuição definida. Isso é feito pela chamada da palavra reservada `yield` com a função do SimPy `env.timeout(intervalo)`, que nada mais é do que uma função que causa um atraso de tempo, um *delay* no tempo dentro do *enviroment* `env` criado:
```python
yield env.timeout(random.expovariate(1.0/2.0))
```
Na linha de código anterior estamos executando `yield env.timeout()` para que o modelo retarde o processo num tempo aleatório gerado pela função ```
random.expovariate()```.

Oportunamente, discutiremos mais a fundo qual o papel do palavra ```yield``` (*spoiler*: ela não é do SimPy, mas originalmente do próprio Python). Por hora, considere que ela é apenas uma maneira de **criar eventos** dentro do ```
env```.


> Atenção: uma função criada no Python (com o comando ```def```) só é tratada como um **processo** ou **gerador de eventos** para o SimPy, caso ela contenha ao menos uma linha de código com o comando ```yield```. Mais adiante, a seção "O que são funções geradoras" explica em mais detalhe o funcionamento do ```yield```.

Colocando tudo junto na função ```
geraChegadas()```, temos:
 
```python
import random             # gerador de números aleatórios
import simpy              # biblioteca de simulação

def geraChegadas(env, nome, taxa):
    # função que cria chegadas de entidades no sistema
    contaChegada = 0
    while True:
        yield env.timeout(random.expovariate(1.0/taxa))
        contaChegada += 1
        print("%s %i chega em: %.1f " % (nome, contaChegada, env.now))
        
random.seed(1000)         # semente do gerador de números aleatórios
env = simpy.Environment() # cria o environment do modelo
# cria o processo de chegadas
env.process(geraChegadas(env, "Cliente", 2))) 
```
O código deve ser autoexplicativo: o laço ```
while```
 é **infinito** enquanto dure a simulação; um contador, ```
contaChegada```, armazena o total de entidades geradas e a função ```
print```, imprime na tela o instante de chegada de cada cliente. Note que, dentro do ```print```, existe uma chamada para a **hora atual de simulação** ```
env.now```. 
Por fim, uma chamada a função ```random.seed()``` garante que os números aleatórios a cada execução do programa serão os mesmos.
###Executando o modelo por um tempo determinado com ```env.run(until=tempo_de_simulacao)```

Se você executar o codigo anterior, nada acontece novamente, pois ainda falta informarmos ao SimPy qual o tempo de duração da simulação. Isto é feito pelo comando: ```env.run(until=tempo_de_simulação)```
No exemplo proposto, o tempo de simulação deve ser de 10 min.

```python
import random             # gerador de números aleatórios
import simpy              # biblioteca de simulação

def geraChegadas(env, nome, taxa):
    # função que cria chegadas de entidades no sistema
    contaChegada = 0
    while True:
        yield env.timeout(random.expovariate(1/taxa))
        contaChegada += 1
        print("%s %i chega em: %.1f " % (nome, contaChegada, env.now))

random.seed(1000)         # semente do gerador de números aleatórios
env = simpy.Environment() # cria o environment do modelo
env.process(geraChegadas(env, "Cliente", 2)) # cria o processo de chegadas
env.run(until=10) # roda a simulação por 10 unidades de tempo
```

Ao executar o programa, temos a saída:
```
Cliente 1 chega em: 3.0 
Cliente 2 chega em: 5.2 
Cliente 3 chega em: 5.4 
Cliente 4 chega em: 6.3 
Cliente 5 chega em: 7.6 
Cliente 6 chega em: 9.1 
```

Agora sim!

Note que ```
env.process(geraChegadas(env))```
 é um comando que **torna** a função ```geraChegadas()``` um **processo** ou um **gerador de eventos** dentro do `Environment ````
env```
. Esse processo só começa a ser executado na linha seguinte, quando ```
env.run(until=10)```
 informa ao SimPy que todo processo pertencente ao ```Environment
env```
 seja executado por um **tempo de simulação** igual a 10 minutos.

## Conceitos desta seção
| Conteúdo | Descrição |
| -- | -- |
| ```env = simpy.Environment()``` | cria um *environment* de simulação |
| ```random.expovariate(lambd)``` | gera números aleatórios exponencialmente distribuidos, com taxa `lambd` |
| ```yield env.timeout(time)``` | gera um atraso dado por `time` |
| ```random.seed(seed)``` | define o gerador de sementes aleatórias para um mesmo valor a cada nova simulação |
| ```env.process(geraChegadas(env))``` | inicia a função ```geraChegadas``` como um *processo* em ```env``` |
| ```env.run(until=tempoSim)``` | executa a simulação (executa todos os processos criandos em ```env```) pelo tempo `tempoSim` |
| ```env.now``` | retorna o instante atual da simulação |


## Desafios (soluções na próxima seção)
>**Desafio 2:** é comum que os comandos de criação de entidades nos [softwares proprietários](https://pt.wikipedia.org/wiki/Software_propriet%C3%A1rio) tenham a opção de limitar o número máximo de entidades geradas durante a simulação. 
Modifique a função ```
geraChegadas```
 de modo que ela receba como parâmetro ```
numeroMaxChegadas```
 e limite a criação de entidades a este número.

>**Desafio 3:** modifique a função ```
geraChegadas```
 de modo que as chegadas entre entidades sejam distribuídas segundo uma distribuição triangular de moda 1, menor valor 0,1 e maior valor 1,1.
 





