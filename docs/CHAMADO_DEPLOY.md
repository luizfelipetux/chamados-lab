# Solicitação de deployment — CHG-2026-014

**Solicitante:** Equipe de Desenvolvimento  
**Sistema:** ChamadosLab 1.0  
**Destino:** Ambiente de homologação

A equipe de desenvolvimento concluiu a primeira versão do ChamadosLab, uma aplicação web interna para abertura e acompanhamento de chamados. Até o momento, o sistema foi executado apenas nos computadores dos desenvolvedores.

Precisamos disponibilizar a aplicação para aproximadamente 30 usuários internos.

## Informações fornecidas pela equipe DEV

- a aplicação é acessada por navegador;
- backend em Python + Flask;
- porta padrão da aplicação: TCP/8000;
- banco relacional MariaDB;
- os dados devem persistir;
- somente a aplicação deve possuir credencial para o banco;
- credenciais devem ser fornecidas por variáveis de ambiente;
- a aplicação e a camada de dados devem poder ser mantidas/reiniciadas independentemente;
- o usuário final não deve utilizar o banco diretamente;
- o ambiente possui recursos computacionais limitados.

## Solicitação à equipe INFRA/OPS

Analise a demanda e proponha:

1. arquitetura de infraestrutura;
2. quantidade de máquinas virtuais;
3. dimensionamento de CPU, memória e disco;
4. endereçamento e conectividade;
5. serviços que deverão ser instalados;
6. portas que precisarão estar disponíveis;
7. procedimento de implantação e validação.

**Não existe uma solicitação prévia para "criar duas VMs". A arquitetura deverá ser justificada a partir dos requisitos.**
