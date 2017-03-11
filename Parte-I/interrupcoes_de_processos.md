# Interrupções de processos: `simpy.Interrupt`

Você está todo feliz e contente atravessando a galáxia no seu [X-Wing](https://en.wikipedia.org/wiki/X-wing_fighter) quando... PIMBA! Seu [dróide astromecânico](https://pt.wikipedia.org/wiki/R2-D2) pifa e só lhe resta interromper a viagem para consertá-lo, antes que apareça um maldito caça [TIE](https://en.wikipedia.org/wiki/TIE_fighter) das forças imperiais.

Nesta seção iremos interromper processos já em execução e depois retomar a operação inicial. A aplicação mais óbvia é para a quebra de equipamentos durante a operação, como no caso do R2D2.

A interrupção de um processo em SimPy é realizada por meio de um comando `Interrupt` aplicado ao processo já iniciado. O cuidado aqui é que quando um recurso é interrompido por outro processo ele causa uma interrupção, de fato, no Python, o que nos permite utilizar o bloco de controle de interrupção`try:...except`, o que não deixa de ser uma boa coisa, dada a sua facilidade.

## Criando quebras de equipamento

Voltando ao exemplo do X-Wing, considere que a cada 10 horas o R2D2 interrompe a viagem para uma manutenção de 5 horas e que a viagem toda levaria \(sem não houvessem paralisações\) 50 horas.

Inicialmente, vamos criar duas variáveis globais: uma para representar se o X-Wing está operando - afinal, não queremos interrompê-lo quando ele já estiver em manutenção - e outra para armazenar o tempo ainda restante para a viagem.

```python
import simpy

viajando = False    # variável global que avisa se o x-wing está operando
duracaoViagem = 30  # variável global que marca a duração atual da viagem
```

O próximo passo, é criar uma função que represente a viagem do x-wing, garantindo não só que ela dure o tempo correto, mas também que lide com o processo de interrupção:

```python
import simpy

viajando = False        # variável global que avisa se o x-wing está operando
duracaoViagem = 30      # variável global que marca a duração atual da viagem

def viagem(env, tempoParada):
    #processo de viagem do x-wing
    global viajando, duracaoViagem

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

    # ao final avisa o término da viagem e sua duração
    print("%5.1f Viagem concluida\tDuração total da viagem: %4.1f horas" 
            %(env.now, env.now-partida))


env = simpy.Environment()
viagem = env.process(viagem(env, 15))

env.run()
```

O importante no programa anterior é notar o bloco `try:...except:,` interno ao laço `while duracaoViagem > 0,` que mantém o nosso X-Wing em processo enquanto a variável `duracaoViagem` for maior que zero. O `except` aguarda um novo comando, o `simpy.Interrupt`, que nada mais é do que uma interrupção causada por algum outro processo dentro do `Environment.`

Quando executado, o programa fornece uma viagem tranquila:

```
  0.0 Viagem iniciada
 30.0 Viagem concluida  Duração total da viagem: 30.0 horas
```

A viagem é tranquila, pois não criamos ainda um "gerador de interrupções", que nada mais é do que um processo em SimPy que cria a interrupção da viagem.

Note, na penúltima linha do código anterior, que o processo em execução foi armazenado na variável `viagem` e oque devemos fazer é interrompê-lo de 10 em 10 horas. Para tanto, a função `paradaTecnica` a seguir, verifica se o processo de viagem está em andamento e paralisa a operação depois de 10 horas:

```python
def paradaTecnica(env, intervaloQuebra, viagem):
    # processo de paradas entre intervalos de quebra
    global viajando, duracaoViagem

    while duracaoViagem > 0:                # este processo só ocorre durante a viagem
        yield env.timeout(intervaloQuebra)  # aguarda a próxima quebra do R2D2
        if viajando:                        # R2D2 somente quebra durante a viagem
            viagem.interrupt()              # interrompe o processo viagem
            viajando = False                # desliga a viagem 

env = simpy.Environment()
viagem = env.process(viagem(env, 15))
env.process(paradaTecnica(env, 10, viagem))

env.run()
```

A função `paradaTecnica,`portanto, recebe como parâmetro o próprio _objeto_ que representa o processo `viagem` e, por meio do comando:

```python
viagem.interrupt()
```

Provoca uma interrupção no processo, a ser reconhecida pela função `viagem` na linha:

```python
except simpy.Interrupt:
```

Adicionalmente, o processo parada técnica também deve ser inciado ao início da simulação, de modo que a parte final do modelo fica:

```python
env = simpy.Environment()
viagem = env.process(viagem(env, 15))
env.process(paradaTecnica(env, 10, viagem))

env.run()
```

Quando executado, o modelo completo fornece como saída:

```python
  0.0 Viagem iniciada
 10.0 Falha do R2D2     Tempo de viagem restante: 20.0 horas
 25.0 Viagem iniciada
 30.0 Falha do R2D2     Tempo de viagem restante: 15.0 horas
 45.0 Viagem iniciada
 50.0 Falha do R2D2     Tempo de viagem restante: 10.0 horas
 65.0 Viagem iniciada
 70.0 Falha do R2D2     Tempo de viagem restante:  5.0 horas
 85.0 Viagem iniciada
 90.0 Falha do R2D2     Tempo de viagem restante:  0.0 horas
105.0 Viagem concluida  Duração total da viagem: 105.0 horas
```

Alguns aspectos importantes do código anterior:

1. A utilização de variáveis globais foi fundamental para informar ao processo de parada o status do processo de viagem. É por meio de variáveis globais que um processo "sabe" o que está ocorrendo no outro;
2. Como a execução `env.run()` não tem um tempo final pré-estabelecido, a execução dos processos é terminada quando o laço:

   ```python
   while duracaoViagem > 0
   ```

   Torna-se falso. Note que esse `while` deve existir nos dois processos em execução, caso contrário, o programa seria executado indefinidamente;

3. Dentro da função `paradaTecnica` a variável global `viajando` impede que ocorram duas quebras ao mesmo tempo. Naturalmente o leitor atento sabe que isso jamais ocorreria, afinal, o tempo de duração da quebra é inferior ao intervalo entre quebras. Mas fica o exercício: execute o mesmo programa, agora para uma duração de quebra de 15 horas e veja o que acontece.
4. Se um modelo possui uma lógica de interrupção `.interrupt()` e não possui um comando `except simpy.Interrupt` para lidar com a paralização do processo, o SimPy finalizará a simulação retornando o erro:

   ```python
   Interrupt: Interrupt(None)
   ```

   Na próxima seção é apresentada uma alternativa para manter o processamento da simulação.



