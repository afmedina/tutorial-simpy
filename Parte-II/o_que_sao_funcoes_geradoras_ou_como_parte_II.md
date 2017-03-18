# O que são funções geradoras? \(Ou como funciona o SimPy?\) - Parte II

## SimPy vs. funções geradoras

No episódio anterior...

> Uma **função geradora** é uma classe especial de funções que têm como característica retornar, cada vez que são chamadas, valores em sequência. O que torna uma função qualquer uma _função geradora_ é a presença do comando `yield` em seu corpo.

Para compreendermos a mecânica do SimPy \(e da maioria dos softwares de simulação\), devemos lembrar que os processos de um modelo de simulação nada mais são que eventos \(ou atividades ou ações\) que interagem entre si de diversas maneiras, tais como: congelando outro evento por tempo determinado, disparando novos eventos ou mesmo interrompendo certo evento já em execução.

Já sabemos que as entidades e eventos em SimPy são modelados como **processos** dentro de um dado **environment**. Cada processo é basicamente uma função iniciada por `def` como qualquer outra construída em Python, mas que contém a palavrinha mágica `yield.` Assim, como descrito no item anterior, todo **processo** em SimPy é também uma **função geradora**.

Um evento bastante elementar em SimPy é o `timeout()` ou, na sua forma mais usual:

```python
yield env.timeout(tempo_de_espera)
```

Imagine por um momento que você é a própria encarnação do SimPy, lidando com diversos eventos, processos, recursos etc. Repentinamente, você, Mr. SimPy, depara-se com a linha de código anterior. Mr. SimPy vai processar a linha em duas etapas principais:  
1. A palavra `yield` suspende imediatamente o processo ou, de outro modo, impede que a execução avance para linha seguinte \(como esperado em toda função geradora\);  
2. Com o processo suspenso, a função `env.timeout(tempo_de_espera)` é executada e só após o seu derradeiro término, o processamento retorna para a linha seguinte do programa.

Portanto, quando um processo encontra um `yield`, ele é suspenso até o instante em que o evento deve ocorrer, quando o SimPy então _dispara_ o novo evento. O que o SimPy faz no caso é **criar um evento a ser disparado **dali a um tempo igual ao `tempo_de_espera.`

Naturalmente, quando num modelo de simulação temos muito eventos interpostos, cabe ao SimPy coordenar os disparos e suspensões dos eventos corretamente ao longo da simulação, respeitando um calendário único do programa - é nesta parte que você deve se emocionar com a habilidade dos programadores que codificaram o calendário de eventos dentro do SimPy...

Em resumo, SimPy é um controlador de eventos, gerados pelo seu programa. Ele recebe seus eventos, ordena pelo momento de execução correto \(ou prioridade, quando existem eventos simultâneos no tempo\) e armazena uma lista de eventos dentro do `environment.` Se uma função dispara um novo evento, cabe ao SimPy adicionar o evento na lista de eventos, de modo ordenado pelo momento de execução \(ou da prioridade daquele evento sobre os outros\).

