# Solução dos desafios 6 e 7

**Desafio 6**: Considere que cada entidade gerada no primeiro exemplo desta seção tem um peso em gramas dado por uma distribuição normal de média 10 e desvio padrão igual a 5. Crie um critério de parada para quando a média dos pesos das entidades geradas esteja no intervalo entre 9,5 e 10,5.

Este primeiro desafio envolve poucas modificações no programa original. Acrescentamos três variáveis novas: ```media```, ```contador``` e ```pesoTotal```; o laço while foi substituido pelo critério de parada e algumas linhas foram acrescentadas para o cálculo da média de peso até a última entidade gerada. O peso de cada entidade é sorteado pela função random.normalvariate(mu, sigma) da bliblioteca random.

```python
import random
import simpy

def geraChegada(env, p):
    media, contador, pesoTotal = 0, 0, 0
    while media > 10.5 or media < 9.5:     #critério de parada
        print("%s: nova chegada em %s" %(p, env.now))
        yield env.timeout(1)
        contador += 1                      #conta entidades geradas
        peso = random.normalvariate(10, 5) #sorteia o peso da entidade
        pesoTotal += peso                  #acumula o peso total até agora
        media = pesoTotal/contador         #calcula média dos pesos
        print("Média atual %.2f" %(media))

random.seed(100)
env = simpy.Environment()
chegadas = env.process(geraChegada(env, "p1"))
env.run()
```
Quando executado, o programa apresenta como resultado:
```
p1: nova chegada em 0
Média atual 4.42
p1: nova chegada em 1
Média atual 11.16
p1: nova chegada em 2
Média atual 11.94
p1: nova chegada em 3
Média atual 12.83
p1: nova chegada em 4
Média atual 10.94
p1: nova chegada em 5
Média atual 11.75
p1: nova chegada em 6
Média atual 10.49
```
**Desafio 7**: Modifique o critério anterior para que a parada ocorra quando a média for 10 com um intervalo de confiança de amplitude 0,5 e nível de significância igual a 95%. Dica: utilize a biblioteca ```numpy``` para isso (consulte o [stackoverflow](http://stackoverflow.com/)!).

Esta situação exige um pouco mais no processo de codificação, contudo é algo muito utilizado em modelos de simulação de eventos discretos.

Como agora queremos o Intervalo de Confiança de uma dada amostra, os valores dos pesos serão armazenados em uma lista (chamada ```pesos```, no caso do desafio).

A biblioteca *numpy* fornece um meio fácil de se estimar a média e o desvio padrão de uma amostra de valores armazenada numa lista:

* ```numpy.mean(pesos)```: estima a média da lista ```pesos```;
* ```numpy.std(pesos)```: estima o desvio-padrão da lista ```pesos```


Para o cálculo do intervalo de confiança, devemos lembrar que, para amostras pequenas, a sua expressão é dada por:

$$\left[ \bar{x} - t_ {{1-\alpha} , n-1} \frac{s}{\sqrt{n}} , \bar{x} + xt_ {{1-\alpha} , n-1} \frac{s}{\sqrt{n}} \right]$$


A biblioteca import scipy.stats possui diversas funções estatísticas, dentre elas, a distribuição t de student, necessária para o cálculo do intervalo de confiança. Como está será uma operação rotineira nos nossos modelos de simulação, o ideal é encapsular o código em uma função específica:

```python
def intervaloConfMedia(a, conf=0.95):
    #retorna a média e a amplitude do intervalo de confiança dos valores contidos em a
    media, sem, m = numpy.mean(a), scipy.stats.sem(a), scipy.stats.t.ppf((1+conf)/2., len(a)-1)
    h = m*sem
    return media, h
 ```

A função anterior calcula a média e amplitude de um intervalo de confiança, a partir da lista de valores e do nível de confiança desejado.

O novo programa ficaria:

```python
import random
import numpy        #biblioteca numpy para computação científica http://www.numpy.org/
import scipy.stats  #bilbioteca scipy.stats de funções estatísticas
import simpy

def intervaloConfMedia(a, conf=0.95):
    #retorna a média e a amplitude do intervalo de confiança dos valores contidos em a
    media, sem, m = numpy.mean(a), scipy.stats.sem(a), scipy.stats.t.ppf((1+conf)/2., len(a)-1)
    h = m*sem
    return media, h

def geraChegada(env, p):
    pesos = []       #lista para armazenar os valores de pesos gerados
    while True:
        print("%s: nova chegada em %s" %(p, env.now))
        yield env.timeout(1)
        pesos.append(random.normalvariate(10, 5)) # adiciona à lista o peso da entidade atual
        
        #cálculo da amplitude do intervalo de confiança, como nível de significância = 95%
        if len(pesos) > 1:           
            media, amplitude = intervaloConfMedia(pesos, 0.95)
            print("Média atual: %.2f. Amplitude atual: %.2f" %(media, amplitude))
            
            #se a amplitude atende ao critério estabelecido, interronpe o processo
            if amplitude < 0.5:
                print("Intervalo de confiança atingido depois de %s valores! [%.2f, %.2f]" % (len(pesos), media-amplitude, media+amplitude))
                break #termina o laço while

random.seed(100)
env = simpy.Environment()
chegadas = env.process(geraChegada(env, "p1"))
env.run()
```
O programa anterior leva 411 amostras para atingir o intervalo desejado:

```
...
Média atual: 10.20. Amplitude atual: 0.51
p1: nova chegada em 402
Média atual: 10.20. Amplitude atual: 0.50
p1: nova chegada em 403
Média atual: 10.18. Amplitude atual: 0.50
p1: nova chegada em 404
Média atual: 10.19. Amplitude atual: 0.50
p1: nova chegada em 405
Média atual: 10.21. Amplitude atual: 0.50
p1: nova chegada em 406
Média atual: 10.21. Amplitude atual: 0.50
p1: nova chegada em 407
Média atual: 10.19. Amplitude atual: 0.50
p1: nova chegada em 408
Média atual: 10.19. Amplitude atual: 0.50
p1: nova chegada em 409
Média atual: 10.17. Amplitude atual: 0.50
p1: nova chegada em 410
Média atual: 10.18. Amplitude atual: 0.50
Intervalo de confiança atingido depois de 411 valores! [9.68, 10.68]
```

Existem diversas maneiras de se estimar o intervalo de confiança utilizando-se as bibliotecas do Python. A maneira aqui proposta se baseia no ```numpy``` e no ```scipy.stats```. Eventualmente tais bibliotecas não estejam instaladas na seu ambiente Python e eu antecipo: isso pode ser um problema para você...

A questão aqui é a demanda que os modelos de simulação usualmente têm para o processamento estatístico de valores armazenados ao longo da simulação. Com o ```numpy``` é tudo mais fácil, principalmente quando se considera o suporte dado pelos usuários da [stackoverflow](http://stackoverflow.com/search?q=numpy).