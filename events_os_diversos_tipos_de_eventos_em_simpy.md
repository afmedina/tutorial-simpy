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
        # inicia o processo da ponte elvatória
        env.process(ponteElevatoria(env))
        # mantém a ponte fechada por 5 minutos
        yield env.timeout(5)
        # dispara o evento de abertura da ponte
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

O comando `succeed()` ainda pode enviar um valor, com a opção:
```python
meuEvento.succeed(value=valor)
```
Assim, poderíamos, por exemplo, enviar para a função `ponteElevatoria` o tempo previsto para que a ponte fique aberta de modo que a função que recebe o sinal de que o evento foi disparado, possa fazer uso do valor no seu processamento interno. O modelo a seguir, implenta tais modificações e sua interpretação é direta:
```python
import simpy

def turno(env):
    # abre e fecha a ponte
    global abrePonte
    
    while True:
        # cria evento para abertura da ponte
        abrePonte = env.event()
        # inicia o processo da ponte elvatória
        env.process(ponteElevatoria(env))
        # mantém a ponte fechada por 5 minutos
        yield env.timeout(5)
        # dispara o evento de abertura da ponte
        abrePonte.succeed(value=5)
        # mantém a ponte aberta por 5 minutos
        yield env.timeout(5)
    
def ponteElevatoria(env):
    # opera a ponte elevatória
    global abrePonte

    print('%2.0f A ponte está fechada =(' %(env.now))
    # aguarda o evento para abertura da ponte
    tempoAberta = yield abrePonte
    print('%2.0f A ponte está  aberta =) e fecha em %2.0f minutos' %(env.now, tempoAberta))
    
env = simpy.Environment()

# inicia o processo de controle do turno
env.process(turno(env))
env.run(until=20)
```
Novamente, o potencial de uso do comando event() é extraordinário, mas, por experiência própria, garanto que seu uso descontrolado pode tornar qualquer código ininteligível (algo semelhante a utilizar desvios de laço do tipo "go to" em um programa (des)estruturado).
 
## Aguardando múltiplos eventos ao mesmo tempo
Outra possibilidade com os eventos é aguardar até que dois ou mais deles ocorram para continuar algum processo. O SimPy possui duas opções muito interessantes para isso:

* `resultado = AnyOf(env, eventos)`: aguarda até que um dos eventos tenham ocorrido - `AnyOf` é equivalente ao símbolo de "|" (ou `or`);
* `resultado = AllOf(env, eventos)`: aguarda até que todos os eventos tenham ocorrido - `AllOf` é equivalente ao símbolo de "&" (ou `and`).

