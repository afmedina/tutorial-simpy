# Outros tipos de recursos: com prioridade e preemptivos

Além do recurso como definido nas seções anteriores, o SimPy possui dois tipos específicos de recursos: com prioridade e "peemptivos".

## Recursos com prioridade: `PriorityResource`

Um recurso pode ter uma fila de entidades desejando ocupá-lo para executar determinado processo. Existindo a fila, o recurso será ocupado respeitando a ordem de chegada das entidades \(ou a regra FIFO\).

Contudo, existem situações em que algumas entidades possuem _prioridades_ sobre as outras, de modo que elas desrespeitam a regra do primeiro a chegar é o primeiro a ser atendido.

Por exemplo, considere um consultório de pronto atendimento de um hospital em que 70% do pacientes são de prioridade baixa \(pulseira verde\), 20% de prioridade intermediária \(pulseira amarela\) e 10% de prioridade alta \(pulseira vermelha\). Existem 2 médicos que realizam o atendimento e que sempre verificam inicialmente a ordem de prioridade dos pacientes na fila. Os pacientes chegam entre si em intervalos exponencialmente distribuídos, com média de 5 minutos e o atendimento é também exponencialmente distribuído, com média de 9 minutos por paciente.

No exemplo, os médicos são recursos, mas também respeitam uma regra específica de prioridade. Um médico ou recurso deste tipo, é criado pelo comando:

```python
medicos = simpy.PriorityResource(env, capacity=capacidade_desejada)
```

Para a solução do exemplo, o modelo aqui proposto terá 3 funções: uma para sorteio do tipo de pulseira, uma para geração de chegadas de pacientes e outra para atendimento dos pacientes.

Como uma máscara inicial do modelo, teríamos:

```python
import simpy
import random

def sorteiaPulseira():
    # retorna a cor da pulseira e sua prioridade
    pass

def chegadaPacientes(env, medicos):
    # gera pacientes exponencialmente distribuídos
    # sorteia a pulseira
    # inicia processo de atendimento
    pass

def atendimento(env, paciente, pulseira, prio, medicos):
    # ocupa um médico e realiza o atendimento do paciente
    pass

random.seed(100)       
env = simpy.Environment()
medicos = simpy.PriorityResource(env, capacity=2) # cria os 2 médicos
chegadas = env.process(chegadaPacientes(env, medicos))

env.run(until=20)
```

O preenchimento da máscara pode ser feito de diversas maneiras, um possibilidade seria:

```python
import simpy
import random

def sorteiaPulseira():
    # retorna a cor da pulseira e sua prioridade
    r = random.random()                 # sorteia número aleatório ente 0 e 1
    if r <= .70:                        # 70% é pulseira verde
        return "pulseira verde", 3
    elif r <= .90:                      # 20% (=90-70) é pulseira amarela
        return "pulseira amarela", 2
    return "pulseira vermelha", 1       # 10% (=100-90) é pulseira vermelha

def chegadaPacientes(env, medicos):
    #gera pacientes exponencialmente distribuídos

    i = 0
    while True:
        yield env.timeout(random.expovariate(1/5))
        i += 1

        # sorteia a pulseira
        pulseira, prio = sorteiaPulseira()
        print("%4.1f Paciente %2i com %s chega" %(env.now, i, pulseira))

        # inicia processo de atendimento
        env.process(atendimento(env, "Paciente %2i" %i, pulseira, prio, medicos))

def atendimento(env, paciente, pulseira, prio, medicos):
    # ocupa um médico e realiza o atendimento do paciente

    with medicos.request(priority=prio) as req:
        yield req
        print("%4.1f %s com %s inicia o atendimento" %(env.now, paciente, pulseira))
        yield env.timeout(random.expovariate(1/9))
        print("%4.1f %s com %s termina o atendimento" %(env.now, paciente, pulseira))

random.seed(100)       
env = simpy.Environment()
# cria os médicos
medicos = simpy.PriorityResource(env, capacity=2) 
chegadas = env.process(chegadaPacientes(env, medicos))

env.run(until=20)
```

O importante a ser destacado é que a prioridade é informada ao `request` do recurso `medicos` pelo argumento `priority:`

```python
with medicos.request(priority=prio) as req:
    yield req
```

Para o SimPy, **quando menor o valor fornecido** para o parâmetro `priority,` **maior a prioridade** daquela entidade na fila. Assim, a função `sorteiaPulseira` retorna 3 para a pulseira verde \(de menor prioridade\) e 1 para a vermelha \(de maior prioridade\).

Quando o modelo anterior é executado, fornece como saída:

```python
 0.8 Paciente  1 com pulseira verde chega
 0.8 Paciente  1 com pulseira verde inicia o atendimento
 8.2 Paciente  2 com pulseira amarela chega
 8.2 Paciente  2 com pulseira amarela inicia o atendimento
11.0 Paciente  3 com pulseira verde chega
11.4 Paciente  4 com pulseira verde chega
11.7 Paciente  5 com pulseira vermelha chega
11.8 Paciente  1 com pulseira verde termina o atendimento
11.8 Paciente  5 com pulseira vermelha inicia o atendimento
15.5 Paciente  5 com pulseira vermelha termina o atendimento
15.5 Paciente  3 com pulseira verde inicia o atendimento
18.8 Paciente  3 com pulseira verde termina o atendimento
18.8 Paciente  4 com pulseira verde inicia o atendimento
```

Percebemos que o paciente 5 chegou no instante 11,7 minutos, depois do pacientes 3 e 4, mas iniciou seu atendimento assim que um médico ficou livre no instante 11,8 minutos \(exatamente aquele que atendia ao Paciente 1\).

## Recursos que podem ser interrompidos: `PreemptiveResource`

Considere, no exemplo anterior, que o paciente de pulseira vermelha tem uma prioridade tal que ele interrompe o atendimento atual do médico e imediatamente é atendido. Os recursos com [preemptividade](https://pt.wikipedia.org/wiki/Preemptividade) são recursos que aceitam a interrupção da tarefa em execução para iniciar outra de maior prioridade.

Um recurso capaz de ser interrompido é criado pelo comando:

```python
medicos = simpy.PreemptiveResource(env, capacity=capacidade)
```

Assim, o modelo anterior precisa ser modificado de modo a criar os médicos corretamente:

```python
random.seed(100)       
env = simpy.Environment()
# cria os médicos
medicos = simpy.PreemptiveResource(env, capacity=2)
chegadas = env.process(chegadaPacientes(env, medicos))

env.run(until=20)
```

Agora, devemos modificar a função `atendimento`para garantir que quando um recurso for requisitado por um processo de menor prioridade, ele causará uma interrupção no Python, o que obriga a utilização de bloco de controle de interrupção `try:...except`.

Quando um recurso deve ser interrompido, o SimPy retorna um interrupção do tipo `simpy.Interrupt,`como mostrado no código a seguir \(noteo bloco `try...except` dentro da função atendimento\):

```python
def atendimento(env, paciente, pulseira, prio, medicos):
    # ocupa um médico e realiza o atendimento do paciente

    with medicos.request(priority=prio) as req:
        yield req
        print("%4.1f %s com %s inicia o atendimento" %(env.now, paciente, pulseira))
        try:
            yield env.timeout(random.expovariate(1/9))
            print("%4.1f %s com %s termina o atendimento" %(env.now, paciente, pulseira))
        except:
            print("%4.1f %s com %s tem atendimento interrompido" %(env.now, paciente, pulseira))

random.seed(100)       
env = simpy.Environment()
# cria os médicos
medicos = simpy.PreemptiveResource(env, capacity=2)
chegadas = env.process(chegadaPacientes(env, medicos))

env.run(until=20)
```

Quando simulado por apenas 20 minutos, o modelo acrescido das correções apresentadas fornece a seguinte saída:

```python
 0.8 Paciente  1 com pulseira verde chega
 0.8 Paciente  1 com pulseira verde inicia o atendimento
 8.2 Paciente  2 com pulseira amarela chega
 8.2 Paciente  2 com pulseira amarela inicia o atendimento
11.0 Paciente  3 com pulseira verde chega
11.4 Paciente  4 com pulseira verde chega
11.7 Paciente  5 com pulseira vermelha chega
11.7 Paciente  1 com pulseira verde tem atendimento interrompido
11.7 Paciente  5 com pulseira vermelha inicia o atendimento
15.3 Paciente  5 com pulseira vermelha termina o atendimento
15.3 Paciente  3 com pulseira verde inicia o atendimento
18.7 Paciente  3 com pulseira verde termina o atendimento
18.7 Paciente  4 com pulseira verde inicia o atendimento
```

Note que o Paciente 5 interrompe o atendimento do Paciente 1, como desejado.

Contudo, a implementação anterior está cheia de limitações: pacientes com pulseira amarela não deveriam interromper o atendimento, mas na implementação proposta eles devem interromper o atendimento de pacientes de pulseira verde. Para estas situações, o `request`possui um argumento `preempt` que permite ligar ou desligar a opção de preemptividade:

```python
with medicos.request(priority=prio, preempt=preempt) as req:
    yield req
```

O modelo alterado para interromper apenas no caso de pulseiras vermelhas, ficaria \(note que o argumento `preempt` é agora fornecido diretamente a partir da função `sorteiaPulseira):`

```python
import simpy
import random

def sorteiaPulseira():
    # retorna a cor da pulseira e sua prioridade
    r = random.random() # sorteia número aleatório ente 0 e 1
    if r <= .70: # 70% é pulseira verde
        return "pulseira verde", 3, False
    elif r <= .90: # 20% (=90-70) é pulseira amarela
        return "pulseira amarela", 2, False
    return "pulseira vermelha", 1, True # 10% (=100-90) é pulseira vermelha

def chegadaPacientes(env, medicos):
    #gera pacientes exponencialmente distribuídos

    i = 0
    while True:
        yield env.timeout(random.expovariate(1/5))
        i += 1

        # sorteia a pulseira
        pulseira, prio, preempt = sorteiaPulseira()
        print("%4.1f Paciente %2i com %s chega" %(env.now, i, pulseira))

        # inicia processo de atendimento
        env.process(atendimento(env, "Paciente %2i" %i, pulseira, prio, preempt, medicos))

def atendimento(env, paciente, pulseira, prio, preempt, medicos):
    # ocupa um médico e realiza o atendimento do paciente

    with medicos.request(priority=prio, preempt=preempt) as req:
        yield req
        print("%4.1f %s com %s inicia o atendimento" %(env.now, paciente, pulseira))
        try:
            yield env.timeout(random.expovariate(1/9))
            print("%4.1f %s com %s termina o atendimento" %(env.now, paciente, pulseira))
        except:
            print("%4.1f %s com %s tem atendimento interrompido" %(env.now, paciente, pulseira))

random.seed(100)       
env = simpy.Environment()
# cria os médicos
medicos = simpy.PreemptiveResource(env, capacity=2)
chegadas = env.process(chegadaPacientes(env, medicos))

env.run(until=20)
```

O modelo anterior, quando executado por apenas 20 minutos, fornece como saída:

```python
 0.8 Paciente  1 com pulseira verde chega
 0.8 Paciente  1 com pulseira verde inicia o atendimento
 8.2 Paciente  2 com pulseira amarela chega
 8.2 Paciente  2 com pulseira amarela inicia o atendimento
11.0 Paciente  3 com pulseira verde chega
11.4 Paciente  4 com pulseira verde chega
11.7 Paciente  5 com pulseira vermelha chega
11.7 Paciente  1 com pulseira verde tem atendimento interrompido
11.7 Paciente  5 com pulseira vermelha inicia o atendimento
15.3 Paciente  5 com pulseira vermelha termina o atendimento
15.3 Paciente  3 com pulseira verde inicia o atendimento
18.7 Paciente  3 com pulseira verde termina o atendimento
18.7 Paciente  4 com pulseira verde inicia o atendimento
```

## Conteúdos desta seção

| **Conteúdo** | **Descrição** |
| --- | --- |
| `meuRecurso = simpy.PriorityResource(env, capacity=1)` | Cria um recurso com prioridade e capacidade = 1 |
| `meuRequest = meuRecurso.request(env, priority=prio)` | Solicita o recurso meuRecurso \(note que ele ainda não ocupa o recurso\) respeitando a ordem de prioridade primeiro e a regra FIFO a seguir |
| `meuRecursoPreempt = simpy.PreemptiveResource(env, capacity=1)` | Cria um recurso em `env` que pode ser interrompido por entidades de prioridade maior |
| `meuRequest = meuRecursoPreempt.request(env, priority=prio, preempt=preempt)` | Solicita o recurso meuRecurso \(note que ele ainda não ocupa o recurso\) respeitando a ordem de prioridade primeiro e a regra FIFO a seguir. Caso preempt seja False o o recurso não é interrompido |
| `try:...except simpy.Interrupt:` | Chamada de interrupção utilizada na lógica try:...except: |

## Desafios

> **Desafio 11**: acrescente ao último programa proposto o cálculo do tempo de atendimento que ainda falta de atendimento para o paciente que foi interrompido por outro e imprima o resultado na tela.
>
> **Desafio 12**: quando um paciente é interrompido, ele deseja retornar ao atendimento de onde parou. Altere o programa para que um paciente de pulseira verde interrompido possa retornar para ser atendido no tempo restante do seu atendimento. Dica: altere a numeração de prioridades de modo que um paciente verde interrompido tenha prioridade superior ao de um paciente verde que acabou de chegar.



