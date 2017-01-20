## Interrompendo um proccesso sem captura por `try...except`
Caso o modelo possua um comando de interrupção de processo, mas não exista nenhuma lógica de captura do tipo `try... except`, a simulação será finalizada com a mensagem de erro:
```python
Interrupt: Interrupt(None)
```
O SimPy cria, para cada processo, uma propriedade chamada `defused` que permite contornar a paralização. Assim, pode-se interromper um processo, sem que essa interrupção provoque estrago algum ao processamento do modelo. Para *desativar* a paralização do modelo (e manter apenas a paralização do processo), basta tornar a propriedade `defused = True`:
```python
processVar.interrupt()
processVar.defused = True
```


## Conceitos desta seção

| Conteúdo | Descrição |
| --- | --- |
| `processVar = env.process(função_processo(env))` | armazena o processo da função\_processo na variável `processVar` |
| `processVar.interrupt()` | interrompe o processo armazenado na variável `processVar` |
| `try:...except simpy.Interrupt` | lógica `try...except` necessária para interrupção do processo |

## Desafios

> **Desafio 13** Considere que existam dois tipos de paradas: uma do R2D2 e outra do canhão de combate. A parada do canhão de combate ocorre sempre depois de 25 horas de viagem \(em quebra ou não\) e seu reparo dura 2 horas. Contudo, para não perder tempo, a manutenção do canhão só é realizada quando o R2D2 quebra.

> **Desafio 14** Você não acha que pode viajar pelo espaço infinito sem encontrar alguns [TIEs](https://en.wikipedia.org/wiki/TIE_fighter) das forças imperiais, não é mesmo? Considere que a cada 25 horas, você se depara com um TIE imperial. O ataque dura 30 minutos e, se nesse tempo você não estiver com o canhão funcionando, a sua próxima viagem é para o encontro do mestre Yoda.

>Dica: construa uma função `executaCombate`que controla todo o processo de combate. Você vai precisar também de uma variável global que informa se o X-Wing está ou não em combate.
