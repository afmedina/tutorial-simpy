##Adicionando `callbacks` aos eventos

SimPy possui uma ferramenta tão curiosa como poderosa: os `callbacks.` Um `callback` é uma função que você *acrescenta* ao final de um evento. Por exemplo, considere que quando o evento da tartaruga (ou da lebre) termina, desejamos imprimir o vencedor na tela. Assim, quando o evento é *processado*, desejamos que ele processe a seguinte função, que recebe o evento como único parâmetro de entrada:
```python
def campeao(event):
    # imprime a faixa de campeão
    print('%3.1f \o/ Tan tan tan (musica do Senna) A %s é a campeã!\n'
                %(env.now, event.value))
```
Toda função para ser anexada como um `callback`, deve ter aceitar como parâmetro de chamada apenas um evento.

Para anexarmos a função campeão a um evento, basta utilizar o método `callbacks.append(função_criada):`
```python
    # cria os eventos de corrida de cada animal
    lebreEvent = env.timeout(lebreTempo, value='lebre')
    tartarugaEvent = env.timeout(tartarugaTempo, value='tartaruga')
    
    # acrecenta os callbacks
    lebreEvent.callbacks.append(campeao)
    tartarugaEvent.callbacks.append(campeao)
```
O código completo do modelo com `callbacks`ficaria:
```python
import simpy
import random

def corrida(env):
    # a lebre x tartaruga!
    # sorteia aleatoriamente os tempos dos animais
    # cria os eventos que disparam as corridas
    lebreTempo = random.normalvariate(5,2)
    tartarugaTempo = random.normalvariate(5,2)
    # cria os eventos de corrida de cada animal
    lebreEvent = env.timeout(lebreTempo, value='lebre')
    tartarugaEvent = env.timeout(tartarugaTempo, value='tartaruga')
    
    # acrecenta os callbacks
    lebreEvent.callbacks.append(campeao)
    tartarugaEvent.callbacks.append(campeao)

    # começou!
    print('%3.1f Iniciada a corrida!' %(env.now))
    # simule até que alguém chegue primeiro
    yield lebreEvent | tartarugaEvent

def campeao(event):
    # imprime a faixa de campeão
    print('%3.1f \o/ Tan tan tan (musica do Senna) A %s é a campeã!\n'
                %(env.now, event.value))
  

random.seed(10)
env = simpy.Environment()
proc = env.process(corrida(env))
env.run(until=10)
```
Note como o código ficou razoavelmente mais compacto, por eliminamos toda a codificação referente aos testes `if...then...else` para determinar que é o campeão.
Quando executado, o modelo fornece como resultado:
```python
0.0 Iniciada a corrida!
5.3 \o/ Tan tan tan (musica do Senna) A tartaruga é a campeã!
5.4 \o/ Tan tan tan (musica do Senna) A lebre é a campeã!
```
OPS!
Aos 5.4 minutos a lebre, que chegou depois, foi declarada campeã também. Como isso aqui não é a [Federação Paulista de Futebol](https://pt.wikipedia.org/wiki/Campeonato_Paulista_de_Futebol_de_1973), temos de corrigir isso. 

Uma solução prática seria criar uma variável global que torne-se `True`, quando o primeiro corredor ultrapassa a linha, de modo que a função `campeao` consiga distinguir um corredor do outro:
```python
import simpy
import random

vencedor = False    # se já temos um vencedor na corrida
```
A função `campeao` agora deve lidar com uma lógica de desvio de fluxo para determinar se evento representa um campeão ou não:
```python
def campeao(event):
    global vencedor
    
    if not vencedor:
        # imprime a faixa de campeão
        print('%3.1f \o/ Tan tan tan (musica do Senna) A %s é a campeã!'
                    %(env.now, event.value))
        # atualiza a variável global vencedor
        vencedor = True
    else:
        # imprime o perdedor
        print('%3.1f A %s chega em segundo lugar...'
                    %(env.now, event.value)) 
```
Quando simulado, o modelo fornece como saída:
```python
0.0 Iniciada a corrida!
5.3 \o/ Tan tan tan (musica do Senna) A tartaruga é a campeã!
5.4 A lebre chega em segundo lugar...
```
Você pode adicionar quantas funções de `callback` quiser ao seu evento, mas lembre-se que manipular um modelo diretamente por eventos tende a deixar o código confuso. Portanto, não economize nos comentários!

## Todo processo é um evento
Quando um processo é gerado pelo comando `env.process()`, o processo gerado é automaticamente tratado como um evento em SimPy. Assim, você pode adicionar `callbacks` aos processos também ou mesmo retornar um valor (como já vimos na seção....).
Por exemplo, vamos acrescentar uma função de `callback` para quando a corrida terminar:
```python
def final(event):
    # imprime o aviso de final da corrida
    print('%3.1f Ok pessoal, a corrida acabou.' %env.now)
```
Precisamos agora, modificar apenas os comandos que inicializam a função `corrida:`
```python
random.seed(10)
env = simpy.Environment()
proc = env.process(corrida(env))
# adiciona ao processo proc a função callback final
proc.callbacks.append(final)

# executa até que o processo corrida termine
env.run(proc)
```

```python

```

```python

```


## Conceitos desta seção
| Conteúdo | Descrição |
| -- | -- |
| `Event.callbacks.append(callbackFunction)` | adiciona um `callback`, representado pela função `callbackFunction` do modelo. Após o processamento do evento (`Event.processed = True`) a função de `callback` é executada. A função `callbackFunction`, obrigatoriamente deve ter como parâmetro apenas um evento. |

## Desafio
> Desafio 26: 