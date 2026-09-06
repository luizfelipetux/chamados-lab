# Gabarito do professor — Deploy ChamadosLab

## 1. Arquitetura esperada

```text
Linux Mint / navegador
        |
        | HTTP :80
        v
+------------------------+
| VM-WEB                 |
| Alpine Linux           |
| Nginx :80              |
| Flask :8000 localhost  |
+-----------+------------+
            |
            | MariaDB/TCP :3306
            v
+------------------------+
| VM-DB                  |
| Alpine Linux           |
| MariaDB                |
+------------------------+
```

## 2. Dimensionamento recomendado

| VM | vCPU | RAM | Disco | Justificativa |
|---|---:|---:|---:|---|
| VM-WEB | 1 | 512 MB | 4 GB | Alpine + Nginx + Flask têm baixo consumo |
| VM-DB | 1 | 768 MB | 6 GB | MariaDB precisa de mais memória e espaço para dados |

Esses valores são sizing inicial do laboratório, não uma recomendação universal de produção.

## 3. Rede

- VM-WEB: `192.168.56.10/24`
- VM-DB: `192.168.56.20/24`
- host Linux Mint: normalmente `192.168.56.1/24`
- gateway: desnecessário na `vmbr1` para comunicação local

Fluxos esperados:

| Origem | Destino | Porta | Estado |
|---|---|---:|---|
| Linux Mint | VM-WEB | 80 | permitido |
| VM-WEB/Nginx | Flask local | 8000 | local à VM |
| VM-WEB | VM-DB | 3306 | permitido |
| usuário final | VM-DB | 3306 | não deve ser usado/autorizado |

## 4. Relação requisito -> arquitetura -> infraestrutura

| Requisito | Impacto arquitetural | Impacto na infraestrutura |
|---|---|---|
| Acesso via navegador | camada web | VM-WEB com HTTP |
| Banco relacional | camada de dados | MariaDB |
| Persistência | dados fora do processo Flask | armazenamento da VM-DB |
| Banco não usado pelo usuário | acesso mediado pela aplicação | credencial restrita à VM-WEB |
| Manutenção independente | separação de responsabilidades | VM-WEB e VM-DB distintas |
| Credenciais fora do código | configuração externa | variáveis de ambiente |
| Baixo consumo | componentes leves | Alpine + sizing reduzido |

## 5. MariaDB

Inicialização:

```bash
mariadb-install-db --user=mysql --datadir=/var/lib/mysql
rc-service mariadb start
rc-update add mariadb default
```

Configuração esperada:

```text
[mysqld]
bind-address=192.168.56.20
```

Usuário didático:

```sql
CREATE USER 'chamados_app'@'192.168.56.10'
IDENTIFIED BY 'LabSO@2026';

GRANT SELECT, INSERT, UPDATE
ON chamados.*
TO 'chamados_app'@'192.168.56.10';

FLUSH PRIVILEGES;
```

Resultado esperado:

```bash
ss -lntp | grep 3306
```

deve indicar o MariaDB em escuta.

## 6. Aplicação

Variáveis:

```bash
export DB_HOST=192.168.56.20
export DB_PORT=3306
export DB_NAME=chamados
export DB_USER=chamados_app
export DB_PASSWORD='LabSO@2026'
export APP_PORT=8000
```

Antes do Nginx:

```bash
export APP_HOST=0.0.0.0
python app.py
```

Depois do Nginx:

```bash
export APP_HOST=127.0.0.1
python app.py
```

Health check esperado:

```json
{"database":true,"status":"ok"}
```

## 7. Nginx

Papel: receber o HTTP do cliente na porta 80 e encaminhar a requisição ao servidor Flask na porta 8000.

Validação:

```bash
nginx -t
rc-service nginx restart
ss -lntp | grep -E ':80|:8000'
curl http://127.0.0.1:8000/health
curl http://192.168.56.10/health
```

## 8. Troubleshooting

| Sintoma | Hipóteses | Diagnóstico | Correção |
|---|---|---|---|
| WEB não pinga DB | IP/máscara/interface incorretos | `ip addr`, `ip route`, `ping` | corrigir rede |
| Flask acusa conexão recusada | MariaDB parado ou bind incorreto | `rc-service mariadb status`, `ss -lntp` | iniciar serviço/corrigir bind |
| Access denied no banco | usuário, senha ou host incorretos | teste com `mariadb -h ...` | corrigir grants/env |
| `/health` retorna 503 | dependência de banco indisponível | ler JSON e testar DB | restaurar conexão |
| porta 8000 não responde | Flask parado/bind errado | `ps`, `ss -lntp` | reiniciar e corrigir `APP_HOST` |
| porta 80 não responde | Nginx parado/configuração inválida | `nginx -t`, `rc-service nginx status` | corrigir config |
| Nginx retorna 502 | Flask não está em 127.0.0.1:8000 | `curl 127.0.0.1:8000/health` | iniciar Flask |
| aplicação abre mas não grava | grants incompletos ou tabela ausente | logs/SQL manual | criar schema e conceder INSERT |
| após trocar vmbr0 por vmbr1 a Internet some | comportamento esperado da Host-Only | `ip route` | não é erro; pacotes devem ser instalados antes |

## 9. Problemas propositalmente provocáveis

1. Alterar `DB_HOST` para `192.168.56.21`.
2. Parar MariaDB com `rc-service mariadb stop`.
3. Alterar `DB_PASSWORD`.
4. Parar Flask mantendo Nginx ativo para gerar 502.
5. Alterar a porta do Flask para 8001 sem mudar o Nginx.

Pergunta obrigatória antes da correção:

> Em qual camada está a falha: rede, banco, aplicação ou proxy?

## 10. Respostas das questões finais

1. Persistência, restrição de acesso e manutenção independente justificam a camada de dados separada.
2. Para reduzir exposição, aplicar regras através da aplicação e limitar credenciais/privilégios.
3. Mesma VM simplifica e reduz recursos, porém reduz isolamento e acopla manutenção/falhas das duas camadas.
4. Medir CPU, RAM, I/O, conexões, latência, volume de dados, padrão de requisições e gargalos.
5. Runtime, dependências, portas, banco, variáveis de ambiente, persistência, requisitos de segurança, volume de usuários/carga e critérios de saúde.
6. Nginx recebe/proxy HTTP; Flask executa a lógica da aplicação.
7. Para evitar exposição de segredos no repositório, histórico Git e compartilhamentos do código.

## 11. Rubrica sugerida — 10 pontos

| Critério | Pontos |
|---|---:|
| Arquitetura e justificativa pelos requisitos | 2,0 |
| Dimensionamento e rede | 1,0 |
| VMs e serviços corretamente configurados | 2,0 |
| Banco, usuário e persistência | 1,5 |
| Aplicação + Nginx funcionando | 1,5 |
| Diagnóstico/evidências técnicas | 1,0 |
| Relatório e respostas conceituais | 1,0 |
