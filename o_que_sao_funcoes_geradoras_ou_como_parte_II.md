# O que são funções geradoras? (Ou como funciona o SimPy?) - Parte II

## SimPy x funções geradoras

Uma função geradora é uma classe especial de funções que tem como característica retornar, cada vez que são chamadas, valores em sequência. O que torna uma função qualquer uma *função geradora* é a presença do comando ```yield``` em seu corpo.

Para compreendermos a mecânica do SimPy (e da maioria dos softwares de simulação) é só questão de se reconhecer que os processos de um modelo de simulação nada mais são que eventos (ou atividades ou ações) que interagem entre si de diversas maneiras, tais como: congelando outro evento por tempo determinado, disparando novos eventos ou mesmo interrompendo certo evento já em execução.

Já sabemos que as entidades e eventos em SimPy são modelados como **processos** dentro de um dado **environment**. Cada processo é basicamente uma função iniciada por ```def``` como qualquer outra construída em Python, mas que contém a palavrinha mágica ```yield```. Assim, como descrito no item anterior, todo **processo** em SimPy é também uma **função geradora**.

Um evento bastante elementar em SimPy é o ```timeout()``` ou, na sua forma mais usual:

```python
yield env.timeout(tempo_de_espera)```
Imagine por um momento que você é a própria encarnação do SimPy, lidando com diversos eventos, processos etc. Repentinamente, você, Mr. SimPy, depara-se com a linha de código anterior. Mr. SimPy vai processar a linha em duas etapas principais:
1. A palavra ```yield``` suspende imediatamente o processo ou, de outro modo, impede que a execução avance para linha seguinte (como esperado em qualquer toda função geradora);
2. Com o processo suspenso, a função ```env.timeout(tempo_de_espera)``` é executada e só após o seu derradeiro término, o processamento retorna para a linha seguinte do programa. 


Portanto, quuando um processo encontra um ```yield```, o processo é suspenso até o instante em que o evento deve ocorrer, quando o SimPy então *dispara* o novo evento. 

Naturalmente, quando num modelo de simulação temos muito eventos interpostos, cabe ao SimPy coordenar os disparos e suspensões dos eventos corretamente ao longo da simulação, respeitando um calendário único do programa - é nesta parte que você se emociona com a habilidade dos programadores que codificaram o calendário de eventos dentro do SimPy.

