# Documentação da aplicação — ChamadosLab 1.0

## 1. Visão do sistema

**Problema:** solicitações internas são tratadas de forma informal e ficam dispersas em mensagens.

**Objetivo:** disponibilizar uma aplicação web simples para registrar e acompanhar chamados.

**Usuários:** colaboradores da organização.

**Escopo:** abertura, listagem, consulta e alteração de status de chamados.

## 2. Requisitos funcionais

- **RF01** — O sistema deverá permitir cadastrar um chamado com título, solicitante e descrição.
- **RF02** — O sistema deverá listar os chamados cadastrados.
- **RF03** — O sistema deverá permitir visualizar os detalhes de um chamado.
- **RF04** — O sistema deverá permitir alterar o status para Aberto, Em andamento ou Concluído.
- **RF05** — O sistema deverá recuperar os registros persistidos no banco de dados a cada acesso.

## 3. Requisitos não funcionais

- **RNF01 — Plataforma:** a solução deverá executar em Linux e ter baixo consumo de recursos.
- **RNF02 — Acesso:** os usuários deverão acessar o sistema por navegador usando HTTP.
- **RNF03 — Desempenho:** para a carga inicial de cerca de 30 usuários, operações comuns deverão responder em até aproximadamente 2 s em condições normais do laboratório.
- **RNF04 — Persistência:** os chamados deverão permanecer armazenados após reinício da aplicação.
- **RNF05 — Segurança:** o banco não deverá ser utilizado diretamente pelos usuários finais; a credencial da aplicação deverá ser restrita ao host da camada web.
- **RNF06 — Segredos:** usuário e senha do banco não deverão ficar gravados no código-fonte.
- **RNF07 — Manutenção:** aplicação e camada de dados deverão poder ser reiniciadas/manutenidas independentemente.
- **RNF08 — Capacidade:** a infraestrutura inicial deverá privilegiar baixo consumo, mas permitir revisão de sizing caso a quantidade de usuários aumente.

## 4. Dependências

- Python 3
- Flask
- PyMySQL
- MariaDB
- HTTP para acesso dos usuários
- TCP/3306 entre aplicação e banco

## 5. Variáveis de ambiente

- `DB_HOST`
- `DB_PORT`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `APP_HOST`
- `APP_PORT`

## 6. Critério de aceite técnico

A implantação será considerada funcional quando:

1. o usuário conseguir acessar a aplicação pelo navegador;
2. um novo chamado puder ser cadastrado;
3. o chamado continuar disponível após reiniciar a aplicação;
4. a rota `/health` indicar comunicação funcional com o banco.
