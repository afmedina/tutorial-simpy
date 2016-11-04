# Selecionando um recurso específico para um processo com `Store() e FilterStore()`

O SimPy possui um ferramenta para armazenamento de objetos - como recursos, por exemplo - chamada `Store` e um comando de acesso a objetos específicos dentro do `Store` por meio de filtro, o `FilterStore`. O programador vai notar a similaridade entre o `Store` e o [dicionário](http://www3.ifrn.edu.br/~jurandy/fdp/doc/aprenda-python/capitulo_10.html) do Python.

Vamos aprender sobre o `Store` a partir de um exemplo simples: uma barbearia com três barbeiros. Quando você chega a uma barbearia e tem uma ordem de preferência entre os barbeiros, isto é: barbeiro 1 vem antes do 2, que vem antes do 3, precisará selecionar seu _recurso_ barbeiro na ordem certa. 

Inicialmente, vamos criar os recursos:

