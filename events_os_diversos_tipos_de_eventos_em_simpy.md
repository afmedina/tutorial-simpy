# Criando, manipulando e disparando eventos com `event()`
Nesta seção entramos num território de poder dentro do SimPy. A partir deste momento você terá o poder de criar, manipular ou disparar eventos específicos criados por você. 
Mas com todo o poder, vem também a responsabilidade!
Atente-se para o fato de que, sem cuidado, o seu modelo pode ficar um pouco confuso. Isto porque um evento pode ser criado a qualquer momento e fora do contexto original do processo em execução.

## Criando um evento isolado
Considere um problema simples de controle de turno de trabalho: um bar precisa abrir, operar por 4 horas e fechar. Obviamente isso poderia ser implementado com o comandos já vistos neste livro, mas nosso objetivo é criar um evento específico que informe ao bar que ele deve fechar.

Em SimPy, um evento é criado pelo comando `env.event()`:
```python
import simpy

env = simpy.Environment()
fechaBar = env.event()
```
Criar o evento, não significa que ele foi executado. Para disparar o evento fechaBar e marcá-lo como bem sucedido, utilizamos a opção `succeed()`:
```python
fechaBar.succeed()
```
A grande vantagem de se trabalhar com event() é que, em qualquer ponto do modelo, podemos lançar um comando que aguarda até que o evento criado seja disparado:
```python
yield fechaBar   # aguarda até que o evento fechaBar seja disparado
```
Juntando tudo num modelo de abre/fecha um bar, teríamos:
```python
import simpy

def bar(env):
    # abre e fecha o bar
    global fechaBar

    print('%2.1f O bar está aberto' %(env.now))
    # aguarda o envento para fechar o bar
    yield fechaBar
    print('%2.1f O bar está fechado' %(env.now))

def turno(env):
    global fechaBar
    yield env.timeout(4)
    # dispara o evento fechar o bar
    fechaBar.succeed()

env = simpy.Environment()

# cria o evento fechaBar
fechaBar = env.event()

env.process(bar(env))
env.process(turno(env))
env.run()
```
Quando executado, o modelo anterior fornece:
```
0.0 O bar está aberto
4.0 O bar está fechado
```
No exemplo anterior, fizemos uso de uma variável global para enviar a informação de que o evento de fechamento do bar foi disparado. Isso é bom, mas pode ser ruim: note que o evento de fechamento é manipulado fora da função do processo do bar e isso pode deixar as coisas confusas no seu modelo, caso você não tome cuidado.

O modelo ainda pode ser *tunado* para considerar o turno do dia seguinte, modificando-se a função `turno`:
```python
def turno(env):
    global fechaBar
    yield env.timeout(4)
    # dispara o evento fechar o bar
    fechaBar.succeed()
    # 
```

## Aguardando um evento ocorrer para disparar outro  `(wait_event = env.event())`

