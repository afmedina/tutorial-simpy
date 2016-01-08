# Solução dos desafios 4 e 5

## Desafio 4 
Construa uma tabela com duas colunas: tempo de simulação e números de clientes em fila. Quantos clientes existem em fila no instante 5.5?

Para solução do desafio, precisamos inicialmente de uma variável que armazene o número de clientes em fila. Assim, criei a variável global ```clientesFila```, como mostra o ínicio do código alterado da seção anterior:

```python
# -*- coding: utf-8 -*-
from __future__ import print_function # para compatibilidade da função print com o Python 3
import random # gerador de números aleatórios
import simpy  # biblioteca de simulação

TEMPO_MEDIO_CHEGADAS = 1.0  # tempo entre chegadas sucessivas de clientes
TEMPO_MEDIO_ATENDIMENTO = 0.5 # tempo médio de atendimento no servidor

clientesFila = 0```

O próximo passo é incrementar essa variável quando um novo cliente entra em fila e, de modo similar, decrementá-la quando um cliente sai da fila para iniciar seu atendimento. Etapas relativamente fáceis de programar se você entendeu a função ```
atendimentoServidor```
 da seção anterior:
 
<!---
alternativa: monitorar o número de clientes no sistema, não apenas na fila
--->

```python
def atendimentoServidor(env, nome, servidorRes):
    global clientesFila
    
    request = servidorRes.request() # solicita o recurso servidorRes
    
    clientesFila += 1 # incrementa contador de novo cliente em fila
    print('%.2f: chegada de novo cliente em fila. Clientes em fila: %d' 
    %(env.now, clientesFila))
    
    yield request # aguarda em fila até o acesso
    
    print('%s inicia o atendimento em: %.1f ' % (nome, env.now()))
    clientesFila -= 1 # decrementa contador de novo cliente em fila
```
<!---
precisa defnir novamente a variável "clientesFila"?
--->

Repare que acrescentei duas chamadas à função ```print```, de modo  a imprimir na tela o número de clientes em fila em cada instante de mudança do valor da variável ```
clientesFila.```
Executado o código, descobrimos que no istante 5,5 min, temos 2 clientes em fila:
```
Cliente 1 chega em: 1.5 
1.50: chegada de novo cliente em fila. Clientes em fila: 1
Cliente 1 inicia o atendimento em: 1.5 
Cliente 1 termina o atendimento em: 1.6.
Cliente 2 chega em: 2.6 
2.61: chegada de novo cliente em fila. Clientes em fila: 1
Cliente 2 inicia o atendimento em: 2.6 
Cliente 2 termina o atendimento em: 2.9.
Cliente 3 chega em: 3.0 
3.05: chegada de novo cliente em fila. Clientes em fila: 1
Cliente 3 inicia o atendimento em: 3.0 
Cliente 4 chega em: 3.8 
3.81: chegada de novo cliente em fila. Clientes em fila: 1
Cliente 5 chega em: 4.0 
3.95: chegada de novo cliente em fila. Clientes em fila: 2
Cliente 3 termina o atendimento em: 5.0.
Cliente 4 inicia o atendimento em: 5.0 
Cliente 6 chega em: 5.1 
5.06: chegada de novo cliente em fila. Clientes em fila: 2
Cliente 4 termina o atendimento em: 5.2.
Cliente 5 inicia o atendimento em: 5.2 
Cliente 5 termina o atendimento em: 5.3.
Cliente 6 inicia o atendimento em: 5.3 
Cliente 7 chega em: 5.7 
5.73: chegada de novo cliente em fila. Clientes em fila: 1
Cliente 6 termina o atendimento em: 5.8.
Cliente 7 inicia o atendimento em: 5.8 
Cliente 8 chega em: 6.0 
5.99: chegada de novo cliente em fila. Clientes em fila: 1
Cliente 9 chega em: 6.0 
6.03: chegada de novo cliente em fila. Clientes em fila: 2
Cliente 7 termina o atendimento em: 6.2.
Cliente 8 inicia o atendimento em: 6.2 
Cliente 8 termina o atendimento em: 6.5.
Cliente 9 inicia o atendimento em: 6.5 
Cliente 9 termina o atendimento em: 6.8.
Cliente 10 chega em: 9.7 
9.69: chegada de novo cliente em fila. Clientes em fila: 1
Cliente 10 inicia o atendimento em: 9.7 
```


##Desafio 5
Calcule o tempo de permanência em fila de cada cliente e imprima o resultado na tela. Para isso, armazene o instante de chegada do cliente na fila em uma variável ```
chegada.```
 Ao final do atendimento, armazene o tempo de fila, numa variável ```
tempoFila```
 e apresente o resultado na tela.
 
A ideia deste desafio é que você se acostume com esse cálculo tão trivial mas tão importante dentro da simulação: o tempo de permanência de uma entidade em algum local. Neste caso, o local é a fila.
A lógica aqui é a de um cronometrista que deve disparar o cronômetro na chegada do cliente e pará-lo ao início do antendimento.
Assim, ao chegar, criamos uma variável ```
chegada```
 que armazena o instante atual fornecido pelo comando ```
env.now```
 do
