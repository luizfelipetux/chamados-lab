# Atividade prática — Deploy profissional com Proxmox

## Objetivo central

Responder à pergunta:

> Como transformar requisitos de uma aplicação em uma infraestrutura capaz de executá-la?

O foco não é "criar duas VMs", mas justificar a arquitetura, provisionar os recursos, implantar a aplicação, testar e diagnosticar problemas.

## Organização

- Trabalho em duplas.
- Dois encontros de 2 aulas de 50 minutos.
- Pequena complementação poderá ser entregue após o segundo encontro.

---

# ETAPA 1 — Análise da demanda

Leia:

- `docs/CHAMADO_DEPLOY.md`
- `docs/DOCUMENTACAO_DEV.md`

Antes de abrir o Proxmox, responda:

1. Quais componentes de infraestrutura são necessários?
2. Quantas máquinas virtuais você propõe?
3. O que deve ficar exposto ao usuário?
4. O que deve ser acessível apenas internamente?
5. Quais portas serão utilizadas?
6. Qual componente precisa de maior preocupação com persistência?
7. Que recursos de CPU, RAM e disco você atribuiria a cada servidor?

## Entregável parcial

Produza:

### A. Diagrama da arquitetura

Não use ainda o diagrama do professor. Represente:

- usuário;
- camada web;
- camada de dados;
- protocolos/portas;
- direção das comunicações.

### B. Inventário proposto

| VM | Função | vCPU | RAM | Disco | Serviços |
|---|---|---:|---:|---:|---|
| | | | | | |
| | | | | | |

### C. Matriz de comunicação

| Origem | Destino | Porta | Motivo |
|---|---|---:|---|
| | | | |

---

# ETAPA 2 — Provisionamento das VMs

Após validação do professor, crie as VMs no Proxmox.

Use temporariamente a `vmbr0` para obter Internet e instalar pacotes.

Identifique a interface de rede dentro de cada Alpine:

```bash
ip link
ip addr
```

## Pacotes da VM-WEB

```bash
apk update
apk add nano python3 py3-pip git nginx curl
```

## Pacotes da VM-DB

```bash
apk update
apk add nano mariadb mariadb-client
```

Depois da instalação, desligue a VM e altere a interface no Proxmox de `vmbr0` para `vmbr1`.

---

# ETAPA 3 — Rede interna

Planejamento recomendado após a discussão coletiva:

- VM-WEB: `192.168.56.10/24`
- VM-DB: `192.168.56.20/24`

Na rede Host-Only não é necessário gateway para a comunicação local.

Confirme o nome real da interface com `ip link`.

Exemplo de `/etc/network/interfaces` para VM-WEB:

```text
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
    address 192.168.56.10/24
```

Para VM-DB, altere o endereço para `192.168.56.20/24`.

Reinicie a rede:

```bash
rc-service networking restart
```

Teste:

```bash
ip addr
ip route
ping -c 3 192.168.56.20
```

Na VM-DB, teste o caminho inverso:

```bash
ping -c 3 192.168.56.10
```

---

# ETAPA 4 — Banco de dados

Na VM-DB:

```bash
mariadb-install-db --user=mysql --datadir=/var/lib/mysql
rc-service mariadb start
rc-update add mariadb default
```
Edite o arquivo de conf do MariaDB, adicione # na frente da linha "skip-networking":
```bash
nano /etc/my.cnf.d/mariadb-server.cnf
```

Verifique:

```bash
rc-service mariadb status
ss -lntp | grep 3306
```

Configure o MariaDB para ouvir no endereço da VM-DB. Localize/edite a configuração do servidor em `/etc/my.cnf.d/` e defina na seção `[mysqld]`:

```text
bind-address=192.168.56.20
```

Reinicie:

```bash
rc-service mariadb restart
```

Crie a estrutura:

```bash
mariadb < /caminho/para/schema.sql
```

Ou copie e execute o conteúdo de `sql/schema.sql`.

Depois acesse o MariaDB como administrador e crie o usuário da aplicação:

