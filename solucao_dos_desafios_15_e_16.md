# Solução dos desafios 15 e 16

> **Desafio 15:** considere, no exemplo do posto, que a taxa de enchimento do tanque é de 5 $$m^3$$/min e a de esvaziamento é de 1 $$m^3$$/min. Altere o modelo para que ele incorpore os tempos de enchimento e esvaziamento, bem como forneça o tempo que o veículo aguardou na fila por atendimento.

Neste caso, são criadas duas constantes:
```python
TAXA_VEICULO = 1            # taxa de bombeamento do veículo
TAXA_CAMINHAO = 5           # taxa de bombeamento do caminhãoon
```
As funções de enchimento e esvaziamento do tanque devem ser modificadas para considerar o tempo de espera que os veículos e caminhões aguardam até que o processo de bombeamento tenha terminado, como representado nas funções a seguir:
```python
def esvaziamentoTanque(env, qtd, tanque):
    # esvazia o tanque
    print("%d Novo veículo de %3.2f m3.\t Nível atual: %5.1f m3" % (env.now, qtd, tanque.level))
    yield tanque.get(qtd)
    #aguarda o tempo de bombeamento
    yield env.timeout(qtd/TAXA_VEICULO)
    print("%d Veículo atendido de %3.2f m3.\t Nível atual: %5.1f m3" % (env.now, qtd, tanque.level))

def enchimentoTanque(env, qtd, tanque):  
    # enche o tanque
    print("%d Novo caminhão com %4.1f m3.\t Nível atual: %5.1f m3" % (env.now, qtd, tanque.level))
    yield tanque.put(qtd)
    #aguarda o tempo de bombeamento
    yield env.timeout(qtd/TAXA_CAMINHAO)
    print("%d Tanque enchido com %4.1f m3.\t Nível atual: %5.1f m3" % (env.now, qtd, tanque.level))
```
Em cada função foi acrescentada uma linha yield env.timeout(qtd/taxa) que representa o tempo que deve-se aguardar pelo bombeamento do produto. 

O modelo completo ficaria:
```python
import simpy
import random        

TANQUE_CAMINHAO = 50        # capacidade de abastecimento do caminhão
TANQUE_VEICULO = 0.10       # capacidade do veículo
TEMPO_CHEGADAS = 5          # tempo entre chegadas sucessivas de veículos
NIVEL_MINIMO = 50           # nível mínimo de reabastecimento do tanque
TEMPO_CONTROLE = 1          # tempo entre verificações do nível do tanque
TAXA_VEICULO = 1            # taxa de bombeamento do veículo
TAXA_CAMINHAO = 5           # taxa de bombeamento do caminhão

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
    #aguarda o tempo de bombeamento
    yield env.timeout(qtd/TAXA_VEICULO)
    print("%d Veículo atendido de %3.2f m3.\t Nível atual: %5.1f m3" % (env.now, qtd, tanque.level))

def enchimentoTanque(env, qtd, tanque):  
    # enche o tanque
    print("%d Novo caminhão com %4.1f m3.\t Nível atual: %5.1f m3" % (env.now, qtd, tanque.level))
    yield tanque.put(qtd)
    #aguarda o tempo de bombeamento
    yield env.timeout(qtd/TAXA_CAMINHAO)
    print("%d Tanque enchido com %4.1f m3.\t Nível atual: %5.1f m3" % (env.now, qtd, tanque.level))

random.seed(150)            
env = simpy.Environment()
#cria um tanque de 100 m3, com 50 m3 no início da simulação
tanque = simpy.Container(env, capacity=100, init=50)
env.process(chegadasVeiculos(env, tanque))
env.process(sensorTanque(env, tanque))

env.run(until = 20)```python
```
Como resultado, o modelo fornece:
```
0 Novo caminhão com 50.0 m3.     Nível atual:  50.0 m3
5 Novo veículo de 0.10 m3.       Nível atual: 100.0 m3
5 Veículo atendido de 0.10 m3.   Nível atual:  99.9 m3
10 Tanque enchido com 50.0 m3.   Nível atual:  99.9 m3
10 Novo veículo de 0.10 m3.      Nível atual:  99.9 m3
10 Veículo atendido de 0.10 m3.  Nível atual:  99.8 m3
15 Novo veículo de 0.10 m3.      Nível atual:  99.8 m3
15 Veículo atendido de 0.10 m3.  Nível atual:  99.7 m3
```
O leitor atento deve ter notado que o caminhão de reabastecimento enche o tanque *antes* mesmo de aguardar o bombeamento, pois a saída do programa indica que um caminhão chegou no instante 0 e que no instante 5, o tanque já possui 100 $$m^3$$ à disposição:

```
0 Novo caminhão com 50.0 m3.    Nível atual:  50.0 m3
5 Novo veículo de 0.10 m3.      Nível atual: 100.0 m3
```
A situação inicialmente *estranha* ainda é reforçada pelo fim da operação de enchimento do tanque no instante 10:

`10 Tanque enchido com 50.0 m3.`

Isto significa que o produto estava disponível nos tanques *antes* mesmo de ter sido bombeado para o mesmo. 
Fica como desafio ao leitor *atento* encontrar uma solução para o problema (dica: que tal pensar em um tanque virtual?

> **Desafio 16:** continuando o exemplo, modifique o modelo de modo que ele represente a situação em que o tanque não pode ser enchido e esvaziado simultâneamente.
Neste caso, o tanque quando bombeando para um sentido (encher ou esvaziar), fica impedido de ser utilizado no outro sentido. Este tipo de situação é bem comum em operações envolvendo tanques de produtos químicos.
Uma possível solução para o problema é utilizar um `Store` para armazenar o `Container `que representa o tanque. Assim, quando um caminhão de reabastecimento chega ele *retira* do Store o tanque e, caso um veículo chegue nesse instante, não conseguirá abastecer pois não encontrará nenhum tanque no Store.

##Teste seus conhecimentos
1. Modifique o problema para considerar que existam 3 bombas de combustível no posto, capazes de atender aos veículos simultâneamente do mesmo tanque.
2. Construa um gráfico (utilizando a biblioteca ```[matplotlib](http://matplotlib.org/)```) do nível do tanque ao longo do tempo.
