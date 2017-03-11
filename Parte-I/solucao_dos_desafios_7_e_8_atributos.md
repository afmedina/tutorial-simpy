# Solução dos desafios 7 e 8

> **Desafio 7**: retome o problema da lavanderia \(Desafio 6\). Estime o tempo médio que os clientes atendidos aguardaram pela lavadora.
>
> Dica: você precisará de uma variável global para o cálculo do tempo de espera e um atributo para marcar a hora de chegada do cliente na lavadora.

O tempo médio de espera por fila de um recurso - no caso lavadoras - é estimado pelo soma do tempo que todos os clientes aguardaram pelo recurso, dividido pelo número de clientes que ocuparam o recurso ao longo da simulação.

Assim, vamos criar duas variáveis globais para armazenar a soma do tempo de espera por lavadora de todos os clientes que ocuparam as lavadoras, bem como o número de clientes que ocuparam as mesmas lavadoras:

```python
import random
import simpy

contaClientes = 0           # conta clientes que chegaram no sistema
tempoEsperaLavadora = 0     # conta tempo de espera total por lavadora
contaLavadora = 0           # conta clientes que ocuparam uma lavadora
```

A seguir, precisamos alterar a função `lavaSeca` para calcular corretamente o tempo de espera por lavadora de cada cliente, somar este valor à variável global `tempoEsperaLavadora` e incrementar o número de clientes que ocuparam lavadoras na variável global `contaLavadora` \(representação apenas da parte do código que é alterada\):

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

print("\nTempo médio de espera por lavadoras: %.2f min. Clientes atendidos: %i" 
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

Tempo médio de espera por lavadoras: 0.00 min. Clientes atendidos: 2
```

> **Desafio 8**: no desafio anterior, caso você simule por 10 ou mais horas, deve notar como o tempo de espera pela lavadora fica muito alto. Para identificar o gargalo do sistema, acrescente a impressão do número de clientes que ficaram em fila ao final da simulação. Você consegue otimizar o sistema a partir do modelo construído?

Quando simulamos o sistema por 10 horas \(=10\*60 minutos\), obtemos como resposta:

```python
...
599.6 Cliente 75 ocupa cesto
600.0 Chegada do cliente 133

Tempo médio de espera por lavadoras: 138.63 min. Clientes atendidos: 77
```

Para a solução do desafio, basta acrescentar uma linha ao final do programa principal que imprime as filas de por recursos \(lavadoras, cestos e secadoras\) ao final da simulação:

```python
env.run(until=600)

print("\nTempo médio de espera por lavadoras: %.2f min. Clientes atendidos: %i" 
        %(tempoEsperaLavadora/contaLavadora, contaLavadora))
print("Fila de clientes ao final da simulação: lavadoras %i cestos %i secadoras %i" 
        %(len(lavadoras.queue), len(cestos.queue), len(secadoras.queue)))
```

Quando simulado por 600 minutos \(ou 10 horas\), a saída do modelo fornece:

```python
...
599.6 Cliente 75 ocupa cesto
600.0 Chegada do cliente 133

Tempo médio de espera por lavadoras: 138.63 min. Clientes atendidos: 77
Fila de clientes ao final da simulação: lavadoras 56 cestos 0 secadoras 0
```

Portanto, ao final da simulação, existem 56 clientes aguardando uma lavadora livre, enquanto nenhum cliente aguarda por cestos ou secadoras. Temos um caso clássico de fila **infinita**, isto é: a taxa de horária de atendimento das lavadoras é menor que a taxa horária com que os clientes chegam à lavanderia. Assim, se 1 cliente ocupa em média 20 minutos uma lavadora, a taxa de atendimento em cada lavadora é de $$\mu=$$ 0.05 clientes\/min \(=1 cliente \/20 min\), enquanto a taxa de chegadas de clientes na lavandeira é de $$\lambda=$$0.20 clientes\/min \(= 1 cliente\/5 min\).

Como a taxa de atendimento é menor que a taxa de chegadas, a fila cresce indefinidamente. Para termos um sistema equilibrado, precisaríamos de um número de lavadoras tal que se garanta que a taxa de atendimento da soma das lavadoras seja maior que a taxa de chegadas de clientes no sistema ou:

$$\rho=\frac{\lambda}{n*\mu} < 1 \to n > \frac{\lambda}{\mu} = \frac{0.20}{0.05}=4$$

Portanto, com 5 \(ou mais\) lavadoras eliminaríamos **o gargalo na lavagem**.

O bom da simulação é que podemos testar se a calculera anterior faz sentido. Quando simulado para 5 lavadoras, o modelo fornece como saída:

```python
...
598.8 Cliente 107 ocupa cesto
599.0 Cliente 105 desocupa secadora

Tempo médio de espera por lavadoras: 4.40 min. Clientes atendidos: 108
Fila de clientes ao final da simulação: lavadoras 0 cestos 0 secadoras 0
```

Com 5 lavadoras, portanto, já não existe fila residual.

## Teste seus conhecimentos

1. Elabore uma pequena rotina capaz de simule o sistema para números diferentes de recursos \(será que o número de cestos e secadoras não está exagerado também?\). Manipule o modelo para encontrar o número mínimo de recursos necessário, de modo a não haver gargalos no sistema.



