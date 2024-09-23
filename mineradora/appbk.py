CREATE TABLE clientes (
    idcliente INT AUTO_INCREMENT PRIMARY KEY,
    cnpj_cpf VARCHAR(20) NOT NULL UNIQUE,
    razao_social VARCHAR(255) NOT NULL,
    apelido VARCHAR(100),
    telefones VARCHAR(255),
    email VARCHAR(255),
    endereco TEXT,
    distancia_km DECIMAL(10, 2)
);
