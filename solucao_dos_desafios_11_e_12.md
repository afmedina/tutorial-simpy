# Solução dos desafios 11 e 12

> **Desafio 11**: acrescente ao último programa proposto o cálculo do tempo de atendimento decorrido para o paciente que foi interrompido por outro e imprima o resultado na tela.

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
        inicioAtendimento = env.now
        try:
            tempoAtendimento = random.expovariate(1/9) # sorteia o tempo de atendimento
            yield env.timeout(tempoAtendimento)
            print("%s com %s termina o atendimento em %.1f" %(paciente, pulseira, env.now))
        except simpy.Interrupt:
            tempoAtendimento -= env.now-inicioAtendimento #recalcula o tempo de atendimento
            print("%s com %s foi interrompido por paciente de maior prioridade em %.1f" %(paciente, pulseira, env.now))
            print("%s ainda precisa de %.1f minutos de atendimento" %(paciente, tempoAtendimento))

random.seed(100)       
env = simpy.Environment()
medicos = simpy.PreemptiveResource(env, capacity=2) # cria os médicos
chegadas = env.process(chegadaPacientes(env, medicos))
env.run(until=20)    
 ``` 

> **Desafio 12**: quando um paciente é interrompido, ele deseja retornar ao antedimento de onde parou. Altere o programa para que um paciente de pulseira verde interrompido possa retornar para ser atendido no tempo restante do seu atendimento. Dica: altere a númeração de prioridades de modo que um paciente verde interrompido tenha prioridade superior ao de um paciente verde que acabou de chegar.

```python 
import simpy
import random

def sorteiaPulseira():
    #retorna a cor da pulseira e sua prioridade
    r = random.random()
    if r <= .70:
        return "pulseira verde", 30, False
    elif r <= .90:
        return "pulseira amarela", 20, False
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
        inicioAtendimento = env.now
        try:
            tempoAtendimento = random.expovariate(1/9) # sorteia o tempo de atendimento
            yield env.timeout(tempoAtendimento)
            print("%s com %s termina o atendimento em %.1f" %(paciente, pulseira, env.now))
        except simpy.Interrupt:
            tempoAtendimento -= env.now-inicioAtendimento #recalcula o tempo de atendimento
            print("%s com %s foi interrompido por paciente de maior prioridade em %.1f" %(paciente, pulseira, env.now))
            print("%s ainda precisa de %.1f minutos de atendimento" %(paciente, tempoAtendimento))
            prio -= 1 #aumenta a prioridade
            env.process(atendimento(env, paciente, pulseira, prio, preempt, medicos))

random.seed(100)       
env = simpy.Environment()
medicos = simpy.PreemptiveResource(env, capacity=2) # cria os médicos
chegadas = env.process(chegadaPacientes(env, medicos))
env.run(until=20)
``` 