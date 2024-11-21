import os
import pandas as pd
import json
import xml.etree.ElementTree as ET
import logging

# Function to configure logging with user choice
def configure_logging():
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    log_filename = f'{script_name}_DRIAMS_TOTAL_logfile.log'
    logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(message)s')

configure_logging()

# Define the base directory
base_dir = '/export/data_ml4ds/bacteria_id/relevant_datasets/DRIAMS_PROCESSED_DATABASE'

# Initialize an empty list to store the data
data = []

# List of subdirectories to explore
subdirs = ['DRIAMS_A', 'DRIAMS_B', 'DRIAMS_C', 'DRIAMS_D']

# Walk through the specified subdirectories
for subdir in subdirs:
    total_path = os.path.join(base_dir, subdir, 'TOTAL')
    for genus in os.listdir(total_path):
        genus_path = os.path.join(total_path, genus)
        if os.path.isdir(genus_path):
            for species in os.listdir(genus_path):
                species_path = os.path.join(genus_path, species)
                if os.path.isdir(species_path):
                    print(f'Processing {genus} {species}...')
                    txt_count = len([f for f in os.listdir(species_path) if f.endswith('.txt')])
                    
                    # Check if the genus and species already exist in the data
                    found = False
                    for entry in data:
                        if entry[0] == genus and entry[1] == species:
                            entry[2] += txt_count
                            found = True
                            break
                    
                    # If not found, add a new entry
                    if not found:
                        data.append([genus, species, txt_count])

# Create a DataFrame
df = pd.DataFrame(data, columns=['Genus', 'Species', 'Count'])

# Save the DataFrame to a CSV file
df.to_csv('bacteria_stats.csv', index=False)

# Create the root element
root = ET.Element("Results")

# Group the data by Genus
grouped = df.groupby('Genus')

# Create XML structure
for genus, group in grouped:
    genus_element = ET.SubElement(root, "Genus", name=genus)
    for _, row in group.iterrows():
        species_element = ET.SubElement(genus_element, "Species", name=row['Species'])
        species_element.text = str(row['Count'])

# Convert the XML structure to a string
xml_str = ET.tostring(root, encoding='unicode')

# Save the XML string to a file
with open('bacteria_stats.xml', 'w') as f:
    f.write(xml_str)
