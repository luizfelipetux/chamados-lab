# ChamadosLab

Aplicação entregue pela equipe DEV para implantação em ambiente Linux.

## Visão geral

ChamadosLab é uma aplicação web simples para abertura e acompanhamento de chamados internos.

### Funcionalidades
- cadastrar chamado;
- listar chamados;
- visualizar detalhes;
- alterar o status;
- persistir os registros em banco relacional.

## Dependências técnicas

- Linux;
- Python 3;
- Flask;
- PyMySQL;
- MariaDB;
- acesso HTTP para os usuários;
- conexão TCP da aplicação com o banco.

A aplicação lê sua configuração por variáveis de ambiente:

- `DB_HOST`
- `DB_PORT`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `APP_HOST`
- `APP_PORT`

A porta padrão da aplicação é `8000`.

## Requisitos de implantação fornecidos pela equipe DEV

- o usuário final deve acessar a aplicação pelo navegador;
- os dados precisam persistir após reinício da aplicação;
- a camada de dados não deve ser utilizada diretamente pelos usuários finais;
- somente a aplicação deve possuir credencial de acesso ao banco;
- as credenciais não devem ser gravadas no código-fonte;
- o ambiente inicial atenderá aproximadamente 30 usuários;
- o ambiente possui recursos computacionais limitados;
- aplicação e banco devem poder ser mantidos/reiniciados de forma independente.

## Execução local da aplicação

1. Crie um ambiente virtual Python.
2. Instale `requirements.txt`.
3. Defina as variáveis de ambiente.
4. Execute:

```bash
python app.py
```

## Health check

A rota `/health` testa a aplicação e a comunicação com o banco.

Exemplo:

```bash
curl http://127.0.0.1:8000/health
```

Resposta esperada quando o banco está disponível:

```json
{"database":true,"status":"ok"}
```
