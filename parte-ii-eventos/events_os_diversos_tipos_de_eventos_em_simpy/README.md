# Events: os diversos tipos de Eventos em SimPy

Nesta seção discutiremos comandos que lhe darão o poder de criar, manipular ou disparar seus próprios eventos, de modo independente dos processos já discutidos nas seções anteriores.

Mas com todo o poder, vem também a responsabilidade!

Atente-se para o fato de que, sem o devido cuidado, o seu modelo pode ficar um pouco confuso. Isto porque um evento pode ser criado a qualquer momento e fora do contexto original do processo em execução, naturalmente aumentando a complexidade do código.

## Criando um evento isolado com `event()`

Considere um problema simples de controle de turno de abertura e fechamento de uma ponte elevatória. A ponte abre para automóveis, opera por 5 minutos, fecha e permite a passagem de embarcações no cruzamento por mais 5 minutos.

Naturalmente, esse modelo poderia ser implementado com os comandos já discutidos neste livro, contudo, a ideia desta seção é demonstrar como criar um evento específico que informe à ponte que ela deve fechar, algo semelhante a um sinal semafórico.

Em SimPy, um evento é criado pelo comando `env.event():`

```python
abrePonte = env.event()            # cria o evento abrePonte
```

Criar um evento, não significa que executá-lo. Criar um evento significa apenas criá-lo na memória. Para processar um evento, isto é, marcá-lo como executado, utilizamos o método `.succeed():`

```python
yield abrePonte.succeed()          # marca o evento abrePonte como executado
```

Podemos utilizar o evento criado de diversas formas em um modelo. Por exemplo, com o comando `yield` podemos fazer um processo aguardar até que o evento criado seja processado, com a linha:

```python
yield abrePonte                    # aguarda até que o evento abrePonte seja processado
```

Retornando ao exemplo da ponte, criaremos um processo que representará o funcionamento da ponte. Inicialmente a ponte estará fechada e aguardará até que o evento `abrePonte` seja processado:

```python
def ponteElevatoria(env):
    # opera a ponte elevatória
    global abrePonte

    print('%2.0f A ponte está fechada =(' %(env.now))
    # aguarda o evento para abertura da ponte
    yield abrePonte
    print('%2.0f A ponte está aberta  =)' %(env.now))
```

Note que `abrePonte`é tratado como uma variável global e isso significa que alguma outra função deve criá-lo e processá-lo, de modo que nossa função `ponteElevatória` abra a ponte no instante correto da simulação.

Assim, criaremos uma função geradora `turno` que representará o processo de controle do turno de abertura/fechamento da ponte e que será responsável por criar e processar o evento de abertura da mesma:

```python
def turno(env):
    # abre e fecha a ponte
    global abrePonte

    while True:
        # cria evento para abertura da ponte
        abrePonte = env.event()
        # inicia o processo da ponte elvatória
        env.process(ponteElevatoria(env))
        # mantém a ponte fechada por 5 minutos
        yield env.timeout(5)
        # processa o evento de abertura da ponte
        yield abrePonte.succeed()
        # mantém a ponte aberta por 5 minutos
        yield env.timeout(5)
```

Note, na função anterior, que o evento é criado, mas **não é processado** imediatamente. De fato, ele só é processado quanto o método `abrePonte.succeed()` é executado, após o tempo de espera de 5 minutos.

Como queremos que a ponte funcione continuamente, um novo evento deve ser criado para representar o novo ciclo de abertura e fechamento. Isso está representado no início do laço com a linha:

```python
# cria evento para abertura da ponte
abrePonte = env.event()
```

Precisamos deixar isso bem claro, paciente leitor: uma vez processado com o método `.succeed(),` o evento é extinto e caso seja necessário executá-lo novamente, teremos de recriá-lo com `env.event().`

Juntando tudo num único modelo de abre/fecha da ponte elevatória, temos:

```python
import simpy

def turno(env):
    # abre e fecha a ponte
    global abrePonte

    while True:
        # cria evento para abertura da ponte
        abrePonte = env.event()
        # inicia o processo da ponte elvatória
        env.process(ponteElevatoria(env))
        # mantém a ponte fechada por 5 minutos
        yield env.timeout(5)
        # processa o evento de abertura da ponte
        yield abrePonte.succeed()
        # mantém a ponte aberta por 5 minutos
        yield env.timeout(5)

def ponteElevatoria(env):
    # opera a ponte elevatória
    global abrePonte

    print('%2.0f A ponte está fechada =(' %(env.now))
    # aguarda o evento para abertura da ponte
    yield abrePonte
    print('%2.0f A ponte está aberta  =)' %(env.now))

env = simpy.Environment()

# inicia o processo de controle do turno
env.process(turno(env))

env.run(until=20)
```

