-- Crear base de datos y seleccionarla
CREATE DATABASE IF NOT EXISTS redes_electricas;
USE redes_electricas;

-- Tabla central: balance
CREATE TABLE balance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    tipo VARCHAR(50),
    energia VARCHAR(50),
    region VARCHAR(100) NOT NULL,
    valor DECIMAL(10,2),
    UNIQUE KEY unique_fecha_region (fecha, region)
);

-- Indicadores generales de demanda
CREATE TABLE demanda_ire_general (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    indicador VARCHAR(100) NOT NULL,
    region VARCHAR(100) NOT NULL,
    valor DECIMAL(10,2),
    porcentaje DECIMAL(5,2),
    UNIQUE KEY unique_fecha_indicador_region (fecha, indicador, region),
    FOREIGN KEY (fecha, region) REFERENCES balance(fecha, region)
);

-- Evolución de la demanda
CREATE TABLE demanda_evolucion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    indicador VARCHAR(100) NOT NULL,
    region VARCHAR(100) NOT NULL,
    valor DECIMAL(10,2),
    FOREIGN KEY (fecha, region) REFERENCES balance(fecha, region)
);

-- Fronteras eléctricas (sin foreign key)
CREATE TABLE fronteras (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    pais VARCHAR(100) NOT NULL,
    valor DECIMAL(10,2),
    porcentaje DECIMAL(5,2)
);

-- Estructura de generación
CREATE TABLE estructura_generacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    indicador VARCHAR(100) NOT NULL,
    region VARCHAR(100) NOT NULL,
    tipo VARCHAR(50),
    valor DECIMAL(10,2),
    porcentaje DECIMAL(5,2),
    FOREIGN KEY (fecha, region) REFERENCES balance(fecha, region)
);