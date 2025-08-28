## Descrição

`smsaback` é um middleware para gerenciamento de logs e endpoints, facilitando a integração e monitoramento de aplicações.

## Instalação

Requisitos:
- Python >= 3.9
- PDM >= 2.25

Para instalar as dependências, utilize:
- execute o comando `pdm install`

## Configuração

### Variáveis de Ambiente

Se as variáveis não forem preenchidas, será utilizado o valor default indicado.

- **ENVIRONMENT**  
  - Tipo: `str`  
  - Descrição: Define o tipo de ambiente de execução (ex: desenvolvimento, produção).  
  - Exemplo: `ENVIRONMENT=producao`  
  - Default: `default`

- **LOG_LEVEL**  
  - Tipo: `str`  
  - Descrição: Define o nível mínimo dos logs registrados (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`).  
  - Exemplo: `LOG_LEVEL=INFO`  
  - Default: `INFO`

- **LOG_CONSOLE**  
  - Tipo: `bool` (`true` ou `false`)  
  - Descrição: Habilita ou desabilita o log no console.  
  - Exemplo: `LOG_CONSOLE=true`  
  - Default: `false`

- **LOG_FILE**  
  - Tipo: `bool` (`true` ou `false`)  
  - Descrição: Habilita ou desabilita a escrita de log em arquivo local. Se habilitado, é necessário preencher a variável `LOG_FILE_PATH`.  
  - Exemplo: `LOG_FILE=true`  
  - Default: `false`

- **LOG_FILE_PATH**  
  - Tipo: `str`  
  - Descrição: Caminho para escrita do arquivo de log local. Atentar ao sistema utilizado, deixa vazio irá escrever os logs na raiz do projeto.
  - Exemplo: `LOG_FILE_PATH=/pastaLogs`  
  - Default: ``

- **LOG_POSTGRES**  
  - Tipo: `bool` (`true` ou `false`)  
  - Descrição: Habilita ou desabilita a escrita do log em banco de dados PostgreSQL. Se habilitado, é necessário preencher a variável `POSTGRES_DSN`.  
  - Exemplo: `LOG_POSTGRES=true`  
  - Default: `false`

- **POSTGRES_URI**  
  - Tipo: `str`  
  - Descrição: String de conexão URI para o PostgreSQL.  
  - Exemplo: `POSTGRES_URI=postgresql://usuario:senha@localhost:5432/`  
  - Default: *Não possui default*. Se o `LOG_POSTGRES` for ativado e não informar essa variável, o middleware não funcionará.
  
- **POSTGRES_DATABASE**  
  - Tipo: `str`  
  - Descrição: String para identificar qual database será utilizado PostgreSQL.  
  - Exemplo: `logsdb`  
  - Default: *Não possui default*. Se o `LOG_POSTGRES` for ativado e não informar essa variável, o middleware não funcionará.

- **LOG_MONGO**  
  - Tipo: `bool` (`true` ou `false`)  
  - Descrição: Habilita ou desabilita o log em banco de dados MongoDB. Se habilitado, é necessário preencher as variáveis `MONGO_URI`, `MONGO_DB` e `MONGO_COLLECTION`.  
  - Exemplo: `LOG_MONGO=true`  
  - Default: `false`

- **MONGO_URI**  
  - Tipo: `str`  
  - Descrição: URI de conexão com o MongoDB.  
  - Exemplo: `MONGO_URI=mongodb://usuario:senha@localhost:27017/`  
  - Default: *Não possui default*. Se o `LOG_MONGO` for ativado e não informar essa variável, o middleware não funcionará.

- **MONGO_DB**  
  - Tipo: `str`  
  - Descrição: Nome do banco de dados MongoDB onde os logs serão armazenados.  
  - Exemplo: `MONGO_DB=logsdb`  
  - Default: `logsdb`

- **MONGO_COLLECTION**  
  - Tipo: `str`  
  - Descrição: Nome da coleção do MongoDB para armazenar os logs.  
  - Exemplo: `MONGO_COLLECTION=logs`  
  - Default: `logs`