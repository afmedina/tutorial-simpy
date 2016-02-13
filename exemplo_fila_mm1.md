## Juntando tudo em um exemplo: a fila M/M/1

A fila M/M/1 (ver [Chwif e Medina, 2015](http://livrosimulacao.eng.br/e-tetra-e-tetra-a-quarta-edicao-do-msed/)) tem intervalos entre chegadas exponencialmente distribuídos, tempos de atendimentos exponencialmente distribuídos e apenas um servidor de atendimento. Para este exemplo, vamos considerar que o tempo médio entre chegadas sucessivas é de 1 min (ou 1 cliente chega por min) e o tempo médio de atendimento é de 0,5 min (ou 2 clientes atendidos por minuto no servidor).

Partindo da função ```
geraChegadas```, codificada na seção anterior, precisamos criar uma função ou processo para ocupar, utilizar e desocupar o servidor. Criaremos uma função ```
atendimentoServidor```
 responsável por manter os clientes em fila e realizar o atendimento.
 
Inicialmente, vamos acrescentar a constante TEMPO_MEDIO_ATENDIMENTO e criar o recurso ```
servidorRes``` com capacidade de atender 1 cliente por vez.

 
```python
import random # gerador de números aleatórios
import simpy  # biblioteca de simulação

TEMPO_MEDIO_CHEGADAS = 1.0  # tempo entre chegadas sucessivas de clientes
TEMPO_MEDIO_ATENDIMENTO = 0.5 # tempo médio de atendimento no servidor

def geraChegadas(env):
    #função que cria chegadas de entidades no sistema
    contaChegada = 0
    while (contaChegada < 10):
        yield env.timeout(random.expovariate(1.0/TEMPO_MEDIO_CHEGADAS))
        contaChegada += 1
        print('Cliente %d chega em: %.1f ' % (contaChegada, env.now))
        
random.seed(1000)   # semente do gerador de números aleatórios

env = simpy.Environment() # cria o environment do modelo

servidorRes = simpy.Resource(env, 1) # cria o recurso servidorRes
env.process(geraChegadas(env, servidorRes))
env.run(until=10)
```
Se você executar o script anterior, o recurso é criado, mas nada acontece, afinal, não existe nenhum processo requisitando o recurso criado.

Precisamos criar uma função que realize o atendimento em 4 etapas:
1. Solicitar um servidor
2. Ocupar o servidor
3. Executar o atendimento por um tempo com média 0.5
4. Liberar o servidor para o próximo cliente

A função ```
atendimentoServidor```
, a seguir, recebe como parâmentros o ```
env```
 atual, o ```
nome```
 do cliente e a recurso ```
servidorRes```
 para executar todo o processo de atendimento.

```python
from __future__ import print_function # para compatibilidade da função print com o Python 3
import random # gerador de números aleatórios
import simpy  # biblioteca de simulação

TEMPO_MEDIO_CHEGADAS = 1.0  # tempo entre chegadas sucessivas de clientes
TEMPO_MEDIO_ATENDIMENTO = 0.5 # tempo médio de atendimento no servidor

def geraChegadas(env):
    #função que cria chegadas de entidades no sistema
    contaChegada = 0
    while (contaChegada < 10):
        yield env.timeout(random.expovariate(1.0/TEMPO_MEDIO_CHEGADAS))
        contaChegada += 1
        print('Cliente %d chega em: %.1f ' % (contaChegada, env.now))
        

def atendimentoServidor(env, nome, servidorRes):
    #função que ocupa o servidor e realiza o atendimento
    request = servidorRes.request() # solicita o recurso servidorRes
    
    yield request # aguarda em fila até o acesso e ocupa o servidorRes

    # tempo de atendimento exponencial
    yield env.timeout(random.expovariate(1.0/TEMPO_MEDIO_ATENDIMENTO))
    
    yield servidorRes.release(request) # libera o recurso servidorRes
    
    
random.seed(1000)   # semente do gerador de números aleatórios

env = simpy.Environment() # cria o environment do modelo
servidorRes = simpy.Resource(env, 1) # cria o recurso servidorRes
env.process(geraChegadas(env)
env.run(until=10)

```
Neste momento, nosso script possui uma função geradora de clientes e uma função de atendimento dos clientes, mas o bom observador nota que não existe conexão entre elas. Em SimPy, *e eu vou sempre repetir isso*, **tudo é processo dentro de um *environment***. Assim, o atendimento é um processo que deve ser iniciado por cada cliente gerado na função ```
criaChegadas.``` Isto é feito por uma chamada a função```
 env.process(função de atendimento).```

A função ```
geraChegadas```
 deve ser alterada, portanto, para receber como parâmetro o recurso ```
servidorRes```
 criado no corpo do programa e para gerar o processo de antendimento por meio da chamada à função ```
env.process:```

```python
def geraChegadas(env, servidorRes):
    #função que cria chegadas de entidades no sistema
    contaChegada = 0
    while (contaChegada < 10):
        yield env.timeout(random.expovariate(1.0/TEMPO_MEDIO_CHEGADAS))
        contaChegada += 1
        print('Cliente %d chega em: %.1f ' % (contaChegada, env.now))
        
        # inicia o processo de atendimento
        env.process(atendimentoServidor(env, "Cliente %d" % contaChegada, servidorRes))
```

Antes de executar o script, vamos acrecentar algumas linhas de impressão na tela para entedermos melhor a função ```
atendimentoServidor:```

```python
def atendimentoServidor(env, nome, servidorRes):
    request = servidorRes.request() # solicita o recurso servidorRes
    
    yield request # aguarda em fila até o acesso
    print('%s inicia o atendimento em: %.1f ' % (nome, env.now))
    
    # tempo de atendimento exponencial
    yield env.timeout(random.expovariate(1.0/TEMPO_MEDIO_ATENDIMENTO))

    print('%s termina o atendimento em: %.1f.' % (nome, env.now)) 
    
    yield servidorRes.release(request) # libera o recurso servidorRes
```
Agora execute o script e voilá!

```
Cliente 1 chega em: 1.5 
Cliente 1 inicia o atendimento em: 1.5 
Cliente 1 termina o atendimento em: 1.6.
Cliente 2 chega em: 2.6 
Cliente 2 inicia o atendimento em: 2.6 
Cliente 2 termina o atendimento em: 2.9.
Cliente 3 chega em: 3.0 
Cliente 3 inicia o atendimento em: 3.0 
Cliente 4 chega em: 3.8 
Cliente 5 chega em: 4.0 
Cliente 3 termina o atendimento em: 5.0.
Cliente 4 inicia o atendimento em: 5.0 
Cliente 6 chega em: 5.1 
Cliente 4 termina o atendimento em: 5.2.
Cliente 5 inicia o atendimento em: 5.2 
Cliente 5 termina o atendimento em: 5.3.
Cliente 6 inicia o atendimento em: 5.3 
Cliente 7 chega em: 5.7 
Cliente 6 termina o atendimento em: 5.8.
Cliente 7 inicia o atendimento em: 5.8 
Cliente 8 chega em: 6.0 
Cliente 9 chega em: 6.0 
Cliente 7 termina o atendimento em: 6.2.
Cliente 8 inicia o atendimento em: 6.2 
Cliente 8 termina o atendimento em: 6.5.
Cliente 9 inicia o atendimento em: 6.5 
Cliente 9 termina o atendimento em: 6.8.
Cliente 10 chega em: 9.7 
Cliente 10 inicia o atendimento em: 9.7```


Existem muitos conceitos a serem discutidos sobre o script anterior e, garanto, que eles serão destrinchados nas seções seguintes. 

Por hora, e para não esticar demais a atividade, analise atentamente os resultados da execução do script e avance para cima dos nossos desafios.


