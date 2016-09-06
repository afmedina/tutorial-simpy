# Container: enchendo ou esvaziando caixas, tanques ou objetos

Um tipo especial de recurso no SimPy é o `conteiner`. Intuitivamente, um `conteiner` seria um taque ou caixa em que se armazenam coisas. Você pode encher ou esvaziar em quantidade, como se fosse um tanque de líquido ou uma caixa de laranjas.

A sua utilização é bem simples, por exemplo, podemos modelar um tanque de 1.000 litros de capacidade, com um estoque inicial de 500 litros, por meio do seguinte código:

```python
import simpy

env = simpy.Environment()
#cria um tanque de 1000 litros, com 500 litros no início da simulação
tanque = simpy.Container(env, capacity=1000, init=500)
```

O `container `possui três comandos importantes:

* Para encher: `tanque.put(quantidade)`
* Para esvaziar: `tanque.get(quantidade)`
* Para obter o nível atual: `tanque.level`

O código a seguir, enche o tanque com mais 100 litros, imprime na tela o nível atual do tanque e esvazia 200 litros do tanque:

```python
import simpy

def exemploTanque(env, tanque):
    yield tanque.put(100)     #coloca 100 litros no tanque
    print("Nível atual do tanque %d" % tanque.level)
    yield tanque.get(200)      #retira 200 litros do tanque
    print("Nível atual do tanque %d" % tanque.level)

env = simpy.Environment()
#cria um tanque de 1000 litros, com 500 litros no início da simulação
tanque = simpy.Container(env, capacity=1000, init=500)
env.process(exemploTanque(env,tanque))
env.run()
```

## Desafios

**Desafio 15:** considere, no exemplo anterior, que a taxa de enchimento do tanque é de 1 litro\/min e a de esvaziamento é de 2 litros\/min. Altere o modelo para que ele incorpore os tempos de enchimento e esvaziamento. Crie duas funções diferentes, uma para encher e outra para evaziar.
**Desafio 16:** continuando o exemplo, crie uma função que de 5 em 5 minutos retira 100 litros do tanque. Crie uma função "sensor" capaz de identificar quando o tanque fica abaixo de 200 litros. Nesse momento, a função deve chamar um processo de enchimento do tanque até sua capacidade máxima.

