#Tutorial SimPy: criando as primeiras entidades


Algo elementar em qualquer pacote de simulação é uma função para criar entidades dentro do modelo. É o “Alô mundo!” dos pacotes de simulação.
Inicialmente, serão necessárias duas bibliotecas do Python: random – biblioteca de geração de números aleatórios – e o próprio SimPy.

Começaremos nosso primeiro programa em SimPy chamando as bibliotecas de interesse (adicionalmente, existe uma chamada para a future, mas isso é apenas para manter a função print, compatível com o Python 3):
```
# -*- coding: utf-8 -*-
from __future__ import print_function # para compatibilidade da função print com o Python 3
import random # gerador de números aleatórios
import simpy # biblioteca de simulação```

Tudo no SimPy gira em torno de processos criados pelo usuário e todos os processos vivem num environment, um “ambiente” de simulação. O programa principal começa com uma chamada ao SimPy, criando um environment “env”:

```
# -*- coding: utf-8 -*-
from __future__ import print_function # para compatibilidade da função print com o Python 3
import random # gerador de números aleatórios
import simpy # biblioteca de simulação
env = simpy.Environment() # cria o environment do modelo
```
Se você executar o programa agora, nada acontece. No momento, você apenas criou um environment, mas não criou nenhum processo, portanto, nada acontece.

Vamos escrever uma função ```
geraChegadas```
 que cria entidades no sistema enquanto durar a simulação.

Temos agora um gerador de números aleatórios, falta informar ao SimPy que queremos nossas entidades segundo essa distribuição. Isso é feito pela chamada da palavra reservada ```
yield```
 com a função do SimPy ```
env.timeout```
, que nada mais é do que uma função que causa um atraso de tempo, um delay do tempo fornecido.

Para gerar chegadas com intervalos exponenciais, a biblioteca random bem detalhada na documentação, possui a função:
```
random.expovariate(lambd)```

Onde ```
lambd```
 é a taxa de surgimento dos eventos ou, matematicamente, o inverso do tempo médio entre eventos sucessivos. No caso, se eu quero que as chegadas sejam entre intervalos de 2 min, a função ficaria:
```
yield env.timeout(random.expovariate (1/2))```

Ou seja: estamos chamando a função ```
yield env.timeout```
 que retarda o processo num tempo aleatório gerado pela função random.expovariate.

Colocando tudo junto na função ```
geraChegadas```
, temos:

Se você executar, nada acontece, pois falta chamarmos a função e informarmos ao SimPy qual o tempo de simulação. A chamada da função nos relembra que tudo em SimPy é gerar processos:

Agora sim!


**Desafio 2:** é comum que os comandos de criação de entidades nos softwares proprietários tenham a opção de limitar o número máximo de entidades geradas durante a simulação. Modifique a função ```
geraChegadas```
 de modo que ela receba como parâmetro o ```
numeroMaxChegadas```
 e limite a criação de entidades a este número. (Solução no próximo post).

**Desafio 3:** modifique a função ```
geraChegadas```
 de modo que as chegadas entre entidades sejam distribuídas segundo uma triangular de moda 1, menor valor 0,1 e maior valor 1,1.




