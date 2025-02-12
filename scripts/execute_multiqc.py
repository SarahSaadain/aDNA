import os
from common_aDNA_scripts import *

def multiqc_for_species(species):
    # run multiqc for raw data
    multiqc_for_raw_data(species)

    # run multiqc for trimmed data
    multiqc_for_adapter_removed_data(species)

    # run multiqc for quality filtered data
    multiqc_for_quality_filtered_data(species)

    # run multiqc for duplicates removed data
    multiqc_for_duplicates_removed_data(species)

def multiqc_for_raw_data(species):
    print_info(f"Running MultiQC for species {species} raw data")

    # raw data
    raw_fastqc_folder = get_folder_path_species_results_qc_fastqc_raw(species)

    file_list = get_files_in_folder_matching_pattern(raw_fastqc_folder, f"*{FILE_ENDING_FASTQC_HTML}")

    if len(file_list) == 0:
        print_warning(f"No fastqc data found for species {species}. Skipping.")
        return

    output_folder = get_folder_path_species_results_qc_multiqc_raw(species)

    files_list = get_files_in_folder_matching_pattern(output_folder, "*.html")

    if len(files_list) > 0:
        print_warning(f"Fastqc data already exists for species {species}. Skipping.")
        return

    run_multiqc(species, raw_fastqc_folder, output_folder)

    print_success(f"MultiQC for species {species} raw data complete")

def multiqc_for_quality_filtered_data(species):
    print_info(f"Running MultiQC for species {species} quality filtered data")  

    quality_filtered_fastqc_folder = get_folder_path_species_results_qc_fastqc_quality_filtered(species)

    file_list = get_files_in_folder_matching_pattern(quality_filtered_fastqc_folder, f"*{FILE_ENDING_FASTQC_HTML}")

    if len(file_list) == 0:
        print_warning(f"No fastqc data found for species {species}. Skipping.")
        return

    output_folder = get_folder_path_species_results_qc_multiqc_quality_filtered(species)

    files_list_multiqc_check = get_files_in_folder_matching_pattern(output_folder, "*.html")

    if len(files_list_multiqc_check) > 0:
        print_warning(f"Fastqc data already exists for species {species}. Skipping.")
        return

    run_multiqc(species, quality_filtered_fastqc_folder, output_folder)

    print_success(f"MultiQC for species {species} quality filtered data complete")

def multiqc_for_duplicates_removed_data(species):
    print_info(f"Running MultiQC for species {species} duplicates removed data")

    duplicates_removed_fastqc_folder = get_folder_path_species_results_qc_fastqc_duplicates_removed(species)

    file_list = get_files_in_folder_matching_pattern(duplicates_removed_fastqc_folder, f"*{FILE_ENDING_FASTQC_HTML}")

    if len(file_list) == 0:
        print_warning(f"No fastqc data found for species {species}. Skipping.")
        return

    output_folder = get_folder_path_species_results_qc_multiqc_duplicates_removed(species)

    files_list = get_files_in_folder_matching_pattern(output_folder, "*.html")

    if len(files_list) > 0:
        print_warning(f"Fastqc data already exists for species {species}. Skipping.")
        return

    run_multiqc(species, duplicates_removed_fastqc_folder, output_folder)

    print_success(f"MultiQC for species {species} duplicates removed data complete")

def multiqc_for_adapter_removed_data(species):
    print_info(f"Running MultiQC for species {species} trimmed data")

    #adapter removed data
    trimmed_fastqc_folder = get_folder_path_species_results_qc_fastqc_adapter_removed(species)

    file_list = get_files_in_folder_matching_pattern(trimmed_fastqc_folder, f"*{FILE_ENDING_FASTQC_HTML}")

    if len(file_list) == 0:
        print_warning(f"No fastqc data found for species {species}. Skipping.")
        return

    output_folder = get_folder_path_species_results_qc_multiqc_adapter_removed(species)

    files_list = get_files_in_folder_matching_pattern(output_folder, "*.html")

    if len(files_list) > 0:
        print_warning(f"Fastqc data already exists for species {species}. Skipping.")
        return

    run_multiqc(species, trimmed_fastqc_folder, output_folder)

    print_success(f"Multiqc for species {species} trimmed data complete")

def run_multiqc(species, fastqc_results_folder, output_folder):

    command = f"{PROGRAM_PATH_MULTIQC} {fastqc_results_folder} -o {output_folder}"
    try:
        subprocess.run(command, shell=True, check=True)
    except Exception as e:
        print_error(f"Failed to run MultiQC for species {species}: {e}")

def all_species_multiqc():

    print("Running MultiQC for all species before and after adapter removal")

    for species in FOLDER_SPECIES: 
        multiqc_for_species(species)

def all_species_multiqc_raw():
    print("Running MultiQC for all species raw data")

    for species in FOLDER_SPECIES: 
        multiqc_for_raw_data(species)

def all_species_multiqc_adapter_removed():
    print("Running MultiQC for all species trimmed data")

    for species in FOLDER_SPECIES: 
       multiqc_for_adapter_removed_data(species)

def all_species_multiqc_quality_filtered():
    print("Running MultiQC for all species quality filtered data")

    for species in FOLDER_SPECIES: 
        multiqc_for_quality_filtered_data(species)

def all_species_multiqc_duplicates_removed():
    print("Running MultiQC for all species duplicates removed data")

    for species in FOLDER_SPECIES: 
        multiqc_for_duplicates_removed_data(species)

def main():
    all_species_multiqc()

if __name__ == "__main__":
    main()
