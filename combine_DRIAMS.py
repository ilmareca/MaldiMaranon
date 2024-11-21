import os
import pandas as pd
import xml.etree.ElementTree as ET

def parse_xml_to_dataframe(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    data = []
    for genus in root.findall(".//Genus"):
        genus_name = genus.attrib['name']
        for species in genus.findall(".//Species"):
            species_name = species.attrib['name']
            value = int(species.text)
            data.append([genus_name, species_name, value])
    
    df = pd.DataFrame(data, columns=['Genus', 'Species', 'Value'])
    return df

def combine_driams_data(base_dir):
    combined_df = pd.DataFrame(columns=['Genus', 'Species', 'Total'])
    driams_dirs = ['DRIAMS_A', 'DRIAMS_B', 'DRIAMS_C', 'DRIAMS_D']
    
    for driams in driams_dirs:
        xml_path = os.path.join(base_dir, driams, 'bacteria_counts', 'total', f'bacteria_counts_{driams[-1]}_total.xml')
        df = parse_xml_to_dataframe(xml_path)
        
        if combined_df.empty:
            combined_df = df
        else:
            combined_df = combined_df.set_index(['Genus', 'Species']).add(df.set_index(['Genus', 'Species']), fill_value=0).reset_index()
    
    return combined_df

def dataframe_to_xml(df, output_xml):
    root = ET.Element("Results")
    
    for genus_name, genus_df in df.groupby('Genus'):
        genus_element = ET.SubElement(root, "Genus", name=genus_name)
        for _, row in genus_df.iterrows():
            species_element = ET.SubElement(genus_element, "Species", name=row['Species'])
            species_element.text = str(int(row['Value']))
    
    tree = ET.ElementTree(root)
    tree.write(output_xml)

def main():
    base_dir = '/export/data_ml4ds/bacteria_id/relevant_datasets/DRIAMS_PROCESSED_DATABASE/stats'
    combined_df = combine_driams_data(base_dir)
    combined_df.to_csv('combined_driams_data.csv', index=False)
    dataframe_to_xml(combined_df, 'combined_driams_data.xml')
    print("Combined data saved to combined_driams_data.csv and combined_driams_data.xml")

if __name__ == "__main__":
    main()
