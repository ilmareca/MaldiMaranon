import os
import json
import csv
import xml.etree.ElementTree as ET

# Solicitar al usuario que ingrese un año
year = input("Please enter the year you want to clean (e.g., 2020): ")

# Directorio que contiene los datos
base_dir = f'/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/{year}/matched_bacteria'
output_dir = f'/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/{year}/stats'

# Diccionario para almacenar los datos agregados
data = {}

# Recorrer la estructura del directorio y contar las muestras
for genus in os.listdir(base_dir):
    genus_dir = os.path.join(base_dir, genus)
    if os.path.isdir(genus_dir):
        for species in os.listdir(genus_dir):
            species_dir = os.path.join(genus_dir, species)
            if os.path.isdir(species_dir):
                count = 0
                for externId in os.listdir(species_dir):
                    externId_dir = os.path.join(species_dir, externId)
                    if os.path.isdir(externId_dir):
                        for targetPosition in os.listdir(externId_dir):
                            targetPosition_dir = os.path.join(externId_dir, targetPosition)
                            if os.path.isdir(targetPosition_dir):
                                count += len(os.listdir(targetPosition_dir))
                if genus not in data:
                    data[genus] = {}
                data[genus][species] = count

# Crear la estructura XML de salida
root = ET.Element('Results')
for genus_name in sorted(data.keys()):
    genus_elem = ET.SubElement(root, 'Genus', name=genus_name)
    for species_name in sorted(data[genus_name].keys()):
        species_elem = ET.SubElement(genus_elem, 'Species', name=species_name)
        species_elem.text = str(data[genus_name][species_name])

# Escribir el XML de salida en un archivo
xml_file = os.path.join(output_dir, f'count_samples_report_{year}.xml')
tree = ET.ElementTree(root)
tree.write(xml_file, encoding='utf-8', xml_declaration=True)

# Escribir el CSV de salida en un archivo
csv_file = os.path.join(output_dir, f'count_samples_report_{year}.csv')
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Genus', 'Species', 'Count'])
    for genus_name in sorted(data.keys()):
        for species_name in sorted(data[genus_name].keys()):
            writer.writerow([genus_name, species_name, data[genus_name][species_name]])

# Escribir el JSON de salida en un archivo
json_file = os.path.join(output_dir, f'count_samples_report_{year}.json')
with open(json_file, mode='w') as file:
    json.dump(data, file, indent=4)