# Interrupções de processos

Você está todo feliz e contente atravessando a galáxia no seu X-Wing quando... PIMBA! Seu [dróide astromecânico](https://pt.wikipedia.org/wiki/R2-D2) pifou e você deve interromper a viagem para consertá-lo.

Nesta seção iremos interromper processos já em execução e depois retomar a operação inicial. A aplicação mais óbvia é para a quebra de equipamentos durante a operação, como no caso do R2D2.

A interrupção de um processo em SimPy é realizada por meio de um comando ```Interrupt``` no processo já iniciado. O cuidado aqui é que quando um recurso é interrompido por outro processo ele causa uma interrupção no Python, o que obriga a utilização de lógica do timpo ```try:...except```.


## Criando quebras de equipamento

 Voltando ao exemplo do X-wing, considere que a cada 10 horas o R2D2, interrompe a viagem para uma manutenção de 5 hora e que a viagem toda levaria (sem as paralizações) 50 horas.

Inicialmente, devemos criar uma função que representa a viagem:

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
    viajando = False
    print("Viagem concluida em %s, duração total da viagem %s" %(env.now, env.now-partida))

env = simpy.Environment()
viagem = env.process(viagem(env, 5))
env.run()```

O importante no programa anterior é notar a lógica ```try:...except:```. O ```except``` aguarda um comando novo, o ```simpy.Interrupt``` que nada mais é que uma interrupção causada por algum outro processo do environment.

Quando executado, o programa fornece uma viagem tranquila:
```
Viagem iniciada em 0
Viagem concluida em 30, duração total da viagem 30
```
Portanto, resta agora criar um processo que cria a interrupção da viagem. Note, na penúltima linha, que temos o processo em execução armazenado na variável ```viagem```. O que devemos fazer é interrompê-lo de 10 em 10 horas. Para tanto, a função paradaTecnica a seguir verifica se o processo de viagem está em andamento e paraliza a operação depois de 10 horas:

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
    viajando = False
    print("Viagem concluida em %s, duração total da viagem %s" %(env.now, env.now-partida))

def paradaTecnica(env, intervalo, viagem):
    #processo de paradas entre intervalo
    global duracaoViagem
    global viajando
    while duracaoViagem > 0:         #este processo só ocorre durante a viagem
        yield env.timeout(intervalo) #aguarda a próxima quebra do R2D2
        if viajando:                 # O R2D2 somente quebra durante a viagem
            viagem.interrupt()       # interrompe o processo viagem
            viajando = False
                
env = simpy.Environment()
viagem = env.process(viagem(env, 5))
env.process(paradaTecnica(env, 10, viagem))
env.run()
```
Quando executado, o programa fornece:
```
Viagem iniciada em 0
Falha do R2D2 em 10, tempo de viagem estimado 20
Viagem iniciada em 15
Falha do R2D2 em 20, tempo de viagem estimado 15
Viagem iniciada em 25
Falha do R2D2 em 30, tempo de viagem estimado 10
Viagem iniciada em 35
Falha do R2D2 em 40, tempo de viagem estimado 5
Viagem iniciada em 45
Falha do R2D2 em 50, tempo de viagem estimado 0
Viagem concluida em 55, duração total da viagem 55
```
Alguns aspectos importantes do código anterior:
1. A utilização de variáveis globais foi fundamental para informar ao processo de parada o status do processo de viagem. 
2. Como a execução ```env.run()``` não tem um tempo final pré-estabelecido, a execução dos processos é terminada quando o ```while duracaoViagem > 0``` torna-se falso. Note que esse while deve existir nos dois processos em execução, caso contrário o programa seria executado indefinidamente.
3. Dentro da função paradaTecnica a variável global ```viajando``` impede que ocorram duas quebras ao mesmo tempo. Naturalmente o leitor atento sabe que isso jamais ocorreria, afinal o tempo de duração da quebra é inferior ao intervalo entre quebras. Mas fica o exercício: execute o mesmo programa, agora para uma duração de quebra de 15 horas.

##Desafios

Considere que existam dois tipos de paradas: uma do R2D2 e outra do canhão de combate. A parada do canhão de combate ocorre sempre depois de 25 horas de viagem (em quebra ou não) e seu reparo dura 2 horas. Contudo, para não perder tempo, a manutenção do canhão só é realizada quando o R2D2 quebra.

Você não acha que pode viajar pelo espaço infinito sem encontrar alguns TEs das forças imperiais, não é mesmo? Considere que a cada 25 horas, você se depara com um TE imperial. O ataque dura 30 minutos e, se nesse tempo você não estiver com o canhão funcionando, a sua próxima viagem é para o encontro com o mestre Yoda. 

Dica: construa uma função executaCombate que controla todo o processo de combate. Você vai precisar também de uma variável global que informe se o X-Wing está ou não em combate.
