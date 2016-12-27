# Solução dos desafios 7 e 8

>**Desafio 7**: retome o problema da lavanderia \(Desafio 6\). Estime o tempo médio que os clientes atendidos aguardaram pela lavadora.

>Dica: você precisará de uma variável global para o cálculo do tempo de espera e um atributo para marcar a hora de chegada do cliente na lavadora.

O tempo médio de espera por fila de um recurso - no caso lavadoras - é estimado pelo soma do tempo que todos os clientes aguardaram pelo recurso, dividido pelo número de clientes que ocuparam o recurso ao longo da simulação.

Assim, vamos criar duas variáveis globais para armazenar a soma do tempo de espera por lavadora de todos os clientes que ocuparam as lavadoras, bem como o número de clientes que ocuparam as mesmas lavadoras:

```python
import random
import simpy

contaClientes = 0           # conta clientes que chegaram no sistema
tempoEsperaLavadora = 0     # conta tempo de espera total por lavadora
contaLavadora = 0           # conta clientes que ocuparam uma lavadora
```
A seguir, precisamos alterar a função `lavaSeca` para calcular corretamente o tempo de espera por lavadora de cada cliente, somar este valor à variável global `tempoEsperaLavadora` e incrementar o número de clientes que ocuparam lavadoras na variável global `contaLavadora` (representação apenas da parte do código que é alterada):
```python
def lavaSeca(env, cliente, lavadoras, cestos, secadoras):
    # função que processa a operação de cada cliente dentro da lavanderia
    global tempoEsperaLavadora, contaLavadora
    
    # marca atributo chegada com o tempo atual de chegada da entidade
    chegada = env.now
    # ocupa a lavadora
    req1 = lavadoras.request()
    yield req1
    # incrementa lavadoras ocupadas
    contaLavadora += 1
    # calcula o tempo de espera em fila por lavadora
    tempoFilaLavadora = env.now - chegada
    tempoEsperaLavadora += tempoFilaLavadora
    print("%4.1f %s ocupa lavadora" %(env.now, cliente))
    yield env.timeout(distributions('lavar'))
```
Ao final do programa, basta acrescentar uma linha para imprimir o tempo médio em fila de espera por lavadoras e o número de vezes que uma lavadora foi ocupada ao longo da simulação:
```python
random.seed(10)
env = simpy.Environment()
lavadoras = simpy.Resource(env, capacity=3)
cestos = simpy.Resource(env, capacity=2)
secadoras = simpy.Resource(env, capacity=1)
env.process(chegadaClientes(env, lavadoras, cestos, secadoras))

env.run(until=40)
print("\nEspera por lavadoras: %.2f Clientes atendidos: %i" 
        %(tempoEsperaLavadora/contaLavadora, contaLavadora))
```
Quando executado por 40 minutos, o modelo completo com as alterações anteriores fornece como saída:
```python
 4.2 Chegada do cliente 1
 4.2 Cliente 1 ocupa lavadora
12.6 Chegada do cliente 2
12.6 Cliente 2 ocupa lavadora
24.2 Cliente 1 ocupa cesto
27.2 Cliente 1 desocupa lavadora
27.2 Cliente 1 ocupa secadora
28.8 Cliente 1 desocupa cesto
32.6 Cliente 2 ocupa cesto
36.3 Cliente 2 desocupa lavadora
38.7 Cliente 1 desocupa secadora
38.7 Cliente 2 ocupa secadora

Espera por lavadoras: 0.00 Clientes atendidos: 2
```
>**Desafior 8**: no desafio anterior, caso você simule por 10 ou mais horas, deve notar como o tempo de espera pela lavadora fica muito alto. Para identificar o gargalo do sistema, acrescente a impressão do número de clientes que ficaram em fila ao final da simulação. Você consegue otimizar o sistema a partir do modelo contruído?

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
print("Fila de clientes ao final da simulação: lavadoras %.2f   cestos %.2f secadoras %.2f" 
        %(len(lavadoras.queue), len(cestos.queue), len(secadoras.queue)))
```

Quando simulado por 60.000 minutos, o resultado fornece 3.929 clientes esperando por lavadoras. Temos aí um caso clássico de fila infinita, isto é: a taxa de atendimento das lavadoras é menor que a taxa de chegada de clientes. Assim, se 1 cliente ocupa em média 20 minutos na lavadora,  a taxa de adendimento em cada lavadora é de $$\mu=$$ 0.05 clientes\/min \(=1 cliente \/20 min\), enquanto a taxa de chegadas de clientes na lavandeira é de $$\lambda=$$0.20 clientes\/min \(= 1 cliente\/5 min\). Assim, para termos um sistema equilibrado, precisaríamos de um número de lavadoras de modo a garantir que a taxa de atendimento da soma das lavadoras seja maior que a taxa de chegadas de clientes no sistema ou:

$$\rho=\frac{\lambda}{n*\mu} < 1 \to n > \frac{\lambda}{\mu} = \frac{0.20}{0.05}=4$$

Assim, precisamos de 5 \(ou mais\) lavadoras **apenas para eliminar o gargalo na lavagem**. Simulando o sistema com 5 lavadoras, temos:

```python
Espera por lavadoras: 16.06 Clientes atendidos: 11907
Fila de clientes ao final da simulação: lavadoras 0.00   cestos 0.00 secadoras 0.00

```
Com 5 lavadoras, já não existe fila residual, mas o tempo médio de espera ainda está alto. Fica como exercício, elaborar uma pequena rotina que simule o sistema para números diferentes de recursos (será que o número de cestos e secadoras não está exagerado também?). Manipule o modelo para resolver essas questões.

