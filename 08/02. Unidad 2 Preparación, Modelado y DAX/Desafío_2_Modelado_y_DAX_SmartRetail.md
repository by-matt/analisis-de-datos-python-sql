# Desafío Evaluado: Preparación, Modelado de Datos y DAX en Power BI
**Módulo 08 - Unidad 2: Preparación, Modelado y DAX**  
**Caso:** SmartRetail  
**Estudiante:** Byron Calderón — Analista de Datos  
**Entregable Oficial Integrado**

---

## 📌 Requerimiento 1: Transformación y Limpieza de Datos (Power Query)

### Procedimiento de Limpieza y Transformación:
1. **Normalización de Nombres y Tipos de Datos:**
   - Se renombraron los encabezados en ambas consultas (`Ventas` e `Inventario`) para evitar discrepancias de mayúsculas/minúsculas y caracteres especiales.
   - Se asignaron tipos de datos estricto: `Fecha` (Date), `Cantidad` y `Stock_Actual` (Integer), `Precio_Unitario` y `Total` (Currency).

2. **Reemplazo e Imputación de Valores Nulos/Inconsistentes:**
   - Se revisaron los valores de texto en las columnas `Categoria` y `Producto`, aplicando la función `Text.Trim` y `Text.Clean` para remover espacios accidentales.

3. **Filtrado Operativo de Ventas:**
   - **Criterio de Negocio:** Filtrar únicamente transacciones de ventas significativas donde `Cantidad > 10`.
   - **Resultado:** Se excluye la transacción `ID_Venta 1005` (`Cantidad = 10`), manteniendo 4 registros relevantes (`ID_Venta` 1001, 1002, 1003 y 1004) con un volumen total de facturación de **\$90,500**.

4. **Combinación de Consultas (*Merge Queries*):**
   - Se realizó una combinación externa izquierda (*Left Outer Join*) entre la tabla `Ventas` y la tabla `Inventario` utilizando como clave de enlace la columna `Producto`.
   - Esto permite enriquecer las transacciones de venta con la información de stock actual disponible en bodega para cada ítem.

### Código M de Power Query:
```powerquery
// Consulta: Ventas_Preparada
let
    Origen = Csv.Document(File.Contents("C:\SmartRetail\ventas.csv"),[Delimiter=",", Columns=8, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars=true]),
    TiposAjustados = Table.TransformColumnTypes(Encabezados,{
        {"ID_Venta", Int64.Type}, 
        {"Fecha", type date}, 
        {"Tienda", type text}, 
        {"Categoria_Producto", type text}, 
        {"Producto", type text}, 
        {"Cantidad", Int64.Type}, 
        {"Precio_Unitario", Currency.Type}, 
        {"Total", Currency.Type}
    }),
    FiltroCantidad = Table.SelectRows(TiposAjustados, each [Cantidad] > 10),
    CombinadoInventario = Table.NestedJoin(FiltroCantidad, {"Producto"}, Inventario, {"Producto"}, "Tabla_Inventario", JoinKind.LeftOuter),
    InventarioExpandido = Table.ExpandTableColumn(CombinadoInventario, "Tabla_Inventario", {"Stock_Actual"}, {"Stock_Actual_Inventario"})
in
    InventarioExpandido
```

---

## 📌 Requerimiento 2: Modelado de Datos Relacional (Esquema Estrella)

### Estructura del Modelo de Datos:
El modelo sigue una arquitectura de **Esquema en Estrella** (*Star Schema*), separando los hechos de las dimensiones para maximizar el rendimiento analítico en DAX.

```
       +-----------------------+
       |     Dim_Calendario    |
       +-----------------------+
       | PK: FechaKey (Date)   |
       +-----------+-----------+
                   | 1
                   | 
                   | *
       +-----------+-----------+
       |       Fact_Ventas     |
       +-----------------------+
       | PK: ID_Venta          |
       | FK: FechaKey          |
       | FK: ID_Producto       |
       | FK: TiendaID          |
       | Cantidad, Total       |
       +-----------+-----------+
                   | *
                   | 
                   | 1
       +-----------+-----------+
       |      Dim_Producto     |
       +-----------------------+
       | PK: ID_Producto       |
       | Producto, Categoria   |
       | Stock_Actual          |
       +-----------------------+
```

