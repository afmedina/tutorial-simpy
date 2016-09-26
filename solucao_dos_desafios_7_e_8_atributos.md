# Solução dos desafios 7 e 8

**Desafio 7**: retome o problema da lavanderia \(Desafio 6\). Estime o tempo médio que os clientes atendidos aguardaram pela lavadora.

Dica: você precisará de uma variável global para o cálculo do tempo de espera e um atributo para marcar a hora de chegada do cliente na lavadora.

```python
import random
import simpy

tempoEsperaLavadora = 0 # conta tempo de espera total por lavadora
contaLavadora = 0 # conta clientes que entraram na lavadora
contaClientes = 0 # conta clientes que chegaram no sistema

def distributions(tipo):
    #função que armazena as distribuições utilizadas no modelo
    return {
        'chegadas': random.expovariate(1.0/5.0),
        'lavar': 20,
        'carregar': random.uniform(1, 4),
        'descarregar': random.uniform(1, 2),
        'secar': random.uniform(9, 12),
    }.get(tipo, 0.0)

def chegadaClientes(env, lavadoras, cestos, secadoras):
    #função que gera a chegada de clientes
    global contaClientes
    contaClientes = 0
    while True:
        contaClientes += 1
        yield env.timeout(distributions('chegadas'))
        print("Cliente %s chega em %.1f" %(contaClientes, env.now))
        env.process(lavaSeca(env, "Cliente %s" %contaClientes, lavadoras, cestos, secadoras))

def lavaSeca(env, cliente, lavadoras, cestos, secadoras):
    #função que processa a operação de cada cliente dentro da lavanderia
    global utilLavadora, tempoEsperaLavadora, contaLavadora

    #marca chegada no sistema
    chegada = env.now

    #ocupa a lavadora
    req1 = lavadoras.request()
    yield req1
    print("%s ocupa lavadora em %.1f" %(cliente, env.now))

    # marca o tempo de espera em fila por lavadora e totaliza
    tempoEspera = env.now - chegada
    tempoEsperaLavadora += tempoEspera

    yield env.timeout(distributions('lavar'))
    contaLavadora += 1

    #antes de retirar da lavadora, pega um cesto
    req2 = cestos.request()
    yield req2
    print("%s ocupa cesto em %.1f" %(cliente, env.now))
    yield env.timeout(distributions('carregar'))

    #libera a lavadora, mas não o cesto
    lavadoras.release(req1)
    print("%s desocupa lavadora em %.1f" %(cliente, env.now))

    #ocupa a secadora antes de liberar o cesto
    req3 = secadoras.request()
    yield req3
    print("%s ocupa secadora em %.1f" %(cliente, env.now))
    yield env.timeout(distributions('descarregar'))

    #libera o cesto mas não a secadora
    cestos.release(req2)
    print("%s desocupa cesto em %.1f" %(cliente, env.now))
    yield env.timeout(distributions('secar'))

    #pode liberar a secadora
    print("%s desocupa secadora em %.1f" %(cliente, env.now))
    secadoras.release(req3)



random.seed(10)
env = simpy.Environment()
lavadoras = simpy.Resource(env, capacity = 3)
cestos = simpy.Resource(env, capacity = 20)
secadoras = simpy.Resource(env, capacity = 10)
env.process(chegadaClientes(env, lavadoras, cestos, secadoras))

env.run(until = 600)             

print("Espera por lavadoras: %.2f Clientes atendidos: %i" %(tempoEsperaLavadora/contaLavadora, contaLavadora))
```

**Desafior 8**: no desafio anterior, você deve ter notado como o tempo de espera pela lavadora está muito alto. Para identificar o gargalo do sistema, acrescente a impressão do número de clientes que ficaram em fila ao final da simulação. Você consegue otimizar o sistema a partir do modelo contruído?

Para a solução do desafio, basta acrescetar uma linha ao final do programa principal:

```python
random.seed(10)
env = simpy.Environment()
lavadoras = simpy.Resource(env, capacity = 3)
cestos = simpy.Resource(env, capacity = 20)
secadoras = simpy.Resource(env, capacity = 10)
env.process(chegadaClientes(env, lavadoras, cestos, secadoras))

env.run(until = 60000)

print("Espera por lavadoras: %.2f Clientes atendidos: %i" %(tempoEsperaLavadora/contaLavadora, contaLavadora))
print("Fila de clientes ao final da simulação: lavadoras %.2f   cestos %.2f secadoras %.2f" %(len(lavadoras.queue), len(cestos.queue), len(secadoras.queue)))`
```
Quando simulado por 60.000 minutos, o resultado fornece 3.929 clientes esperando por lavadoras. Temos aí um caso clássico de fila infinita, isto é: a taxa de atendimento das lavadoras é menor que a taxa de chegada de clientes. Assim, se 1 cliente ocupa em média 20 minutos na lavadora,  a taxa de adendimento em cada lavadora é de $$\mu=$$ 0.05 clientes/min (=1 cliente /20 min), enquanto a taxa de chegadas de clientes na lavandeira é de $$\lambda=$$0.20 clientes/min (= 1 cliente/5 min). Assim, para termos um sistema equilibrado, precisaríamos de um número de lavadoras de modo a garantir que a taxa de atendimento da soma das lavadoras seja maior que a taxa de chegadas de clientes no sistema ou:

$$\rho=\frac{\lambda}{n*\mu} < 1 \to n > \frac{\lambda}{\mu} = \frac{0.20}{0.05}=4$$

Assim, precisamos de 5 (ou mais) lavadoras **apenas para eliminar o gargalo na lavagem**. Simulando o sistema com 5 lavadoras, temos:
```python
Espera por lavadoras: 10223.25 Clientes atendidos: 7995
Fila de clientes ao final da simulação: lavadoras 3929.00   cestos 0.00 secadoras 0.00
```


