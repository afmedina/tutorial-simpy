# Solução dos desafios 11 e 12

> **Desafio 11**: acrescente ao último programa proposto o cálculo do tempo de atendimento que ainda falta para o paciente que foi interrompido por outro e imprima o resultado na tela.

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
            print("%4.1f %s com %s termina o atendimento" 
                %(env.now, paciente, pulseira))
        except simpy.Interrupt:
            # recalcula o tempo de atendimento
            tempoAtendimento -= env.now-inicioAtendimento 
            print("%4.1f %s com %s tem atendimento interrompido" 
                    %(env.now, paciente, pulseira))
            print("%4.1f %s ainda precisa de %4.1f min de atendimento" 
                    %(env.now, paciente, tempoAtendimento))
```

Quando o modelo é executado por apenas 20 minutos, com a alteração apresentada da função `atendimento,` temos como saída:

```python
 0.8 Paciente  1 com pulseira verde chega
 0.8 Paciente  1 com pulseira verde inicia o atendimento
 8.2 Paciente  2 com pulseira amarela chega
 8.2 Paciente  2 com pulseira amarela inicia o atendimento
11.0 Paciente  3 com pulseira verde chega
11.4 Paciente  4 com pulseira verde chega
11.7 Paciente  5 com pulseira vermelha chega
11.7 Paciente  1 com pulseira verde tem atendimento interrompido
11.7 Paciente  1 ainda precisa de  0.1 min de atendimento
11.7 Paciente  5 com pulseira vermelha inicia o atendimento
15.3 Paciente  5 com pulseira vermelha termina o atendimento
15.3 Paciente  3 com pulseira verde inicia o atendimento
18.7 Paciente  3 com pulseira verde termina o atendimento
18.7 Paciente  4 com pulseira verde inicia o atendimento
```

> **Desafio 12**: quando um paciente é interrompido, ele deseja retornar ao atendimento de onde parou. Altere o programa para que um paciente de pulseira verde interrompido possa retornar para ser atendido no tempo restante do seu atendimento. Dica: altere a numeração de prioridades de modo que um paciente verde interrompido tenha prioridade superior ao de um paciente verde que acabou de chegar.

Novamente, as alterações no modelo anterior resumem-se à função `atendimento`: precisamos aumentar a prioridade de um paciente interrompido em relação aos pacientes que acabam de chegar com a mesma pulseira, afinal, ele tem prioridade em relação a um paciente recém chegado de gravidade equivalente. Além disso, tal paciente, deve ser atendido pelo tempo _restante_ de atendimento, de modo que a função deve receber como parâmetro esse tempo.

O artifício utilizado neste segundo caso foi acrescentar um parâmetro opcional à função, `tempoAtendimento`, de modo que se ele não é fornecido \(caso de um paciente novo\), a função sorteia um tempo exponecialmente distribuído, com média de 9 minutos. De outro modo, se o parâmetro é fornecido, isso significa que ele é um parceiro interrompido e, portanto, já tem um tempo restante de atendimento calculado.

O código a seguir, representa uma possível solução para a _nova_ função `atendimento`do desafio:

```python
def atendimento(env, paciente, pulseira, prio, preempt, medicos, tempoAtendimento=None):
    # ocupa um médico e realiza o atendimento do paciente

    with medicos.request(priority=prio, preempt=preempt) as req:
        yield req
        inicioAtendimento = env.now
        print("%4.1f %s com %s inicia o atendimento" %(env.now, paciente, pulseira))
        try:
            # sorteia o tempo de atendimento
            if not tempoAtendimento:
                tempoAtendimento = random.expovariate(1/9) 
            yield env.timeout(tempoAtendimento)
            print("%4.1f %s com %s termina o atendimento" 
                    %(env.now, paciente, pulseira))
        except simpy.Interrupt:
            # recalcula o tempo de atendimento
            tempoAtendimento -= env.now-inicioAtendimento 
            print("%4.1f %s com %s tem atendimento interrompido" 
                    %(env.now, paciente, pulseira))
            print("%4.1f %s ainda precisa de %4.1f min de atendimento"
            %(env.now, paciente, tempoAtendimento))

            # aumenta a prioridade reduzindo o valor 
            prio -= 0.01
            env.process(atendimento(env, paciente, pulseira, prio, preempt, medicos, tempoAtendimento)) 

random.seed(100)       
env = simpy.Environment()
# cria os médicos
medicos = simpy.PreemptiveResource(env, capacity=2)
chegadas = env.process(chegadaPacientes(env, medicos))

env.run(until=20)
```

Quando executado por apenas 20 minutos, o modelo completo - acrescido da nova função `atendimento`, fornece como saída:

```python
 0.8 Paciente  1 com pulseira verde chega
 0.8 Paciente  1 com pulseira verde inicia o atendimento
 8.2 Paciente  2 com pulseira amarela chega
 8.2 Paciente  2 com pulseira amarela inicia o atendimento
11.0 Paciente  3 com pulseira verde chega
11.4 Paciente  4 com pulseira verde chega
11.7 Paciente  5 com pulseira vermelha chega
11.7 Paciente  1 com pulseira verde tem atendimento interrompido
11.7 Paciente  1 ainda precisa de  0.1 min de atendimento
11.7 Paciente  5 com pulseira vermelha inicia o atendimento
15.3 Paciente  5 com pulseira vermelha termina o atendimento
15.3 Paciente  1 com pulseira verde inicia o atendimento
15.5 Paciente  1 com pulseira verde termina o atendimento
15.5 Paciente  3 com pulseira verde inicia o atendimento
18.8 Paciente  3 com pulseira verde termina o atendimento
18.8 Paciente  4 com pulseira verde inicia o atendimento
```

Note que agora, o Paciente 1, diferentemente do que ocorre na saída do desafio 11, é atendido antes do Paciente 3, representando o fato de que, mesmo interrompido, ele voltou para o início da fila.

