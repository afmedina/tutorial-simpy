# Solução dos desafios 9 e 10

> **Desafio 9**: Considere que cada entidade gerada no primeiro exemplo desta seção tem um peso em gramas dado por uma distribuição normal de média 10 e desvio padrão igual a 3. Crie um critério de parada para quando a média dos pesos das entidades geradas esteja no intervalo entre 9,5 e 10,5.

Este primeiro desafio envolve poucas modificações no programa original. Acrescentamos três variáveis novas: `media,` `contador` e `pesoTotal;` o laço `while` foi substituído pelo critério de parada e algumas linhas foram acrescentadas para o cálculo da média de peso até a última entidade gerada. O peso de cada entidade é sorteado pela função `random.normalvariate(mu, sigma)` da biblioteca `random.`

```python
import simpy
import random

def geraChegada(env, numEntidades):
    media, contador, pesoTotal = 0, 0, 0

    while media > 10.5 or media < 9.5:      # critério de parada
        yield env.timeout(1)
        contador += 1                       # conta entidades geradas
        peso = random.normalvariate(10, 3)  # sorteia o peso da entidade
        pesoTotal += peso                   # acumula o peso total até agora
        media = pesoTotal/contador          # calcula média dos pesos
        print("%4.1f nova chegada\tPeso: %4.1f kg\tMédia atual: %4.1f" 
                 %(env.now, peso, media))


random.seed(100)
env = simpy.Environment()
chegadas = env.process(geraChegada(env, 5)) # gere apenas 5 entidades
env.run()                                   # executa até o fim de todos os processos
```

Quando executado, o modelo anterior apresenta como resultado:

```python
 1.0 nova chegada       Peso:  6.7 kg   Média atual:  6.7
 2.0 nova chegada       Peso: 14.7 kg   Média atual: 10.7
 3.0 nova chegada       Peso: 12.1 kg   Média atual: 11.2
 4.0 nova chegada       Peso: 13.3 kg   Média atual: 11.7
 5.0 nova chegada       Peso:  6.0 kg   Média atual: 10.6
 6.0 nova chegada       Peso: 13.5 kg   Média atual: 11.0
 7.0 nova chegada       Peso:  5.8 kg   Média atual: 10.3
```

> **Desafio 10**: Modifique o critério anterior para que a parada ocorra quando a média for 10 kg, com um intervalo de confiança de amplitude 0,5 e nível de significância igual a 95%. Dica: utilize a biblioteca `numpy` para isso \(consulte o [Stack Overflow](http://stackoverflow.com/%29!\).

Esta situação exige um pouco mais no processo de codificação, contudo é algo muito utilizado em modelos de simulação de eventos discretos.

Como agora queremos o Intervalo de Confiança de uma dada amostra, os valores dos pesos serão armazenados em uma lista \(`pesosList`, no caso do desafio\).

A biblioteca [_numpy_ ](http://www.numpy.org/)fornece um meio fácil de se estimar a média e o desvio padrão de uma amostra de valores armazenada numa lista:

* `numpy.mean(pesosList)`: estima a média da lista `pesosList`;
* `numpy.std(pesosList)`: estima o desvio-padrão da lista `pesosList`

Para o cálculo do intervalo de confiança, devemos lembrar que, para amostras pequenas, a sua expressão é dada por:

$$
[\bar{x}- t_{1-\alpha , n-1} \frac{s}{\sqrt{n}} , \bar{x} + t_{1-\alpha , n-1} \frac{s}{\sqrt{n}}]
$$

A biblioteca [_scipy.stats_](https://docs.scipy.org/doc/scipy/reference/stats.html) possui diversas funções estatísticas, dentre elas, a distribuição t de student, necessária para o cálculo do intervalo de confiança. Como está será uma operação rotineira nos nossos modelos de simulação, o ideal é encapsular o código em uma função específica:

```python
def intervaloConfMedia(a, conf=0.95):
    # retorna a média e a amplitude do intervalo de confiança dos valores contidos em a
    media, sem = numpy.mean(a), scipy.stats.sem(a)
    m = scipy.stats.t.ppf((1+conf)/2., len(a)-1)
    h = m*sem
    return media, h
```

A função anterior calcula a média e amplitude de um intervalo de confiança, a partir da lista de valores e do nível de confiança desejado.

O novo programa então ficaria:

```python
import simpy
import random
import numpy        # biblioteca numpy para computação científica http://www.numpy.org/
import scipy.stats  # bilbioteca scipy.stats de funções estatísticas

def intervaloConfMedia(a, conf=0.95):
    # retorna a média e a amplitude do intervalo de confiança dos valores contidos em a
    media, sem = numpy.mean(a), scipy.stats.sem(a)
    m = scipy.stats.t.ppf((1+conf)/2., len(a)-1)
    return media, h

def geraChegada(env):
    pesosList = []                          # lista para armazenar os valores de pesos gerados

    while True:      
        yield env.timeout(1)
        # adiciona à lista o peso da entidade atual
        pesosList.append(random.normalvariate(10, 5))

        # calcula a amplitude do intervalo de confiança, com nível de significância = 95%
        if len(pesosList) > 1:           
            media, amplitude = intervaloConfMedia(pesosList, 0.95)
            print("%4.1f Média atual: %.2f kg\tAmplitude atual: %.2f kg"
                    %(env.now, media, amplitude))

            # se a amplitude atende ao critério estabelecido, interronpe o processo
            if amplitude < 0.5:
                print("\n%4.1f Intervalo de confiança atingido após %s valores! [%.2f, %.2f]" 
                    % (env.now, len(pesosList), media-amplitude, media+amplitude))
                #termina o laço while
                break 


random.seed(100)
env = simpy.Environment()
chegadas = env.process(geraChegada(env)) 
env.run()                                   # executa até o fim de todos os processos
```

O programa anterior leva 411 amostras para atingir o intervalo desejado:

```python
...
410.0 Média atual: 10.17 kg     Amplitude atual: 0.50 kg
411.0 Média atual: 10.18 kg     Amplitude atual: 0.50 kg

411.0 Intervalo de confiança atingido após 411 valores! [9.68, 10.68]
```

Existem diversas maneiras de se estimar o intervalo de confiança utilizando-se as bibliotecas do Python. A maneira aqui proposta se baseia no `numpy` e no `scipy.stats`. Eventualmente tais bibliotecas não estejam instaladas na seu ambiente Python e eu antecipo: isso pode ser um baita problema para você =\(

A questão aqui é que os modelos de simulação usualmente têm grande demanda por processamento estatístico de valores durante ou mesmo ao final da simulação. A biblioteca `numpy` facilita bastante esta tarefa, principalmente quando se considera o suporte dado pelos usuários do [Stack Overflow .](http://stackoverflow.com/search?q=numpy)

Como sugestão, habitue-se a construir funções padronizadas para monitoramento e cálculos estatísticos, de modo que você pode reaproveitá-las em novos programas. Em algum momento, inclusive, você pode [criar sua própria biblioteca](http://stackoverflow.com/questions/15746675/how-to-write-a-python-module) de funções para análise de saída de modelos de simulação e compartilhar com a comunidade de software livre.

