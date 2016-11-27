# Enchendo ou esvaziando caixas, tanques ou objetos com `Container()`

Um tipo especial de recurso no SimPy é o `conteiner`. Intuitivamente, um `conteiner` seria um taque ou caixa em que se armazenam coisas. Você pode encher ou esvaziar em quantidade, como se fosse um tanque de líquido ou uma caixa de laranjas.

A sua utilização é bem simples, por exemplo, podemos modelar um tanque de 100 unidades de capacidade \($$m^3$$, por exemplo\), com um estoque inicial de 50 unidades, por meio do seguinte código:

```python
import simpy

env = simpy.Environment()
#cria um tanque de 100 m3 de capacidade, com 50 m3 no início da simulação
tanque = simpy.Container(env, capacity=100, init=50)
```

O `container`possui três comandos importantes:

* Para encher: `tanque.put(quantidade)`
* Para esvaziar: `tanque.get(quantidade)`
* Para obter o nível atual: `tanque.level`

## Enchendo o meu container `yield meuContainer.put(quantidade)`

Considere que um posto de gasolina possui um tanque com capacidade de 100 $$m^3$$ \(ou 100.000 litros\) de combustível. Incialmente o tanque contém 50 $$m^3$$ armazenado.

Vamos criar uma função, `enchimentoTanque`, que enche o tanque com 50 $$m^3$$ sempre que um novo caminhão de reabastecimento de combustível chega ao posto:

```python
import simpy
import random        

TANQUE_CAMINHAO = 50       # capacidade de abastecimento do caminhão

def enchimentoTanque(env, qtd, tanque):  
    # enche o tanque
    print("%d Novo caminhão com %4.1f m3.\t Nível atual: %5.1f m3" % (env.now, qtd, tanque.level))
    yield tanque.put(qtd)
    print("%d Tanque enchido com %4.1f m3.\t Nível atual: %5.1f m3" % (env.now, qtd, tanque.level))

random.seed(150)            
env = simpy.Environment()
#cria um tanque de 100 m3, com 50 m3 no início da simulação
tanque = simpy.Container(env, capacity=100, init=50)
env.process(enchimentoTanque(env, TANQUE_CAMINHAO, tanque))

env.run(until = 500)
```
A saída do programa é bastante simple, afinal o processo de enchimento do tanque é executado apenas uma vez:
```python
0 Novo caminhão de combustível com 50.0 m3. Nível atual:  50.0 m3
0 Tanque enchido com 50.0 m3. Nível atual: 100.0 m3
```
Se você iniciar o tanque do posto a sua plena capacidade (100 $$m^3$$), deve o caminhão tenta abastecer, mas não consegue por falta de espaço, virtualmente aguardando espaço no tanque na linha `yield tanque.put(qtd)` dentro da função `enchimentoTanque`.

##Esvaziando o meu container: `yield meuContainer.get(quantidade)`
Considere agora que o posto atende automóveis que chegam em intervalos constantes de 5 minutos entre si e que cada veículo abastece 100 litros ou 0.10 $$m^3$$.

Partindo do modelo anterior, vamos criar duas funções: uma para gerar os veículos e outra para transferir o combustível do tanque para o veículo. A nossa máscara de modelagem ficaria:
```python
import simpy
import random        

TANQUE_CAMINHAO = 50        # capacidade de abastecimento do caminhão
TANQUE_VEICULO = 0.10       # capacidade do veículo
TEMPO_CHEGADAS = 5          # tempo entre chegadas sucessivas de veículos

def chegadasVeiculos(env, tanque):
    #gera chegadas de veículos por produto
        
def esvaziamentoTanque(env, qtd, tanque):
    # esvazia o tanque

def enchimentoTanque(env, qtd, tanque):  
    # enche o tanque
    print("%d Novo caminhão com %4.1f m3.\t Nível atual: %5.1f m3" % (env.now, qtd, tanque.level))
    yield tanque.put(qtd)
    print("%d Tanque enchido com %4.1f m3.\t Nível atual: %5.1f m3" % (env.now, qtd, tanque.level))

random.seed(150)            
env = simpy.Environment()
#cria um tanque de 100 m3, com 50 m3 no início da simulação
tanque = simpy.Container(env, capacity=100, init=50)
env.process(chegadasVeiculos(env, tanque))

env.run(until = 20)
```

A função `chegadasVeiculos `gera os veículos que buscam abastecimento no posto e chama o função esvaziamentoTanque que provoca o esvaziamento do tanque do posto na quantidade do tanque do veículo:
```python
def chegadasVeiculos(env, tanque):
    #gera chegadas de veículos por produto
    while True:
        yield env.timeout(TEMPO_CHEGADAS)
        # carrega veículo
        env.process(esvaziamentoTanque(env, TANQUE_VEICULO, tanque))
```

