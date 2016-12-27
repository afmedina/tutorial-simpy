# Solução dos desafios 11 e 12

> **Desafio 11**: acrescente ao último programa proposto o cálculo do tempo de atendimento que ainda falta de atendimento para o paciente que foi interrompido por outro e imprima o resultado na tela.

Neste caso, precisamos acrescentar o cálculo do tempo faltante para o paciente na função `atendimento:`
```python
def atendimento(env, paciente, pulseira, prio, preempt, medicos):
    # ocupa um médico e realiza o atendimento do paciente

    with medicos.request(priority=prio, preempt=preempt) as req:
        yield req
        inicioAtendimento = env.now
        print("%4.1f %s com %s inicia o atendimento" %(env.now, paciente, pulseira))
        try:
            # sorteia o tempo de atendimento
            tempoAtendimento = random.expovariate(1/9) 
            yield env.timeout(tempoAtendimento)
            print("%4.1f %s com %s termina o atendimento" %(env.now, paciente, pulseira))
        except simpy.Interrupt:
            # recalcula o tempo de atendimento
            tempoAtendimento -= env.now-inicioAtendimento 
            print("%4.1f %s com %s tem atendimento interrompido" %(env.now, paciente, pulseira))
            print("%4.1f %s ainda precisa de %4.1f min de atendimento" %(env.now, paciente, tempoAtendimento))
    
```

> **Desafio 12**: quando um paciente é interrompido, ele deseja retornar ao antedimento de onde parou. Altere o programa para que um paciente de pulseira verde interrompido possa retornar para ser atendido no tempo restante do seu atendimento. Dica: altere a númeração de prioridades de modo que um paciente verde interrompido tenha prioridade superior ao de um paciente verde que acabou de chegar.

```python
import simpy
import random

def sorteiaPulseira():
    # retorna a cor da pulseira e sua prioridade
    r = random.random()                      # sorteia número aleatório ente 0 e 1
    if r <= .70:                             # 70% é pulseira verde
        return "pulseira verde", 30, False
    elif r <= .90:                           # 20% (=90-70) é pulseira amarela
        return "pulseira amarela", 20, False
    return "pulseira vermelha", 1, True      # 10% (=100-90) é pulseira vermelha
    
def chegadaPacientes(env, medicos):
    # gera pacientes exponencialmente distribuídos
    
    i = 0
    while True:
        yield env.timeout(random.expovariate(1/5))
        i += 1
        
        # sorteia a pulseira
        pulseira, prio, preempt = sorteiaPulseira()
        print("Paciente %s chega em %.1f com %s" %(i, env.now, pulseira))
        
        # inicia processo de atendimento
        env.process(atendimento(env, "Paciente %s" % i, pulseira, prio, preempt, medicos))

def atendimento(env, paciente, pulseira, prio, preempt, medicos):
    # ocupa um médico e realiza o atendimento do paciente

    with medicos.request(priority=prio, preempt=preempt) as req:
        yield req
        print("%s com %s inicia o atendimento em %.1f" %(paciente, pulseira, env.now))
        inicioAtendimento = env.now
        try: 
            # priocesso normal, sorteia o tempo de atendimento
            tempoAtendimento = random.expovariate(1/9) 
            yield env.timeout(tempoAtendimento)
            print("%s com %s termina o atendimento em %.1f" %(paciente, pulseira, env.now))
        except simpy.Interrupt:
            # houve interrupção, recalcula o tempo de atendimento
            tempoAtendimento -= env.now-inicioAtendimento 
            print("%s com %s foi interrompido por paciente de maior prioridade em %.1f" %(paciente, pulseira, env.now))
            print("%s ainda precisa de %.1f minutos de atendimento" %(paciente, tempoAtendimento))
            
            # aumenta a prioridade            
            prio -= 1 
            env.process(atendimento(env, paciente, pulseira, prio, preempt, medicos))

random.seed(100)       
env = simpy.Environment()
medicos = simpy.PreemptiveResource(env, capacity=2) # cria os médicos
chegadas = env.process(chegadaPacientes(env, medicos))
env.run(until=20)
```

