import os
from common_aDNA_scripts import *

import raw_reads_processing.analysis.determine_reads_processing_result as determine_reads_processing_result

def plot_reads_processing_result(species: str):

    print_info(f"Plotting reads processing result for species {species}") 

    input_file_path = os.path.join(get_folder_path_species_results_qc_reads_processing(species), f"{species}_reads_processing_result{FILE_ENDING_TSV}")

    if not os.path.exists(input_file_path):
        print_warning(f"Input file not found: {input_file_path}")
        return

    output_folder_path = get_folder_path_species_results_plots_reads_processing(species)

    if os.path.exists(output_folder_path):
        print_info(f"Output folder already exists: {output_folder_path}. Skipping.")
        return

    r_script = get_r_script(R_SCRIPT_PLOT_READS_BEFORE_AFTER_PROCESSING, FOLDER_RAW_READS_PROCESSING)

    call_r_script(r_script, species, input_file_path, output_folder_path)

def plot_sequence_length_distribution(species: str):
    print_info(f"Plotting sequence length distribution for species {species}")   

    analysis_files = get_files_in_folder_matching_pattern(get_folder_path_species_results_qc_read_length_distribution(species), f"*{FILE_ENDING_TSV}")

    if len(analysis_files) == 0:
        print_warning(f"No sequence length distribution files found for species {species}. Skipping.")
        return

    r_script = get_r_script(R_SCRIPT_PLOT_SEQUENCE_LENGTH_DISTRIBUTION, FOLDER_RAW_READS_PROCESSING)

    for analysis_file in analysis_files:
        
        output_folder_path = get_folder_path_species_results_plots_read_length_distribution(species)

        if os.path.exists(output_folder_path):
            print_info(f"Output folder already exists: {output_folder_path}. Skipping.")
            continue

        print_info(f"Plotting sequence length distribution for file {analysis_file} to {output_folder_path}")

        call_r_script(r_script, species, analysis_file, output_folder_path)

    print_info(f"Finished plotting sequence length distribution for species {species}")

def species_generate_plots(species: str):
    print_info(f"Generating plots for species {species}")

    plot_reads_processing_result(species)
    plot_sequence_length_distribution(species)

    print_info(f"Finished generating plots for species {species}")

def all_species_generate_plots():

    print("Generating plots for all species")

    for species in FOLDER_SPECIES:
        species_generate_plots(species)

    print_info("Finished generating plots for all species")

def main():
    all_species_generate_plots()

if __name__ == "__main__":
    main()