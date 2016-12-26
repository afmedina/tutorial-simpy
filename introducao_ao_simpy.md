[](http://stackoverflow.com/questions/tagged/simpy)![SimPy logo](SimPy_Logo300.png)

# Apresentação

Este livro é construído a partir de seções compactas. A ideia é elaborar textos curtos, para que o leitor, a cada seção, tenha uma visão clara do conteúdo apresentado, construindo o conhecimento de maneira sólida e respeitando a sua curva de aprendizado.

**SimPy** \(_Simulation in Python_\) é um _[framework](https://pt.wikipedia.org/wiki/Framework)_[^1] para a construção de modelos de simulação de eventos discretos em Python e distribuído segundo a [licença MIT](https://pt.wikipedia.org/wiki/Licen%C3%A7a_MIT).  Ele se diferencia dos softwares usuais de simulação, pois não se trata de uma aplicação com objetos prontos, facilmente conectáveis entre si por simples cliques do mouse, como a maioria dos softwares comerciais de simulação. Com o **SimPy**, cabe ao usuário construir um programa de computador em Python que represente seu modelo. Excencialmente, **SimPy** é uma biblioteca de comandos que conferem ao Python o poder de construir modelos de eventos discretos.

Com **SimPy** é possível pode-se construir, além de modelos de simulação discreta, modelos de simulação em “Real Time”, modelos de agentes e até mesmo modelos de simulação contínua. De fato, e como você notará ao longo deste texto, essas possibilidades estão mais associadas ao Python do que propriamente aos recursos fornecidos pelso **SimPy**.

## Por que utilizar o SimPy?

Talvez a pergunta correta seja: "por que utilizar o Python?"

Python é hoje, talvez, a linguagem mais utilizada no meio científico e uma breve pesquisa pela Internet vai sugerir artigos, posts e intermináveis discussões sobre os porquês desse sucesso todo. Eu resumiria o sucesso do Python em 3 grandes razões:

* **Facilidade de codificação**. Engenheiros, matemáticos e pesquisadores em geral querem pensar no problema, nem tanto na linguagem e Python cumpre o que promete quando se fala em facilidade. Se ela é fácil de codificar, mais fácil ainda é ler e interpretar um código feito em Python;
* **Bibliotecas! Bibliotecas!** Um número inacreditável de bibliotecas \(particularmente para a área científica\) está disponível para o programador \(e pesquisador\).
* **Scripts**. A funcionalidade de trabalhar com [scripts](https://pt.wikipedia.org/wiki/Linguagem_de_script)[^2] ou pequenos trechos de código interpretado \(basicamente, Python é uma linguagem script\) diminui drasticamente o tempo de desenvolvimento e aprendizado da linguagem.

Além disso, SimPy, quando comparado com pacotes comerciais, é gratuito - o que por si só é uma grande vantagem num mercado em que os softwares são precificados a partir de milhares de dólares - e bastante
flexível, no sentido de que não é engessado apenas pelos módulos existentes.

Sob o aspecto funcional, SimPy se apresenta como uma _biblioteca_ em Python e isso significa que um modelo de simulação desenvolvido com ele, terá à disposição tudo que existe de bom para quem programa em Python: o código fica fácil de ler \(e desenvolver\), o modelo pode ser distribuído como um pacote \(sem a necessidade do usuário final instalar o Python para executá-lo\), além das diversas bibliotecas de estatística e otimização disponíveis em Python, que ampliam em muito o horizonte de aplicação dos modelos.

Esta disponibilidade de bibliotecas, bem como ser um software livre, torna o SimPy particularmente interessante para quem está desenvolvendo suas pesquisas acadêmicas na área de simulação. O seu modelo provavelmente ficará melhor documentado e portanto mais fácil de ser compreendido, potencializando a divulgação dos resultados de sua pesquisa em dissertações, congressos e artigos científicos.

## Prós e contras

Prós:

* Código aberto e livre \([licença MIT](https://pt.wikipedia.org/wiki/Licen%C3%A7a_MIT)\);
* Diversas funções de bibliotecas de otimização, matemática e estatística podem ser incorporadas ao modelo;
* Permite a programação de lógicas sofisticadas, apoiando-se no Python \(e suas bibliotecas\);
* Comunidade ativa de desenvolvedores e usuários que mantém a bilbioteca atualizada;

Contras:

* Ausência de ferramentas para animação;
* Necessidade de se programar cada processo do modelo;
* Exige conhecimento prévio em Python;
* Não inclui um ambiente visual de desenvolvimento.


## Um breve histórico do SimPy
<....>

## Onde procurar ajuda sobre o SimPy
Atualmente existem três fontes de consulta sobre o SimPy na internet:
* O próprio site do projeto http://simpy.readthedocs.io, com exemplos e uma detalhada descrição da da Interface de Programação de Aplicações (*Application Programming Interface* - API);
* A [lista de discussão](https://groups.google.com/forum/#!forum/python-simpy) de usuários é bastante ativa, com respostas bem elaboradoras;
* O [Stack Overflow](http://stackoverflow.com/questions/tagged/simpy) tem um número razoável de questões e exemplos, mas cuidados pois boa parte do material ainda refere-se à versão 2 do SimPy.

## Desenvolvimento deste livro

Este texto foi planejado em formato de seções compactas, de modo que sejam curtas e didáticas – tendo por meta que cada seção não ultrapasse muito além de 500 palavras.

Esta é a primeira edição de um livro sobre uma linguagem que vem apresentando um interesse crescente. Naturalmente, o aumento de usuários - e espera-se que este livro contribua para isso - provocará também o surgimento de mais conhecimento, mais soluções criativas e que deverão ser incorporadas neste livro em futuras revisões.

O plano proposto por este texto é caminhar pela seguinte sequência:

* Introdução ao SimPy
* Instalação
* Conceitos básicos: entidades, recursos, filas etc.
* Conceitos avançados: prioridade de recursos, compartilhamento de recursos, controle de filas _Store_ de recursos etc.
* Experimentação \(replicações, tempo de _warm-up_, intervalos de confiança etc.\)
* Aplicações

  [^1]: Em português, ainda é comum o estrageirismo "framework" entre profissionais da Ciência da Computação. 

  [^2]: Script é uma sequência de comandos executados no interior de algum programa por meio de um interpretador. 


