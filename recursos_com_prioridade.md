# Outros tipos de recursos: com prioridade e preemptivos

Além do recurso como definido nas seções anteriores, o SimPy possui recursos com prioridade e "peemptivos", isto é: recursos que podem ser interrompidos por outros processos.

## Recursos com prioridade: ```PriorityResource```

Um recurso normal pode ter uma fila de entidades desejando ocupá-lo para executar determinado processo. Existindo a fila, o recurso será ocupado respeitando a ordem de chegada das entidades (ou a regra FIFO).

Contudo, existem situações em que algumas entidades possuem *prioridades* sobre as outras, de modo que elas desrespeitam a regra do primeiro a chegar é o primeiro a ser atendido.

Por exemplo, considere um consultório de pronto atendimento de um hospital em que 70% do pacientes são de prioridade baixa (pulseira verde), 20% de prioridade intermediária (pulseira amarela) e 10% de prioridade alta (pulseira vermelha). Existem 2 médicos que realizam o atendimento, sempre primeiro verificando a ordem de prioridade do paciente e depois a sua ordem na fila. Os pacientes chegam entre intervalos exponencialmente distribuídos com média de 5 minutos e o atendimento é também exponencial, com média de 9 minutos por paciente.

No caso do exemplo, os médicos são nossos recursos, mas eles respeitam a prioridade. Um médico ou recurso deste tipo, é sempre criado pelo comando:
```medicos = simpy.PriorityResource(env, capacity=capacidade_desejada)```

Para solução do exemplo, o programa aqui proposta terá 3 funções: uma para sorteio do tipo de pulseira e outras duas para processamento das chegas e pedidos. Como uma máscara inicial, teríamos:
```python
import simpy
import random

def sorteiaPulseira():
    #retorna a cor da pulseira e sua prioridade
    pass
    
def chegadaPacientes(env, medicos):
    #gera pacientes exponencialmente distribuídos
    #sorteia a pulseira
    #inicia processo de atendimento
    pass

def atendimento(env, paciente, pulseira, prio, medicos):
    #ocupa um médico e realiza o atendimento do paciente
    pass

random.seed(100)       
env = simpy.Environment()
medicos = simpy.PriorityResource(env, capacity=2) # cria os médicos
chegadas = env.process(chegadaPacientes(env, medicos))
env.run(until=20)       
```

O preenchimento da máscara pode ser feito de diversas maneira, a nossa abordagem foi a seguinte:

```python
import simpy
import random

def sorteiaPulseira():
    #retorna a cor da pulseira e sua prioridade
    r = random.random()
    if r <= .70:
        return "pulseira verde", 3
    elif r <= .90:
        return "pulseira amarela", 2
    return "pulseira vermelha", 1
    
def chegadaPacientes(env, medicos):
    #gera pacientes exponencialmente distribuídos
    #sorteia a pulseira
    #inicia processo de atendimento
    i = 0
    while True:
        yield env.timeout(random.expovariate(1/5))
        i += 1
        pulseira, prio = sorteiaPulseira()
        print("Paciente %s chega em %.1f com %s" %(i, env.now, pulseira))
        env.process(atendimento(env, "Paciente %s" % i, pulseira, prio, medicos))

def atendimento(env, paciente, pulseira, prio, medicos):
    #ocupa um médico e realiza o atendimento do paciente
    with medicos.request(priority=prio) as req:
        yield req
        print("%s com %s inicia o atendimento em %.1f" %(paciente, pulseira, env.now))
        yield env.timeout(random.expovariate(1/9))
        print("%s com %s termina o atendimento em %.1f" %(paciente, pulseira, env.now))

random.seed(100)       
env = simpy.Environment()
medicos = simpy.PriorityResource(env, capacity=2) # cria os médicos
chegadas = env.process(chegadaPacientes(env, medicos))
env.run(until=20)
``` 
O importante a ser destacado é que a prioridade é informada ao ```request``` do recurso ```medicos``` pelo argumento ```priority```:
```
with medicos.request(priority=prio) as req:
...
```
Para o SimPy, quando menor o valor fornecido para ```priority```, maior a prioridade daquela entidade. Assim, a função ```sorteiaPulseira``` retorna 3 para a pulseira verde (de menor prioridade) e 1 para a vermelha (de maior prioridade).

Quando o programa anterior é executado, fornece como saída:

```
Paciente 1 chega em 0.8 com pulseira verde
Paciente 1 com pulseira verde inicia o atendimento em 0.8
Paciente 2 chega em 8.2 com pulseira amarela
Paciente 2 com pulseira amarela inicia o atendimento em 8.2
Paciente 3 chega em 11.0 com pulseira verde
Paciente 4 chega em 11.4 com pulseira verde
Paciente 5 chega em 11.7 com pulseira vermelha
Paciente 1 com pulseira verde termina o atendimento em 11.8
Paciente 5 com pulseira vermelha inicia o atendimento em 11.8
Paciente 5 com pulseira vermelha termina o atendimento em 15.5
Paciente 3 com pulseira verde inicia o atendimento em 15.5
Paciente 3 com pulseira verde termina o atendimento em 18.8
Paciente 4 com pulseira verde inicia o atendimento em 18.8
```
Percebemos que o paciente 5 chegou depois do 3 e do 4, mas iniciou seu atendimento assim que um médico terminou seu atendimento (exatamente aquele que atendia ao Paciente 1).
## Recursos que podem ser interrompidos: ```PreemptiveResource```
Considere, no exemplo anterior, que o paciente de pulseira vermelha tem uma prioridade tal que ele interrompe o atendimento atual do médico e imediatamente é atendido. A recursos com [preemptividade](https://pt.wikipedia.org/wiki/Preemptividade) são recursos que aceitam a interrupção da tarefa em execução para iniciar outra de maior prioridade. 

Um recurso capaz de ser interrompida é criado pelo comando:
```
medicos = simpy.PreemptiveResource(env, capacity=capacidade)
```
O cuidado aqui é que quando um recurso é requisitado por um processo de menor prioridade ele causa uma interrupção no Python, o que obriga a utilização de lógica do tipo ```try:...except```. O SimPy retornará uma interrupção do tipo simpy.Interrupt, como mostrado no exemplo a seguir (note a lógica de try...except dentro da função atendimento):

```python
import simpy
import random

def sorteiaPulseira():
    #retorna a cor da pulseira e sua prioridade
    r = random.random()
    if r <= .70:
        return "pulseira verde", 3
    elif r <= .90:
        return "pulseira amarela", 2
    return "pulseira vermelha", 1
    
def chegadaPacientes(env, medicos):
    #gera pacientes exponencialmente distribuídos
    #sortei a pulseira
    #inicia processo de atendimento
    i = 0
    while True:
        yield env.timeout(random.expovariate(1/5))
        i += 1
        pulseira, prio = sorteiaPulseira()
        print("Paciente %s chega em %.1f com %s" %(i, env.now, pulseira))
        env.process(atendimento(env, "Paciente %s" % i, pulseira, prio, medicos))

def atendimento(env, paciente, pulseira, prio, medicos):
    #ocupa um médico e realiza o atendimento do paciente
    with medicos.request(priority=prio) as req:
        yield req
        print("%s com %s inicia o atendimento em %.1f" %(paciente, pulseira, env.now))
        try:
            yield env.timeout(random.expovariate(1/9))
            print("%s com %s termina o atendimento em %.1f" %(paciente, pulseira, env.now))
        except simpy.Interrupt:
            #caso o simpy receba uma interrupção execute:
            print("%s com %s foi interrompido por paciente de maior prioridade em %.1f" %(paciente, pulseira, env.now))

random.seed(100)       
env = simpy.Environment()
medicos = simpy.PreemptiveResource(env, capacity=2) # cria os médicos
chegadas = env.process(chegadaPacientes(env, medicos))
env.run(until=20)
```

Como resultado, o programa retorna a seguinte saída:

```
Paciente 1 chega em 0.8 com pulseira verde
Paciente 1 com pulseira verde inicia o atendimento em 0.8
Paciente 2 chega em 8.2 com pulseira amarela
Paciente 2 com pulseira amarela inicia o atendimento em 8.2
Paciente 3 chega em 11.0 com pulseira verde
Paciente 4 chega em 11.4 com pulseira verde
Paciente 5 chega em 11.7 com pulseira vermelha
Paciente 1 com pulseira verde foi interrompido por paciente de maior prioridade em 11.7
Paciente 5 com pulseira vermelha inicia o atendimento em 11.7
Paciente 5 com pulseira vermelha termina o atendimento em 15.3
Paciente 3 com pulseira verde inicia o atendimento em 15.3
Paciente 3 com pulseira verde termina o atendimento em 18.7
Paciente 4 com pulseira verde inicia o atendimento em 18.7
```

Note como agora o Paciente 5 interrompe o atendimento do Paciente 1, como desejado. 

Contudo, a implementação anterior está cheia de limitações: pacientes com pulseira amarela não deveriam interromper o atendimento, mas na implementação proposta eles devem interromper o atendimento de pacientes de pulseira verde. Para este caso, o request possui um argumento que liga ou desliga a opção de preemptividade:
```
with medicos.request(priority=prio, preempt=preempt) as req:
```
O argumento ```preempt``` do ```request``` pode assumir o valor ```True``` ou ```False```, ligando ou desligando a preemptividade.

O programa alterado para interromper apenas no caso de pulseiras vermelhas, ficaria:

```python
import simpy
import random

def sorteiaPulseira():
    #retorna a cor da pulseira e sua prioridade
    r = random.random()
    if r <= .70:
        return "pulseira verde", 3, False
    elif r <= .90:
        return "pulseira amarela", 2, False
    return "pulseira vermelha", 1, True
    
def chegadaPacientes(env, medicos):
    #gera pacientes exponencialmente distribuídos
    #sorteia a pulseira
    #inicia processo de atendimento
    i = 0
    while True:
        yield env.timeout(random.expovariate(1/5))
        i += 1
        pulseira, prio, preempt = sorteiaPulseira()
        print("Paciente %s chega em %.1f com %s" %(i, env.now, pulseira))
        env.process(atendimento(env, "Paciente %s" % i, pulseira, prio, preempt, medicos))

def atendimento(env, paciente, pulseira, prio, preempt, medicos):
    #ocupa um médico e realiza o atendimento do paciente
    with medicos.request(priority=prio, preempt=preempt) as req:
        yield req
        print("%s com %s inicia o atendimento em %.1f" %(paciente, pulseira, env.now))
        try:
            yield env.timeout(random.expovariate(1/9))
            print("%s com %s termina o atendimento em %.1f" %(paciente, pulseira, env.now))
        except simpy.Interrupt:
            print("%s com %s foi interrompido por paciente de maior prioridade em %.1f" %(paciente, pulseira, env.now))

random.seed(100)       
env = simpy.Environment()
medicos = simpy.PreemptiveResource(env, capacity=2) # cria os médicos
chegadas = env.process(chegadaPacientes(env, medicos))
env.run(until=20)
```
## Conteúdos desta seção
| **Conteúdo** | **Descrição** |
| -- | -- |
| ```meuRecurso = simpy.PriorityResource(env, capacity=1)``` | cria um recurso em ```env``` com prioridade de atendimento e capacidade = 1 |
|``` meuRequest = meuRecurso.request(env, priority=prio)``` | solicita o recurso meuRecurso (note que ele ainda não ocupa o recurso) respeitando a ordem de prioridade primeiro e a regra FIFO a seguir |
| ```meuRecursoPreempt = simpy.PreemptiveResource(env, capacity=1)``` | cria um recurso em ```env``` que pode ser interrompido por entidades de prioridade maior|
|``` meuRequest = meuRecursoPreempt.request(env, priority=prio, preempt=preempt)``` | solicita o recurso meuRecurso (note que ele ainda não ocupa o recurso) respeitando a ordem de prioridade primeiro e a regra FIFO a seguir. Caso preempt seja False o o recurso não é interrompido |
| ```try:...except simpy.Interrupt:``` | chamada de interrupção utilizada na lógica try:...except: |

##Desafios

> **Desafio 11**: acrescente ao último programa proposto o cálculo do tempo de atendimento decorrido para o paciente que foi interrompido por outro e imprima o resultado na tela.


> **Desafio 12**: quando um paciente é interrompido, ele deseja retornar ao antedimento de onde parou. Altere o programa para que um paciente de pulseira verde interrompido possa retornar para ser atendido no tempo restante do seu atendimento. Dica: altere a númeração de prioridades de modo que um paciente verde interrompido tenha prioridade superior ao de um paciente verde que acabou de chegar.

