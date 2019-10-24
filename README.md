# SMUS
Projeto de monitoramento de umidade de solos em tempo real.
### Utilizando
Flask\
Sqlite\
JS
### Andamento do Projeto
##### 28/09 - 
Finalização da Fase de Planejamento
##### 05/10 - 
Construção Sketch\
Criação Canal ThingSpeak\
Teste de Conexão com broker (falhou)\
Esboço da Aplicação com créditos
##### 07/10 - 
Adição de tela de Login\
Script de criação do banco\
Front quebrado
##### 09/10 - 
Correções no Front\
Correções script do banco: persistência de tabela e criação de usuário admin
##### 10/10 -
Alterações README
##### 14/10 -
Autenticação de usuário (a parte https://repl.it/@IsadoraMenezes/authTest)
Remontagem na protoboard
##### 15/10 -
Alteração no Sketch\
Teste no Canal do ThingSpeak: https://thingspeak.com/channels/879252
##### 16/10 -
Pesquisa para elaboração do relatório 
##### 17/10 -
Merge entre projeto de Autenticação e projeto principal\
Reorganização dos arquivos para atender ao padrão Flask
##### 19/10 -
Feita a conexão com o broker CloudMQTT, falha no envio das informações por hora.
##### 21/10 -
Alteração na forma de captação dos dados, passando a pegar diretamente do ThingSpeak através da API em um arquivo json\
Início das tratativas dos dados para inserção no banco
##### 23/10 -
Captura dos dados de leitura do json\
Resolução do sql para inserção de dados no banco (feitos em projeto a parte: https://repl.it/@IsadoraMenezes/testeEscritaNoBanco, https://repl.it/@IsadoraMenezes/testeEscritaNoBanco2, https://repl.it/@IsadoraMenezes/testedeinformacoesnobanco)
##### 25/10 -
Inserção de dados no banco ainda com problemas oriundos da plataforma\
Organização de projetos associados em https://repl.it/repls/folder/PSE \
Captura das informações do banco e exibição na página inicial

