CREATE TABLE director(
    id_director SERIAL PRIMARY KEY,
    ci VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    password VARCHAR(100) NOT NULL
);
CREATE TABLE profesor(
    id_profesor SERIAL PRIMARY KEY,
    ci VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    password VARCHAR(100) NOT NULL
);
CREATE TABLE curso(
    id_curso SERIAL PRIMARY KEY,
    grado VARCHAR(20) NOT NULL,
    paralelo CHAR(1) NOT NULL
);
CREATE TABLE estudiante(
    id_estudiante SERIAL PRIMARY KEY,
    ci VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    password VARCHAR(100) NOT NULL,
    id_curso INTEGER NOT NULL,
    FOREIGN KEY(id_curso)
    REFERENCES curso(id_curso)
);
CREATE TABLE materia(
    id_materia SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL
);
CREATE TABLE profesor_materia(
    id_profesor_materia SERIAL PRIMARY KEY,
    id_profesor INTEGER NOT NULL,
    id_materia INTEGER NOT NULL,
    id_curso INTEGER NOT NULL,
    FOREIGN KEY(id_profesor)
    REFERENCES profesor(id_profesor),
    FOREIGN KEY(id_materia)
    REFERENCES materia(id_materia),
    FOREIGN KEY(id_curso)
    REFERENCES curso(id_curso)
);
CREATE TABLE representante(
    id_representante SERIAL PRIMARY KEY,
    id_estudiante INTEGER NOT NULL,
    cargo VARCHAR(20) NOT NULL,
    FOREIGN KEY(id_estudiante)
    REFERENCES estudiante(id_estudiante)
);
CREATE TABLE practica(
    id_practica SERIAL PRIMARY KEY,
    id_materia INTEGER NOT NULL,
    titulo VARCHAR(100) NOT NULL,
    FOREIGN KEY(id_materia)
    REFERENCES materia(id_materia)
);
CREATE TABLE nota_practica(
    id_nota_practica SERIAL PRIMARY KEY,
    id_practica INTEGER NOT NULL,
    id_estudiante INTEGER NOT NULL,
    nota NUMERIC(5,2) NOT NULL,
    FOREIGN KEY(id_practica)
    REFERENCES practica(id_practica),
    FOREIGN KEY(id_estudiante)
    REFERENCES estudiante(id_estudiante)
);
CREATE TABLE nota_trimestre(
    id_nota SERIAL PRIMARY KEY,
    id_estudiante INTEGER NOT NULL,
    id_materia INTEGER NOT NULL,
    trimestre INTEGER NOT NULL,
    nota NUMERIC(5,2) NOT NULL,
    FOREIGN KEY(id_estudiante)
    REFERENCES estudiante(id_estudiante),
    FOREIGN KEY(id_materia)
    REFERENCES materia(id_materia)
);
CREATE TABLE permiso_notas(
    id_permiso SERIAL PRIMARY KEY,
    id_profesor INTEGER UNIQUE NOT NULL,
    habilitado BOOLEAN DEFAULT FALSE,
    FOREIGN KEY(id_profesor)
    REFERENCES profesor(id_profesor));
	
INSERT INTO curso(grado, paralelo)
VALUES
('4to Secundaria','A'),
('4to Secundaria','B'),
('4to Secundaria','C'),
('4to Secundaria','D'),
('4to Secundaria','E');
INSERT INTO materia(nombre)
VALUES
('Lenguaje'),
('Matematicas'),
('Ciencias Sociales'),
('Biologia'),
('Ingles'),
('Quimica'),
('Fisica'),
('Educacion Fisica'),
('Informatica');

INSERT INTO director
(ci,nombre,apellido,password)
VALUES
('10000000','Juan','Director','admin123');

INSERT INTO profesor
(ci,nombre,apellido,password)
VALUES
('20000001','Carlos','Mamani','1234'),
('20000002','Maria','Quispe','1234'),
('20000003','Luis','Flores','1234'),
('20000004','Ana','Rojas','1234'),
('20000005','Pedro','Choque','1234'),
('20000006','Sandra','Perez','1234'),
('20000007','Miguel','Lopez','1234'),
('20000008','Valeria','Guzman','1234'),
('20000009','Jose','Condori','1234');

INSERT INTO permiso_notas(id_profesor)
SELECT id_profesor
FROM profesor;

INSERT INTO profesor_materia
(id_profesor,id_materia,id_curso)
VALUES
(1,1,1),
(2,2,1),
(3,3,1),
(4,4,1),
(5,5,1),
(6,6,1),
(7,7,1),
(8,8,1),
(9,9,1);

SELECT
    e.nombre,
    e.apellido,
    AVG(n.nota) AS promedio,
    CASE
        WHEN AVG(n.nota) >= 51
        THEN 'APROBADO'
        ELSE 'REPROBADO'
    END AS estado
FROM estudiante e
JOIN nota_trimestre n
ON e.id_estudiante=n.id_estudiante
GROUP BY
e.id_estudiante,
e.nombre,
e.apellido;

INSERT INTO estudiante
(
    ci,
    nombre,
    apellido,
    password,
    id_curso,
    fecha_ingreso
)
VALUES
-- 4to A (1)
('80000001','Carlos','Mamani','1234',1),
('80000002','Ana','Quispe','1234',1),
('80000003','Luis','Choque','1234',1),
('80000004','Maria','Flores','1234',1),
('80000005','Pedro','Rojas','1234',1),
('80000006','Valeria','Guzman','1234',1),
('80000007','Miguel','Condori','1234',1),
('80000008','Daniela','Lopez','1234',1),
('80000009','Jorge','Vargas','1234',1),
('80000010','Sofia','Mendoza','1234',1),
('80000011','Kevin','Alarcon','1234',1),
('80000012','Paola','Huanca','1234',1),
('80000013','Diego','Ticona','1234',1),
('80000014','Fernanda','Calle','1234',1),
('80000015','Jose','Apaza','1234',1),

