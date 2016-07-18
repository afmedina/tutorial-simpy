# Solução dos desafios 7 e 8

**Desafio 7**: retome o problema da lavanderia \(Desafio 6\). Estime o tempo médio que os clientes atendidos aguardaram pela lavadora. Dica: você precisará de uma variável global para o cálculo do tempo de espera e um atributo para marcar a hora de chegada no sistema.

```python
import random
import simpy

tempoEsperaLavadora = 0
tempoEsperaCesto = 0
tempoEsperaSecadora = 0
contaClientes = 0

lavadorasUtilList = []
cestosUtilList = []
secadorasUtilList = []

def distributions(tipo):
     #função que armazena as distribuições utilizadas no modelo
     return {
     'chegadas': random.expovariate(1.0/5.0),
     'lavar': 20,
     'carregar': random.uniform(1, 4),
     'descarregar': random.uniform(1, 2),
     'secar': random.uniform(9, 12),
    }.get(tipo, 0.0)

def chegadaClientes(env, lavadoras, cestos, secadoras):
     #função que gera a chegada de clientes
     global contaClientes
     contaClientes = 0
     while True:
         contaClientes += 1
         yield env.timeout(distributions('chegadas'))
         print("Cliente %s chega em %.1f" %(contaClientes, env.now))
         env.process(lavaSeca(env, "Cliente %s" %contaClientes, lavadoras, cestos, secadoras))

def lavaSeca(env, cliente, lavadoras, cestos, secadoras):
     #função que processa a operação de cada cliente dentro da lavanderia
     global utilLavadora

     #ocupa a lavadora
     req1 = lavadoras.request()
     yield req1
     print("%s ocupa lavadora em %.1f" %(cliente, env.now))
     yield env.timeout(distributions('lavar'))

     #antes de retirar da lavadora, pega um cesto
     req2 = cestos.request()
     yield req2
     print("%s ocupa cesto em %.1f" %(cliente, env.now))
     yield env.timeout(distributions('carregar'))

     #libera a lavadora, mas não o cesto
     lavadoras.release(req1)
     print("%s desocupa lavadora em %.1f" %(cliente, env.now))

     #ocupa a secadora antes de liberar o cesto
     req3 = secadoras.request()
     yield req3
     print("%s ocupa secadora em %.1f" %(cliente, env.now))
     yield env.timeout(distributions('descarregar'))

     #libera o cesto mas não a secadora
     cestos.release(req2)
     print("%s desocupa cesto em %.1f" %(cliente, env.now))
     yield env.timeout(distributions('secar'))

     #pode liberar a secadora
     print("%s desocupa secadora em %.1f" %(cliente, env.now))
     secadoras.release(req3)

def monitor(env, lavadoras, cestos, secadoras, intervalo = 5):
 # calcula a ocupacao atual de cada recurso
     while True:
         yield env.timeout(intervalo)
         lavadorasUtilList.append((env.now, lavadoras.count, len(lavadoras.queue)))
         cestosUtilList.append((env.now, lavadoras.count, len(cestos.queue)))
         secadorasUtilList.append((env.now, lavadoras.count, len(secadoras.queue)))
def integraMonitor(resList, res):
     # estima a ocupação média de cada recurso
     sum1, sum2, sum3 = 0, 0, 0
     for i in resList:
         sum1 += i[0]*i[1]
         sum2 += i[0]
         sum3 += i[0]*i[2]


     return sum1/(sum2*res.capacity), sum3/sum2

random.seed(10)

env = simpy.Environment()

lavadoras = simpy.Resource(env, capacity = 3)
cestos = simpy.Resource(env, capacity = 2)
secadoras = simpy.Resource(env, capacity = 1)

env.process(chegadaClientes(env, lavadoras, cestos, secadoras))
env.process(monitor(env, lavadoras, cestos, secadoras))
env.run(until = 60000)

util = integraMonitor(lavadorasUtilList, lavadoras), integraMonitor(cestosUtilList, cestos), integraMonitor(secadorasUtilList, secadoras)
taxaChegadas = 1.0/5.0
print("Ocupações: lavadoras %.2f cestos %.2f secadoras %.2f" %(util[0][0], util[1][0], util[2][0]))
print("Filas: lavadoras %.2f cestos %.2f secadoras %.2f" %(util[0][1], util[1][1], util[2][1]))
print("Espera: lavadoras %.2f cestos %.2f secadoras %.2f" %(util[0][1]/taxaChegadas, util[1][1]/taxaChegadas, util[2][1]/taxaChegadas))
print (tempoEsperaLavadora/contaClientes)
print("Fila de clientes ao final da simulação: lavadoras %.2f cestos %.2f secadoras %.2f" %(len(lavadoras.queue), len(cestos.queue), len(secadoras.queue)))
```

**Desafior 8**: no desafio anterior, você deve ter notado como o tempo de espera pela lavadora está muito alto. Altere o programa para que ele calcule os tempo de espera por cestos, secadoras e o tempo total no sistema.