Quando executado por 20 minutos, o modelo anterior fornece:

```text
 0 A ponte está fechada =(
 5 A ponte está aberta  =)
10 A ponte está fechada =(
15 A ponte está aberta  =)
```

No exemplo anterior, fizemos uso de uma variável global, `abrePonte`, para enviar a informação de que o evento de abertura da ponte foi disparado.

Isso é bom, mas também pode ser ruim =\).

Note que o evento de abertura da ponte é criado e processado dentro da função `turno(env),` portanto, **fora** da função que controla o processo de abertura e fechamento da ponte, `ponteElevatoria(env).`As coisas podem realmente ficar confusas no seu modelo, caso você não tome o devido cuidado.

O método`.succeed()` ainda pode enviar um valor como parâmetro:

```python
meuEvento.succeed(value=valor)
```

Poderíamos, por exemplo, enviar à função `ponteElevatoria` o tempo previsto para que a ponte fique aberta. O modelo a seguir, por exemplo, transfere o tempo de abertura \(5 minutos\) à função `ponteElevatoria` que o armazena na variável `tempoAberta:`

```python
import simpy

def turno(env):
    # abre e fecha a ponte
    global abrePonte

    while True:
        # cria evento para abertura da ponte
        abrePonte = env.event()
        # inicia o processo da ponte elvatória
        env.process(ponteElevatoria(env))
        # mantém a ponte fechada por 5 minutos
        yield env.timeout(5)
        # dispara o evento de abertura da ponte
        yield abrePonte.succeed(value=5)
        # mantém a ponte aberta por 5 minutos
        yield env.timeout(5)

def ponteElevatoria(env):
    # opera a ponte elevatória
    global abrePonte

    print('%2.0f A ponte está fechada =(' %(env.now))
    # aguarda o evento para abertura da ponte
    tempoAberta = yield abrePonte
    print('%2.0f A ponte está  aberta =) e fecha em %2.0f minutos' 
            %(env.now, tempoAberta))

env = simpy.Environment()
# inicia o processo de controle do turno
env.process(turno(env))

env.run(until=20)
```

Dentro da função `ponteElevatoria` a linha:

```python
# aguarda o evento para abertura da ponte
tempoAberta = yield abrePonte
```

Aguarda até que o evento `abrePonte` seja executado e resgata seu valor \(o tempo que a ponte deve permanecer aberta\) na variável `tempoAberta.`

Concluindo, o potencial de uso do comando `event()` é extraordinário, mas, por experiência própria, garanto que seu uso descuidado pode tornar qualquer código ininteligível, candidato ao [Campeonato Mundial de Código C Ofuscado](http://www.ioccc.org/) \(sim, isso existe!\) ou mesmo algo semelhante a utilizar desvios de laço `go... to` em um programa \(des\)estruturado\).

## Conceitos desta seção

| Conteúdo | Descrição |
| :--- | :--- |
| `meuEvento = env.event()` | cria um novo _evento_ `meuEvento` durante a simulação, mas não o processa. |
| `yield meuEvento` | aguarda até que o evento `meuEvento` seja processado |
| `yield meuEvento.succeed(value=valor)` | processa o evento `meuEvento`, isto é, engatilha o evento no tempo atual e inicia o seu processamento, retornando o parâmetro opcional `valor.` |

## Desafios

> **Desafio 21:** crie um processo de geração de automóveis que desejam cruzar a ponte, durante o horário de pico que dura 4 horas. Os intervalos entre chegadas sucessivas de veículos para travessia são exponencialmente distribuídos com média de 10 segundos \(ou 6 veículos/min\), e a ponte permite a travessia de 10 veículos por minuto. Após 4 horas de operação, quantos veículos estão em espera por travessia da ponte?
>
> **Desafio 22:** para o sistema anterior, construa um gráfico para o número de veículos em fila em função do tempo de abertura da ponte para travessia de automóveis. Qual o tempo mínimo que você recomendaria para abertura da ponte.

