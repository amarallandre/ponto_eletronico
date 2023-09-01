CREATE DATABASE ponto_eletronico;

CREATE TABLE registros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_funcionario INT,
    data DATE,
    horario_entrada DATETIME,
    horario_almoco_saida DATETIME,
    horario_almoco_retorno DATETIME,
    horario_saida DATETIME,
    FOREIGN KEY (id_funcionario) REFERENCES funcionarios(id)
);