# Introdução ao SimPy

Este livro foi elaborado a partir de seções compactas em textos curtos, para que o leitor, a cada seção, tenha uma visão clara do conteúdo apresentado, construindo o conhecimento de maneira sólida e respeitando a sua curva de aprendizado pessoal.

**SimPy** \(_Simulation in Python_\) é um [_framework_](https://pt.wikipedia.org/wiki/Framework) para a construção de modelos de simulação de eventos discretos em Python e distribuído segundo a [licença MIT](https://pt.wikipedia.org/wiki/Licen%C3%A7a_MIT). Ele se diferencia dos pacotes comerciais usualmente utilizados na simulação de eventos discretos, pois não se trata de uma aplicação com objetos prontos, facilmente conectáveis entre si por simples cliques do mouse. Com o **SimPy**, cabe ao usuário construir um programa de computador em Python que represente seu modelo. Essencialmente, **SimPy** é uma biblioteca de comandos que conferem ao Python o poder de construir modelos de eventos discretos.

Com o **SimPy** é pode-se construir, além de modelos de simulação discreta, modelos de simulação em “Real Time”, modelos de agentes e até mesmo modelos de simulação contínua. De fato, e como você notará ao longo deste texto, essas possibilidades estão mais associadas ao Python do que propriamente aos recursos fornecidos pelo **SimPy**.

## Por que utilizar o SimPy?

Talvez a pergunta correta seja: "por que utilizar o Python?"

Python é hoje, talvez, a linguagem mais utilizada no meio científico e uma breve pesquisa pela Internet vai sugerir artigos, posts e intermináveis discussões sobre os porquês desse sucesso todo. Eu resumiria o sucesso do Python em 3 grandes razões:

* **Facilidade de codificação**. Engenheiros, matemáticos e pesquisadores em geral querem pensar no problema, nem tanto na linguagem e Python cumpre o que promete quando se fala em facilidade. Se ela é fácil de codificar, mais fácil ainda é ler e interpretar um código feito em Python;
* **Bibliotecas! Bibliotecas!** Um número inacreditável de bibliotecas \(particularmente para a área científica\) está disponível para o programador \(e pesquisador\).
* **Scripts**. A funcionalidade de trabalhar com [scripts](https://pt.wikipedia.org/wiki/Linguagem_de_script%29[^2]%20ou%20pequenos%20trechos%20de%20código%20interpretado%20%28basicamente,%20Python%20é%20uma%20linguagem%20script\) diminui drasticamente o tempo de desenvolvimento e aprendizado da linguagem.

Além disso, o SimPy, quando comparado com pacotes comerciais, é gratuito - o que por si só é uma grande vantagem num mercado em que os softwares são precificados a partir de milhares de dólares - e bastante flexível, no sentido de que não é engessado apenas pelos módulos existentes.

Sob o aspecto funcional, SimPy se apresenta como uma _biblioteca_ em Python e isso significa que um modelo de simulação desenvolvido com ele, terá à disposição tudo que existe de bom para quem programa em Python: o código fica fácil de ler \(e desenvolver\), o modelo pode ser distribuído como um pacote \(sem a necessidade do usuário final instalar o Python para executá-lo\), além das diversas bibliotecas de estatística e otimização disponíveis em Python, que ampliam, em muito, o horizonte de aplicação dos modelos.

Esta disponibilidade de bibliotecas, bem como ser um software livre, torna o SimPy particularmente interessante para quem está desenvolvendo sua pesquisa acadêmica na área de simulação. O seu modelo provavelmente ficará melhor documentado e portanto mais fácil de ser compreendido, potencializando a divulgação dos resultados de sua pesquisa em dissertações, congressos e artigos científicos.

## Prós e contras

Prós:

* Código aberto e livre \([licença MIT](https://pt.wikipedia.org/wiki/Licen%C3%A7a_MIT%29\);
* Diversas funções de bibliotecas de otimização, matemática e estatística podem ser incorporadas ao modelo;
* Permite a programação de lógicas sofisticadas, apoiando-se no Python \(e suas bibliotecas\);
* Comunidade ativa de desenvolvedores e usuários que mantém a biblioteca atualizada;

Contras:

* Ausência de ferramentas para animação;
* Necessidade de se programar cada processo do modelo;
* Exige conhecimento prévio em Python;
* Não inclui um ambiente visual de desenvolvimento.

## Um breve histórico do SimPy

&lt;....&gt;

## Onde procurar ajuda sobre o SimPy

Atualmente existem três fontes de consulta sobre o SimPy na internet:

* O próprio site do projeto [http://simpy.readthedocs.io](http://simpy.readthedocs.io), com exemplos e uma detalhada descrição da da Interface de Programação de Aplicações \(_Application Programming Interface_ - API\);
* A [lista de discussão](https://groups.google.com/forum/#!forum/python-simpy) de usuários é bastante ativa, com respostas bem elaboradoras;
* O [Stack Overflow](http://stackoverflow.com/questions/tagged/simpy) tem um número razoável de questões e exemplos, mas cuidado pois boa parte do material ainda refere-se à antiga versão 2 do SimPy, bastante diferente da versão 3, base deste livro.

## Desenvolvimento deste livro

Este texto foi planejado em formato de seções compactas, de modo que sejam curtas e didáticas – tendo por meta que cada seção não ultrapasse muito além de 500 palavras.

Esta é a primeira edição de um livro sobre uma linguagem que vem apresentando um interesse crescente. Naturalmente, o aumento de usuários - e espera-se que este livro contribua para isso - provocará também o surgimento de mais conhecimento, mais soluções criativas e que deverão ser incorporadas neste livro em futuras revisões.

O plano proposto por este texto é caminhar pela seguinte sequência:

* Introdução ao SimPy
* Instalação do pacote
* Conceitos básicos: entidades, recursos, filas etc.
* Conceitos avançados: prioridade de recursos, compartilhamento de recursos, controle de filas _Store_ de recursos etc.
* Experimentação \(replicações, tempo de _warm-up_, intervalos de confiança etc.\)
* Aplicações