Vamos partir de um exemplo baseado numa obscura fábula infantil: [a Lebre e a Tartaruga](https://en.wikipedia.org/wiki/The_Tortoise_and_the_Hare). 

No nosso exemplo, vamos sortear o tempo de corrida de cada bicho e identificar quem foi o vencedor. Assim, além do sorteio, criaremos dois eventos que representam a corrida de cada bicho:
```python
def corrida(env):
    # a lebre x tartaruga!
    # sorteia aleatoriamente os tempos dos animais
    lebreTempo = random.normalvariate(5,2)
    tartarugaTempo = random.normalvariate(5,2)
    # cria os eventos de corrida de cada animal
    lebreEvent = env.timeout(lebreTempo, value='lebre')
    tartarugaEvent = env.timeout(tartarugaTempo, value='tartaruga')
```
Na função `corrida`, criamos portanto os eventos `lebreEvent` e `tartarugaEvent`, mas atenção: **eventos foram criados, mas não foram executados**. Como não existe um `yield` aplicado aos eventos, eles estão apenas criados na memória do Python, e esperando o momento de serem executados no SimPy.

Agora, vamos acrescentar uma um `yield` com condição de que ele aguarde até que ao menos um dos bichos tenham terminado a corrida:
```python        
    # começou!
    start = env.now
    print('%3.1f Iniciada a corrida!' %(env.now))
    # simule até que alguém chegue primeiro
    resultado = yield lebreEvent | tartarugaEvent
    tempo = env.now - start
```
A variável resultado armazena nesse instante o evento que terminou primeiro. Assim, a função precisa apenas de uma lógica de comparação e impressão do bicho vencedor. O código a seguir completa o modelo e já o deixa pronto para a execução:
```python
def corrida(env):
    # a lebre x tartaruga!
    # sorteia aleatoriamente os tempos dos animais
    lebreTempo = random.normalvariate(5,2)
    tartarugaTempo = random.normalvariate(5,2)
    # cria os eventos de corrida de cada animal
    lebreEvent = env.timeout(lebreTempo, value='lebre')
    tartarugaEvent = env.timeout(tartarugaTempo, value='tartaruga')
           
    # começou!
    start = env.now
    print('%3.1f Iniciada a corrida!' %(env.now))
    # simule até que alguém chegue primeiro
    resultado = yield lebreEvent | tartarugaEvent
    tempo = env.now - start
    
    # quem venceu?
    if lebreEvent not in resultado:
        print('%3.1f A tartaruga venceu em %3.1f minutos' %(tempo, env.now))
    elif tartarugaEvent not in resultado:
        print('%3.1f A lebre venceu em %3.1f minutos' %(tempo, env.now))
    else:
        print('%3.1f Houve um empate em %3.1f minutos' %(tempo, env.now))

random.seed(10)
env = simpy.Environment()
proc = env.process(corrida(env))
env.run(until=10)
```
Quando executado, o bicho pega:
```python
0.0 Iniciada a corrida!
5.3 A tartaruga venceu em 5.3 minutos
```
>**Observação:** a linha:
```python
> resultado = yield lebreEvent | tartarugaEvent
```
> poderia ter sido substituída, pela linha:
```python
> resultado = yield AnyOf(env, lebreEvent, tartarugaEvent)
```

## Propriedades úteis dos eventos
Um evento qualquer tem 3 propriedades que fazem a alegria de qualquer leitor:
* `Event.value`: o valor que foi passado para o evento no momento de sua criação;
* `Event.triggered`: `True`, caso o `Event` já tenha sido programado e inserido na fila de eventos do SimPy e `False`, caso contrário;
* `Event.processed`: `True`, caso o `Event` já tenha sido executado e `False`, caso contrário;

Antes de avançar - e com o intuito de facilitar o aprendizagem do *lebrístico* leitor - vamos acrescentar ao código uma função para imprimir o status de cada evento dentro de uma lista e enventos:
```python
def printEventStatus(env, eventList):
    # imprime o status das entidades
    for event in eventList:
        print('%3.1f Evento (value): %s\t programado: %s\t processado: %s'
            %(env.now, event.value, event.triggered, event.processed))   
```
Vamos agora acrescentar a função ao nosso modelo da lebre x tartaruga:
```python
import simpy
import random

def corrida(env):
    # a lebre x tartaruga!
    # sorteia aleatoriamente os tempos dos animais
    lebreTempo = random.normalvariate(50,2)
    tartarugaTempo = random.normalvariate(5,2)
    # cria os eventos de corrida de cada animal
    lebreEvent = env.timeout(lebreTempo, value='lebre')
    tartarugaEvent = env.timeout(tartarugaTempo, value='tartaruga')

    # cria lista de eventos
    eventList = [lebreEvent, tartarugaEvent]
    printEventStatus(env, eventList)
            
    # começou!
    start = env.now
    print('%3.1f Iniciada a corrida!' %(env.now))
    # simule até que alguém chegue primeiro
    resultado = yield lebreEvent | tartarugaEvent
    tempo = env.now - start
    
    # quem venceu?
    if lebreEvent not in resultado:
        print('%3.1f A tartaruga venceu em %3.1f minutos' %(tempo, env.now))
    elif tartarugaEvent not in resultado:
        print('%3.1f A lebre venceu em %3.1f minutos' %(tempo, env.now))
    else:
        print('%3.1f Houve um empate em %3.1f minutos' %(tempo, env.now))
    printEventStatus(env, eventList)

def printEventStatus(env, eventList):
    # imprime o status das entidades
    for event in eventList:
        print('%3.1f Evento (value): %s\t programado: %s\t processado: %s'
            %(env.now, event.value, event.triggered, event.processed))        
    
random.seed(10)
env = simpy.Environment()
proc = env.process(corrida(env))
env.run(until=10)
```

## Aguardando um evento ocorrer para disparar outro  `(wait_event = env.event())`

