## Desafios
>**Desafio 23:**Considere que existe uma probabilidade de que a Lebre, por alguma razão mal explicada (eu realizaria um teste antidoping nos competidores), resolva que é uma boa idéia tirar uma soneca de 5 mintos em algum instante entre 2 e 10 minutos do início da corrida. Modele esta nova situação (dica: crie um função `soneca` que gera um evento que pode ocasionar a parada da Lebre ainda durante a corrida).



>**Desafio 24:**É interessante notar, que mesmo quando um dos competidores *perde* a corrida, de fato, o respectivo evento **não é** cancelado. Altere o modelo anterior para marcar o horário de chegada dos dois competidores, garantindo que os eventos `lebreEvent` e `tartarugaEvent` sejam executados até o fim.