-- ====================================================================
-- DESAFÍO 1: ARQUITECTURA RELACIONAL Y CONSULTAS BÁSICAS EN SQL
-- ====================================================================

-- --------------------------------------------------------------------
-- Requerimiento 2: Escritura de consultas básicas en SQL
-- --------------------------------------------------------------------

-- Consulta 1: Listar los nombres y correos de clientes de la ciudad de "Valparaíso"
-- Explicación: Seleccionamos los campos nombre y correo de la tabla clientes, 
-- aplicando un filtro WHERE para la columna ciudad.
SELECT nombre, correo
FROM clientes
WHERE ciudad = 'Valparaíso';


-- Consulta 2: Mostrar las ventas realizadas en junio, con nombre del cliente y total
-- Explicación: Unimos la tabla ventas con clientes por su clave foránea común id_cliente.
-- Luego, filtramos las fechas correspondientes al mes de junio de 2024.
SELECT clientes.nombre AS nombre_cliente, ventas.total AS total_venta
FROM ventas
INNER JOIN clientes ON ventas.id_cliente = clientes.id_cliente
WHERE ventas.fecha BETWEEN '2024-06-01' AND '2024-06-30';


-- Consulta 3: Obtener el total de productos vendidos por tienda (sucursal)
-- Explicación: Unimos la tabla ventas con sucursales. Agrupamos los resultados 
-- por el nombre de la sucursal y sumamos la cantidad de productos para cada una.
SELECT sucursales.nombre_sucursal, SUM(ventas.cantidad) AS total_productos_vendidos
FROM ventas
INNER JOIN sucursales ON ventas.id_sucursal = sucursales.id_sucursal
GROUP BY sucursales.nombre_sucursal;
