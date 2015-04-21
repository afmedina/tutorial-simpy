# Instalando o SimPy
A nossa jornada começa pela instalação de alguns programas e bibliotecas úteis para o Simpy. Selecionei, para começar o tutorial, os seguintes pacotes:
1.	Python 2.7
2.	Pip
3.	Simpy 3.0.4
4.	Numpy

Um breve preambulo das minhas escolhas: no momento da elaboração deste tutorial, o Python já está na versão 3.4.0, mas como tenho interesse em utilizar o PyPy em algum momento mais à frente, tive de optar por uma versão compatível do Python, no caso a 2.7. Para o SimPy, você pode utilizar as versões mais atuais do Python.

Pip é um instalador de bibliotecas, facilita muito a vida do programador. 

O SimPy é o mais atual (e já sabemos que a versão 3 traz grandes alterações em relação à 2).

Quanto ao Numpy, vamos aproveitar o embalo para instalá-lo, pois será muito útil para nossos modelos de simulação.
##Passo 1: Anaconda, the easy way
Atenção:
* Se você já tem o Python e o Pip instalados em sua máquina, pule diretamente para o Passo 3: “Instalando o Simpy”. 
* Se você já tem o Python instalado, mas não o Pip (quem tem o Python +3.4, já tem o Pip instalado), pule para o Passo 2: “Instalando o Pip”

Se esta é a sua primeira vez, minha sugestão: não perca tempo e instale a distribuição gratuita Anaconda. 
	 
É fácil, limpo e ela já instala na sua máquina mais de 200 pacotes (entre eles o Numpy) verificando toda sorte de compatibilidade, para que você não tenha trabalho algum.

![Anaconda logo](https://github.com/afmedina/tutorial-simpy/blob/master/Anaconda_Logo180.png?raw=true)

Atualmente eles disponibilizam as versões 2.7 e 3.4 do Python (em 32 e 64 bit).

Baixe o arquivo com a versão desejada (mais uma vez: SimPy roda nas duas versões) e siga as instruções do instalador.
##Passo 2: Instalando o Pip (para quem não instalou o Anaconda)
(Nota: se a versão instalada do Python for +3.4 ou você fez o passo anterior, você pode pular este passo, pois o pip já está instalado no seu computador).
1.	Baixe o pacote ```
get-pip.py```
 para o seu computador, salvando em uma pasta de trabalho conveniente. 
2.	Execute ```
python get-pip.py```
 na pasta de trabalho escolhida (note a mensagem final de que o pip foi instalado com sucesso).

![cmd get-pip.py](https://github.com/afmedina/tutorial-simpy/blob/master/instalacao%20cmd%20get-pip.png?raw=true)
##Passo 3: Instalando o Simpy
Instalar o Simpy é fácil!

Digite numa janela cmd: 
```
pip install -U simpy
```
![cmd simpy](https://github.com/afmedina/tutorial-simpy/blob/master/instalacao%20cmd%20simpy.png?raw=true)

A mensagem de ```
Sucessfully```
 indica que você já está pronto para o SimPy. Mas, antes disso, tenho uma sugestão para você:
##Passo 4: Instalando um Ambiente Integrado de Desenvolvimento (IDE) para aumentar a produtividade no Python
Os IDEs, para quem não conhece, são pacotes que facilitam a vida do programador. Geralmente possuem editor de texto avançado, recursos de verificação de erros, estados de variáveis, processamento passo-a-passo etc.
Se você instalou o Anaconda, então já ganhou um dos bons: o Spyder, que já está configurado e pronto para o uso (repare na janela superior-direita, um tutorial de uso):
 
Pessoalmente, eu utilizo o Wing IDE 101 que é gratuito e eu acho muito bom:
 
Mas ATENÇÃO: se você instalou o Anaconda e pretende utilizar algum IDE que não o Spyder, siga as instruções deste link, para configurar o uso do seu IDE. (É fácil, não se avexe não!)
Se você instalou chegou aqui com tudo instalado, o próximo passo é começar para valer com o SimPy!
No próximo post, é claro. Precisamos tomar um chá depois deste zilhões de megabytes instalados.