SimPy:
```python
def atendimentoServidor(env, nome, servidorRes):
    global clientesFila
    
    chegada = env.now() # armazena o instante de chegada do cliente
    request = servidorRes.request() # solicita o recurso servidorRes```


Agora, inciado o atendimento (logo após o ```yield```
 que ocupa o recurso), a variável ```tempoFila``` armazena o tempo de permanência em fila. Como num cronômetro, o tempo em fila é calculado pelo instante atual do cronômetro menos o instante de disparo dele já armazenado na variável chegada:
```python
def atendimentoServidor(env, nome, servidorRes):
    global clientesFila
    
    chegada = env.now() # armazena o instante de chegada do cliente
    request = servidorRes.request() # solicita o recurso servidorRes
    
    clientesFila += 1 # incrementa contador de novo cliente em fila
    print('%.2f: chegada de novo cliente em fila. Clientes em fila: %d' 
    %(env.now, clientesFila))
    
    yield request # aguarda em fila até o acesso
    
    tempoFila = env.now()-chegada
```

<!---
"chegada" é um atributo da entidade cliente, explicar!
(como uma varíavel só pode armazenar diferentes valores, um para cada cliente?)

Resp: pq cada entidade cria um processo diferente quando chama atendimentoServido(). chegada, no caso, é local.
--->

Para imprimir o resultado, vou simplesmente alterar a chamada à função ```print``` na linha seguinte, de modo que o código final da função ```
atendimentoServidor```
 fica:
```python
def atendimentoServidor(env, nome, servidorRes):
    global clientesFila
    
    chegada = env.now() # armazena o instante de chegada do cliente
    request = servidorRes.request() # solicita o recurso servidorRes
    
    clientesFila += 1 # incrementa contador de novo cliente em fila
    print('%.2f: chegada de novo cliente em fila. Clientes em fila: %d'
    %(env.now(), clientesFila))
    
    yield request # aguarda em fila até o acesso
    
    tempoFila = env.now()-chegada
    print('%s inicia o atendimento em: %.1f. Tempo em fila: %.1f min ' 
    % (nome, env.now(), tempoFila))
    clientesFila -= 1 # decrementa contador de novo cliente em fila
    
    # tempo de atendimento exponencial
    yield env.timeout(random.expovariate(1.0/TEMPO_MEDIO_ATENDIMENTO))

    print('%s termina o atendimento em: %.1f.' % (nome, env.now())) 

    yield servidorRes.release(request) # libera o recurso servidorRes
```
    
A execução do programa mostra na tela o tempo de espera de cada cliente.

```
Cliente 1 chega em: 1.5 
1.50: chegada de novo cliente em fila. Clientes em fila: 1
Cliente 1 inicia o atendimento em: 1.5. Tempo em fila: 0.0 
Cliente 1 termina o atendimento em: 1.6.
Cliente 2 chega em: 2.6 
2.61: chegada de novo cliente em fila. Clientes em fila: 1
Cliente 2 inicia o atendimento em: 2.6. Tempo em fila: 0.0 
Cliente 2 termina o atendimento em: 2.9.
Cliente 3 chega em: 3.0 
3.05: chegada de novo cliente em fila. Clientes em fila: 1
Cliente 3 inicia o atendimento em: 3.0. Tempo em fila: 0.0 
Cliente 4 chega em: 3.8 
3.81: chegada de novo cliente em fila. Clientes em fila: 1
Cliente 5 chega em: 4.0 
3.95: chegada de novo cliente em fila. Clientes em fila: 2
Cliente 3 termina o atendimento em: 5.0.
Cliente 4 inicia o atendimento em: 5.0. Tempo em fila: 1.2 
Cliente 6 chega em: 5.1 
5.06: chegada de novo cliente em fila. Clientes em fila: 2
Cliente 4 termina o atendimento em: 5.2.
Cliente 5 inicia o atendimento em: 5.2. Tempo em fila: 1.2 
Cliente 5 termina o atendimento em: 5.3.
Cliente 6 inicia o atendimento em: 5.3. Tempo em fila: 0.2 
Cliente 7 chega em: 5.7 
5.73: chegada de novo cliente em fila. Clientes em fila: 1
Cliente 6 termina o atendimento em: 5.8.
Cliente 7 inicia o atendimento em: 5.8. Tempo em fila: 0.1 
Cliente 8 chega em: 6.0 
5.99: chegada de novo cliente em fila. Clientes em fila: 1
Cliente 9 chega em: 6.0 
6.03: chegada de novo cliente em fila. Clientes em fila: 2
Cliente 7 termina o atendimento em: 6.2.
Cliente 8 inicia o atendimento em: 6.2. Tempo em fila: 0.2 
Cliente 8 termina o atendimento em: 6.5.
Cliente 9 inicia o atendimento em: 6.5. Tempo em fila: 0.5 
Cliente 9 termina o atendimento em: 6.8.
Cliente 10 chega em: 9.7 
9.69: chegada de novo cliente em fila. Clientes em fila: 1
Cliente 10 inicia o atendimento em: 9.7. Tempo em fila: 0.0 ```
