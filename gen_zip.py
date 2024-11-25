import os
import zipfile

# Definir las carpetas de origen y los años correspondientes
base_path = "/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2"
years = ["2018", "2019", "2020", "2021", "2022", "2023"]
output_zip = os.path.join(base_path, "archivos_por_año.zip")  # Guardar el ZIP en base_path

# Crear el archivo ZIP
with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for year in years:
        source_folder = os.path.join(base_path, year, "matched_bacteria")
        
        # Verificar si la carpeta del año existe
        if not os.path.exists(source_folder):
            print(f"Advertencia: La carpeta para el año {year} no existe. Se omitirá.")
            continue
        
        # Agregar archivos de la carpeta correspondiente al ZIP
        for root, dirs, files in os.walk(source_folder):
            for file in files:
                file_path = os.path.join(root, file)
                
                # Crear la estructura deseada dentro del ZIP
                relative_path = os.path.relpath(file_path, base_path)
                archive_path = os.path.join(year, os.path.relpath(file_path, source_folder))
                
                # Agregar al ZIP
                zipf.write(file_path, archive_path)
                print(f"Agregado: {archive_path}")

print(f"Archivo ZIP creado: {output_zip}")
