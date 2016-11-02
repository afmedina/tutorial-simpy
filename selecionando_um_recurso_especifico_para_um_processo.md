# Selecionando um recurso específico para um processo com `Store() e FilterStore()`

SimPy possui um ferramenta `Store` para armazenamento de objetos - como recursos, por exemplo - e um comando de acesso a esse objetos por meio de filtro, o `FilterStore`.

Um exemplo simples, é uma barbearia com três barbeiros. Se você tem uma ordem de preferência entre os barbeiros, isto é: barbeiro 1 vem antes do 2, que vem antes do 3, precisará selecionar seu _recurso_ barbeiro na ordem certa.

Inicialmente, vamos criar os recursos:

