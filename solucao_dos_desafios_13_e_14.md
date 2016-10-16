# Solução dos desafios 13 e 14

> **Desafio 13** Considere que existam dois tipos de paradas: uma do R2D2 e outra do canhão de combate. A parada do canhão de combate ocorre sempre depois de 25 horas de viagem (em quebra ou não) e seu reparo dura 2 horas. Contudo, para não perder tempo, a manutenção do canhão só é realizada quando o R2D2 quebra.

```python 
import simpy

viajando = False    #variável global que avisa se o x-wing está operando
duracaoViagem = 30  #variável global que marca a duração atual da viagem

def viagem(env, tempoParada):
    #processo de viagem do x-wing
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
    
    #ao final avisa o término da viagem e sua duração
    print("Viagem concluida em %s, duração total da viagem %s" %(env.now, env.now-partida))

def paradaTecnica(env, intervalo, viagem):
    #processo de paradas entre intervalo
    global viajando
    while duracaoViagem > 0:         #este processo só ocorre durante a viagem
        yield env.timeout(intervalo) #aguarda a próxima quebra do R2D2
        if viajando:                 # O R2D2 somente quebra durante a viagem
            viagem.interrupt()       # interrompe o processo viagem
            viajando = False
                
env = simpy.Environment()
viagem = env.process(viagem(env, 15))
env.process(paradaTecnica(env, 10, viagem))
env.run()
```

> **Desafio 14** Você não acha que pode viajar pelo espaço infinito sem encontrar alguns TEs das forças imperiais, não é mesmo? Considere que a cada 25 horas, você se depara com um TE imperial. O ataque dura 30 minutos e, se nesse tempo você não estiver com o canhão funcionando, a sua próxima viagem é para o encontro com o mestre Yoda. 

> Dica: construa uma função executaCombate que controla todo o processo de combate. Você vai precisar também de uma variável global que informa se o X-Wing está ou não em combate.

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