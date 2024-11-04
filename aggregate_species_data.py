import os
from collections import defaultdict
import csv
import json
import xml.etree.ElementTree as ET

# Directory containing the XML files
base_dir = '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results'

# Dictionary to store the aggregated data
data = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

# Parse each XML file and aggregate the data
years = set()
for year in os.listdir(base_dir):
    year_dir = os.path.join(base_dir, year, 'stats')
    report_file = os.path.join(year_dir, 'report.xml')
    if os.path.isfile(report_file):
        years.add(year)
        tree = ET.parse(report_file)
        root = tree.getroot()
        for genus in root.findall('Genus'):
            genus_name = genus.get('name')
            for species in genus.findall('Species'):
                species_name = species.get('name')
                count = int(species.text)
                data[genus_name][species_name][year] += count

# Create the output XML structure
root = ET.Element('Results')
for genus_name, species_data in data.items():
    genus_elem = ET.SubElement(root, 'Genus', name=genus_name)
    for species_name, counts in species_data.items():
        species_elem = ET.SubElement(genus_elem, 'Species', name=species_name)
        total_count = 0
        for year in sorted(years):
            count = counts.get(year, 0)
            year_elem = ET.SubElement(species_elem, 'Year', name=year)
            year_elem.text = str(count)
            total_count += count
        total_elem = ET.SubElement(species_elem, 'Total')
        total_elem.text = str(total_count)

# Write the output XML to a file
output_file = 'aggregated_report.xml'
tree = ET.ElementTree(root)
tree.write(output_file, encoding='utf-8', xml_declaration=True)
# Write the output CSV to a file
csv_file = 'aggregated_report.csv'
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Genus', 'Species', 'Year', 'Count', 'Total'])
    for genus_name, species_data in data.items():
        for species_name, counts in species_data.items():
            total_count = 0
            for year in sorted(years):
                count = counts.get(year, 0)
                writer.writerow([genus_name, species_name, year, count, ''])
                total_count += count
            writer.writerow([genus_name, species_name, 'Total', '', total_count])

# Write the output JSON to a file
json_file = 'aggregated_report.json'
json_data = {}
for genus_name, species_data in data.items():
    json_data[genus_name] = {}
    for species_name, counts in species_data.items():
        json_data[genus_name][species_name] = {}
        total_count = 0
        for year in sorted(years):
            count = counts.get(year, 0)
            json_data[genus_name][species_name][year] = count
            total_count += count
        json_data[genus_name][species_name]['Total'] = total_count

with open(json_file, 'w') as file:
    json.dump(json_data, file, indent=4)