-- Database: "PuenteChino"

-- DROP DATABASE "PuenteChino";

CREATE TABLE estructura (
    id_estructura SERIAL NOT NULL,
    nombre_estructura varchar(100) NOT NULL,

    PRIMARY KEY(id_estructura)
);
CREATE TABLE sensores (
    id_sensor SERIAL NOT NULL,
    id_estructura INT NOT NULL,
    tipo_sensor varchar(100) NOT NULL,
    nombre_sensor varchar(100) NOT NULL,

    PRIMARY KEY(id_sensor),
    UNIQUE (nombre_sensor),
    FOREIGN KEY (id_estructura)
        REFERENCES estructura(id_estructura)
);
CREATE TABLE acelerometro1 (
    id_lectura SERIAL NOT NULL,
    nombre_sensor varchar(100) NOT NULL,
    fecha timestamp NOT NULL,
    lectura float NOT NULL,
    
    PRIMARY KEY(id_lectura),
    
    FOREIGN KEY (nombre_sensor)
        REFERENCES sensores(nombre_sensor)
);
CREATE TABLE acelerometro2 (
    id_lectura SERIAL NOT NULL,
    nombre_sensor varchar(100) NOT NULL,
    fecha timestamp NOT NULL,
    lectura float NOT NULL,
    
    PRIMARY KEY(id_lectura),
    
    FOREIGN KEY (nombre_sensor)
        REFERENCES sensores(nombre_sensor)
);
CREATE TABLE acelerometro3 (
    id_lectura SERIAL NOT NULL,
    nombre_sensor varchar(100) NOT NULL,
    fecha timestamp NOT NULL,
    lectura float NOT NULL,
    
    PRIMARY KEY(id_lectura),
    
    FOREIGN KEY (nombre_sensor)
        REFERENCES sensores(nombre_sensor)
);
CREATE TABLE acelerometro4 (
    id_lectura SERIAL NOT NULL,
    nombre_sensor varchar(100) NOT NULL,
    fecha timestamp NOT NULL,
    lectura float NOT NULL,
    
    PRIMARY KEY(id_lectura),
    
    FOREIGN KEY (nombre_sensor)
        REFERENCES sensores(nombre_sensor)
);
CREATE TABLE acelerometro5 (
    id_lectura SERIAL NOT NULL,
    nombre_sensor varchar(100) NOT NULL,
    fecha timestamp NOT NULL,
    lectura float NOT NULL,
    
    PRIMARY KEY(id_lectura),
    
    FOREIGN KEY (nombre_sensor)
        REFERENCES sensores(nombre_sensor)
);
CREATE TABLE acelerometro6 (
    id_lectura SERIAL NOT NULL,
    nombre_sensor varchar(100) NOT NULL,
    fecha timestamp NOT NULL,
    lectura float NOT NULL,
    
    PRIMARY KEY(id_lectura),
    
    FOREIGN KEY (nombre_sensor)
        REFERENCES sensores(nombre_sensor)
);
CREATE TABLE acelerometro7 (
    id_lectura SERIAL NOT NULL,
    nombre_sensor varchar(100) NOT NULL,
    fecha timestamp NOT NULL,
    lectura float NOT NULL,
    
    PRIMARY KEY(id_lectura),
    
    FOREIGN KEY (nombre_sensor)
        REFERENCES sensores(nombre_sensor)
);
CREATE TABLE acelerometro8 (
    id_lectura SERIAL NOT NULL,
    nombre_sensor varchar(100) NOT NULL,
    fecha timestamp NOT NULL,
    lectura float NOT NULL,
    
    PRIMARY KEY(id_lectura),
    
    FOREIGN KEY (nombre_sensor)
        REFERENCES sensores(nombre_sensor)
);
CREATE TABLE acelerometro9 (
    id_lectura SERIAL NOT NULL,
    nombre_sensor varchar(100) NOT NULL,
    fecha timestamp NOT NULL,
    lectura float NOT NULL,
    
    PRIMARY KEY(id_lectura),
    
    FOREIGN KEY (nombre_sensor)
        REFERENCES sensores(nombre_sensor)
);
CREATE TABLE acelerometro10 (
    id_lectura SERIAL NOT NULL,
    nombre_sensor varchar(100) NOT NULL,
    fecha timestamp NOT NULL,
    lectura float NOT NULL,
    
    PRIMARY KEY(id_lectura),
    
    FOREIGN KEY (nombre_sensor)
        REFERENCES sensores(nombre_sensor)
);
CREATE TABLE acelerometro11 (
    id_lectura SERIAL NOT NULL,
    nombre_sensor varchar(100) NOT NULL,
    fecha timestamp NOT NULL,
    lectura float NOT NULL,
    
    PRIMARY KEY(id_lectura),
    
    FOREIGN KEY (nombre_sensor)
        REFERENCES sensores(nombre_sensor)
);
CREATE TABLE acelerometro12 (
    id_lectura SERIAL NOT NULL,
    nombre_sensor varchar(100) NOT NULL,
    fecha timestamp NOT NULL,
    lectura float NOT NULL,
    
    PRIMARY KEY(id_lectura),
    
    FOREIGN KEY (nombre_sensor)
        REFERENCES sensores(nombre_sensor)
);
CREATE TABLE acelerometro13 (
    id_lectura SERIAL NOT NULL,
    nombre_sensor varchar(100) NOT NULL,
    fecha timestamp NOT NULL,
    lectura float NOT NULL,
    
    PRIMARY KEY(id_lectura),
    
    FOREIGN KEY (nombre_sensor)
        REFERENCES sensores(nombre_sensor)
);
CREATE TABLE acelerometro14 (
    id_lectura SERIAL NOT NULL,
    nombre_sensor varchar(100) NOT NULL,
    fecha timestamp NOT NULL,
    lectura float NOT NULL,
    
    PRIMARY KEY(id_lectura),
    
    FOREIGN KEY (nombre_sensor)
        REFERENCES sensores(nombre_sensor)
);
CREATE TABLE vel_viento (
    id_lectura SERIAL NOT NULL,
    nombre_sensor varchar(100) NOT NULL,
    fecha timestamp NOT NULL,
    lectura float NOT NULL,
    
    PRIMARY KEY(id_lectura),
    
    FOREIGN KEY (nombre_sensor)
        REFERENCES sensores(nombre_sensor)
);
CREATE TABLE dir_viento (
    id_lectura SERIAL NOT NULL,
    nombre_sensor varchar(100) NOT NULL,
    fecha timestamp NOT NULL,
    lectura float NOT NULL,
    
    PRIMARY KEY(id_lectura),
    
    FOREIGN KEY (nombre_sensor)
        REFERENCES sensores(nombre_sensor)
);
CREATE TABLE temperatura (
    id_lectura SERIAL NOT NULL,
    nombre_sensor varchar(100) NOT NULL,
    fecha timestamp NOT NULL,
    lectura float NOT NULL,
    
    PRIMARY KEY(id_lectura),
    
    FOREIGN KEY (nombre_sensor)
        REFERENCES sensores(nombre_sensor)
);
CREATE TABLE humedad (
    id_lectura SERIAL NOT NULL,
    nombre_sensor varchar(100) NOT NULL,
    fecha timestamp NOT NULL,
    lectura float NOT NULL,
    
    PRIMARY KEY(id_lectura),
    
    FOREIGN KEY (nombre_sensor)
        REFERENCES sensores(nombre_sensor)
);
