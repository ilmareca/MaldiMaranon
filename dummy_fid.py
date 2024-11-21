def load_and_convert_fid_to_hex(fid_file, output_hex_file):
    # Cargar el archivo FID en modo binario
    with open(fid_file, 'rb') as f:
        content = f.read()

    # Convertir el contenido a hexadecimal
    hex_content = content.hex()

    # Guardar el contenido hexadecimal en un archivo TXT
    with open(output_hex_file, 'w') as f:
        f.write(hex_content)

def load_and_strip_hex_file(hex_file, output_stripped_file):
    # Cargar el archivo hexadecimal
    with open(hex_file, 'r') as f:
        content = f.read()

    # Verificar si el contenido es todo ceros
    if set(content.strip()) == {'0'}:
        print("Warning: El archivo está vacío o contiene solo ceros.")

    # Hacer .strip() al contenido
    stripped_content = content.strip()

    # Guardar el contenido procesado en un archivo TXT
    with open(output_stripped_file, 'w') as f:
        f.write(stripped_content)

def main():
    fid_file = 'fid'
    output_hex_file = 'fid_output_hex.txt'
    output_stripped_file = 'fid_output_stripped.txt'

    # Convertir FID a hexadecimal y guardar en un archivo
    load_and_convert_fid_to_hex(fid_file, output_hex_file)
    print(f"Hexadecimal content saved to {output_hex_file}")

    # Cargar el archivo hexadecimal, verificar si está vacío, hacer strip y guardar en otro archivo
    load_and_strip_hex_file(output_hex_file, output_stripped_file)
    print(f"Stripped content saved to {output_stripped_file}")

if __name__ == "__main__":
    main()