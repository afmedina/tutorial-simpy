# Solução dos desafios 6 e 7

**Desafio 6**: Considere que cada entidade gerada no primeiro exemplo desta seção tem um peso em gramas dado por uma distribuição normal de média 10 e desvio padrão igual a 5. Crie um critério de parada para quando a média dos pesos das entidades geradas esteja no intervalo entre 9,5 e 10,5.

Este primeiro desafio envolve poucas modificações no programa original:

```python
import random
import simpy

def geraChegada(env, p):
    media, contador, pesoTotal = 0, 0, 0
    while media > 10.5 or media < 9.5:
        print("%s: nova chegada em %s" %(p, env.now))
        yield env.timeout(1)
        contador += 1
        peso = random.normalvariate(10, 5)
        pesoTotal += peso
        media = pesoTotal/contador
        print("Média atual %.2f" %(media))
        
env = simpy.Environment()
chegadas = env.process(geraChegada(env, "p1"))
env.run()
```


**Desafio 7**: Modifique o critério anterior para que a parada ocorra quando a média for 10 com um intervalo de confiança de amplitude 0,5 e nível de significância igual a 95%. Dica: utilize a biblioteca ```numpy``` para isso (consulte o stackoverflow!).