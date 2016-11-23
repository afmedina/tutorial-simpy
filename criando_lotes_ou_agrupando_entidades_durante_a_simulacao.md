# Criando lotes (ou agrupando) entidades durante a simulação

Uma situação bastante comum em modelos de simulação é o agrupamento de entidades em lotes ou o seu oposto: o desmembramento de um lote em diversas entidades separadas. É usual em softwares de simulação proprietários existir um comando (ou bloco) específico para isso. Por exemplo, o Arena possui o "Batch/Separate", o Simul8 o "Batching" etc.

Vamos partir de um exemplo simples, em que uma célula de produção deve realizar a tarefa de montagem de um certo componente a partir do encaixe de 1 peça A com duas peças B. O operador da célula leva em média 5 minutos para montar o componente, segundo uma distribuição normal com desvio padrão de 1 minuto. Os processos de chegadas dos lotes A e B são distintos entre si, com tempos entre chegadas sucessivas uniformemente distribuidos no intervalo de 40 a 60 minutos.

## Uma tática para agrupamento de lotes utilizando `Container`

Uma maneira de resolver o problema é criar um ```Container``` para cada peça. Assim, criamos dois estoques, para as peças A e B, de modo que o componente só poderá iniciar sua montagem se cada estoque contiver ao menos o número de peças necessárias para sua montagem.

Comecemos criando uma possível máscara para o problema:
```python
import simpy
import random

TEMPO_CHEGADAS = [40, 50]       # intervalo entre chegadas de peças
TEMPO_MONTAGEM = [5, 1]         # intervalo entre chegadas de peças


def chegadaPecas(env, pecasContainerDict, tipo, tamLote):
    # gera lotes de pecas em intervalos uniformemente distribuídos
    # encaminha para o estoque
    pass
        
def montagem(env, pecasContainerDict, numA, numB):
    # montagem do componente
    pass
    
random.seed(100)            
env = simpy.Environment()

#cria estoques de peças 
pecasContainerDict = {}
pecasContainerDict['A'] = simpy.Container(env)
pecasContainerDict['B'] = simpy.Container(env)

# inicia processos de chegadas de pecas
env.process(chegadaPecas(env, pecasContainerDict, 'A', 10))
env.process(chegadaPecas(env, pecasContainerDict, 'B', 10))
# inicia processo de montagem
env.process(montagem(env, pecasContainerDict, 1, 2))
env.run(until = 80)   
```
Na máscara anterior, foram criadas duas funções: ```chegaPecas```, que gera os lotes de peças A e B e armazena nos respectivos estoques e ```montagem```, que retira as peças do estoque e montam o componente.

Note que criei um dicionário no Python para armazenar o Container de cada peça:


