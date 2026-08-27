-- ====================================================================
-- DESAFÍO: ARQUITECTURA RELACIONAL Y CONSULTAS BÁSICAS EN SQL
-- ====================================================================

-- --------------------------------------------------------------------
-- Requerimiento 2: Escritura de consultas básicas en SQL
-- --------------------------------------------------------------------

-- Consulta 1: Listar los nombres y correos de clientes de la ciudad de "Valparaíso"
-- Explicación: Filtramos la tabla 'clientes' usando la condición WHERE para la ciudad deseada.
SELECT nombre, correo
FROM clientes
WHERE ciudad = 'Valparaíso';


-- Consulta 2: Mostrar las ventas realizadas en junio, con nombre del cliente y total
-- Explicación: Unimos las tablas 'ventas' y 'clientes' a través de su clave foránea.
-- Filtramos por el rango de fechas correspondientes al mes de junio de 2024 (según los datos de ejemplo).
SELECT clientes.nombre AS nombre_cliente, ventas.total AS total_venta
FROM ventas
INNER JOIN clientes ON ventas.id_cliente = clientes.id_cliente
WHERE ventas.fecha BETWEEN '2024-06-01' AND '2024-06-30';


-- Consulta 3: Obtener el total de productos vendidos por tienda (sucursal)
-- Explicación: Unimos las tablas 'ventas' y 'sucursales'. Agrupamos por el nombre de la sucursal
-- y sumamos la columna 'cantidad' para obtener el total de productos físicos vendidos en cada una.
SELECT sucursales.nombre_sucursal, SUM(ventas.cantidad) AS total_productos_vendidos
FROM ventas
INNER JOIN sucursales ON ventas.id_sucursal = sucursales.id_sucursal
GROUP BY sucursales.nombre_sucursal;
