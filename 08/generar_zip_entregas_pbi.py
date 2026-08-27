import zipfile
import os

dir_1 = r"c:\Users\VN\Downloads\ANALISIS DE DATOS\08\01. Unidad 1 Fundamentos de BI y Obtención de Datos"
dir_2 = r"c:\Users\VN\Downloads\ANALISIS DE DATOS\08\02. Unidad 2 Preparación, Modelado y DAX"
dir_3 = r"c:\Users\VN\Downloads\ANALISIS DE DATOS\08\03. Unidad 3 Visualización, Reportes y DashboardsCarpeta"

# Package 1
zip_1_path = os.path.join(dir_1, "Entrega_Desafio1_SmartRetail.zip")
with zipfile.ZipFile(zip_1_path, 'w', zipfile.ZIP_DEFLATED) as z:
    z.write(os.path.join(dir_1, "SmartRetail_Desafio1.pbix"), arcname="SmartRetail_Desafio1.pbix")
    z.write(os.path.join(dir_1, "Desafío_1_Presentacion_y_Conexion_SmartRetail.pdf"), arcname="Desafío_1_Presentacion_y_Conexion_SmartRetail.pdf")
    z.write(os.path.join(dir_1, "Desafío_1_Presentacion_y_Conexion_SmartRetail.docx"), arcname="Desafío_1_Presentacion_y_Conexion_SmartRetail.docx")
print("Created:", zip_1_path)

# Package 2
zip_2_path = os.path.join(dir_2, "Entrega_Desafio2_SmartRetail.zip")
with zipfile.ZipFile(zip_2_path, 'w', zipfile.ZIP_DEFLATED) as z:
    z.write(os.path.join(dir_2, "SmartRetail_Desafio2.pbix"), arcname="SmartRetail_Desafio2.pbix")
    z.write(os.path.join(dir_2, "Desafío_2_Modelado_y_DAX_SmartRetail.pdf"), arcname="Desafío_2_Modelado_y_DAX_SmartRetail.pdf")
    z.write(os.path.join(dir_2, "Desafío_2_Modelado_y_DAX_SmartRetail.docx"), arcname="Desafío_2_Modelado_y_DAX_SmartRetail.docx")
print("Created:", zip_2_path)

# Package 3
zip_3_path = os.path.join(dir_3, "Entrega_Prueba3_SmartRetail.zip")
with zipfile.ZipFile(zip_3_path, 'w', zipfile.ZIP_DEFLATED) as z:
    z.write(os.path.join(dir_3, "SmartRetail_Dashboard_Ejecutivo.pbix"), arcname="SmartRetail_Dashboard_Ejecutivo.pbix")
    z.write(os.path.join(dir_3, "Prueba_3_Dashboard_Ejecutivo_SmartRetail.pdf"), arcname="Prueba_3_Dashboard_Ejecutivo_SmartRetail.pdf")
    z.write(os.path.join(dir_3, "Prueba_3_Dashboard_Ejecutivo_SmartRetail.docx"), arcname="Prueba_3_Dashboard_Ejecutivo_SmartRetail.docx")
print("Created:", zip_3_path)