```sql
CREATE USER 'chamados_app'@'192.168.56.10'
IDENTIFIED BY 'LabSO@2026';

GRANT SELECT, INSERT, UPDATE
ON chamados.*
TO 'chamados_app'@'192.168.56.10';

FLUSH PRIVILEGES;
```

Não use o usuário `root` do banco na aplicação.

---

# ETAPA 5 — Obtenção e execução da aplicação

Na VM-WEB:

```bash
cd /opt
git clone URL_DO_REPOSITORIO chamados-lab
cd chamados-lab
```

Crie o ambiente virtual:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

Se o comando `venv` não estiver disponível na versão do Alpine usada no laboratório, instale o pacote Python correspondente disponível no repositório e repita a criação.

Defina as variáveis da aplicação:

```bash
export DB_HOST=192.168.56.20
export DB_PORT=3306
export DB_NAME=chamados
export DB_USER=chamados_app
export DB_PASSWORD='LabSO@2026'
export APP_HOST=0.0.0.0
export APP_PORT=8000
```

Execute:

```bash
python app.py
```

Teste na própria VM:

```bash
curl http://127.0.0.1:8000/health
```

Teste do Linux Mint:

```bash
curl http://192.168.56.10:8000/health
```

Acesse no navegador:

```text
http://192.168.56.10:8000
```

Cadastre um chamado.

---

# ETAPA 6 — Nginx como reverse proxy

Pare a aplicação e altere:

```bash
export APP_HOST=127.0.0.1
```

Execute novamente:

```bash
python app.py
```

Copie a configuração:

```bash
cp deploy/nginx-chamados.conf /etc/nginx/http.d/default.conf
nginx -t
rc-service nginx restart
```

Agora:

```text
Navegador -> TCP/80 -> Nginx -> TCP/8000 -> Flask -> TCP/3306 -> MariaDB
```

Teste:

```bash
curl http://192.168.56.10/health
```

Acesse no navegador:

```text
http://192.168.56.10
```

---

# ETAPA 7 — Validação e evidências

## Infraestrutura

- [ ] duas VMs funcionando;
- [ ] endereçamento correto;
- [ ] VM-WEB alcança VM-DB;
- [ ] host Linux Mint alcança VM-WEB.

## Banco

- [ ] MariaDB ativo;
- [ ] porta 3306 em escuta;
- [ ] banco `chamados` criado;
- [ ] usuário da aplicação não é `root`;
- [ ] usuário está restrito ao host da VM-WEB.

## Aplicação

- [ ] Python e dependências instalados;
- [ ] `/health` responde corretamente;
- [ ] aplicação consulta o MariaDB;
- [ ] novo chamado é cadastrado;
- [ ] registro permanece após reiniciar a aplicação.

## Nginx

- [ ] Nginx ativo;
- [ ] porta 80 em escuta;
- [ ] acesso final ocorre por `http://192.168.56.10`.

Comandos úteis:

```bash
ip addr
ip route
ping
ss -lntp
ps
free -m
df -h
rc-service
curl
```

---

# Entrega

A dupla deverá entregar:

1. diagrama da arquitetura;
2. tabela de dimensionamento;
3. evidência da aplicação funcionando;
4. evidência de registro persistido no banco;
5. evidência de comunicação VM-WEB -> VM-DB;
6. relatório curto do processo e problemas encontrados;
7. respostas das questões abaixo;
8. demonstração presencial.

## Questões finais

1. Qual requisito levou à criação de uma camada de dados separada?
2. Por que o banco não deve ser acessado diretamente pelo usuário final?
3. Que vantagens e desvantagens existiriam se aplicação e banco estivessem na mesma VM?
4. A aplicação passou de 30 para 3.000 usuários. O que você precisa medir antes de simplesmente aumentar CPU e RAM?
5. Quais informações a equipe DEV deve fornecer para que a INFRA/OPS consiga implantar um sistema?
6. Qual é a função do Nginx e qual é a função do Flask neste ambiente?
7. Por que as credenciais não devem ser gravadas em `app.py`?
