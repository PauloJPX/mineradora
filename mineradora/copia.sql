CREATE TABLE `acesso` (
  `idacesso` int NOT NULL AUTO_INCREMENT,
  `idusuario` int DEFAULT NULL,
  `idmodulo` int DEFAULT NULL,
  PRIMARY KEY (`idacesso`),
  KEY `idusuario` (`idusuario`),
  KEY `idmodulo` (`idmodulo`),
  CONSTRAINT `acesso_ibfk_1` FOREIGN KEY (`idusuario`) REFERENCES `usuarios` (`idusuario`),
  CONSTRAINT `acesso_ibfk_2` FOREIGN KEY (`idmodulo`) REFERENCES `modulo` (`idmodulo`)
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO acesso (idacesso, idusuario, idmodulo) VALUES (53, 8, 7);
INSERT INTO acesso (idacesso, idusuario, idmodulo) VALUES (54, 9, 1);
INSERT INTO acesso (idacesso, idusuario, idmodulo) VALUES (55, 9, 5);


CREATE TABLE `caminhao` (
  `idcaminhao` int NOT NULL AUTO_INCREMENT,
  `placa` varchar(10) NOT NULL,
  `modelo` varchar(50) DEFAULT NULL,
  `ano` year DEFAULT NULL,
  `capacidade` float DEFAULT NULL,
  `proprietario` varchar(100) DEFAULT NULL,
  `motorista` varchar(100) DEFAULT NULL,
  `capacidade_tanque` float DEFAULT NULL,
  PRIMARY KEY (`idcaminhao`),
  UNIQUE KEY `placa` (`placa`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO caminhao (idcaminhao, placa, modelo, ano, capacidade, proprietario, motorista, capacidade_tanque) VALUES (2, 'aaa', 'teste', 1980, 123.0, 'jose paulo', 'joao teste', 456.0);
INSERT INTO caminhao (idcaminhao, placa, modelo, ano, capacidade, proprietario, motorista, capacidade_tanque) VALUES (3, 'abc123', 'bercedes bens', 1994, 12.0, 'jose da silva', 'joao', 123.0);
INSERT INTO caminhao (idcaminhao, placa, modelo, ano, capacidade, proprietario, motorista, capacidade_tanque) VALUES (5, 'gvq111', 'mercedez', 2007, 15.0, 'igor', 'igor', 50.0);


CREATE TABLE `clientes` (
  `idcliente` int NOT NULL AUTO_INCREMENT,
  `cnpj_cpf` varchar(20) NOT NULL,
  `razao_social` varchar(255) NOT NULL,
  `apelido` varchar(100) DEFAULT NULL,
  `telefones` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `endereco` text,
  `distancia_km` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`idcliente`),
  UNIQUE KEY `cnpj_cpf` (`cnpj_cpf`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO clientes (idcliente, cnpj_cpf, razao_social, apelido, telefones, email, endereco, distancia_km) VALUES (1, '88974391791', 'jpvoo sytemas ltda', 'paulojpx', '21 998502710\r\n21 249-2529', 'jpaulojpx@gmail.com', 'caminho cabungui 807 vargem grande', Decimal('13.00'));
INSERT INTO clientes (idcliente, cnpj_cpf, razao_social, apelido, telefones, email, endereco, distancia_km) VALUES (2, '06767876897', 'luciane borges', 'luluzinha', '8484787487', 'lu@hotmail.com', 'jfkgfjkgfkjgkj', Decimal('20.00'));
INSERT INTO clientes (idcliente, cnpj_cpf, razao_social, apelido, telefones, email, endereco, distancia_km) VALUES (5, '16985696708', 'polimix sao pedro', 'polimix sp', '3783750750', 'kjfkdjfk@kejkej', 'kfjgkjkf', Decimal('15.00'));


CREATE TABLE `entrega` (
  `identrega` int NOT NULL AUTO_INCREMENT,
  `numero_entrega` varchar(50) NOT NULL,
  `data_entrega` date NOT NULL,
  `idvenda` int NOT NULL,
  `idcaminhao` int NOT NULL,
  `quantidade` decimal(10,2) NOT NULL,
  PRIMARY KEY (`identrega`),
  UNIQUE KEY `unique_numero_entrega` (`numero_entrega`),
  KEY `idvenda` (`idvenda`),
  KEY `idcaminhao` (`idcaminhao`),
  CONSTRAINT `entrega_ibfk_1` FOREIGN KEY (`idvenda`) REFERENCES `vendas` (`idvenda`) ON DELETE RESTRICT,
  CONSTRAINT `entrega_ibfk_2` FOREIGN KEY (`idcaminhao`) REFERENCES `caminhao` (`idcaminhao`) ON DELETE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO entrega (identrega, numero_entrega, data_entrega, idvenda, idcaminhao, quantidade) VALUES (30, '3', datetime.date(2024, 11, 3), 11, 2, Decimal('3333.00'));
INSERT INTO entrega (identrega, numero_entrega, data_entrega, idvenda, idcaminhao, quantidade) VALUES (33, '2', datetime.date(2024, 11, 7), 14, 3, Decimal('777.00'));
INSERT INTO entrega (identrega, numero_entrega, data_entrega, idvenda, idcaminhao, quantidade) VALUES (34, '33', datetime.date(2024, 11, 15), 17, 5, Decimal('7.50'));
INSERT INTO entrega (identrega, numero_entrega, data_entrega, idvenda, idcaminhao, quantidade) VALUES (35, '44', datetime.date(2024, 11, 15), 18, 5, Decimal('66.00'));


CREATE TABLE `modulo` (
  `idmodulo` int NOT NULL AUTO_INCREMENT,
  `nome_modulo` varchar(50) NOT NULL,
  `rota` varchar(100) NOT NULL,
  PRIMARY KEY (`idmodulo`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO modulo (idmodulo, nome_modulo, rota) VALUES (1, 'Home', 'inicio.inicial');
INSERT INTO modulo (idmodulo, nome_modulo, rota) VALUES (2, 'Clientes', 'clientes.cadastro_cliente');
INSERT INTO modulo (idmodulo, nome_modulo, rota) VALUES (3, 'Caminhões', 'caminhoes.cadastro_caminhao');
INSERT INTO modulo (idmodulo, nome_modulo, rota) VALUES (4, 'Produtos', 'produtos.cadastro_produto');
INSERT INTO modulo (idmodulo, nome_modulo, rota) VALUES (5, 'Vendas', 'vendas.incluir_venda');
INSERT INTO modulo (idmodulo, nome_modulo, rota) VALUES (6, 'Entregas', 'entregas.incluir_entrega');
INSERT INTO modulo (idmodulo, nome_modulo, rota) VALUES (7, 'Consultas', 'consultas.pagina_consultas');
INSERT INTO modulo (idmodulo, nome_modulo, rota) VALUES (9, 'Cadastro de Usuário', 'usuarios.cadastro');
INSERT INTO modulo (idmodulo, nome_modulo, rota) VALUES (10, 'Acessos', 'acesso.cadastro_acesso');


CREATE TABLE `produtos` (
  `idproduto` int NOT NULL AUTO_INCREMENT,
  `descricao` varchar(255) NOT NULL,
  `nosso` tinyint(1) NOT NULL,
  `preco_de_custo` decimal(10,2) NOT NULL,
  `preco_de_venda` decimal(10,2) NOT NULL,
  PRIMARY KEY (`idproduto`),
  UNIQUE KEY `unique_descricao` (`descricao`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO produtos (idproduto, descricao, nosso, preco_de_custo, preco_de_venda) VALUES (1, 'areia', 1, Decimal('23.00'), Decimal('33.00'));
INSERT INTO produtos (idproduto, descricao, nosso, preco_de_custo, preco_de_venda) VALUES (6, 'diesel', 0, Decimal('5.00'), Decimal('6.00'));


CREATE TABLE `usuarios` (
  `idusuario` int NOT NULL AUTO_INCREMENT,
  `usuario` varchar(50) NOT NULL,
  `senha` varchar(255) NOT NULL,
  `is_admin` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`idusuario`),
  UNIQUE KEY `usuario` (`usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO usuarios (idusuario, usuario, senha, is_admin) VALUES (5, 'gerente', 'scrypt:32768:8:1$6v5WOQTVs8CGWZwA$46adcec8031ad5c9ed16e6c970af98f0908bce840027650c12e97f50b968e26ece07f3103baa2f164d2aa54ab94792ee475465fe3f308be79f179ac169803fb1', 1);
INSERT INTO usuarios (idusuario, usuario, senha, is_admin) VALUES (6, 'admin', 'scrypt:32768:8:1$e5mjcTNv3Sgc0Omo$337bba3a77fe3e710321c00622a7876f0dfb26493077aa5047ee7db1a60b68385fd58a405d774367dbc1acf67835bf4a1334060859398ff7b71809ea2871e005', 1);
INSERT INTO usuarios (idusuario, usuario, senha, is_admin) VALUES (8, 'lu', 'scrypt:32768:8:1$WgRFklbKSy6v3RkS$fce0cbf1d5db0446605a7027e56eae6b81d7c26b379582738a48c99a25b2de3b0c7b70ef097f1b3fe6885e79e9d78234fd707cb1ef730967f6e2e69a7b7fb10a', 0);
INSERT INTO usuarios (idusuario, usuario, senha, is_admin) VALUES (9, 'rosano', 'scrypt:32768:8:1$slTwfw7bHbb7jT5Z$4c9889417a0938a4c39eeb7c71837d7a5333e51722c33a38ab3fcefb229eba5ccf693ff85c4f159f9e3d6bb1d92e2cac8a689d622bf279451d30b7e626761cf1', 0);


CREATE TABLE `vendas` (
  `idvenda` int NOT NULL AUTO_INCREMENT,
  `numerovenda` int NOT NULL,
  `idcliente` int NOT NULL,
  `idproduto` int NOT NULL,
  `data_venda` date NOT NULL,
  `data_entrega` date DEFAULT NULL,
  `quantidade` decimal(10,2) DEFAULT NULL,
  `valor_produto` decimal(10,2) NOT NULL,
  `valor_produto_negociado` decimal(10,2) NOT NULL,
  `valor_frete` decimal(10,2) NOT NULL,
  `valor_total` decimal(10,2) NOT NULL,
  PRIMARY KEY (`idvenda`),
  UNIQUE KEY `unique_numerovenda` (`numerovenda`),
  KEY `idcliente` (`idcliente`),
  KEY `idproduto` (`idproduto`),
  CONSTRAINT `vendas_ibfk_1` FOREIGN KEY (`idcliente`) REFERENCES `clientes` (`idcliente`),
  CONSTRAINT `vendas_ibfk_2` FOREIGN KEY (`idproduto`) REFERENCES `produtos` (`idproduto`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO vendas (idvenda, numerovenda, idcliente, idproduto, data_venda, data_entrega, quantidade, valor_produto, valor_produto_negociado, valor_frete, valor_total) VALUES (3, 3, 1, 1, datetime.date(2024, 9, 12), NULL, Decimal('23.00'), Decimal('1.00'), Decimal('1.00'), Decimal('23.00'), Decimal('46.00'));
INSERT INTO vendas (idvenda, numerovenda, idcliente, idproduto, data_venda, data_entrega, quantidade, valor_produto, valor_produto_negociado, valor_frete, valor_total) VALUES (11, 1, 1, 1, datetime.date(2024, 10, 15), NULL, Decimal('12.00'), Decimal('1.00'), Decimal('1.00'), Decimal('34.00'), Decimal('46.00'));
INSERT INTO vendas (idvenda, numerovenda, idcliente, idproduto, data_venda, data_entrega, quantidade, valor_produto, valor_produto_negociado, valor_frete, valor_total) VALUES (14, 4, 1, 1, datetime.date(2024, 10, 30), NULL, Decimal('12.00'), Decimal('1.00'), Decimal('21.00'), Decimal('34.00'), Decimal('286.00'));
INSERT INTO vendas (idvenda, numerovenda, idcliente, idproduto, data_venda, data_entrega, quantidade, valor_produto, valor_produto_negociado, valor_frete, valor_total) VALUES (15, 7, 1, 1, datetime.date(2024, 10, 30), NULL, Decimal('12.50'), Decimal('1.00'), Decimal('3.00'), Decimal('12.00'), Decimal('49.50'));
INSERT INTO vendas (idvenda, numerovenda, idcliente, idproduto, data_venda, data_entrega, quantidade, valor_produto, valor_produto_negociado, valor_frete, valor_total) VALUES (16, 5, 2, 1, datetime.date(2024, 11, 5), NULL, Decimal('12.00'), Decimal('1.00'), Decimal('0.50'), Decimal('22.00'), Decimal('28.00'));
INSERT INTO vendas (idvenda, numerovenda, idcliente, idproduto, data_venda, data_entrega, quantidade, valor_produto, valor_produto_negociado, valor_frete, valor_total) VALUES (17, 22, 5, 1, datetime.date(2024, 11, 15), NULL, Decimal('38.00'), Decimal('33.00'), Decimal('35.00'), Decimal('1330.00'), Decimal('2660.00'));
INSERT INTO vendas (idvenda, numerovenda, idcliente, idproduto, data_venda, data_entrega, quantidade, valor_produto, valor_produto_negociado, valor_frete, valor_total) VALUES (18, 33, 5, 1, datetime.date(2024, 11, 15), NULL, Decimal('50.00'), Decimal('33.00'), Decimal('35.00'), Decimal('700.00'), Decimal('2450.00'));


