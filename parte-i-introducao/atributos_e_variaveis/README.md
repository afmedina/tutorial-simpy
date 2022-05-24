# Atributos e variáveis

Qual a diferença entre atributo e variável para um modelo de simulação? O atributo pertence à entidade, enquanto a variável pertence ao modelo. De outro modo, se um cliente chega a uma loja e compra 1, 2 ou 3 produtos, esse cliente possui um **atributo** imediato: o **número de produtos** comprados. Note que o atributo "número de produtos" é um valor diferente para cada cliente, ou seja: é um valor exclusivo do cliente.

Por outro lado, um parâmetro de saída importante seria o número total de produtos vendidos nesta loja ao longo da duração da simulação. O total de produtos é a soma dos atributos "número de produtos" de cada cliente que comprou algo na loja. Assim, o total vendido é uma **variável** do modelo, que se acumula a cada nova compra, independentemente de quem é o cliente.

Em SimPy a coisa é trivial: toda variável **local** funciona como atributo da entidade gerada e toda variável **global** é naturalmente uma variável do modelo. Não se trata de uma regra absoluta, nem tampouco foi imaginada pelos desenvolvedores da biblioteca, é decorrente da necessidade de se representar os processos do modelo de simulação por meio de **funções** que, por sua vez representam entidades executando alguma coisa.

Usuários de pacotes comerciais (Simul8, Anylogic, Arena etc.) estão acostumados a informar explicitamente ao modelo o que é atributo e o que é variável. Em SimPy, basta lembrar que as variáveis globais serão variáveis de todo o modelo e que os atributos de interesse devem ser transferidos de um processo ao outro por transferência de argumentos no cabeçalho das funções.

Voltemos ao exemplo de chegadas de clientes numa loja. Queremos que cada cliente tenha como atributo o número de produtos desejados:

```python
import random    # gerador de números aleatórios
import simpy     # biblioteca de simulação

contaVendas = 0  # variável global que manrca o número de vendas realizadas

def geraChegadas(env):
    # função que cria chegadas de entidades no sistema
    # variável local = atributo da entidade
    contaEntidade = 0 
    while True:
        yield env.timeout(1)
        contaEntidade += 1
        # atributo do cliente: número de produtos desejados
        produtos = random.randint(1,3) 
        print("%.1f Chegada do cliente %i\tProdutos desejados: %d"
                % (env.now, contaEntidade, produtos))

        # inicia o processo de atendimento do cliente de atributos contaEntidade
        # e do número de produtos
        env.process(compra(env, "cliente %d" % contaEntidade, produtos))

def compra(env, nome, produtos):
    # função que realiza a venda para as entidades
    # nome e produtos, são atributo da entidade

    global contaVendas # variável global = variável do modelo

    for i in range(0, produtos):
        yield env.timeout(2)
        contaVendas += produtos
        print("%.1f Compra do %s \tProdutos comprados: %d" % (env.now, nome, produtos))

random.seed(1000)               # semente do gerador de números aleatórios
env = simpy.Environment()       # cria o environment do modelo
env.process(geraChegadas(env))  # cria o processo de chegadas

env.run(until=5)                # roda a simulação por 10 unidades de tempo
print("\nTotal vendido: %d produtos" % contaVendas)
```

A execução do programa por apenas 5 minutos, apresenta como resposta:

```python
1.0 Chegada do cliente 1        Produtos desejados: 2
2.0 Chegada do cliente 2        Produtos desejados: 3
3.0 Compra do cliente 1         Produtos comprados: 2
3.0 Chegada do cliente 3        Produtos desejados: 1
4.0 Compra do cliente 2         Produtos comprados: 3
4.0 Chegada do cliente 4        Produtos desejados: 2

Total vendido: 5 produtos
```

É importante destacar no exemplo, que o cliente (ou entidade) gerado(a) pela função `geraChegadas`é enviado(a) para a função `compra` com seu atributo `produtos,` como se nota na linha em que o cliente chama o processo de compra:

```python
env.process(compra(env, "cliente %d" % contaEntidade, produtos))
```

Agora raciocine de modo inverso: seria possível representar o número total de produtos vendidos como uma variável local? Intuitivamente, somos levados a refletir na possibilidade de _transferir_ o número total de produtos como uma parâmetro de chamada da função. Mas, reflita mais um tiquinho... É possível passar o total vendido como um parâmetro de chamada da função?