-- 4to B (2)
('80000016','Roberto','Mamani','1234',2),
('80000017','Carla','Quispe','1234',2),
('80000018','Brayan','Choque','1234',2),
('80000019','Lucia','Flores','1234',2),
('80000020','Fernando','Rojas','1234',2),
('80000021','Natalia','Guzman','1234',2),
('80000022','Cristian','Condori','1234',2),
('80000023','Gabriela','Lopez','1234',2),
('80000024','Marco','Vargas','1234',2),
('80000025','Tatiana','Mendoza','1234',2),
('80000026','Juan','Alarcon','1234',2),
('80000027','Camila','Huanca','1234',2),
('80000028','Oscar','Ticona','1234',2),
('80000029','Roxana','Calle','1234',2),
('80000030','Pablo','Apaza','1234',2),

-- 4to C (3)
('80000031','Mauricio','Mamani','1234',3),
('80000032','Andrea','Quispe','1234',3),
('80000033','Ricardo','Choque','1234',3),
('80000034','Patricia','Flores','1234',3),
('80000035','Alfredo','Rojas','1234',3),
('80000036','Vanessa','Guzman','1234',3),
('80000037','Samuel','Condori','1234',3),
('80000038','Erika','Lopez','1234',3),
('80000039','Jhonatan','Vargas','1234',3),
('80000040','Noelia','Mendoza','1234',3),
('80000041','Ruben','Alarcon','1234',3),
('80000042','Karen','Huanca','1234',3),
('80000043','Victor','Ticona','1234',3),
('80000044','Melani','Calle','1234',3),
('80000045','Alex','Apaza','1234',3),

-- 4to D (4)
('80000046','Eduardo','Mamani','1234',4),
('80000047','Monica','Quispe','1234',4),
('80000048','Raul','Choque','1234',4),
('80000049','Yessica','Flores','1234',4),
('80000050','Julio','Rojas','1234',4),
('80000051','Eliana','Guzman','1234',4),
('80000052','Hector','Condori','1234',4),
('80000053','Cynthia','Lopez','1234',4),
('80000054','Martin','Vargas','1234',4),
('80000055','Daniela','Mendoza','1234',4),
('80000056','Ivan','Alarcon','1234',4),
('80000057','Jessica','Huanca','1234',4),
('80000058','Ronald','Ticona','1234',4),
('80000059','Lizeth','Calle','1234',4),
('80000060','Mauricio','Apaza','1234',4),

-- 4to E (5)
('80000061','Rodrigo','Mamani','1234',5),
('80000062','Veronica','Quispe','1234',5),
('80000063','Javier','Choque','1234',5),
('80000064','Alejandra','Flores','1234',5),
('80000065','Gustavo','Rojas','1234',5),
('80000066','Bianca','Guzman','1234',5),
('80000067','Felipe','Condori','1234',5),
('80000068','Lorena','Lopez','1234',5),
('80000069','Andres','Vargas','1234',5),
('80000070','Micaela','Mendoza','1234',5),
('80000071','David','Alarcon','1234',5),
('80000072','Dayana','Huanca','1234',5),
('80000073','Wilson','Ticona','1234',5),
('80000074','Nataly','Calle','1234',5),
('80000075','Bruno','Apaza','1234',5);

INSERT INTO representante(id_estudiante,cargo)
VALUES
(1,'DELEGADO'),
(2,'CODELEGADO'),

(16,'DELEGADO'),
(17,'CODELEGADO'),

(31,'DELEGADO'),
(32,'CODELEGADO'),

(46,'DELEGADO'),
(47,'CODELEGADO'),

(61,'DELEGADO'),
(62,'CODELEGADO');

select * from estudiante;
DELETE FROM representante;
SELECT * FROM profesor_materia;
SELECT current_database();
--AÑADIENDO PROFESORES Y MATERIAS---

INSERT INTO profesor_materia
(id_profesor,id_materia,id_curso)
VALUES

-- 4to B
(1,1,2),
(2,2,2),
(3,3,2),
(4,4,2),
(5,5,2),
(6,6,2),
(7,7,2),
(8,8,2),
(9,9,2),

-- 4to C
(1,1,3),
(2,2,3),
(3,3,3),
(4,4,3),
(5,5,3),
(6,6,3),
(7,7,3),
(8,8,3),
(9,9,3),

-- 4to D
(1,1,4),
(2,2,4),
(3,3,4),
(4,4,4),
(5,5,4),
(6,6,4),
(7,7,4),
(8,8,4),
(9,9,4),

-- 4to E
(1,1,5),
(2,2,5),
(3,3,5),
(4,4,5),
(5,5,5),
(6,6,5),
(7,7,5),
(8,8,5),
(9,9,5);
SELECT *
FROM profesor_materia
ORDER BY id_curso, id_materia;

SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public';

SELECT
    column_name,
    data_type
FROM information_schema.columns
WHERE table_name = 'nota_trimestre';

SELECT
    column_name,
    data_type
FROM information_schema.columns
WHERE table_name = 'nota_practica';

SELECT
    column_name,
    data_type
FROM information_schema.columns
WHERE table_name = 'estudiante';

SELECT * FROM estudiante;

ALTER TABLE estudiante
ADD COLUMN fecha_ingreso DATE;

UPDATE estudiante
SET fecha_ingreso = '2025-02-03'
WHERE fecha_ingreso IS NULL;

SELECT
    column_name,
    data_type
FROM information_schema.columns
WHERE table_name = 'estudiante';

ALTER TABLE practica
ADD COLUMN trimestre INTEGER;

SELECT *
FROM practica;