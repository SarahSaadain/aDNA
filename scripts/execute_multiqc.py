import os
from common_aDNA_scripts import *

def multiqc_before_after(species):
    # before: run multiqc for raw data
    multiqc_for_raw_data(species)

    # after: run multiqc for trimmed data
    multiqc_for_trimmed_data(species)

def multiqc_for_raw_data(species):
    print_info(f"Running MultiQC for species {species} raw data")

    # raw data
    raw_fastqc_folder = get_folder_path_species_results_qc_fastqc_raw(species)
    output_folder = get_folder_path_species_results_qc_multiqc_raw(species)

    files_list = get_files_in_folder_matching_pattern(output_folder, "*.html")

    if len(files_list) > 0:
        print_warning(f"Fastqc data already exists for species {species}. Skipping.")
        return

    run_multiqc(species, raw_fastqc_folder, output_folder)

    print_success(f"MultiQC for species {species} raw data complete")

def multiqc_for_trimmed_data(species):
    print_info(f"Running MultiQC for species {species} trimmed data")

    #adapter removed data
    trimmed_fastqc_folder = get_folder_path_species_results_qc_fastqc_adapter_removed(species)
    output_folder = get_folder_path_species_results_qc_multiqc_adapter_removed(species)

    files_list = get_files_in_folder_matching_pattern(output_folder, "*.html")

    if len(files_list) > 0:
        print_warning(f"Fastqc data already exists for species {species}. Skipping.")
        return


    run_multiqc(species, trimmed_fastqc_folder, output_folder)

    print_success(f"Multiqc for species {species} trimmed data complete")

def run_multiqc(species, fastqc_results_folder, output_folder):

    command = f"multiqc {fastqc_results_folder} -o {output_folder}"
    try:
        subprocess.run(command, shell=True, check=True)
    except Exception as e:
        print_error(f"Failed to run MultiQC for species {species}: {e}")

def all_species_multiqc_before_after():

    print("Running MultiQC for all species before and after adapter removal")

    for species in FOLDER_SPECIES: 
        multiqc_before_after(species)

def all_species_multiqc_raw():
    print("Running MultiQC for all species raw data")

    for species in FOLDER_SPECIES: 
        multiqc_for_raw_data(species)

def all_species_multiqc_trimmed():
    print("Running MultiQC for all species trimmed data")

    for species in FOLDER_SPECIES: 
       multiqc_for_trimmed_data(species)
        

def main():
    all_species_multiqc_before_after()

if __name__ == "__main__":
    main()