### Definición Explícita de Llaves y Relaciones:
1. **Tabla Fact (`Fact_Ventas`):** Contiene los hechos numéricos de transacciones comerciales (`Cantidad`, `Total`, `Precio_Unitario`).
2. **Tabla Dimensión (`Dim_Producto`):** Contiene atributos de productos (`ID_Producto`, `Producto`, `Categoria`, `Stock_Actual`).
   - **Llave Primaria (PK):** `Dim_Producto[ID_Producto]`
   - **Llave Foránea (FK):** `Fact_Ventas[ID_Producto]`
   - **Relación:** 1 a Muchos (`1:*`), dirección de filtro **Unidireccional** (de `Dim_Producto` a `Fact_Ventas`), **Activa**.
3. **Tabla Dimensión (`Dim_Calendario`):** Creada dinámicamente en DAX para análisis temporal continuo.
   - **Relación:** `Dim_Calendario[Fecha]` (1) a `Fact_Ventas[Fecha]` (*), Unidireccional y Activa.

---

## 📌 Requerimiento 3: Cálculos DAX (Columnas, Medidas y Tablas Calculadas)

### 1. Columna Calculada en DAX (Clasificación de Inventario)
Se creó en la tabla `Dim_Producto` para categorizar el nivel de stock crítico:

```dax
Estado_Stock = 
SWITCH(
    TRUE(),
    Dim_Producto[Stock_Actual] < 30, "Bajo",
    Dim_Producto[Stock_Actual] <= 80, "Medio",
    "Alto"
)
```
* **Resultado:**
  - `Croissant` (20 unidades) -> **Bajo** (Requiere reposición urgente).
  - `Pan Integral` (60 unidades) y `Yogurt` (30 unidades) -> **Medio**.
  - `Leche Entera` (120 unidades) y `Jugo Naranja` (85 unidades) -> **Alto**.

---

### 2. Medidas DAX Fundamentales

#### Medida 1: Ventas Totales
```dax
Ventas Totales = SUM(Fact_Ventas[Total])
```
* **Valor Calculado:** **\$90,500.00**

#### Medida 2: Promedio de Venta por Categoría
```dax
Promedio Venta Categoria = AVERAGE(Fact_Ventas[Total])
```
* **Valores Calculados por Categoría:**
  - **Bebidas:** \$36,000.00
  - **Lácteos:** \$21,250.00
  - **Panadería:** \$12,000.00

---

### 3. Tabla Calculada en DAX (Ventas Acumuladas por Categoría)
Tabla sintética generada en DAX para resúmenes ejecutivos rápidos:

```dax
Ventas_Acumuladas_Categoria = 
SUMMARIZE(
    Fact_Ventas,
    Fact_Ventas[Categoria_Producto],
    "Ventas_Acumuladas", SUM(Fact_Ventas[Total]),
    "Cantidad_Total", SUM(Fact_Ventas[Cantidad])
)
```

| Categoria_Producto | Ventas_Acumuladas | Cantidad_Total |
| :--- | :--- | :--- |
| **Lácteos** | \$42,500.00 | 45 unidades |
| **Bebidas** | \$36,000.00 | 30 unidades |
| **Panadería** | \$12,000.00 | 15 unidades |

---

### 4. Pregunta Analítica de Negocio Resuelta

**Pregunta Analítica:** *¿Cuáles sucursales concentran el mayor volumen de facturación por cada categoría de producto y cuál es el impacto en su inventario disponible?*

**Análisis de Resultados Visuales:**
* **Sucursal A:** Lidera la facturación global con **\$56,000** (\$36,000 en Bebidas y \$20,000 en Lácteos). Posee niveles de inventario en estado **Alto** (120 unidades de Leche Entera y 85 de Jugo Naranja).
* **Sucursal C:** Generó **\$22,500** en Lácteos (`Yogurt`), pero su stock está en nivel **Medio** (30 unidades), lo que sugiere programar un pedido de reposición esta semana.
* **Sucursal B:** Registra **\$12,000** en Panadería (`Pan Integral`). Su producto `Croissant` está en estado **Bajo (20 unidades)** y requiere pedido de emergencia.
