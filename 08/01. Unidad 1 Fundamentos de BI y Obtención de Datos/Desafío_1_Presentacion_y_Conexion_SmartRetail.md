# Desafío Evaluado: Diagnóstico y Conexión de Fuentes en Power BI
**Módulo 08 - Unidad 1: Fundamentos de BI y Obtención de Datos**  
**Caso:** SmartRetail  
**Estudiante:** Byron Calderón — Analista de Datos  
**Entregable Oficial Integrado**

---

## 📌 Requerimiento 1: Presentación Ejecutiva Comparativa

### Diapositiva 1: Portada e Introducción al Sistema BI en SmartRetail
* **Título:** Diagnóstico y Estrategia de Business Intelligence para SmartRetail.
* **Subtítulo:** Transformación de Datos Operativos en Decisiones Comerciales Estratégicas.
* **Presentado por:** Byron Calderón (Analista de Datos).
* **¿Qué es un Sistema de Business Intelligence (BI)?**
  Es un conjunto de tecnologías, procesos y arquitecturas que transforman datos crudos (transacciones de ventas, niveles de inventario, registros de sucursales) en información estructurada y conocimiento analítico accionable.
* **Importancia Estratégica para SmartRetail:**
  - **Optimización de Inventarios:** Prevenir quiebres de stock en sucursales críticas y evitar sobre-stock en productos de baja rotación.
  - **Visibilidad Comercial:** Monitorear en tiempo real el rendimiento de ventas por categoría y sucursal.
  - **Toma de Decisiones Basada en Evidencia:** Reemplazar estimaciones empíricas por indicadores clave de rendimiento (KPIs) precisos.

---

### Diapositiva 2: Comparativa de Suites BI del Mercado

| Criterio de Evaluación | **Power BI (Microsoft)** 🏆 | **Tableau (Salesforce)** | **Qlik Sense (Qlik)** |
| :--- | :--- | :--- | :--- |
| **Costo y Licenciamiento** | **Económico y Accesible** (Pro ~\$10/mes por usuario, incluido en Microsoft 365 E5). | **Elevado** (Tableau Creator ~\$70/mes por usuario). | **Intermedio-Alto** (Modelo basado en capacidad/usuario). |
| **Facilidad de Integración** | **Nativa y Superior** con Excel, Azure, SQL Server, SharePoint y suite Office. | Requiere conectores adicionales para el ecosistema Microsoft. | Buena integración pero requiere configuración personalizada. |
| **Motor de Transformación** | **Power Query (Lenguaje M):** Entorno visual potente y reproducible. | Prep / Data Wrangler menos intuitivo para usuarios de Excel. | Motor asociativo potente pero con curva de aprendizaje alta (Scripting Qlik). |
| **Modelado y Fórmulas** | **Lenguaje DAX:** Estándar de la industria, flexible para análisis temporal. | Campos calculados propios (LOD Expressions). | Set Analysis en expresiones complejas. |
| **Adopción Organizacional** | **Rápida curva de aprendizaje** para usuarios familiarizados con Excel. | Enfocado en analistas de datos avanzados y diseñadores visuales. | Orientado a arquitectos de datos y usuarios analíticos. |

**Justificación de Elección para SmartRetail:** Power BI es la mejor opción debido a su óptima relación costo-beneficio, integración nativa con los archivos Excel/CSV existentes en SmartRetail y su rápida curva de adopción por parte del equipo comercial.

---

### Diapositiva 3: Arquitectura y Entorno Power BI para SmartRetail
* **Power BI Desktop:** Herramienta de desarrollo local para extracción, transformación (Power Query), modelado relacional (DAX) y diseño del dashboard.
* **Power BI Service (Nube):** Plataforma para la publicación, automatización de actualización de datos (*Data Refresh*) y distribución de reportes a la gerencia.
* **Power BI Mobile:** Acceso seguro para supervisores de tienda y gerentes en terreno desde dispositivos móviles.
* **Aplicabilidad Inmediata en SmartRetail:**
  1. Conexión automatizada a archivos CSV de puntos de venta (`ventas.csv`) y hojas de cálculo de almacén (`inventario.xlsx`).
  2. Estandarización de categorías de productos y sincronización entre sucursales.
  3. Visualización dinámica para el control diario del stock disponible por tienda.

