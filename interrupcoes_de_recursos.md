# Interrupções de processos


Você está todo feliz e contente atravessando a galáxia no seu X-Wing quando... PIMBA! Seu [dróide astromecânico](https://pt.wikipedia.org/wiki/R2-D2) pifou e você deve interromper a viagem para consertá-lo.

Nesta seção iremos interromper processos já em execução e depois retomar a operação inicial. A aplicação mais óbvia é para a quebra de equipamentos durante a operação, como no caso do R2D2.

A interrupção de um processo em SimPy é realizada por meio de um comando ```Interrupt``` no processo já iniciado. O cuidado aqui é que quando um recurso é requisitado por um processo de menor prioridade ele causa uma interrupção no Python, o que obriga a utilização de lógica do timpo ```try:...except```.



## Criando quebras de equipamento

 Voltando ao exemplo do X-wing, considere que a cada 10 horas o R2D2, interrompe a viagem para uma manutenção de 1 hora e que a viagem toda levaria (sem as paralizações) 50 horas.

Inicialmente, devemos criar uma função que representa a viagem:
