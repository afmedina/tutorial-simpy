``# Criando lotes (ou agrupando) entidades durante a simulação

Uma situação bastante comum em modelos de simulação é o agrupamento de entidades em lotes ou o seu oposto: desagrupamento de um lote em diversas entidades. É muito comum em softwares de simulação existir um comando (ou bloco) específico para isso. Por exemplo, o Arena possui o "Batch/Separate", o Simul8 o "Batching" etc.

Considere uma célula de produção que realiza a tarefa de montagem de um componente a partir do encaixe de 1 peça A com duas peças B. O operador da célula leva em média 5 minutos para montar o componente, segundo uma distribuição normal com desvio padrão de 1 minuto. Os processos de chegadas dos lotes A e B são distintos entre si, com tempos entre chegadas sucessivas uniformemente distribuidos no intervalo de 40 a 60 minutos.

## Uma tática para agrupamento de lotes utilizando `Store`

Uma maneira de resolver o problema é utilizar o comando Store visto na seção anterior. Assim, criamos dois estoques, para as peças A e B, de modo que o componente só poderá iniciar sua montagem se cada estoque contiver o número de peças necessárias para sua montagem.

Vamos começar criando uma possível máscara para o problema:
```python
import simpy
import random

TEMPO_CHEGADAS = [40, 50]       # intervalo entre chegadas de peças
TEMPO_MONTAGEM = [5, 1]         # intervalo entre chegadas de peças


def chegadaPecas(env, pecasContainerDict, tipo, tamLote):
    # gera lotes de pecas em intervalos uniformemente distribuídos
    # encaminha para o estoque
    while True:
        pecasContainerDict[tipo].put(tamLote)
        print("%5.1f Chegada de lote tipo %s: +%i peças."
                %(env.now, tipo, tamLote))
        yield env.timeout(random.uniform(*TEMPO_CHEGADAS))

        
def montagem(env, pecasContainerDict, numA, numB):
    # montagem da peça C
    while True:
        chegada = env.now
        yield pecasContainerDict['A'].get(numA)
        yield pecasContainerDict['B'].get(numB)
        espera = env.now - chegada
        print("%5.1f Inicia montagem.\tEstoque A: %i\tEstoque B: %i\tEspera: %4.1f"
                %(env.now, pecasContainerDict['A'].level, pecasContainerDict['B'].level, espera))
        yield env.timeout(random.normalvariate(*TEMPO_MONTAGEM))
        # acumula peça C no estoque
        yield pecasContainerDict['C'].put(1)
        print("%5.1f Fim da montagem.\tEstoque A: %i\tEstoque B: %i\tEstoque C: %i\t"
            %(env.now, pecasContainerDict['A'].level, pecasContainerDict['B'].level,
              pecasContainerDict['C'].level))
    
random.seed(100)            
env = simpy.Environment()

#cria estoques de peças 
pecasContainerDict = {}
pecasContainerDict['A'] = simpy.Container(env)
pecasContainerDict['B'] = simpy.Container(env)
pecasContainerDict['C'] = simpy.Container(env)

# inicia processos de chegadas de pecas
env.process(chegadaPecas(env, pecasContainerDict, 'A', 10))
env.process(chegadaPecas(env, pecasContainerDict, 'B', 10))
# inicia processo de montagem
env.process(montagem(env, pecasContainerDict, 1, 2))
env.run(until = 80)   
```

