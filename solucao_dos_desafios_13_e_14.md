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
    #processo de viagem do x-wing
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

> **Desafio 14** Você não acha que pode viajar pelo espaço infinito sem encontrar alguns TEs das forças imperiais, não é mesmo? Considere que a cada 25 horas, você se depara com um TE imperial. O ataque dura 30 minutos e, se nesse tempo você não estiver com o canhão funcionando, a sua próxima viagem é para o encontro do mestre Yoda.

> Dica: construa uma função executaCombate que controla todo o processo de combate. Você vai precisar também de uma variável global que informa se o X-Wing está ou não em combate.

Incialmente, precisamos de uma variável global para verificar a situação do canhão:
```python 
import simpy

canhao = True
viajando = False    #variável global que avisa se o x-wing está operando
duracaoViagem = 50  #variável global que marca a duração atual da viagem

def viagem(env, tempoParada, tempoParadaCanhao):
    #processo de viagem do x-wing
    global canhao
    global viajando
    global duracaoViagem
    
    partida = env.now         #inicio da viagem
    while duracaoViagem > 0:  #enquanto ainda durar a viagem, execute:
        try:
            viajando = True
            inicioViagem = env.now #(re)inicio da viagem
            print("Viagem iniciada em %s" %(env.now))
            yield env.timeout(duracaoViagem) #tempo de viagem restante
            duracaoViagem -= env.now-inicioViagem
        except simpy.Interrupt:
            #se o processo de viagem foi interrompido execute:
            duracaoViagem -= env.now-inicioViagem #atualiza o tempo restante de viagem
            print("Falha do R2D2 em %s, tempo de viagem estimado %s" %(env.now, duracaoViagem ))
            yield env.timeout(tempoParada) #tempo de manutenção do R2D2
            if not canhao:
                yield env.timeout(tempoParadaCanhao) #tempo de manutenção do canhão
                canhao = True
                print("Canhão operante em %s" % (env.now))
    
    #ao final avisa o término da viagem e sua duração
    viajando, canhao = False, False
    print("Viagem concluida em %s, duração total da viagem %s" %(env.now, env.now-partida))

def paradaTecnica(env, intervalo, viagem):
    #processo de paradas entre intervalo
    global viajando
    global duracaoViagem
    while duracaoViagem > 0:         #este processo só ocorre durante a viagem
        yield env.timeout(intervalo) #aguarda a próxima quebra do R2D2
        if viajando:                 # O R2D2 somente quebra durante a viagem
            viagem.interrupt()       # interrompe o processo viagem
            viajando = False
            
def quebraCanhao(env, intervalo, combate):
    #processo de paradas entre intervalo
    global canhao
    global duracaoViagem
    while duracaoViagem > 0:            #este processo só ocorre durante a viagem
        yield env.timeout(intervalo)    #aguarda a próxima quebra do canhao
        if canhao:
            canhao = False
            print("Canhão inoperante em %s" % (env.now))
            if emCombate:
                combate.interrupt()

def executaCombate(env, intervalo, duracaoCombate):
    #processo de paradas entre intervalo
    global emCombate
    global canhao
    global duracaoViagem
    emCombate = False
    while duracaoViagem > 0:            #este processo só ocorre durante a viagem
        yield env.timeout(intervalo)    #aguarda o próximo encontro com forças imperirais
        emCombate = True                #inicio do combate
        if not canhao:
            print("Fim da viagem. O lado negro venceu em %s" %(env.now))
            duracaoViagem = 0
        else:
            print("Combate iniciado em %s. Reze para que o canhão não quebre!" %(env.now))
            try:
                yield env.timeout(duracaoCombate)
                emCombate = False
                print("Fim do combate em %d. R2D2 diz: tá tudo tranquilo, tá tudo normalizado." %(env.now))
            except simpy.Interrupt:
                print("OPS... O canhão quebrou durante o combate.")
                print("Fim da viagem. O lado negro venceu em %s" % (env.now))
                duracaoViagem = 0
                                
                                
env = simpy.Environment()
viagem = env.process(viagem(env, 5, 2))
combate = env.process(executaCombate(env, 25, 0.5))
env.process(paradaTecnica(env, 10, viagem))
env.process(quebraCanhao(env, 25, combate))
env.run(until=combate)
``` 