CREATE DATABASE IF NOT EXISTS redes_electricas;
USE redes_electricas;


CREATE TABLE balance (
    fecha DATE,
    valor DECIMAL(10,2),
    tipo VARCHAR(50),
    energia VARCHAR(50),
    region VARCHAR(100),
    PRIMARY KEY (fecha, tipo, energia, region)
);


CREATE TABLE demanda_ire_general (
    fecha DATE,
    valor DECIMAL(10,2),
    porcentaje DECIMAL(5,2),
    indicador VARCHAR(100),
    region VARCHAR(100),
    PRIMARY KEY (fecha, indicador, region),
    FOREIGN KEY (fecha) REFERENCES balance(fecha)
);


CREATE TABLE demanda_evolucion (
    fecha DATE,
    valor DECIMAL(10,2),
    indicador VARCHAR(100),
    region VARCHAR(100),
    PRIMARY KEY (fecha, indicador, region)
);


CREATE TABLE fronteras (
    fecha DATE,
    valor DECIMAL(10,2),
    porcentaje DECIMAL(5,2),
    pais VARCHAR(100),
    año INT,
    PRIMARY KEY (fecha, pais)
);


ALTER TABLE fronteras ADD UNIQUE (pais);

CREATE TABLE enlace_baleares (
    fecha DATE,
    valor DECIMAL(10,2),
    porcentaje DECIMAL(5,2),
    pais VARCHAR(100),
    año INT,
    PRIMARY KEY (fecha, pais),
    FOREIGN KEY (pais) REFERENCES fronteras(pais)
);


CREATE TABLE energia_renovable_norenovable (
    fecha DATE,
    valor DECIMAL(10,2),
    porcentaje DECIMAL(5,2),
    indicador VARCHAR(100),
    region VARCHAR(100),
    tipo VARCHAR(50),
    año INT,
    PRIMARY KEY (fecha, indicador, region, tipo)
);

CREATE TABLE estructura_generacion (
    fecha DATE,
    valor DECIMAL(10,2),
    porcentaje DECIMAL(5,2),
    indicador VARCHAR(100),
    region VARCHAR(100),
    tipo VARCHAR(50),
    año INT,
    PRIMARY KEY (fecha, indicador, region, tipo)
);

CREATE TABLE demanda_ire_industria (
    fecha DATE,
    valor DECIMAL(10,2),
    porcentaje DECIMAL(5,2),
    indicador VARCHAR(100),
    region VARCHAR(100),
    año INT,
    PRIMARY KEY (fecha, indicador, region),
    FOREIGN KEY (fecha) REFERENCES balance(fecha)
);

CREATE TABLE demanda_ire_servicios (
    fecha DATE,
    valor DECIMAL(10,2),
    porcentaje DECIMAL(5,2),
    indicador VARCHAR(100),
    region VARCHAR(100),
    año INT,
    PRIMARY KEY (fecha, indicador, region),
    FOREIGN KEY (fecha) REFERENCES balance(fecha)
);
