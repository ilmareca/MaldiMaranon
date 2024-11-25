import matplotlib.pyplot as plt
from spectrum import SpectrumObject, Normalizer
import os

def visualize_and_save_multiple_spectra(acqu_files, fid_files, output_dir, output_filename, normalize=False):
    colors = ['b', 'g', 'r', 'c', 'm']  # Colores para los diferentes espectros

    plt.figure()

    for i, (acqu_file, fid_file) in enumerate(zip(acqu_files, fid_files)):
        # Crear un objeto SpectrumObject desde los archivos Bruker
        spectrum = SpectrumObject.from_bruker(acqu_file, fid_file)

        # Normalizar el espectro si es necesario
        if normalize:
            normalizer = Normalizer()
            spectrum = normalizer(spectrum)

        # Visualizar el espectro
        plt.plot(spectrum.mz, spectrum.intensity, color=colors[i % len(colors)], label=f'Spectrum {i+1}')

    plt.xlabel('m/z')
    plt.ylabel('Intensidad')
    plt.title('Espectros Bruker Superpuestos' + (' Normalizados' if normalize else ''))
    plt.legend()

    # Asegurarse de que el directorio de salida exista
    os.makedirs(output_dir, exist_ok=True)

    # Guardar la figura en el directorio de salida
    output_path = os.path.join(output_dir, output_filename)
    plt.savefig(output_path)
    plt.close()
    print(f"Espectros guardados en: {output_path}")

if __name__ == "__main__":
    # Define las rutas a tus archivos Bruker para cada especie
    species_data = {
        'Escherichia_Coli': {
            'acqu_files': [
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Escherichia/Coli/18252920/0_D5/1/1SLin/acqu',
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Escherichia/Coli/18115713/0_E12/1/1SLin/acqu',
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Escherichia/Coli/18129745/0_A12/1/1SLin/acqu',
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Escherichia/Coli/18145755/0_B11/1/1SLin/acqu',
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Escherichia/Coli/18148292/0_F5/1/1SLin/acqu'
            ],
            'fid_files': [
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Escherichia/Coli/18252920/0_D5/1/1SLin/fid',
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Escherichia/Coli/18115713/0_E12/1/1SLin/fid',
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Escherichia/Coli/18129745/0_A12/1/1SLin/fid',
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Escherichia/Coli/18145755/0_B11/1/1SLin/fid',
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Escherichia/Coli/18148292/0_F5/1/1SLin/fid'
            ]
        },
        # Agrega más especies aquí
        'Enterococcus_Faecalis': {
            'acqu_files': [
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Enterococcus/Faecalis/18128679/0_D2/1/1SLin/acqu',
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Enterococcus/Faecalis/18128154/0_B7/1/1SLin/acqu',
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Enterococcus/Faecalis/18141809/0_B3/1/1SLin/acqu',
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Enterococcus/Faecalis/18153673/0_C5/1/1SLin/acqu',
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Enterococcus/Faecalis/18162817/0_E8/1/1SLin/acqu'
            ],
            'fid_files': [
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Enterococcus/Faecalis/18128679/0_D2/1/1SLin/fid',
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Enterococcus/Faecalis/18128154/0_B7/1/1SLin/fid',
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Enterococcus/Faecalis/18141809/0_B3/1/1SLin/fid',
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Enterococcus/Faecalis/18153673/0_C5/1/1SLin/fid',
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Enterococcus/Faecalis/18162817/0_E8/1/1SLin/fid'
            ]
        },
        # Agrega más especies aquí
        'Staphylococcus_Aureus': {
            'acqu_files': [
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Staphylococcus/Aureus/18215596/0_B5/1/1SLin/acqu',
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Staphylococcus/Aureus/18115713/0_F1/1/1SLin/acqu',
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Staphylococcus/Aureus/18120280/0_A6/1/1SLin/acqu',
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Staphylococcus/Aureus/18125381/0_D11/1/1SLin/acqu',
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Staphylococcus/Aureus/18138077/0_A4/1/1SLin/acqu'
            ],
            'fid_files': [
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Staphylococcus/Aureus/18215596/0_B5/1/1SLin/fid',
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Staphylococcus/Aureus/18115713/0_F1/1/1SLin/fid',
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Staphylococcus/Aureus/18120280/0_A6/1/1SLin/fid',
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Staphylococcus/Aureus/18125381/0_D11/1/1SLin/fid',
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Staphylococcus/Aureus/18138077/0_A4/1/1SLin/fid'
            ]
        },
        # Agrega más especies aquí
        'Klebsiella_Pneumoniaee': {
            'acqu_files': [
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Klebsiella/Pneumoniae/16061980/0_E5/1/1SLin/acqu',
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Klebsiella/Pneumoniae/18117816/0_D9/1/1SLin/acqu',
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Klebsiella/Pneumoniae/18137525/0_A12/1/1SLin/acqu',
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Klebsiella/Pneumoniae/18146335/0_F1/1/1SLin/acqu',
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Klebsiella/Pneumoniae/18157589/0_C3/1/1SLin/acqu'
            ],
            'fid_files': [
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Klebsiella/Pneumoniae/16061980/0_E5/1/1SLin/fid',
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Klebsiella/Pneumoniae/18117816/0_D9/1/1SLin/fid',
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Klebsiella/Pneumoniae/18137525/0_A12/1/1SLin/fid',
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Klebsiella/Pneumoniae/18146335/0_F1/1/1SLin/fid',
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Klebsiella/Pneumoniae/18157589/0_C3/1/1SLin/fid'
            ]
        },
        # Agrega más especies aquí
        'Staphylococcus_Epidermidis': {
            'acqu_files': [
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Staphylococcus/Epidermidis/18115317/0_D4/1/1SLin/acqu',
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Staphylococcus/Epidermidis/18115836/0_A12/1/1SLin/acqu',
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Staphylococcus/Epidermidis/18116724/0_A7/1/1SLin/acqu',
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Staphylococcus/Epidermidis/18128578/0_B5/1/1SLin/acqu',
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Staphylococcus/Epidermidis/18151897/0_G9/1/1SLin/acqu'
            ],
            'fid_files': [
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Staphylococcus/Epidermidis/18115317/0_D4/1/1SLin/fid',
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Staphylococcus/Epidermidis/18115836/0_A12/1/1SLin/fid',
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Staphylococcus/Epidermidis/18116724/0_A7/1/1SLin/fid',
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Staphylococcus/Epidermidis/18128578/0_B5/1/1SLin/fid',
                '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2018/matched_bacteria/Staphylococcus/Epidermidis/18151897/0_G9/1/1SLin/fid'
            ]
        }
    }

    # Define el directorio base de salida
    base_output_dir = '/export/usuarios01/ilmareca/github/MaldiMaranon/images/spectrum'

    # Visualiza y guarda los espectros para cada especie
    for species, files in species_data.items():
        output_dir = os.path.join(base_output_dir, species)
        output_filename = 'espectro_bruker.png'
        visualize_and_save_multiple_spectra(files['acqu_files'], files['fid_files'], output_dir, output_filename)
        
        # Generar y guardar los espectros normalizados
        output_filename_normalized = 'espectro_bruker_normalized.png'
        visualize_and_save_multiple_spectra(files['acqu_files'], files['fid_files'], output_dir, output_filename_normalized, normalize=True)