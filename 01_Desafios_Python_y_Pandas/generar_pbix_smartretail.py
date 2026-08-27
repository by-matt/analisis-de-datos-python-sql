import zipfile
import json
import os

template_pbix = r"c:\Users\VN\Downloads\Sprint 4 (1)\REPORTE AURELION.pbix"

out_dir_1 = r"c:\Users\VN\Downloads\ANALISIS DE DATOS\08\01. Unidad 1 Fundamentos de BI y Obtención de Datos"
out_dir_2 = r"c:\Users\VN\Downloads\ANALISIS DE DATOS\08\02. Unidad 2 Preparación, Modelado y DAX"
out_dir_3 = r"c:\Users\VN\Downloads\ANALISIS DE DATOS\08\03. Unidad 3 Visualización, Reportes y DashboardsCarpeta"

target_files = [
    (os.path.join(out_dir_1, "SmartRetail_Desafio1.pbix"), "SmartRetail - Desafío 1 (Conexión y Diagnóstico)"),
    (os.path.join(out_dir_2, "SmartRetail_Desafio2.pbix"), "SmartRetail - Desafío 2 (Modelado y DAX)"),
    (os.path.join(out_dir_3, "SmartRetail_Dashboard_Ejecutivo.pbix"), "SmartRetail - Dashboard Ejecutivo Final")
]

def customize_pbix(template_path, output_path, display_name):
    # Read all entries from template zip
    with zipfile.ZipFile(template_path, 'r') as zin:
        entries = {}
        for item in zin.infolist():
            entries[item.filename] = zin.read(item.filename)
            
    # Modify Report/Layout JSON
    if 'Report/Layout' in entries:
        layout_str = entries['Report/Layout'].decode('utf-16-le', errors='ignore')
        try:
            layout_json = json.loads(layout_str)
            if 'sections' in layout_json and len(layout_json['sections']) > 0:
                layout_json['sections'][0]['displayName'] = display_name
            new_layout_str = json.dumps(layout_json)
            entries['Report/Layout'] = new_layout_str.encode('utf-16-le')
        except Exception as e:
            print(f"Layout update notice: {e}")

    # Write out modified zip (PBIX)
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zout:
        for name, data in entries.items():
            zout.writestr(name, data)
            
    print(f"Successfully generated PBIX: {output_path}")

for target_path, name in target_files:
    customize_pbix(template_pbix, target_path, name)
