# O que são funções geradoras? (Ou como funciona o SimPy)

##Iterador
Na programação voltada ao objeto, *iteradores* são métodos que permitem ao programador observar os valores dentro de um dado objeto.

<!---
esta seção está bem confusa, rever

Só joguei uns conceitos. AInda não sei como apresentar isso de modo didático
--->

Quando você percorre uma lista com o comando ```
for,```
 por exemplo, está intrinsecamente utilizando um iterador:
```
 lista = [1, 2, 3]
 for i in lista:
    print (i)```
No exemplo, o comando ```for``` permite vasculhar cada elemento dentro da lista.

##Funções geradoras
Elas existem e [estão entre nós há tempos](https://en.wikipedia.org/wiki/Generator_(computer_programming), nós é que não sabíamos...

Uma função geradora é uma classe especial de funções que tem como característica retornar valores em sequência, cada vez que são chamadas. O que torna uma função qualquer uma *função geradora* é a presença do comando ```yield``` em seu corpo. Por exemplo, cada vez que a função a seguir é chamada, ela retorna um novo número da sequência entre 0 e 10:
```
def seqNum():
    n = 0
    while n <= 10:
        yield n
        n += 1

for i in seqNum():
    print(i)```


Se você executou o programa anterior, deve ter notado que o ```yield``` funciona como um ```return``` dentro da função, mas com o *superpoder* de aguardar o retorno do fluxo de controle do programa ali mesmo na linha do ```yield```, ou seja: a segunda chamada da função **não** executa o corpo inteiro da função! Isto significa que, numa segunda chamada à função, a execução retoma a partir da linha seguinte ao ```yield``` e o próximo valor de *n* será o anterior incrementado de 1.

Uma função geradora é, de fato, um *iterador* e você normalmente vai utilizá-la dentro de algum *loop*. 

Que tal uma função que nos diaga a posição atual de um Zumbi que só pode andar num tabuleiro de xadrez (8x8 posições)?
```
def seqNum():
    n = 0
    while n <= 10:
        yield n
        n += 1
    
for i in seqNum():
    print(i)
```
Execute o programa e reflita sobre cada chamada à função seqNum dentro do for.
    
    

    