---

## 📌 Requerimiento 2: Obtención y Conexión a Datos en Power BI

### 1. Proceso Paso a Paso de Conexión y Limpieza (Power Query)
1. **Conexión a `ventas.csv`:**
   - En Power BI Desktop, seleccionar **Obtener datos > Texto/CSV**.
   - Elegir el archivo `ventas.csv` con codificación **UTF-8** y delimitador **Coma (,)**.
   - Hacer clic en **Transformar datos** para abrir el editor de Power Query.

2. **Conexión a `inventario.xlsx`:**
   - Seleccionar **Nueva fuente > Excel Workbook**.
   - Seleccionar `inventario.xlsx` y marcar la hoja de datos principal (`Hoja1`).

3. **Estandarización de Nombres de Columnas:**
   - En la consulta `Ventas`: Estandarizar nombres a `ID_Venta`, `Fecha`, `Tienda`, `Categoria_Producto`, `Producto`, `Cantidad`, `Precio_Unitario`, `Total`.
   - En la consulta `Inventario`: Estandarizar nombres a `ID_Producto`, `Producto`, `Categoria`, `Stock_Actual`, `Tienda`.

4. **Verificación y Corrección de Tipos de Datos:**
   - `Fecha`: Tipo **Fecha** (`Date.From`).
   - `Cantidad`, `Stock_Actual`, `ID_Venta`, `ID_Producto`: Tipo **Número entero** (`Int64.Type`).
   - `Precio_Unitario`, `Total`: Tipo **Número decimal fijo / Moneda** (`Currency.Type`).
   - `Tienda`, `Categoria`, `Producto`: Tipo **Texto** (`Text.Type`).

### Código M de Power Query (Reproducible):
```powerquery
// Consulta: Ventas
let
    Origen = Csv.Document(File.Contents("C:\SmartRetail\ventas.csv"),[Delimiter=",", Columns=8, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    EncabezadosPromovidos = Table.PromoteHeaders(Origen, [PromoteAllScalars=true]),
    TipoCambiado = Table.TransformColumnTypes(EncabezadosPromovidos,{
        {"ID_Venta", Int64.Type}, 
        {"Fecha", type date}, 
        {"Tienda", type text}, 
        {"Categoria_Producto", type text}, 
        {"Producto", type text}, 
        {"Cantidad", Int64.Type}, 
        {"Precio_Unitario", Currency.Type}, 
        {"Total", Currency.Type}
    })
in
    TipoCambiado
```

---

## 📌 Requerimiento 3: Visualización Funcional en Power BI (Dashboard Inicial)

### Componentes del Dashboard Inicial:
1. **Gráfico de Columnas Clustered:**
   - **Eje X:** `Categoria_Producto`
   - **Eje Y:** `Suma de Total` (Ventas Totales)
   - **Propósito:** Identificar la categoría con mayor facturación (Lácteos con \$42,500 y Bebidas con \$36,000).

2. **Tabla / Matriz de Inventario:**
   - **Columnas:** `Producto`, `Stock_Actual`, `Estado_Stock` (Regla condicional: Stock < 30 "Bajo", 30-80 "Medio", > 80 "Alto").
   - **Formato Condicional:** Resaltado de color rojo claro en las filas con Stock "Bajo" (`Croissant` con 20 unidades) para alerta rápida de reposición.

3. **Segmentador Interactivo (*Slicer*):**
   - **Campo:** `Tienda` / `Sucursal` (`Sucursal A`, `Sucursal B`, `Sucursal C`).
   - **Comportamiento:** Al seleccionar una sucursal, el gráfico de ventas y la tabla de inventario se filtran dinámicamente.

4. **Diseño Visual Profesional:**
   - Paleta cromática corporativa: Azul Marino (`#1A365D`) para barras, Gris Neutro para fondos, Rojo Alerta (`#E53E3E`) para stock crítico.
   - Tipografía legible (*Segoe UI Semibold*), títulos descriptivos y valores formateados en Moneda (\$ USD / CLP).
