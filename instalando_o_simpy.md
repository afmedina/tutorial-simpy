# Instalando o SimPy
Nossa jornada começa por um tutorial de instalação de alguns programas e bibliotecas úteis para o SimPy. Selecionamos, para começar o tutorial, os seguintes pacotes:

1. Python 3.4
2. Pip
3. SimPy 3.0.10
4. NumPy

Um breve preâmbulo das nossas escolhas: no momento da elaboração deste tutorial, o **Python** já está na versão 3.5.0, mas o **Anaconda** (explicado adiante) ainda fornece a versão 3.4. Se você já possui uma instalação com o Python 3.5, pode instalar o SimPy sem problemas, pois ele é compatível com as versões mais recentes do Python.

**Pip** é um instalador de bibliotecas e facilita muito a vida do programador. 

O **SimPy** 3.0.10 é a versão mais atual no momento em que este tutorial é escrito e traz grandes modificações em relação à versão 2.0.

> Atenção: existe vasto material disponível na Internet para o SimPy. Contudo, um cuidado especial deve ser tomado: grande parte deste material refere-se a versão 2.0, que possui diferenças críticas em relação à versão mais atual. Este texto é para a versão 3 em diante.


Quanto ao **NumPy**, vamos aproveitar o embalo para instalá-lo, pois será muito útil nos nossos modelos de simulação. Basicamente, NumPy acrescenta um tipo de dados (*n-dimensional array*) que facilita a codificação de modelos de simulação, particularmente na análise de dados de saída do modelo.


##Passo 1: Anaconda, the easy way
Atenção:
> * Se você já tem o Python e o Pip instalados em sua máquina, pule diretamente para o Passo 3: “Instalando o SimPy”; 
> * Se você já tem o Python instalado, mas não o Pip (quem tem o Python +3.4, já tem o Pip instalado), pule para o Passo 2: “Instalando o Pip”

Se esta é a sua primeira vez, nossa sugestão: não perca tempo e instale a distribuição gratuita [Anaconda](http://continuum.io/downloads). 

![Anaconda logo](https://github.com/afmedina/tutorial-simpy/blob/master/Anaconda_Logo180.png?raw=true)
	 
Por meio do Anaconda, tudo é mais fácil, limpo e o processo já instala mais de 200 pacotes verificados por toda sorte de compatibilidade, para que você não tenha trabalho algum. (Entre os pacotes instalados está o [NumPy](http://www.numpy.org/) que, como explicado, será muito útil no desenvolvimento dos seus modelos).

Atualmente eles disponibilizam as versões 2.7, 3.4 e 3.5 do Python (em 32 e 64 bit) na [página de downloads](http://continuum.io/downloads).

Baixe o arquivo com a versão desejada (mais uma vez: SimPy roda nas duas versões) e siga as instruções do instalador.
##Passo 2: Instalando o Pip (para quem não instalou o Anaconda)
>Se a versão instalada do Python for +3.4 ou você fez o passo anterior,  pode pular este passo, pois o pip já deve estar instalado no seu computador.

1.	Baixe o pacote `get-pip.py`
 [por este link](https://bootstrap.pypa.io/get-pip.py) para o seu computador, salvando-o em uma pasta de trabalho conveniente. 
2.	Execute `python get-pip.py`
 na pasta de trabalho escolhida (note a mensagem final de que o pip foi instalado com sucesso).

![cmd get-pip.py](https://github.com/afmedina/tutorial-simpy/blob/master/instalacao%20cmd%20get-pip.png?raw=true)
##Passo 3: Instalando o Simpy
Instalar o Simpy é fácil!

Digite numa janela cmd: 
```
pip install -U simpy
```
![cmd simpy](https://github.com/afmedina/tutorial-simpy/blob/master/instalacao%20cmd%20simpy.png?raw=true)

A mensagem "Sucessfully" indica que você já está pronto para o SimPy. Mas, antes disso, tenho uma sugestão para você:

##Passo 4: Instalando um Ambiente Integrado de Desenvolvimento (IDE) para aumentar a produtividade no Python
Os IDEs, para quem não conhece, são interfaces que facilitam a vida do programador. Geralmente possuem um editor de textos avançado, recursos de verificação de erros, monitoram os estados de variáveis, permitem o processamento passo-a-passo etc.

Se você instalou o Anaconda, então já ganhou um dos bons: o **Spyder**, que já está configurado e pronto para o uso. Geralmente (a depender da sua versão do Sistema Operacional) ele aparece como um ícone na área de trabalho. Se não localizar o ícone, procure por **Spyder** no seu computador (repare no *"y"*) ou digite em uma janela de cmd o comando `spyder.`

Aberto, o Spyder fica como a figura a seguir (repare que a janela superior-direita apresenta um tutorial de uso):
![IDE Spider](https://github.com/afmedina/tutorial-simpy/blob/master/instalacao%20spyder800.png?raw=true)

Outro IDE muito bom é o [Wing IDE 101](http://wingware.com/downloads/wingide-101) que é gratuito (e possui uma versão profissional paga):

![IDE Wing 101](https://github.com/afmedina/tutorial-simpy/blob/master/instalacao%20wing%20101%20800.png?raw=true)


>Atenção: se você instalou o Anaconda e pretende utilizar algum IDE que não o Spyder, siga as instruções [deste link](http://docs.continuum.io/anaconda/ide_integration), para configurar corretamenta seu IDE. (É fácil, não se avexe não!)

Se você chegou até aqui com tudo instalado, o próximo passo é começar para valer com o SimPy!

Na próxima seção, é claro. Precisamos tomar um chazinho depois deste zilhões de bytes instalados.




