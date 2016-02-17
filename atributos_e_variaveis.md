# Atributos e variáveis: diferenças em SimPy

Qual a diferença entre atributo e variável para um modelo de simulação? O atributo pertence à entidade, enquanto a variável pertence ao modelo. De outro modo, se um cliente chega a uma loja e compra 1, 2 ou 3 produtos, esse cliente possui um **atributo** imediato: o seu número de produtos. Note que o atributo "número de produtos" é um valor diferente para cada cliente, ou seja: é um valor exclusivo do cliente.

Por outo lado, em determinado momento do dia, podemos totalizar o total de produtos vendidos até aquele instante, pela soma dos atributos "número de produtos" de cada cliente. Assim, o total vendido é uma **variável** do modelo, que se acumula a cada novo cliente.

Em SimPy a coisa é mais trivial: toda variável **local** funciona como atributo da entidade gerada e toda variável **global** é naturalmente uma variável do modelo. Isso não é uma regra absoluta, nem tampouco foi imaginada pelos desenvolvedores da biblioteca. É uma característica do Python que exige a construção de uma função específica para cada processo gerado (e são as entidades que contém atributos, quem executam tais processos). 

Usuários de pacotes comerciais (Simul8, GPSS, Arena etc.) estão acostumados a informar ao modelo o que é atributo e o que é variável. Em SimPy, basta lembrar que as variáveis globais serão variáveis de todo o modelo.

Por exemplo, imaginemos a chegada de clientes numa loja. Queremos que cada cliente tenha como atributo o número de produtos desejados:

```python
import random # gerador de números aleatórios
import simpy  # biblioteca de simulação

contaVendas = 0

def geraChegadas(env):
    #função que cria chegadas de entidades no sistema
    contaEntidade = 0 # variável local = atributo da entidade
    while True:
        yield env.timeout(1)
        contaEntidade += 1
        produtos = random.randint(1,3) # atributo
        print("Cliente %i chega em: %.1f quer %d produtos" 
        % (contaEntidade, env.now, produtos))
        
        # inicia o processo de atendimento do cliente de atributos contaEntidade
        #e do número de produtos
        env.process(compra(env, "Cliente %d" % contaEntidade, produtos))
        
def compra(env, nome, produtos):
    #função que realiza a venda para as entidades
    # nome e produtos, são atributo da entidade
    
    global contaVendas # variável global = variável do modelo
   
    for i in range(0,produtos):
        yield env.timeout(2)
        contaVendas += 1
        print("%s chega em: %.1f e compra %d produtos" % (nome, env.now, produtos))

random.seed(1000)   # semente do gerador de números aleatórios
env = simpy.Environment() # cria o environment do modelo
env.process(geraChegadas(env)) # cria o processo de chegadas
env.run(until=10) # roda a simulação por 10 unidades de tempo
print("Total vendido: %d produtos" % contaVendas)
```

A execução do programa apresenta como resposta:

```python
Cliente 1 chega em: 1.0 quer 2 produtos
Cliente 2 chega em: 2.0 quer 3 produtos
Cliente 1 chega em: 3.0 e compra 2 produtos
Cliente 3 chega em: 3.0 quer 1 produtos
Cliente 2 chega em: 4.0 e compra 3 produtos
Cliente 4 chega em: 4.0 quer 2 produtos
Cliente 1 chega em: 5.0 e compra 2 produtos
Cliente 3 chega em: 5.0 e compra 1 produtos
Cliente 5 chega em: 5.0 quer 2 produtos
Cliente 2 chega em: 6.0 e compra 3 produtos
Cliente 4 chega em: 6.0 e compra 2 produtos
Cliente 6 chega em: 6.0 quer 1 produtos
Cliente 5 chega em: 7.0 e compra 2 produtos
Cliente 7 chega em: 7.0 quer 2 produtos
Cliente 2 chega em: 8.0 e compra 3 produtos
Cliente 4 chega em: 8.0 e compra 2 produtos
Cliente 6 chega em: 8.0 e compra 1 produtos
Cliente 8 chega em: 8.0 quer 1 produtos
Cliente 5 chega em: 9.0 e compra 2 produtos
Cliente 7 chega em: 9.0 e compra 2 produtos
Cliente 9 chega em: 9.0 quer 3 produtos

Total vendido: 12 produtos```

##Atributos em modelos orientados ao objeto
Para aqueles que programam com classes e objetos, o atributo é naturalmente o atributo da entidade (ou do processo). A vantagem é que podemos criar atributos em recursos também, basta que o recurso seja criado dentro de uma classe. Por exemplo, a fila M/M/1 poderia ser modelada com o servidor de atendimento como uma classe:



##Desafios
**Desafio 7**: retome o problema da lavanderia (Desafio 6). Estime o tempo médio que os clientes atendidos aguardaram pela lavadora. Dica: você precisará de uma variável global para o cálculo do tempo de espera e um atributo para marcar a hora de chegada no sistema.

**Desafior 8**: no desafio anterior, você deve ter notado como o tempo de espera pela lavadora está muito alto. Altere o programa para que ele calcule os tempo de espera por cestos, secadoras e o tempo total no sistema.