Do modo como o problema foi modelado, isso não é possível, pois cada chegada gera um novo processo `compra` independente para cada cliente e não há como transferir tal valor de uma chamada do processo para outra. A seção a seguir, apresenta uma alternativa interessante que evita o uso de variáveis globais num modelo de simulação.

## Atributos em modelos orientados ao objeto

Para aqueles que programam com classes e objetos, o atributo é naturalmente o atributo da entidade (ou do processo). Uma facilidade que a programação voltada ao objeto possui é que podemos criar atributos para recursos também. Neste caso, basta que o recurso seja criado dentro de uma classe.

Por exemplo, a fila M\M\1 poderia ser modelada por uma classe `Servidor,` em que um dos seus atributos é o próprio `Resource` do SimPy, como mostra o código a seguir:

```python
import random
import simpy

class Servidor(object):
    # cria a classe Servidor
    # note que um dos atributos é o próprio Recurso do simpy
    def __init__(self, env, capacidade, duracao):
        # atributos do recurso
        self.env = env
        self.res = simpy.Resource(env, capacity=capacidade)
        self.taxaExpo = 1.0/duracao
        self.clientesAtendidos = 0

    def atendimento(self, cliente):
        # executa o atendimento
        print("%.1f Início do atendimento do %s" % (env.now, cliente))
        yield self.env.timeout(random.expovariate(self.taxaExpo))
        print("%.1f Fim do atendimento do %s" % (env.now, cliente))

def processaCliente(env, cliente, servidor):
    # função que processa o cliente

    print('%.1f Chegada do %s' % (env.now, cliente))
    with servidor.res.request() as req: # note que o Resource é um atributo também
        yield req

        print('%.1f Servidor ocupado pelo %s' % (env.now, cliente))
        yield env.process(servidor.atendimento(cliente))
        servidor.clientesAtendidos += 1
        print('%.1f Servidor desocupado pelo %s' % (env.now, cliente))


def geraClientes(env, intervalo, servidor):
    # função que gera os clientes
    i = 0
    while True:
        yield env.timeout(random.expovariate(1.0/intervalo))
        i += 1
        env.process(processaCliente(env, 'cliente %d' % i, servidor))


random.seed(1000)

env = simpy.Environment()
# cria o objeto servidor (que é um recurso)
servidor = Servidor(env, 1, 1)      
env.process(geraClientes(env, 3, servidor))

env.run(until=5)
```

Quando processado por apenas 5 minutos, o modelo anterior fornece:

```python
4.5 Chegada do cliente 1
4.5 Servidor ocupado pelo cliente 1
4.5 Início do atendimento do cliente 1
4.6 Fim do atendimento do cliente 1
4.6 Servidor desocupado pelo cliente 1
```

No caso da programação voltada ao objeto, uma variável do modelo pode pertencer a uma classe, sem a necessidade de que a variável seja global. Por exemplo, o atributo `clientesAtendidos`da classe `Servidor` é uma variável que representa o total de cliente atendidos ao longo da simulação. Caso a representação utilizada não fosse voltada ao objeto, o número de clientes atendidos seria forçosamente uma variável global.

## Conteúdos desta seção

| **Conteúdo**               | **Descrição**                                                                                                                                         |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| representação de atributos | os atributos devem ser representados localmente e transferidos entre funções (ou processos) como parâmetros das funções (ou processos)                |
| representação de variáveis | as variáveis do modelo são naturalmente representadas como variáveis globais ou, no caso da programação voltada ao objeto, como atributos de classes. |

## Desafios

> **Desafio 7**: retome o problema da lavanderia (Desafio 6). Estime o tempo médio que os clientes atendidos aguardaram pela lavadora. Dica: você precisará de uma variável global para o cálculo do tempo de espera e um atributo para marcar a hora de chegada no sistema.
>
> **Desafio 8**: no desafio anterior, caso você simule por 10 ou mais horas, deve notar como o tempo de espera pela lavadora fica muito alto. Para identificar o gargalo do sistema, acrescente a impressão do número de clientes que ficaram em fila ao final da simulação. Você consegue otimizar o sistema a partir do modelo construído?
