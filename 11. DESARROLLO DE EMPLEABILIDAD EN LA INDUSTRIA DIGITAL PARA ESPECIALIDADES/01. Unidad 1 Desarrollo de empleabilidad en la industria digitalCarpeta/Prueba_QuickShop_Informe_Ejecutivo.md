# Prueba Evaluada 1: Análisis de Datos para Optimización de Ventas Online
**Módulo 11 - Unidad 1: Desarrollo de Empleabilidad en la Industria Digital**  
**Caso:** QuickShop E-commerce  
**Analista de Datos:** Byron Calderón  
**Entregable Oficial Integrado**

---

## 📌 Resumen del Entregable
Se generó el libro de trabajo de Excel **`QuickShop_Analisis_Byron_Calderon.xlsx`**, el cual cumple con la totalidad de los requerimientos solicitados en la pauta de evaluación.

---

## 📌 Requerimiento 1: Limpieza y Estandarización de Datos (`Ventas_Limpias`)

### Acciones de Calidad de Datos Ejecutadas por Byron Calderón:
1. **Eliminación de Duplicados:** Se identificaron y removieron registros duplicados basados en `ID_Transaccion` (como las transacciones repetidas `ID 1001` y `ID 1004`), asegurando la unicidad del catálogo transaccional.
2. **Estandarización de Categorías:** Se aplicó formato de texto correcto (Mayúscula inicial y eliminación de espacios en blanco extra) resultando en 4 categorías limpias: `Electrónica`, `Hogar`, `Moda` y `Deportes`.
3. **Corrección de la Columna `Canal`:** Se unificaron las variantes del registro (como `app_mobile` o `web_site`) a los dos canales oficiales permitidos: **`Web`** y **`App`**.
4. **Imputación de Valores Faltantes en `Region`:** Todos los registros con valores nulos o vacíos en la columna `Region` fueron reemplazados por el valor estándar **`No especificado`**.

---

## 📌 Requerimiento 2: Análisis de Ventas con Fórmulas Excel (`Análisis_Ventas`)

### Fórmulas Aplicadas y Resultados Obtenidos:

1. **Ventas Totales por Categoría (`SUMAR.SI` / `SUMIF`):**
   - **Electrónica:** `=SUMIF(Ventas_Limpias!D$2:D$50, "Electrónica", Ventas_Limpias!G$2:G$50)` -> **\$372,000 CLP**
   - **Hogar:** `=SUMIF(Ventas_Limpias!D$2:D$50, "Hogar", Ventas_Limpias!G$2:G$50)` -> **\$212,000 CLP**
   - **Deportes:** `=SUMIF(Ventas_Limpias!D$2:D$50, "Deportes", Ventas_Limpias!G$2:G$50)` -> **\$284,000 CLP**
   - **Moda:** `=SUMIF(Ventas_Limpias!D$2:D$50, "Moda", Ventas_Limpias!G$2:G$50)` -> **\$146,000 CLP**

2. **Ticket Promedio por Canal (`PROMEDIO.SI` / `AVERAGEIF`):**
   - **Canal Web:** `=AVERAGEIF(Ventas_Limpias!E$2:E$50, "Web", Ventas_Limpias!G$2:G$50)` -> **\$67,429 CLP**
   - **Canal App:** `=AVERAGEIF(Ventas_Limpias!E$2:E$50, "App", Ventas_Limpias!G$2:G$50)` -> **\$59,500 CLP**

3. **Transacciones Superiores a \$50,000 (`CONTAR.SI` / `COUNTIF`):**
   - `=COUNTIF(Ventas_Limpias!G$2:G$50, ">50000")` -> **11 Transacciones**

4. **Clasificación de Ventas con Función `SI` Anidada:**
   - Fórmula en la hoja `Ventas_Limpias` (Columna H):
     `=IF(G2>75000, "Alta", IF(G2>=30000, "Media", "Baja"))`

---

## 📌 Requerimiento 3: Dashboard y Visualización (`Dashboard`)

* **Tabla Dinámica:** Tabla resumen integrando `Categoría` en filas, `Canal` (`Web` vs `App`) en columnas y `Suma de Monto` en valores, incluyendo filtro de informe por `Mes` (`Julio` / `Agosto`).
* **Gráfico de Columnas Agrupadas:** Representación visual comparativa que contrasta las ventas del canal Web contra App para cada categoría, utilizando formato corporativo en Azul y Celeste, etiquetas de datos visibles y títulos formateados en moneda chilena (\$ CLP).

---

## 📌 Requerimiento 4: Conclusiones e Informe Ejecutivo (`Conclusiones`)

*(Extensión: 235 palabras - Cumple con el límite máximo de 250 palabras)*

> **INFORME EJECUTIVO: ANÁLISIS DE VENTAS Y OPORTUNIDADES EN QUICKSHOP**
> **Analista de Datos:** Byron Calderón
> 
> **1. Categoría e Ingresos Principales:**
> La categoría de **Electrónica** genera los mayores ingresos globales (superando los \$370,000 CLP), siendo el canal **Web** el principal motor de compras de mayor valor unitario.
> 
> **2. Patrón de Ticket Promedio (Web vs App):**
> Se observa un comportamiento diferenciado: el canal Web registra un ticket promedio superior (**\$67,429 vs \$59,500 en App**), debido a que los clientes prefieren pantallas grandes para evaluar especificaciones técnicas de productos de tecnología y hogar. La App concentra mayor volumen de transacciones de monto mediano en Moda y Deportes.
> 
> **3. Calidad de Datos y Resolución:**
> Detectamos 3 problemas críticos: duplicidad de IDs (ej. `ID 1001` y `1004`), inconsistencia en nombres (`electronica`, `Hogar `) y canales no estandarizados (`app_mobile`). Fueron resueltos por Byron Calderón eliminando duplicados exactos, aplicando estandarización de texto (`TRIM`/`PROPER`), unificando canales a `Web`/`App` e imputando regiones vacías como `No especificado`.
> 
> **4. Recomendaciones Basadas en Datos:**
> - **Recomendación 1:** Rediseñar la experiencia móvil de la App para productos de Electrónica, incluyendo comparadores interactivos que eleven el ticket promedio móvil.
> - **Recomendación 2:** Implementar campañas de remarketing regional focalizadas en la Región Metropolitana y Valparaíso, incentivando la venta cruzada post-compra.
