# Tutorial SimPy: criando, ocupando e desocupando recursos

## Criando simpy.Resource

Em SimPy, tudo é processo e, portanto, criar um recurso também é um processo. A função que cria recursos é a: 

```
meuRecurso = simpy.Resource(env, capacity=1)```


Se o parâmetro *capacity* não for fornecido, a função assume *capacity*=1. Note que ```
meuRecurso``` foi criando dentro do Environment ```
env```
.

## Ocupando

É interessante notar que ocupar um recurso no SimPy é feito em duas etapas:
1. Solicitar o recurso desejado com um ```
request(```
) e
2. Aguardar o acesso ao recurso com um ```
yield```

Assim, uma chamada ao recurso ```
meuRecurso```
 ficaria:

```
request = meuRecurso.request() # solicita o recurso meuRecurso (note que ele ainda não ocupa o recurso)
yield request # aguarda em fila a liberação do recurso```

Se pode parecer estranho que a ocupação de um recurso envolva duas linhas de código, o bom observador deve notar que isso pode dar flexibilidade em situção de lógica intrincada.

## Desocupando

Recurso criado e ocupado é liberado com a função ```
recurso.release(request):```

```
meuRecurso.release(resquest)
```

## Juntando tudo em um exemplo: a fila M/M/1

A fila M/M/1 (ver...) tem chegadas exponenciais, atendimentos exponenciais e apenas um servidor.

Partindo da função geraChegadas, precisamos criar uma função ou processo para ocupar, utilizar e desocupar o servidor.





