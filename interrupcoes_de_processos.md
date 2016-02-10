# Interrupções de recursos: ```PreemptiveResource```

Você está todo feliz e contente atravessando a galáxia no seu X-Wing quando... PIMBA! Seu [dróide astromecânico](https://pt.wikipedia.org/wiki/R2-D2) pifou e você deve interromper a viagem para consertá-lo.

Nesta seção iremos interromper processos já em execução, liberando eventuais recursos em utilização para algum processo já iniciado. A aplicação mais óbvia é para a quebra de equipamentos durante a operação, como no caso do R2D2.

A interrupção de um processo em SimPy é realizada por meio de recursos com [preemptividade](https://pt.wikipedia.org/wiki/Preemptividade) (capacidade de interromper outra tarefa em execução). Basicamente, a cada processo é atribuída uma prioridade definida por um número inteiro, tal que quanto menor seu valor, maior a prioridade do processo. Assim, o SimPy permite que um processo de maior prioridade interrompa outro de menor prioridade.

O recurso com preemptividade é definido pelo comando:

```res = simpy.PreemptiveResource(env, capacity=1)```

E no momento do request, devemos lançar o valor da prioridade daquele processo:

```yield resource.request(priority=prioridade)```

O cuidado aqui é que quando um recurso é requisitado por um processo de menor prioridade ele causa uma interrupção no Python, o que obriga a utilização de lógica do timpo ```try:...except```.

No exemplo a seguir, temos três processos com prioridades 2, 1, 0 que disputam um mesmo recurso. O recurso de prioridade 0 e gerado por último, mas fura a fila e causa uma interrupção no processo.

```python
import simpy

def geraProcessos(env, res):
    env.process(ocupaRecurso(env, "Estudar", res, 2))
    yield env.timeout(1)
    env.process(ocupaRecurso(env, "Procastinar", res, 1))
    yield env.timeout(1)
    env.process(ocupaRecurso(env, "Janta está na mesa", res, 0))
    
def ocupaRecurso(env, processo, resource, prioridade):
    with resource.request(priority=prioridade) as req:
        print('%s fez request em %s com prioridade %s' % (processo, env.now, prioridade))
        yield req
        print('%s ocupou o recurso estudante em %s' % (processo, env.now))
        try:
            inicioProcesso = env.now
            yield env.timeout(3)
        except simpy.Interrupt:
            tempoOperando = env.now - inicioProcesso
            print('%s foi interrompido em %s após %s' %(processo, env.now, tempoOperando))

    
env = simpy.Environment()
res = simpy.PreemptiveResource(env, capacity=1)
env.process(geraProcessos(env, res))
env.run()```

## Criando quebras de equipamento

A utilização mais interessante do recurso de preemptividade são nos sistemas que envolvem quebras de equipamento para manutenção. Voltando ao exemplo do X-wing, considere que a cada 10 horas o R2D2, interrompe a viagem para uma manutenção de 1 hora e que a viagem toda levaria (sem as paralizações) 50 horas.

Inicialmetne, devemos criar uma função que representa a viagem:

