# Gravar Saída em Arquivo ou Planilha

Modelos de simulação são usualmente ferramentas utilizadas para simulação de diversos cenários distintos, exigindo a manipulação de um número considerável de dados e informações. Assim, uma boa prática é armazenar os dados do modelo, tanto de entrada quanto de saída, em uma planilha eletrônica.

Embora o SimPy não tenha funções específicas de comunicação com planilhas, o Python possui diversas bibliotecas para isso. A minha preferida é a [xlwings](https://www.xlwings.org/). Você pode encontrar cursos on-line de uso da biblioteca no próprio site dos desenvolvedores ou procurar, pois existe muita coisa no [youtube ](https://youtu.be/5iyL9tMw8vA)e no [stackoverflow](https://stackoverflow.com/).

## Comunicação com a biblioteca

A biblioteca ganhou meu coração por ser de uso simples e isso inclui poucos comandos a serem aprendidos.

Vamos começar _planilhando_ nosso modelo de fila M/M/1 criado na seção "Criando, ocupando e desocupando recursos". Nesse modelo, temos dois parâmetros de entrada: o tempo médio entre chegadas de clientes e o tempo médio de atendimento no servidor \(lembrando que em uma fila M/M/1 tanto os intervalos entre chegadas sucessivas de clientes quanto os atendimentos no servidor são exponencialmente distribuídos\).

```text
import random                           # gerador de números aleatórios
```

```python
import simpy                            # biblioteca de simulação

TEMPO_MEDIO_CHEGADAS = 1.0              # tempo médio entre chegadas sucessivas de clientes
TEMPO_MEDIO_ATENDIMENTO = 0.5           # tempo médio de atendimento no servidor

def geraChegadas(env):
    # função que cria chegadas de entidades no sistema
    contaChegada = 0
    while True:
        # aguardo um intervalo de tempo exponencialmente distribuído
        yield env.timeout(random.expovariate(1.0/TEMPO_MEDIO_CHEGADAS))
        contaChegada += 1
        print('%.1f Chegada do cliente %d' % (env.now, contaChegada))

random.seed(25)                                 # semente do gerador de números aleatórios
env = simpy.Environment()                       # cria o environment do modelo
servidorRes = simpy.Resource(env, capacity=1)   # cria o recurso servidorRes
env.process(geraChegadas(env))                  # incia processo de geração de chegadas

env.run(until=5)                                # executa o modelo por 10 min
```

