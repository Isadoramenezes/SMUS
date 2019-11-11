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
##### 30/10 -
Tentativa de correção de informações duplicadas [concluído em 04.11] \
Estudo para emissão de alerta e criação de dashboard admin: https://repl.it/@IsadoraMenezes/testeNiveisDeAcesso, https://repl.it/@IsadoraMenezes/novoTesteControleDeAcesso, https://repl.it/@IsadoraMenezes/dash
##### 31/10 -
Execução de testes e implementação da primeira versão da emissão de alerta, com tratamento de dados do banco: https://repl.it/@IsadoraMenezes/TesteAlerta
##### 01/11 - 
Estudo para construção do controle de acesso
##### 03/11 - 
Primeira versão da implementação do registro de usuários (falhou) \
Teste da função validate(login) apontou falha na validação [passando sem senha]
##### 04/11 -
Implementação correta do registro de usuários \
Aplicação de Extends nos templates (reuso de código) \
Correção na validação de login \
Correção da inserção de dados duplicados no banco (alterações no subscriber)
##### 05/11 -
Correção do problema de leitura do sensor \
Correção na medição da leitura
##### 06/11 -
Ajustes na emissão do alerta [em andamento]
##### 08/11 -
Finalização versão 2.0 Documento Geral do Projeto