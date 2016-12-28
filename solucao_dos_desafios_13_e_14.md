# Solução dos desafios 13 e 14

> **Desafio 13** Considere que existam dois tipos de paradas: uma do R2D2 e outra do canhão de combate. A parada do canhão de combate ocorre sempre depois de 25 horas de viagem (em quebra ou não) e seu reparo dura 2 horas. Contudo, para não perder tempo, a manutenção do canhão só é realizada quando o R2D2 quebra.

Inicialmente, precisamos de uma variável global para verificar a situação do canhão:
```python 
import simpy

canhao = True           # variável global que avisa se o canhão está funcionando
viajando = False        # variável global que avisa se o x-wing está operando
duracaoViagem = 30      # variável global que marca a duração atual da viagem
```
A função viagem, agora deve lidar com um tempo de parada do canhão. Contudo, não existe uma interrupção para o canhão, pois nosso indomável piloto jedi apenas verifica a situação do canhão ao término do concerto do R2D2:

```python 
def viagem(env, tempoParada, tempoParadaCanhao):
    # processo de viagem do x-wing
    global viajando, duracaoViagem, canhao
    
    partida = env.now         # início da viagem
    while duracaoViagem > 0:  # enquanto ainda durar a viagem, execute:
        try:
            viajando = True
            # (re)inicio da viagem
            inicioViagem = env.now 
            print("%5.1f Viagem iniciada" %(env.now))
            # tempo de viagem restante
            yield env.timeout(duracaoViagem) 
            duracaoViagem -= env.now - inicioViagem
            
        except simpy.Interrupt:
            # se o processo de viagem foi interrompido execute
            # atualiza o tempo restante de viagem
            duracaoViagem -= env.now - inicioViagem 
            print("%5.1f Falha do R2D2\tTempo de viagem restante: %4.1f horas" 
                    %(env.now, duracaoViagem))
            # tempo de manutenção do R2D2
            yield env.timeout(tempoParada)
            print("%5.1f R2D2 operante" %env.now)
            # se o canhão não estiver funcionando
            if not canhao:
                print("%5.1f R2, ligue o canhão!" % env.now)
                # tempo de manutenção do canhão
                yield env.timeout(tempoParadaCanhao)
                canhao = True
                print("%5.1f Pi..bi...bi\tTradução: canhão operante!" % env.now)
    
    # ao final avisa o término da viagem e sua duração
    print("%5.1f Viagem concluida\tDuração total da viagem: %4.1f horas" 
            %(env.now, env.now-partida))
```

Além da função de parada técnica (já pertencente ao nosso modelo desde a seção anterior), precisamos de uma função que tire de operação o canhão, ou seja, apenas desligue a variável global `canhao:`
```python
def quebraCanhao(env, intervaloCanhao):
    # processo de quebra do canhao entre intervalos definidos
    global canhao, duracaoViagem
    
    while duracaoViagem > 0:                # este processo só ocorre durante a viagem
        yield env.timeout(intervaloCanhao)  # aguarda a próxima quebra do canhao
        if canhao:
            canhao = False
            print("%5.1f Pi uiui...bi\tTradução: canhão inoperante!" % (env.now))
```
Por fim, o processo de quebra do canhão deve ser inciado juntamente com o resto do modelo de simulação:
```python
env = simpy.Environment()
viagem = env.process(viagem(env, 15, 2))
env.process(paradaTecnica(env, 10, viagem))
env.process(quebraCanhao(env, 25))

env.run()
```
Quando o modelo completo é executado, ele fornece como saída:
```python
  0.0 Viagem iniciada
 10.0 Falha do R2D2     Tempo de viagem restante: 20.0 horas
 25.0 Pi uiui...bi      Tradução: canhão inoperante!
 25.0 R2D2 operante
 25.0 R2, ligue o canhão!
 27.0 Pi..bi...bi       Tradução: canhão operante!
 27.0 Viagem iniciada
 30.0 Falha do R2D2     Tempo de viagem restante: 17.0 horas
 45.0 R2D2 operante
 45.0 Viagem iniciada
 50.0 Pi uiui...bi      Tradução: canhão inoperante!
 50.0 Falha do R2D2     Tempo de viagem restante: 12.0 horas
 65.0 R2D2 operante
 65.0 R2, ligue o canhão!
 67.0 Pi..bi...bi       Tradução: canhão operante!
 67.0 Viagem iniciada
 70.0 Falha do R2D2     Tempo de viagem restante:  9.0 horas
 75.0 Pi uiui...bi      Tradução: canhão inoperante!
 85.0 R2D2 operante
 85.0 R2, ligue o canhão!
 87.0 Pi..bi...bi       Tradução: canhão operante!
 87.0 Viagem iniciada
 90.0 Falha do R2D2     Tempo de viagem restante:  6.0 horas
100.0 Pi uiui...bi      Tradução: canhão inoperante!
105.0 R2D2 operante
105.0 R2, ligue o canhão!
107.0 Pi..bi...bi       Tradução: canhão operante!
107.0 Viagem iniciada
110.0 Falha do R2D2     Tempo de viagem restante:  3.0 horas
125.0 Pi uiui...bi      Tradução: canhão inoperante!
125.0 R2D2 operante
125.0 R2, ligue o canhão!
127.0 Pi..bi...bi       Tradução: canhão operante!
127.0 Viagem iniciada
130.0 Falha do R2D2     Tempo de viagem restante:  0.0 horas
145.0 R2D2 operante
145.0 Viagem concluida  Duração total da viagem: 145.0 horas
150.0 Pi uiui...bi      Tradução: canhão inoperante!
```

