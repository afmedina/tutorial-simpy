# Solução dos desafios 15 e 16

> **Desafio 15:** considere, no exemplo do posto, que a taxa de enchimento do tanque é de 1 litro/min e a de esvaziamento é de 2 litros/min. Altere o modelo para que ele incorpore os tempos de enchimento e esvaziamento, bem como forneça o tempo que o veículo aguardou na fila por atendimento.

Neste caso, são criadas duas constantes:
```python
TAXA_VEICULO = 2            # taxa de bombeamento do veículo
TAXA_CAMINHAO = 1           # taxa de bombeamento do caminhãoon
```
As funções de enchimento e esvaziamento do tanque devem ser modificadas para considerar o tempo de espera que os veículos e caminhões aguardam até que o processo de bombeamento tenha terminado, como representado nas funções a seguir:
```python
def esvaziamentoTanque(env, qtd, tanque):
    # esvazia o tanque
    print("%d Novo veículo de %3.2f m3.\t Nível atual: %5.1f m3" % (env.now, qtd, tanque.level))
    yield tanque.get(qtd)
    print("%d Tanque esvaziado de %3.2f m3.\t Nível atual: %5.1f m3" % (env.now, qtd, tanque.level))

def enchimentoTanque(env, qtd, tanque):  
    # enche o tanque
    print("%d Novo caminhão com %4.1f m3.\t Nível atual: %5.1f m3" % (env.now, qtd, tanque.level))
    yield tanque.put(qtd)
    print("%d Tanque enchido com %4.1f m3.\t Nível atual: %5.1f m3" % (env.now, qtd, tanque.level))
```


> **Desafio 16:** continuando o exemplo, modifique o modelo de modo que ele represente a situação em que o tanque não pode ser enchido e esvaziado simultâneamente.

##Teste seus conhecimentos
1. Modifique o problema para considerar que existam 3 bombas de combustível no posto, capazes de atender aos veículos simultâneamente do mesmo tanque.
2. Construa um gráfico (utilizando a biblioteca ```[matplotlib](http://matplotlib.org/)```) do nível do tanque ao longo do tempo.
