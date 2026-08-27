-- ====================================================================
-- PRUEBA: DISEÑO Y MANIPULACIÓN DE TABLAS SQL
-- ====================================================================

-- --------------------------------------------------------------------
-- Requerimiento 1: Crear estructura de tabla con restricciones
-- --------------------------------------------------------------------

-- Explicación: Creamos la tabla 'proveedores_capacitaciones' con:
-- - id_proveedor como SERIAL (entero autoincremental) y clave primaria.
-- - razon_social como VARCHAR no nulo para la razón social.
-- - rut como VARCHAR único y no nulo para evitar registros duplicados.
-- - categoria con una restricción CHECK que solo acepta 'Interno' o 'Externo'.
-- - estado como BOOLEAN con valor por defecto TRUE (activo).

CREATE TABLE proveedores_capacitaciones (
    id_proveedor SERIAL PRIMARY KEY,
    razon_social VARCHAR(150) NOT NULL,
    rut VARCHAR(12) NOT NULL UNIQUE,
    categoria VARCHAR(20) NOT NULL CHECK (categoria IN ('Interno', 'Externo')),
    estado BOOLEAN NOT NULL DEFAULT TRUE
);


-- --------------------------------------------------------------------
-- Requerimiento 2: Insertar y validar registros
-- --------------------------------------------------------------------

-- Inserción de 4 proveedores válidos:
-- Nota: Dejamos que 'id_proveedor' se autoincremente y 'estado' tome su default (TRUE).
INSERT INTO proveedores_capacitaciones (razon_social, rut, categoria) VALUES
('Capacitaciones Alfa S.A.', '76.123.456-7', 'Interno'),
('Instituto de Formación Beta Ltda.', '77.987.654-3', 'Externo'),
('Consultores Educativos Gamma', '76.456.789-0', 'Interno'),
('Academia Técnica Delta', '78.321.654-K', 'Externo');


-- Inserciones erróneas para validación de restricciones (comentadas para no detener la ejecución):

-- ERROR 1: Duplicación de RUT (Viola la restricción UNIQUE)
-- Consulta de prueba:
-- INSERT INTO proveedores_capacitaciones (razon_social, rut, categoria) 
-- VALUES ('Capacitaciones Omega', '76.123.456-7', 'Interno');
--
-- ERROR GENERADO EN EL MOTOR (PostgreSQL):
-- ERROR: duplicate key value violates unique constraint "proveedores_capacitaciones_rut_key"
-- DETAIL: Key (rut)=(76.123.456-7) already exists.
-- Explicación: El RUT '76.123.456-7' ya fue registrado para el proveedor Alfa S.A.
-- La restricción UNIQUE impide que existan dos proveedores con el mismo RUT.

-- ERROR 2: Categoría no válida (Viola la restricción CHECK)
-- Consulta de prueba:
-- INSERT INTO proveedores_capacitaciones (razon_social, rut, categoria) 
-- VALUES ('Capacitaciones Innova', '79.111.222-3', 'Mixto');
--
-- ERROR GENERADO EN EL MOTOR (PostgreSQL):
-- ERROR: new row for relation "proveedores_capacitaciones" violates check constraint "proveedores_capacitaciones_categoria_check"
-- DETAIL: Failing row contains (5, Capacitaciones Innova, 79.111.222-3, Mixto, t).
-- Explicación: Intentamos insertar la categoría 'Mixto', pero la cláusula CHECK 
-- limita los valores permitidos únicamente a 'Interno' o 'Externo'.


-- --------------------------------------------------------------------
-- Requerimiento 3: Actualizar información
-- --------------------------------------------------------------------

-- Actualización 3.1: Cambiar la categoría del proveedor 'Capacitaciones Alfa S.A.' (id = 1) de 'Interno' a 'Externo'.
-- Usamos el filtro WHERE id_proveedor = 1 para actualizar de forma controlada y segura un solo registro.
UPDATE proveedores_capacitaciones
SET categoria = 'Externo'
WHERE id_proveedor = 1;


-- Actualización 3.2: Cambiar el estado de otro proveedor a FALSE (ej: 'Instituto de Formación Beta Ltda.' con id = 2).
-- Usamos el filtro WHERE id_proveedor = 2 para desactivar este proveedor específico en la base de datos.
UPDATE proveedores_capacitaciones
SET estado = FALSE
WHERE id_proveedor = 2;


-- --------------------------------------------------------------------
-- Requerimiento 4: Eliminar registros con condiciones
-- --------------------------------------------------------------------

-- Eliminación 4.1: Eliminar el proveedor cuyo estado sea FALSE.
-- Filtramos estrictamente usando WHERE estado = FALSE para no afectar a los proveedores activos.
DELETE FROM proveedores_capacitaciones
WHERE estado = FALSE;


-- Justificación teórica sobre la importancia de filtrar correctamente con WHERE:
--
-- "En SQL, la cláusula WHERE actúa como una barrera de seguridad indispensable para sentencias UPDATE y DELETE.
-- Si ejecutamos un comando DELETE FROM proveedores_capacitaciones sin la cláusula WHERE, el motor borrará 
-- ABSOLUTAMENTE TODOS los registros de la tabla, provocando una pérdida masiva e irreparable de datos.
-- Por lo tanto, filtrar por la clave primaria (ID) o por condiciones lógicas muy específicas (como estado = FALSE)
-- garantiza la integridad física de los datos y asegura que las operaciones afecten únicamente a las filas deseadas."
