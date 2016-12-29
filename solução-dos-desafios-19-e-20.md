# Solução dos desafios 19 e 20
>**Desafio 19**: considere que o sistema possui uma segunda etapa de montagem após a união de uma peça A e uma peça B da mesma cor. Na etapa seguinte, os componentes são unidos por cores diferentes, um a um. Assim, um componente branco e unido um componente verde e o tempo de montagem segue a mesma distribuição. Construa um modelo de simulação para representar esse sistema.

Uma solução bacana para este desafio é alterar a função `montagem` de modo a deixá-la genérica para as duas etapas de montagem. 

>**Desafio 20**: considere que a montagem de peças na primeira etapa da montagem é feita na proporção de duas peças do tipo A para 1 do tipo B. Modifique a função `montagem` de modo que ela aceite o número de peças a ser unidas como parâmetro de entrada da função.