CREATE DATABASE IF NOT EXISTS chamados
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE chamados;

CREATE TABLE IF NOT EXISTS chamados (
    id INT NOT NULL AUTO_INCREMENT,
    titulo VARCHAR(120) NOT NULL,
    solicitante VARCHAR(100) NOT NULL,
    descricao TEXT NOT NULL,
    status ENUM('Aberto', 'Em andamento', 'Concluído')
        NOT NULL DEFAULT 'Aberto',
    criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);
