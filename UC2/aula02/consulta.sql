CREATE DATABASE vendas_online;
use vendas_online;

#tabela produtos:

CREATE TABLE produtos (
 id_produto INT PRIMARY KEY,
 nome VARCHAR(255),
 categoria VARCHAR(100),
 preco DECIMAL(10, 2),
 estoque INT
);

LOAD DATA LOCAL infile "c:\Users\luiz.calmeida\Documents\BigDataSenacNI\UC2\aula02\vendas_produtos.csv"
INTO TABLE vendas_online.produtos

SELECT * FROM PRODUTOS,

SELECT nome,preco
FROM produtos,

SELECT nome,preco
FROM produtos
WHERE categoria = 'Escritório';
