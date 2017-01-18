## Desafio
> Desafio 26: acrescente à função `final` um comando para armazenar quem venceu e em que tempo. Simule para 10 replicações e calcule a média e a porcentagem de vitórias de cada corredor. 

Neste caso, podemos criar uma lista `resultadoList` para armazenar a `tuple` (tempo, vencedor) de cada replicação. Os valores podem ser armazenados no instante em que a função `campeão` idenfica o vencedor, isto é:
```python
def campeao(event):
    global vencedor

    if not vencedor:
        # imprime a faixa de campeão
        print('%3.1f \o/ Tan tan tan (musica do Senna) A %s é a campeã!'
                    %(env.now, event.value))
        # atualiza a variável global vencedor
        vencedor = True
        # armazena o resultado na lista resultadoList
        resultadoList.append((env.now, event.value))

    else:
        # imprime o perdedor
        print('%3.1f A %s chega em segundo lugar...'
                    %(env.now, event.value))
```
Como o desafio pede que sejam executadas 10 replicações da corrida, devemos modificar a chamada do modelo para refletir isso. Incialmente, criamos a lista `resultadoList` e, a seguir, criamos um laço para executar o modelo 10 replicações:
```python
# lista para armazenar os resultados das corridas/replicações
resultadoList = []
random.seed(10)

# processa 10 replicações
for i in range(10):
    # True, se já temos um vencedor na corrida, False caso contrário
    vencedor = False
    env = simpy.Environment()
    proc = env.process(corrida(env))
    proc.callbacks.append(final)
    # executa até que o processo corrida termine
    env.run(proc)
```
Note que a variável global `vencedor` é atualizada dentro do laço (na seção seguinte, ela era criada logo no cabeçalho do modelo), afinal, a cada replicação precisamos garantir que as variáveis do modelo sejam reinicializadas.

Uma vez que as 10 replicações tenham sido executadas, basta calcular as estatísiticas desejadas. O número de vitórias é facilmente extraída da lista de vencedores:

```python
# separa a lista de resultados em duas listas
tempos, vencedores = zip(*resultadoList)
# conta o número de vitórias
lebreWin = vencedores.count('lebre')
tartarugaWin = vencedores.count('tartaruga')

# calcula a percentagem de vitórias da lebre
lebreP = lebreWin/(lebreWin+tartarugaWin)
```
Para o cálculo da média do tempo de corrida, temos diversas possibilidades. A escolhida aqui foi utilizar a função `mean` da biblioteca `numpy`:
```python
# importa a função para cálculo da média a partir biblioteca numpy
from numpy import mean

print('Tempo médio de corrida: %3.1f\tLebre venceu: %3.1f%%\tTartaruga venceu: %3.1f%%'
        % (mean(tempos), lebreP*100, (1-lebreP)*100))
```
Quando executado, o modelo fornece como resposta:
```python
0.0 Iniciada a corrida!
5.3 \o/ Tan tan tan (música do Senna) A tartaruga é a campeã!
5.3 Ok pessoal, a corrida acabou.
0.0 Iniciada a corrida!
5.1 \o/ Tan tan tan (música do Senna) A tartaruga é a campeã!
5.1 Ok pessoal, a corrida acabou.
0.0 Iniciada a corrida!
4.4 \o/ Tan tan tan (música do Senna) A tartaruga é a campeã!
4.4 Ok pessoal, a corrida acabou.
0.0 Iniciada a corrida!
6.1 \o/ Tan tan tan (música do Senna) A lebre é a campeã!
6.1 Ok pessoal, a corrida acabou.
0.0 Iniciada a corrida!
5.4 \o/ Tan tan tan (música do Senna) A lebre é a campeã!
5.4 Ok pessoal, a corrida acabou.
0.0 Iniciada a corrida!
0.5 \o/ Tan tan tan (música do Senna) A lebre é a campeã!
0.5 Ok pessoal, a corrida acabou.
0.0 Iniciada a corrida!
4.8 \o/ Tan tan tan (música do Senna) A lebre é a campeã!
4.8 Ok pessoal, a corrida acabou.
0.0 Iniciada a corrida!
3.5 \o/ Tan tan tan (música do Senna) A lebre é a campeã!
3.5 Ok pessoal, a corrida acabou.
0.0 Iniciada a corrida!
4.9 \o/ Tan tan tan (música do Senna) A lebre é a campeã!
4.9 Ok pessoal, a corrida acabou.
0.0 Iniciada a corrida!
5.4 \o/ Tan tan tan (música do Senna) A tartaruga é a campeã!
5.4 Ok pessoal, a corrida acabou.

Tempo médio de corrida: 4.5     Lebre venceu: 60.0%     Tartaruga venceu: 40.0%
```
## Teste seu conhecimento
1. Acrescente o cálculo do intervalo de confiança ao resultados do tempo médio de corrida e simule um número de replicações suficientes para garantir que este intervalo seja no máximo de 5% em torno da média, para um nível de significância de 95%.
2. Reformule o modelo para que ele aceite uma lista de corredores diferentes, não só uma lebre e uma tartaruga. 
