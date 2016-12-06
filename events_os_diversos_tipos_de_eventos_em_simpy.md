# Criando, manipulando e disparando eventos com `event()`
Nesta seção entramos num território de poder dentro do SimPy. A partir deste momento você terá o poder de criar, manipular ou disparar eventos específicos criados por você. 
Mas com todo o poder, vem também a responsabilidade!
Atente-se para o fato de que, sem cuidado, o seu modelo pode ficar um pouco confuso. Isto porque um evento pode ser criado a qualquer momento e fora do contexto original do processo em execução.

## Criando um evento isolado com `event`
Considere um problema simples de controle de turno de abertura ou fechamento de uma ponte elevatória que abre, opera com veículos por 5 minutos e fecha para passagem de embarcações. Obviamente isso poderia ser implementado com o comandos já vistos neste livro, mas nosso objetivo nesta seção é criar um evento específico que informe ao bar que ele deve fechar.

Em SimPy, um evento é criado pelo comando `env.event()`:
```python
abrePonte = env.event()
```
Criar o evento, não significa que ele foi executado. Para disparar o evento `abrePonte `e marcá-lo como bem sucedido, utilizamos a opção `succeed()`:
```python
abrePonte.succeed()
```
A grande vantagem de se trabalhar com `event()` é que, em qualquer ponto do modelo, podemos lançar um comando que aguarda até que o evento criado seja disparado:
```python
yield abrePonte   # aguarda até que o evento abrePonte seja disparado
```
Incialmente, vamos criar uma função geradora que representa o processo de controle do turno de abertura/fechamento da ponte e responsável por gerar o evento que dispara o abertura da mesma:
```python
def turno(env):
    # abre e fecha a ponte
    global abrePonte
    
    while True:
        # cria evento para abertura da ponte
        abrePonte = env.event()
        # inicia o proce da ponte elvatória
        env.process(ponteElevatoria(env))
        # mantém a ponte fechada por 5 minutos
        yield env.timeout(5)
        # dispara o evento de abertur da ponte
        abrePonte.succeed()
        # mantém a ponte aberta por 5 minutos
        yield env.timeout(5)
```
Note, na função anterior, que o evento é criado, mas **não é disparado** imediatamente. De fato, ele só é disparado quanto o método `abrePonte.succeed()` é executado, algumas linhas abaixo na função. 
Para garantir que um novo ciclo de abertura e fechamento se repita (dentro do laço infinito criado), deve-se criar um novo evento e isso está garantido no início do laço com a linha:
```python
abrePonte = env.event()
```
Isso precisa ficar bem claro, paciente leitor: uma vez disparado com o succeed, o evento é extindo.
Juntando tudo num modelo de abre/fecha um bar, teríamos:
```python
import simpy

def turno(env):
    # abre e fecha a ponte
    global abrePonte
    
    while True:
        # cria evento para abertura da ponte
        abrePonte = env.event()
        # inicia o proce da ponte elvatória
        env.process(ponteElevatoria(env))
        # mantém a ponte fechada por 5 minutos
        yield env.timeout(5)
        # dispara o evento de abertur da ponte
        abrePonte.succeed()
        # mantém a ponte aberta por 5 minutos
        yield env.timeout(5)
    
def ponteElevatoria(env):
    # opera a ponte elevatória
    global abrePonte

    print('%2.0f A ponte está fechada =(' %(env.now))
    # aguarda o evento para abertura da ponte
    yield abrePonte
    print('%2.0f A ponte está aberta  =)' %(env.now))
    
env = simpy.Environment()

# inicia o processo de controle do turno
env.process(turno(env))
env.run(until=20)
```
Quando executado, o modelo anterior fornece:
```
 0 A ponte está fechada =(
 5 A ponte está aberta  =)
10 A ponte está fechada =(
15 A ponte está aberta  =)

```
No exemplo anterior, fizemos uso de uma variável global para enviar a informação de que o evento de abertura da ponte foi disparado. Isso é bom, mas também pode ser ruim: note que o evento de abertura é manipulado **fora** da função do processo do bar e isso pode deixar as coisas confusas no seu modelo, caso você não tome o devido cuidado.


## Aguardando um evento ocorrer para disparar outro  `(wait_event = env.event())`