A função que representa o processo de esvaziamento do tanque é semelhante a de enchimento da seção anterior, a menos da opção `get(qtd)`, que retira a quantidade `qtd `do `container tanque`:
```python
def esvaziamentoTanque(env, qtd, tanque):
    # esvazia o tanque
    print("%d Novo veículo de %3.2f m3.\t Nível atual: %5.1f m3" % (env.now, qtd, tanque.level))
    yield tanque.get(qtd)
    print("%d Veículo atendido de %3.2f.\t Nível atual: %5.1f m3" % (env.now, qtd, tanque.level))
```

O programa completo fica:
```python
import simpy
import random        

TANQUE_CAMINHAO = 50        # capacidade de abastecimento do caminhão
TANQUE_VEICULO = 0.10       # capacidade do veículo
TEMPO_CHEGADAS = 5          # tempo entre chegadas sucessivas de veículos

def chegadasVeiculos(env, tanque):
    # gera chegadas de veículos por produto
    while True:
        yield env.timeout(TEMPO_CHEGADAS)
        # carrega veículo
        env.process(esvaziamentoTanque(env, TANQUE_VEICULO, tanque))
        
def esvaziamentoTanque(env, qtd, tanque):
    # esvazia o tanque
    print("%d Novo veículo de %3.2f m3.\t Nível atual: %5.1f m3" % (env.now, qtd, tanque.level))
    yield tanque.get(qtd)
    print("%d Veículo atendido de %3.2f m3.\t Nível atual: %5.1f m3" % (env.now, qtd, tanque.level))

def enchimentoTanque(env, qtd, tanque):  
    # enche o tanque
    print("%d Novo caminhão com %4.1f m3.\t Nível atual: %5.1f m3" % (env.now, qtd, tanque.level))
    yield tanque.put(qtd)
    print("%d Tanque enchido com %4.1f m3.\t Nível atual: %5.1f m3" % (env.now, qtd, tanque.level))

random.seed(150)            
env = simpy.Environment()
#cria um tanque de 100 m3, com 50 m3 no início da simulação
tanque = simpy.Container(env, capacity=100, init=50)
env.process(chegadasVeiculos(env, tanque))

env.run(until = 200)
```
Quando executado:
```
5 Novo veículo de 0.10 m3.       Nível atual:  50.0 m3
5 Veículo atendido de 0.10 m3.   Nível atual:  49.9 m3
10 Novo veículo de 0.10 m3.      Nível atual:  49.9 m3
10 Veículo atendido de 0.10.     Nível atual:  49.8 m3
15 Novo veículo de 0.10 m3.      Nível atual:  49.8 m3
15 Veículo atendido de 0.10 m3.  Nível atual:  49.7 m3

```
## Criando um sensor para o nível atual do `container`
Ainda no exemplo do posto, vamos chamar um caminhão de reabastecimento sempre que o tanque atingir o nível de 50 $$m^3$$. Para isso, vamos criar uma função `sensorTanque `que reconheça o instante em que o nível do tanque abaixou do valor desejado e, portanto, envie um caminhão de reabastecimento.

Incialmente, para identificar se o nível do tanque abaixou além no nível mínimo, precisamos verificar o nível atual. Contudo, esse processo de verificação não é contínuo no tempo e deve ter o seu intervalo entre verificações pré-definido no modelo.

Assim, são necessários dois parâmetros: um para o nível mínimo e outro para o intervalo entre verificações do nível do tanque. Uma possível codificação para a função `sensorTanque `seria:
```python
NIVEL_MINIMO = 50           # nível mínimo de reabastecimento do tanque
TEMPO_CONTROLE = 1          # tempo entre verificações do nível do tanque

def sensorTanque(env, tanque):
    # quando o tanque baixar se certo nível, dispara o enchimento
    while True:
        if tanque.level <= NIVEL_MINIMO:
            # dispara pedido de enchimento
            yield env.process(enchimentoTanque(env, TANQUE_CAMINHAO, tanque))
        # aguarda um tempo para fazer a nova chegagem do nível do tanque
        yield env.timeout(TEMPO_CONTROLE)
```
A função `sensorTanque `é um loop infinito (`while True`) que a cada 1 minuto (configurável na constante `TEMPO_CONTROLE`) verifica se o nível do tanque está abaixo ou igual ao nível mínimo (configurável na constante `NIVEL_MINIMO`).

