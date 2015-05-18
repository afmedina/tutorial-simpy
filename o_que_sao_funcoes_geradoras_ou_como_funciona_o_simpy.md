# O que são funções geradoras? (Ou como funciona o SimPy)

##Iterador
Na programação voltada ao objeto, *iteradores* são objetos que permitem ao programador observar os valores dentro de um dado objeto.

Quando você percorre uma lista com o comando ```
for,```
 por exemplo, está intrinsecamente utilizando um iterador:
```
 for i in lista:
    print (i)```
No exemplo, o comando ```for``` permite vasculhar cada elemento dentro da lista.

##Funções geradoras
Elas existem e estão entre nós há tempos, nós é que não sabíamos..
Uma função geradora é uma classe especial de funções que tem como característica retornar valores em sequencia, cada vez que são chamadas. O que torna uma função qualquer uma *função geradora* é a presença do comando yield em seu corpo. Por exemplo, cada vez que a função a seguir é chamada, ela retorna um novo número no intervalo entre 0 e 10:
```
def seqNum():
    n = 0
    while n <= 10:
        yield n
        n += 1```


O yield funciona como um return dentro da função, mas com o *superpoder* de aguardar o retorno do fluxo de controle do programa ali na linha do yield. Isto significa que, numa segunda chamada à função, o próximo valor de n será o anterior incrementado de 1.

Uma função geradora é, de fato, um iterador e você normalmente vai utilizá-la dentro de alguma iteração. Por exemplo, para realizarmos uma contagem regressiva, poderíamos:
```
def seqNum():
    n = 0
    while n <= 10:
        yield n
        n += 1
    
for i in seqNum():
    print(i)
```
    
    

    
