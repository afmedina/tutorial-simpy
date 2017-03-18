## Adicionando `callbacks` aos eventos

SimPy possui uma ferramenta tão curiosa quanto poderosa: os `callbacks.` Um `callback` é uma função que você _acrescenta_ ao final de um evento. Por exemplo, considere que quando o evento da tartaruga \(ou da lebre\) termina, desejamos imprimir o vencedor na tela. Assim, quando o evento é _processado_, desejamos que ele processe a seguinte função, que recebe o evento como **único** parâmetro de entrada:

```python
def campeao(event):
    # imprime a faixa de campeão
    print('%3.1f \o/ Tan tan tan (música do Senna) A %s é a campeã!\n'
                %(env.now, event.value))
```

Toda função para ser anexada como um `callback`, deve possuir como parâmetro de chamada apenas um único evento. Note também, que o valor de `env.now` impresso na tela é possível pois `env` é uma variável global para o Python. \(Caso você ainda tenha alguma dificuldade para entender como o Python lida com variáveis globais e locais, um bom caminho é [ler este bom guia](http://www.python-course.eu/python3_global_vs_local_variables.php)\).

Para anexarmos a função `campeão` a um evento, utilizaremos o método `callbacks.append(função_criada):`

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
    print('%3.1f \o/ Tan tan tan (música do Senna) A %s é a campeã!\n'
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
5.3 \o/ Tan tan tan (música do Senna) A tartaruga é a campeã!
5.4 \o/ Tan tan tan (música do Senna) A lebre é a campeã!
```

OPS!

Aos 5.4 minutos a lebre, que chegou depois, foi declarada campeã também. Como isso aqui não é a [Federação Paulista de Futebol](https://pt.wikipedia.org/wiki/Campeonato_Paulista_de_Futebol_de_1973), temos de corrigir o modelo e garantir que vença sempre quem chegar primeiro.

Uma solução prática seria criar uma variável global que se torna `True` quando o primeiro corredor ultrapassa a linha, de modo que a função `campeao` consiga distinguir se já temos um vencedor ou não:

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
        print('%3.1f \o/ Tan tan tan (música do Senna) A %s é a campeã!'
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
5.3 \o/ Tan tan tan (música do Senna) A tartaruga é a campeã!
5.4 A lebre chega em segundo lugar...
```

Você pode adicionar quantas funções de `callback` quiser ao seu evento, mas lembre-se que manipular um modelo diretamente por eventos tende a deixar o código ligeiramente confuso e a boa prática recomenda não economizar nos comentários.

## Todo processo é um evento

Quando um processo é gerado pelo comando `env.process(),` o processo gerado é automaticamente tratado como um evento pelo SimPy. Você pode igualmente adicionar `callbacks` aos processos ou mesmo retornar um valor \(como já vimos na seção....\).  
Por exemplo, vamos acrescentar uma função de `callback` para ao processo `corrida` que informa o final da corrida para o público:

```python
def final(event):
    # imprime o aviso de final da corrida
    print('%3.1f Ok pessoal, a corrida acabou.' %env.now)
```

Precisamos agora, modificar apenas os comandos que inicializam a função `corrida,` anexando o `callback` criado:

```python
random.seed(10)
env = simpy.Environment()
proc = env.process(corrida(env))
# adiciona ao processo proc a função callback final
proc.callbacks.append(final)

# executa até que o processo corrida termine
env.run(proc)
```

Note que, além de adicionarmos a função `final` como `callback` da função `corrida,` modificamos o comando `env.run()` para que ele simule até que a função `corrida` termine seu processamento. \(Experimente substituir a linha `env.run(proc)` por `env.run(until=10)` e verifique o que acontece\).

Quando executado, o modelo fornece como saída:

```python
0.0 Iniciada a corrida!
5.3 \o/ Tan tan tan (musica do Senna) A tartaruga é a campeã!
5.3 Ok pessoal, a corrida acabou.
```

Uma boa pedida para `callbacks` é construir funções que calculem estatísticas de termino de processamento ou, como veremos na próxima seção, quando desejamos trabalhar com falhas.

## Conceitos desta seção

| Conteúdo | Descrição |
| --- | --- |
| `Event.callbacks.append(callbackFunction)` | adiciona um `callback`, representado pela função `callbackFunction` do modelo. Após o processamento do evento \(`Event.processed = True`\) a função de `callback` é executada. A função `callbackFunction,` obrigatoriamente deve ter como parâmetro apenas um evento. |

## Desafio

> Desafio 26: acrescente à função `final` um comando para armazenar quem venceu e em que tempo. Simule para 10 replicações e calcule a média e a porcentagem de vitórias de cada corredor.



