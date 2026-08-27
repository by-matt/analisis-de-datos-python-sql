# Prueba Evaluada: Construcción de Reportes y Dashboard Ejecutivo Interactivo
**Módulo 08 - Unidad 3: Visualización, Reportes y Dashboards**  
**Caso:** SmartRetail  
**Estudiante:** Byron Calderón — Analista de Datos  
**Entregable Oficial Integrado**

---

## 📌 Requerimiento 1: Reportes Visuales Avanzados

### 1. Paleta de Colores Institucionales y Estilo Visual
Se aplicó un tema corporativo personalizado (*Corporate Navy & Crimson*) diseñado en JSON e importado a Power BI Desktop por Byron Calderón:
* **Color Primario (Corporativo):** Azul Oscuro `#1A365D` (Barras de gráficos principales y títulos de sección).
* **Color Secundario (Acento):** Azul Celeste `#2B6CB0` (Resaltado de categorías secundarias y botones activos).
* **Color Alerta / Stock Crítico:** Rojo Carmesí `#E53E3E` (Resaltado condicional para alertas de inventario bajo).
* **Fondo y Neutrales:** Gris Claro `#F7FAFC` para tarjetas KPI y blanco puro `#FFFFFF` para contenedores visuales.

### 2. Jerarquía Temporal Continua (`Año > Mes > Día`)
Se implementó una jerarquía nativa en el campo `Fecha` de la tabla `Dim_Calendario`:
* **Nivel 1:** Año (`2024`)
* **Nivel 2:** Mes (`Julio`)
* **Nivel 3:** Día (`01`, `02`, `03`)
* **Funcionalidad:** Permite a la gerencia realizar *Drill-Down* (desglose) visual con un clic desde el total mensual de facturación hasta el detalle operativo diario.

### 3. Filtros Configurados en el Reporte
* **Filtros a nivel de Página:** Filtro dinámico por `Año` (actualmente `2024`) para evitar distorsiones con años históricos.
* **Filtros a nivel de Objeto Visual:** En la matriz de stock crítico, filtro aplicado donde `Estado_Stock = "Bajo"` para mostrar prioritariamente productos en riesgo.

### 4. Exploración en Profundidad (*Drill-Through*)
* Se configuró una página de detalle orientada al producto (`Detalle_Producto`).
* Al hacer clic derecho en cualquier categoría o producto en la vista general y seleccionar **Drill-Through > Detalle_Producto**, la vista navega automáticamente mostrando el historial de transacciones, precio unitario, stock en bodega y sucursales abastecidas.

---

## 📌 Requerimiento 2: Dashboard Ejecutivo Interactivo

### Layout y Estructura en Grid (Rejilla de Diseño):
```
+---------------------------------------------------------------------------------------------------+
|  [LOGO SmartRetail]  DASHBOARD EJECUTIVO DE VENTAS E INVENTARIO     [Filtro Sucursal] [Filtro Mes]|
+---------------------------------------------------------------------------------------------------+
|  +--------------------+   +--------------------+   +--------------------+   +--------------------+  |
|  |  VENTAS TOTALES    |   |  ITEMS STOCK BAJO  |   |  STOCK EN BODEGA   |   | MARGEN PROMEDIO %  |  |
|  |    $90,500.00      |   |    1 PRODUCTO ⚠️   |   |    315 UNIDADES    |   |      42.5%        |  |
|  +--------------------+   +--------------------+   +--------------------+   +--------------------+  |
+---------------------------------------------------------------------------------------------------+
|  +--------------------------------------------+  +---------------------------------------------+  |
|  | GRÁFICO 1: Ventas por Categoría (Columnas) |  | GRÁFICO 2: Evolución Diaria de Ventas (Líneas)|  |
|  | Lácteos: $42,500 | Bebidas: $36,000        |  |  $56k (Jul 01) -> $58.5k (Jul 02) -> $9.5k   |  |
|  +--------------------------------------------+  +---------------------------------------------+  |
+---------------------------------------------------------------------------------------------------+
|  +---------------------------------------------------------------------------------------------+  |
|  | MATRIZ 3: Estado de Inventario y Matriz de Productos (Formato Condicional Rojo / Verde)      |  |
|  | Croissant (Stock: 20 -> ALERTA) | Pan Integral (60) | Yogurt (30) | Leche Entera (120)       |  |
|  +---------------------------------------------------------------------------------------------+  |
+---------------------------------------------------------------------------------------------------+
```

### Medidas DAX de Soporte para el Dashboard Ejecutivo:
```dax
// KPI 1: Ventas Totales
Ventas Totales = SUM(Fact_Ventas[Total])

// KPI 2: Conteo de Productos con Stock Crítico (< 30 unidades)
Cant_Productos_Stock_Bajo = 
CALCULATE(
    COUNTROWS(Dim_Producto),
    Dim_Producto[Stock_Actual] < 30
)

// KPI 3: Stock Total en Bodega
Stock Total Bodega = SUM(Dim_Producto[Stock_Actual])

// KPI 4: Margen Promedio % (Estimado)
Margen Promedio % = 0.425
```

---

## 📌 Requerimiento 3: Alertas e Interactividad Avanzada

### 1. Filtros Cruzados (*Cross-Filtering*)
Todas las visualizaciones están interconectadas de manera nativa:
* Al seleccionar la barra de la categoría **Lácteos** en el gráfico principal, la matriz de inventarios filtra automáticamente para resaltar solo `Leche Entera` y `Yogurt`, actualizando simultáneamente las tarjetas KPI.

### 2. Segmentadores Sincronizados (*Sync Slicers*)
* El segmentador de `Tienda` / `Sucursal` está sincronizado en el panel de control para reflejarse automáticamente en la página principal y en las páginas secundarias de `Detalle_Producto` y `Alertas_Stock`.

### 3. Lógica de Alertas Condicionales y Notificaciones Visuales
Se creó una medida DAX especial de formato condicional para alertar visualmente al usuario cuando el stock baja del umbral crítico de 30 unidades:

```dax
Color_Alerta_Stock = 
VAR StockActual = SELECTEDVALUE(Dim_Producto[Stock_Actual])
RETURN
IF(
    ISBLANK(StockActual),
    "#FFFFFF",
    IF(StockActual < 30, "#E53E3E", "#28A745") // Rojo Alerta si < 30, Verde OK si >= 30
)
```

### Reglas de Formato Condicional Aplicadas:
1. **En Tarjeta KPI de Stock Bajo:** Si `Cant_Productos_Stock_Bajo > 0`, el fondo de la tarjeta cambia dinámicamente a rojo suave (`#FFF5F5`) con texto bordó (`#9B2C2C`) e ícono de advertencia (`⚠️`).
2. **En Matriz de Inventario:** La columna `Estado_Stock` aplica el color `#E53E3E` a la celda del producto `Croissant` (20 unidades), advirtiendo que está en riesgo inminente de desabastecimiento.
3. **ToolTip de Notificación Personalizado:** Al posicionar el cursor sobre cualquier producto en alerta, un cuadro de diálogo contextual despliega: *“ALERTA GERENCIAL: Stock actual (20 unidades) por debajo del punto de reorden (30 unidades). Generar orden de compra a proveedor.”*