> **Desafio 14** Você não acha que pode viajar pelo espaço infinito sem encontrar alguns [TIEs](https://en.wikipedia.org/wiki/TIE_fighter) das forças imperiais, não é mesmo? Considere que a cada 25 horas, você se depara com um TIE imperial. O ataque dura 30 minutos e, se nesse tempo você não estiver com o canhão funcionando, a sua próxima viagem é para o encontro do mestre Yoda.

> Dica: construa uma função executaCombate que controla todo o processo de combate. Você vai precisar também de uma variável global que informa se o X-Wing está ou não em combate.

Incialmente, precisamos de uma variável global para verificar a situação do combate:
```python 
import simpy

emCombate = False       # variável global que avisa se o x-wing está em combate
canhao = True           # variável global que avisa se o canhão está funcionando
viajando = False        # variável global que avisa se o x-wing está operando
duracaoViagem = 30      # variável global que marca a duração atual da viagem
```
A função `executaCombate` a seguir, incia o processo de combate e verifica quem foi o vitorioso:

```python 
def executaCombate(env, intervaloCombate, duracaoCombate):
    # processo de execução do combate

    global emCombate, canhao, duracaoViagem
    
    while duracaoViagem > 0: # este processo só ocorre durante a viagem
        # aguarda o próximo encontro com as forças imperirais
        yield env.timeout(intervaloCombate)
        # inicio do combate
        emCombate = True 
        if not canhao:
            print("%5.1f Fim da viagem\tO lado negro venceu" %env.now)
            break
        else:
            print("%5.1f Combate iniciado\tReze para que o canhão não quebre!"
                    %env.now)
            try:
                yield env.timeout(duracaoCombate)
                emCombate = False
                print("%5.1f Fim do combate\tR2D2 diz: tá tudo tranquilo, tá tudo normalizado."
                        %env.now)
            except simpy.Interrupt:
                print("%5.1f OPS... O canhão quebrou durante o combate." %env.now)
                print("%5.1f Fim da viagem\tO lado negro venceu" %env.now)
                break
```
A quebra de canhão agora deve verificar se a nave está em combate, pois, neste caso, o X-Wing será esmagado pelo TIE:

```python 
def quebraCanhao(env, intervaloCanhao, combate):
    # processo de quebra do canhao entre intervalos definidos
    global canhao, duracaoViagem, emCombate
    
    while duracaoViagem > 0:                # este processo só ocorre durante a viagem
        yield env.timeout(intervaloCanhao)  # aguarda a próxima quebra do canhao
        if canhao:
            canhao = False
            print("%5.1f Pi uiui...bi\tTradução: canhão inoperante!" % (env.now))
            if emCombate:
                combate.interrupt()
```
Finalmente, a incialização do modelo deve contar com uma chamada para o processo `executaCombate:`

```python 

env = simpy.Environment()
viagem = env.process(viagem(env, 15, 2))
combate = env.process(executaCombate(env, 20, 0.5))
env.process(paradaTecnica(env, 10, viagem))
env.process(quebraCanhao(env, 25, combate))

env.run(until=combate)
``` 
A última linha do código anterior tem algo importante: optei por executar a simulação enquanto durar o processo de combate, afinal, ele mesmo só é executado caso a X-Wing esteja ainda em viagem.

Por fim, quando executado, o modelo completo fornece como saída:
```python 
  0.0 Viagem iniciada
 10.0 Falha do R2D2     Tempo de viagem restante: 20.0 horas
 20.0 Combate iniciado  Reze para que o canhão não quebre!
 20.5 Fim do combate    R2D2 diz: tá tudo tranquilo, tá tudo normalizado.
 25.0 Pi uiui...bi      Tradução: canhão inoperante!
 25.0 R2D2 operante
 25.0 R2, ligue o canhão!
 27.0 Pi..bi...bi       Tradução: canhão operante!
 27.0 Viagem iniciada
 30.0 Falha do R2D2     Tempo de viagem restante: 17.0 horas
 40.5 Combate iniciado  Reze para que o canhão não quebre!
 41.0 Fim do combate    R2D2 diz: tá tudo tranquilo, tá tudo normalizado.
 45.0 R2D2 operante
 45.0 Viagem iniciada
 50.0 Pi uiui...bi      Tradução: canhão inoperante!
 50.0 Falha do R2D2     Tempo de viagem restante: 12.0 horas
 61.0 Fim da viagem     O lado negro venceu
``` 
## Teste seus conhecimentos
1. Não colocamos distribuições aleatórias nos processos. Acrecente distribuições nos diversos processos e verifique se o modelo precisa de alterações;
2. Acrescente a tentativa da destruição da Estrela da Morte ao final da viagem: com 50% de chances, nosso intréptido jedi consegue acertar um tiro na entrada do reator e explodir a Estrela da Morte (se ele erra, volta ao combate). Replique algumas vezes o modelo e estime a probabilidade de sucesso da operação.

