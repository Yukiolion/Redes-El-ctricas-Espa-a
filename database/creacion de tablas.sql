CREATE DATABASE IF NOT EXISTS redes_electricas;
USE redes_electricas;
CREATE TABLE balance (
    fecha INT,
    valor DECIMAL(10,2),
    tipo CHAR(50),
    energia CHAR(50),
    region CHAR(100),
    PRIMARY KEY (fecha, tipo, energia, region)
);
CREATE TABLE demanda_ire_general (
    fecha INT,
    valor DECIMAL(10,2),
    porcentaje DECIMAL(5,2),
    indicador CHAR(100),
    region CHAR(100),
    PRIMARY KEY (fecha, indicador, region),
    FOREIGN KEY (fecha) REFERENCES balance(fecha)
);
CREATE TABLE demanda_evolucion (
    fecha INT,
    valor DECIMAL(10,2),
    indicador CHAR(100),
    region CHAR(100),
    PRIMARY KEY (fecha, indicador, region),
    FOREIGN KEY (indicador) REFERENCES demanda_ire_general(indicador)
);
CREATE TABLE fronteras (
    fecha INT,
    valor DECIMAL(10,2),
    porcentaje DECIMAL(5,2),
    pais CHAR(100),
    año INT,
    PRIMARY KEY (fecha, pais),
    FOREIGN KEY (fecha) REFERENCES demanda_evolucion(fecha)
);
CREATE TABLE enlace_baleares (
    fecha INT,
    valor DECIMAL(10,2),
    porcentaje DECIMAL(5,2),
    pais CHAR(100),
    año INT,
    PRIMARY KEY (fecha, pais),
    FOREIGN KEY (pais) REFERENCES fronteras(pais)
);
CREATE TABLE energia_renovable_norenovable (
    fecha INT,
    valor DECIMAL(10,2),
    porcentaje DECIMAL(5,2),
    indicador CHAR(100),
    region CHAR(100),
    tipo CHAR(50),
    año INT,
    PRIMARY KEY (fecha, indicador, region, tipo),
    FOREIGN KEY (año) REFERENCES enlace_baleares(año)
);
CREATE TABLE estructura_generacion (
    fecha INT,
    valor DECIMAL(10,2),
    porcentaje DECIMAL(5,2),
    indicador CHAR(100),
    region CHAR(100),
    tipo CHAR(50),
    año INT,
    PRIMARY KEY (fecha, indicador, region, tipo),
    FOREIGN KEY (tipo) REFERENCES energia_renovable_norenovable(tipo)
);