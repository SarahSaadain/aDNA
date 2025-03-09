import os
import subprocess
from common_aDNA_scripts import *

import determine_reads_processing_result as determine_reads_processing_result

def call_r_script(script_path, *args):
    if not os.path.exists(script_path):
        raise FileNotFoundError(f"R script not found: {script_path}")

    command = ["Rscript", script_path] + list(args)
    try:
        subprocess.run(command, check=True)
        print(f"Successfully executed {command}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing {script_path}: {e}")

def plot_reads_processing_result(species):

    print_info(f"Plotting reads processing result for species {species}") 

    input_file_path = os.path.join(get_folder_path_species_results_qc_reads_processing(species), f"{species}_reads_processing_result{FILE_ENDING_TSV}")

    if not os.path.exists(input_file_path):
        print_error(f"Input file not found: {input_file_path}")
        return

    output_folder_path = get_folder_path_species_results_plots_reads_processing(species)

    r_script = get_r_script(R_SCRIPT_PLOT_READS_BEFORE_AFTER_PROCESSING)

    call_r_script(r_script, species, input_file_path, output_folder_path)

def plot_depth_analysis(species):
    print_info(f"Plotting depth analysis for species {species}")

# gives a list with the path and file names
    analysis_files = get_files_in_folder_matching_pattern(get_folder_path_species_results_qc_depth_breath(species), f"*{FILE_ENDING_ANALYSIS_TSV}")

# here have multiple files, one for each sample, hence the list
    if len(analysis_files) == 0:
        print_warning(f"No depth analysis files found for species {species}. Skipping.")
        return

    r_script = get_r_script(R_SCRIPT_PLOT_DEPTH)

    for analysis_file in analysis_files:

        sample = os.path.basename(analysis_file).replace(FILE_ENDING_ANALYSIS_TSV, "")

        output_folder_path = get_folder_path_species_results_plots_depth_sample(species, sample)

        print_info(f"Plotting depth analysis for file {analysis_file} to {output_folder_path}")

        call_r_script(r_script, species, analysis_file, output_folder_path)

    print_info(f"Finished plotting depth analysis for species {species}")

def plot_breadth_analysis(species):
    print_info(f"Plotting breadth analysis for species {species}")

    analysis_files = get_files_in_folder_matching_pattern(get_folder_path_species_results_qc_depth_breath(species), f"*{FILE_ENDING_ANALYSIS_TSV}")

    if len(analysis_files) == 0:
        print_warning(f"No breadth analysis files found for species {species}. Skipping.")
        return

    r_script = get_r_script(R_SCRIPT_PLOT_BREADTH)

    for analysis_file in analysis_files:

        sample = os.path.basename(analysis_file).replace(FILE_ENDING_ANALYSIS_TSV, "")

        output_folder_path = get_folder_path_species_results_plots_breadth_sample(species, sample)

        print_info(f"Plotting breadth analysis for file {analysis_file} to {output_folder_path}")

        call_r_script(r_script, species, analysis_file, output_folder_path)

    print_info(f"Finished plotting breadth analysis for species {species}")

def plot_endogenous_reads(species):
    print_info(f"Plotting endogenous reads for species {species}")

    analysis_files = get_files_in_folder_matching_pattern(get_folder_path_species_results_endogenous_reads(species), f"*_endogenous_reads{FILE_ENDING_CSV}")

    if len(analysis_files) == 0:
        print_warning(f"No endogenous reads files found for species {species}. Skipping.")
        return

    r_script = get_r_script(R_SCRIPT_PLOT_ENDOGENOUS_READS)

    for analysis_file in analysis_files:

        output_folder_path = get_folder_path_species_results_plots_endogenous_reads(species)

        print_info(f"Plotting endogenous reads for file {analysis_file} to {output_folder_path}")

        call_r_script(r_script, species, analysis_file, output_folder_path)

    print_info(f"Finished plotting endogenous reads for species {species}")

def plot_sequence_length_distribution(species):
    print_info(f"Plotting sequence length distribution for species {species}")   

    analysis_files = get_files_in_folder_matching_pattern(get_folder_path_species_results_qc_read_length_distribution(species), f"*{FILE_ENDING_TSV}")

    if len(analysis_files) == 0:
        print_warning(f"No sequence length distribution files found for species {species}. Skipping.")
        return

    r_script = get_r_script(R_SCRIPT_PLOT_SEQUENCE_LENGTH_DISTRIBUTION)

    for analysis_file in analysis_files:
        
        output_folder_path = get_folder_path_species_results_plots_read_length_distribution(species)

        print_info(f"Plotting sequence length distribution for file {analysis_file} to {output_folder_path}")

        call_r_script(r_script, species, analysis_file, output_folder_path)

    print_info(f"Finished plotting sequence length distribution for species {species}")

def species_generate_plots(species):
    print_info(f"Generating plots for species {species}")

    plot_reads_processing_result(species)
    plot_depth_analysis(species)
    plot_breadth_analysis(species)
    plot_endogenous_reads(species)
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