CREATE DATABASE IF NOT EXISTS redes_electricas;

USE redes_electricas;

-- Tabla central
CREATE TABLE balance (
    fecha DATE,
    tipo VARCHAR(50),
    energia VARCHAR(50),
    region VARCHAR(100),
    valor DECIMAL(10,2),
    PRIMARY KEY (fecha, tipo, energia, region),
    UNIQUE (fecha, region)
);


-- Tabla de indicadores generales
CREATE TABLE demanda_ire_general (
    fecha DATE,
    indicador VARCHAR(100),
    region VARCHAR(100),
    valor DECIMAL(10,2),
    porcentaje DECIMAL(5,2),
    PRIMARY KEY (fecha, indicador, region),
    FOREIGN KEY (fecha, region) REFERENCES balance(fecha, region)
);

-- Evolución de demanda conectada a la tabla anterior
CREATE TABLE demanda_evolucion (
    fecha DATE,
    indicador VARCHAR(100),
    region VARCHAR(100),
    valor DECIMAL(10,2),
    PRIMARY KEY (fecha, indicador, region),
    FOREIGN KEY (fecha, indicador, region) REFERENCES demanda_ire_general(fecha, indicador, region)
);

-- Fronteras conectadas a balance por fecha y región
CREATE TABLE fronteras (
    fecha DATE,
    pais VARCHAR(100),
    region VARCHAR(100),
    valor DECIMAL(10,2),
    porcentaje DECIMAL(5,2),
    año INT,
    PRIMARY KEY (fecha, pais),
    UNIQUE (pais)
);

-- Enlace con Baleares conectado a fronteras por pais
CREATE TABLE enlace_baleares (
    fecha DATE,
    pais VARCHAR(100),
    valor DECIMAL(10,2),
    porcentaje DECIMAL(5,2),
    año INT,
    PRIMARY KEY (fecha, pais),
    FOREIGN KEY (pais) REFERENCES fronteras(pais)
);

-- Energías renovables/no renovables conectadas a demanda_evolucion
CREATE TABLE energia_renovable_norenovable (
    fecha DATE,
    indicador VARCHAR(100),
    region VARCHAR(100),
    tipo VARCHAR(50),
    valor DECIMAL(10,2),
    porcentaje DECIMAL(5,2),
    año INT,
    PRIMARY KEY (fecha, indicador, region, tipo),
    FOREIGN KEY (fecha, indicador, region) REFERENCES demanda_evolucion(fecha, indicador, region)
);

-- Estructura de generación conectada a energía renovable/no renovable
CREATE TABLE estructura_generacion (
    fecha DATE,
    indicador VARCHAR(100),
    region VARCHAR(100),
    tipo VARCHAR(50),
    valor DECIMAL(10,2),
    porcentaje DECIMAL(5,2),
    año INT,
    PRIMARY KEY (fecha, indicador, region, tipo),
    FOREIGN KEY (fecha, indicador, region, tipo) REFERENCES energia_renovable_norenovable(fecha, indicador, region, tipo)
);