O modelo completo agora seria:
```python
import simpy
import random        

TANQUE_CAMINHAO = 50        # capacidade de abastecimento do caminhão
TANQUE_VEICULO = 0.10       # capacidade do veículo
TEMPO_CHEGADAS = 5          # tempo entre chegadas sucessivas de veículos
NIVEL_MINIMO = 50           # nível mínimo de reabastecimento do tanque
TEMPO_CONTROLE = 1          # tempo entre verificações do nível do tanque

def sensorTanque(env, tanque):
    # quando o tanque baixar se certo nível, dispara o enchimento
    while True:
        if tanque.level <= NIVEL_MINIMO:
            # dispara pedido de enchimento
            yield env.process(enchimentoTanque(env, TANQUE_CAMINHAO, tanque))
        # aguarda um tempo para fazer a nova chegagem do nível do tanque
        yield env.timeout(TEMPO_CONTROLE)
        
def chegadasVeiculos(env, tanque):
    # gera chegadas de veículos por produto
    while True:
        yield env.timeout(TEMPO_CHEGADAS)
        # carrega veículo
        env.process(esvaziamentoTanque(env, TANQUE_VEICULO, tanque))
        
def esvaziamentoTanque(env, qtd, tanque):
    # esvazia o tanque
    print("%d Novo veículo de %3.2f m3.\t Nível atual: %5.1f m3" % (env.now, qtd, tanque.level))
    yield tanque.get(qtd)
    print("%d Veículo atendido de %3.2f m3.\t Nível atual: %5.1f m3" % (env.now, qtd, tanque.level))

def enchimentoTanque(env, qtd, tanque):  
    # enche o tanque
    print("%d Novo caminhão com %4.1f m3.\t Nível atual: %5.1f m3" % (env.now, qtd, tanque.level))
    yield tanque.put(qtd)
    print("%d Tanque enchido com %4.1f m3.\t Nível atual: %5.1f m3" % (env.now, qtd, tanque.level))

random.seed(150)            
env = simpy.Environment()
#cria um tanque de 100 m3, com 50 m3 no início da simulação
tanque = simpy.Container(env, capacity=100, init=50)
env.process(chegadasVeiculos(env, tanque))
env.process(sensorTanque(env, tanque))

env.run(until = 20)
```
Note a criação do processo do sensorTanque na penúltima linha do programa:
```python
env.process(sensorTanque(env, tanque))
```
Este processo garante que o sensor estará operante ao longo de toda a simulação. Quando executado, o programa anterior retorna:
```
0 Novo caminhão com 50.0 m3.     Nível atual:  50.0 m3
0 Tanque enchido com 50.0 m3.    Nível atual: 100.0 m3
5 Novo veículo de 0.10 m3.       Nível atual: 100.0 m3
5 Veículo atendido de 0.10 m3.   Nível atual:  99.9 m3
10 Novo veículo de 0.10 m3.      Nível atual:  99.9 m3
10 Veículo atendido de 0.10 m3.  Nível atual:  99.8 m3
15 Novo veículo de 0.10 m3.      Nível atual:  99.8 m3
15 Veículo atendido de 0.10 m3.  Nível atual:  99.7 m3
```

>Observação 1. Note que o enchimento ou esvaziamento dos tanques é instântaneo, isto é: não existe nenhuma taxa de enchimento ou esvaziamento associada aos processos. Cabe ao programador modelar situações em que a taxa de transferência é relevante (veja o Desafio 15, a seguir).

>Observação 2: O tanque pode ser esvaziado ou enchido simultâneamente. Novamente cabe ao programador modelar a situação em que isto não se verifica (veja o Desafio 16, a seguir).

## Conceitos desta seção
| Conteúdo | Descrição |
| -- | -- |
| ```meuContainer = simpy.Container(env, capacity=capacity, init=init``` | cria um *container* `meuContainer `com capacidade `capacity `e quantidade inicial de `init`|
| `yield meuContainer.put(quantidade)` | adiciona uma dada `quantidade `ao `meuContainer`, se houver espaço suficiente, caso contrário aguarda até que o espaço esteja disponível|
| `yield meuContainer.get(quantidade)` | retira uma dada `quantidade `ao `meuContainer`, se houver quantidade suficiente, caso contrário aguarda até que a quantidade esteja disponível|
| `meuContainer.level` | retorna a quantidade diponível atualmente em `meuContainer`|

## Desafios

> **Desafio 17:** considere, no exemplo do posto, que a taxa de enchimento do tanque é de 1 litro/min e a de esvaziamento é de 2 litros/min. Altere o modelo para que ele incorpore os tempos de enchimento e esvaziamento, bem como forneça o tempo que o veículo aguardou na fila por atendimento.
> 
> **Desafio 18:** continuando o exemplo, modifique o modelo de modo que ele represente a situação em que o tanque não pode ser enchido e esvaziado simultâneamente.

