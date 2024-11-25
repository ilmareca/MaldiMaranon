import matplotlib.pyplot as plt
from spectrum import SpectrumObject, Normalizer, VarStabilizer, Smoother, BaselineCorrecter, Trimmer
import os

def visualize_and_save_spectrum(spectrum, output_dir, output_filename, title):
    plt.figure()
    plt.plot(spectrum.mz, spectrum.intensity)
    plt.xlabel('m/z')
    plt.ylabel('Intensity')
    plt.title(title)
    plt.savefig(os.path.join(output_dir, output_filename))
    plt.close()

def process_spectrum(spectrum, output_dir, prefix):
    # Step 1: Variance stabilization
    stabilizer = VarStabilizer(method="sqrt")
    spectrum = stabilizer(spectrum)
    visualize_and_save_spectrum(spectrum, output_dir, f'{prefix}_variance_stabilized.png', 'Variance Stabilized Spectrum')

    # Step 2: Smoothing
    smoother = Smoother(halfwindow=10, polyorder=3)
    spectrum = smoother(spectrum)
    visualize_and_save_spectrum(spectrum, output_dir, f'{prefix}_smoothed.png', 'Smoothed Spectrum')

    # Step 3: Baseline correction
    baseline_correcter = BaselineCorrecter(method="SNIP", snip_n_iter=10)
    spectrum = baseline_correcter(spectrum)
    visualize_and_save_spectrum(spectrum, output_dir, f'{prefix}_baseline_corrected.png', 'Baseline Corrected Spectrum')

    # Step 4: Normalization
    normalizer = Normalizer()
    spectrum = normalizer(spectrum)
    visualize_and_save_spectrum(spectrum, output_dir, f'{prefix}_normalized.png', 'Normalized Spectrum')

    # Step 5: Trimming
    trimmer = Trimmer(min=2000, max=20000)
    spectrum = trimmer(spectrum)
    visualize_and_save_spectrum(spectrum, output_dir, f'{prefix}_trimmed.png', 'Trimmed Spectrum')

    return spectrum

def visualize_and_save_multiple_spectra(acqu_files, fid_files, output_dir, output_filename, normalize=False):
    colors = ['b', 'g', 'r', 'c', 'm']  # Colors for different spectra

    plt.figure()

    for i, (acqu_file, fid_file) in enumerate(zip(acqu_files, fid_files)):
        # Create a SpectrumObject from Bruker files
        spectrum = SpectrumObject.from_bruker(acqu_file, fid_file)

        # Save the individual spectrum before processing
        visualize_and_save_spectrum(spectrum, output_dir, f'spectrum_{i+1}.png', f'Spectrum {i+1}')

        # Process the spectrum
        spectrum = process_spectrum(spectrum, output_dir, f'spectrum_{i+1}')

        # Normalize the spectrum if necessary
        if normalize:
            normalizer = Normalizer()
            spectrum = normalizer(spectrum)

        # Plot the spectrum
        plt.plot(spectrum.mz, spectrum.intensity, color=colors[i % len(colors)], label=f'Spectrum {i+1}')

    plt.xlabel('m/z')
    plt.ylabel('Intensity')
    plt.title('Overlaid Bruker Spectra' + (' Normalized' if normalize else ''))
    plt.legend()

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Save the figure in the output directory
    output_path = os.path.join(output_dir, output_filename)
    plt.savefig(output_path)
    plt.close()
    print(f"Spectra saved in: {output_path}")

if __name__ == "__main__":
    # Define the paths to your Bruker files for each species
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
        # Add more species here
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
        # Add more species here
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
        # Add more species here
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
        # Add more species here
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

    # Define the base output directory
    base_output_dir = '/export/usuarios01/ilmareca/github/MaldiMaranon/images/spectrum'

    # Visualize and save the spectra for each species
    for species, files in species_data.items():
        output_dir = os.path.join(base_output_dir, species)
        output_filename = 'overlaid_spectra.png'
        visualize_and_save_multiple_spectra(files['acqu_files'], files['fid_files'], output_dir, output_filename)
        
        # Generate and save the normalized spectra
        output_filename_normalized = 'overlaid_spectra_normalized.png'
        visualize_and_save_multiple_spectra(files['acqu_files'], files['fid_files'], output_dir, output_filename_normalized, normalize=True)