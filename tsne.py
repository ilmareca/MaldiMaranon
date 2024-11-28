import os
import numpy as np
import matplotlib.pyplot as plt
from spectrum import SpectrumObject, VarStabilizer, Smoother, BaselineCorrecter, Normalizer, Trimmer  # Asegúrate de importar todo lo necesario
from sklearn.manifold import TSNE
from scipy import interpolate


# Define the base directory and species names
base_dir = '/export/data_ml4ds/bacteria_id/RAW_MaldiMaranon/data_cleaner_results_v2/2023/matched_bacteria'
species_names = ['Escherichia_Coli', 'Enterococcus_Faecalis', 'Staphylococcus_Aureus', 
                 'Klebsiella_Pneumoniae', 'Staphylococcus_Epidermidis']

# Function to load the spectra from the species directory
def load_spectra(species_name, base_dir, num_spectra=4000):
    species_dir = os.path.join(base_dir, species_name.replace("_", "/"))
    acqu_files = []
    fid_files = []
    
    # Traverse all subdirectories for acqu and fid files
    for root, dirs, files in os.walk(species_dir):
        for file in files:
            if file.endswith("acqu"):
                acqu_files.append(os.path.join(root, file))
            elif file.endswith("fid"):
                fid_files.append(os.path.join(root, file))

    # Ensure we get the first 'num_spectra' acqu and fid pairs
    acqu_files = acqu_files[:num_spectra]
    fid_files = fid_files[:num_spectra]

    return acqu_files, fid_files

# Function to preprocess spectra with variance stabilization, smoothing, baseline correction, normalization, and trimming
def preprocess_spectrum(acqu_file, fid_file, target_length=1000):
    spectrum = SpectrumObject.from_bruker(acqu_file, fid_file)
    
    # Apply each preprocessing step
    spectrum = variance_stabilization(spectrum)
    spectrum = smoothing(spectrum)
    spectrum = baseline_correction(spectrum)
    spectrum = normalization(spectrum)
    spectrum = trimming(spectrum)
    
    # Interpolate to the target length
    mz_new, intensity_new = interpolate_spectrum(spectrum, target_length)
    return intensity_new

# Preprocessing steps

def variance_stabilization(spectrum):
    stabilizer = VarStabilizer(method="sqrt")
    return stabilizer(spectrum)

def smoothing(spectrum):
    smoother = Smoother(halfwindow=10, polyorder=3)
    return smoother(spectrum)

def baseline_correction(spectrum):
    baseline_correcter = BaselineCorrecter(method="SNIP", snip_n_iter=10)
    return baseline_correcter(spectrum)

def normalization(spectrum):
    normalizer = Normalizer()
    return normalizer(spectrum)

def trimming(spectrum, min_mz=2000, max_mz=20000):
    trimmer = Trimmer(min=min_mz, max=max_mz)
    return trimmer(spectrum)

# Function to interpolate spectrum to the target length
def interpolate_spectrum(spectrum, target_length=1000):
    """Interpolate spectrum to ensure the same length."""
    f = interpolate.interp1d(spectrum.mz, spectrum.intensity, kind='linear', fill_value="extrapolate")
    mz_new = np.linspace(spectrum.mz.min(), spectrum.mz.max(), target_length)
    intensity_new = f(mz_new)
    return mz_new, intensity_new

def tsne_visualization(species_names, base_dir, output_base_dir, target_length=1000, num_spectra=4000):
    all_spectra = []
    labels = []
    colors = ['b', 'g', 'r', 'c', 'm']  # Assign a unique color for each species

    for idx, species_name in enumerate(species_names):
        # Load spectra for the species
        acqu_files, fid_files = load_spectra(species_name, base_dir, num_spectra)
        
        print(f"Loading spectra for {species_name}: {len(acqu_files)} files loaded.")
        
        # Process each spectrum for the species
        for acqu_file, fid_file in zip(acqu_files, fid_files):
            intensity_new = preprocess_spectrum(acqu_file, fid_file, target_length)
            all_spectra.append(intensity_new)
            labels.append(species_name)

    # Check number of spectra loaded
    print(f"Total samples loaded for t-SNE: {len(all_spectra)}")
    
    # Apply t-SNE only if there are enough samples
    n_samples = len(all_spectra)
    
    if n_samples < 2:
        print("Not enough samples for t-SNE visualization.")
        return
    
    # Dynamically adjust perplexity based on the number of samples
    perplexity_value = min(n_samples - 1, 30)  # Use 30 if there are more than 30 samples, otherwise use n_samples - 1

    tsne = TSNE(n_components=2, perplexity=perplexity_value)
    tsne_results = tsne.fit_transform(np.array(all_spectra))
    
    # Map species names to colors
    species_labels = {species: idx for idx, species in enumerate(species_names)}
    numeric_labels = [species_labels[label] for label in labels]

    # Plot the t-SNE results
    plt.figure(figsize=(10, 8))
    for idx, species_name in enumerate(species_names):
        species_indices = [i for i, label in enumerate(labels) if label == species_name]
        species_spectra = [tsne_results[i] for i in species_indices]
        plt.scatter([spec[0] for spec in species_spectra], [spec[1] for spec in species_spectra], 
                    label=species_name, color=colors[idx])

    # Add legend, title, and labels
    plt.legend(title="Species")
    plt.xlabel("t-SNE Component 1")
    plt.ylabel("t-SNE Component 2")
    plt.title("t-SNE Visualization of Preprocessed Spectra for 5 Species")
    
    # Save the t-SNE plot
    os.makedirs(output_base_dir, exist_ok=True)
    plt.savefig(os.path.join(output_base_dir, 'tsne_visualization_PREPRO.png'))
    plt.close()


# Running the workflow
output_base_dir = './tsne_results'  # You can specify your output directory
tsne_visualization(species_names, base_dir, output_base_dir)

print(f"t-SNE visualization saved to {output_base_dir}/tsne_visualization_PREPRO.png")
