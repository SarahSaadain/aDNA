import os
from common_aDNA_scripts import *

def plot_depth_analysis(species: str):
    print_info(f"Plotting depth analysis for species {species}")

# gives a list with the path and file names
    analysis_files = get_files_in_folder_matching_pattern(get_folder_path_species_results_qc_depth_breath(species), f"*{FILE_ENDING_ANALYSIS_TSV}")

# here have multiple files, one for each sample, hence the list
    if len(analysis_files) == 0:
        print_warning(f"No depth analysis files found for species {species}. Skipping.")
        return

    r_script = get_r_script(R_SCRIPT_PLOT_DEPTH, FOLDER_REF_GENOME_PROCESSING)

    for analysis_file in analysis_files:

        sample = os.path.basename(analysis_file).replace(FILE_ENDING_ANALYSIS_TSV, "")

        output_folder_path = get_folder_path_species_results_plots_depth_sample(species, sample)

        if os.path.exists(output_folder_path):
            print_info(f"Output folder already exists: {output_folder_path}. Skipping.")
            continue

        print_info(f"Plotting depth analysis for file {analysis_file} to {output_folder_path}")

        call_r_script(r_script, species, analysis_file, output_folder_path)

    print_info(f"Finished plotting depth analysis for species {species}")

def plot_breadth_analysis(species: str):
    print_info(f"Plotting breadth analysis for species {species}")

    analysis_files = get_files_in_folder_matching_pattern(get_folder_path_species_results_qc_depth_breath(species), f"*{FILE_ENDING_ANALYSIS_TSV}")

    if len(analysis_files) == 0:
        print_warning(f"No breadth analysis files found for species {species}. Skipping.")
        return

    r_script = get_r_script(R_SCRIPT_PLOT_BREADTH, FOLDER_REF_GENOME_PROCESSING)

    for analysis_file in analysis_files:

        sample = os.path.basename(analysis_file).replace(FILE_ENDING_ANALYSIS_TSV, "")

        output_folder_path = get_folder_path_species_results_plots_breadth_sample(species, sample)

        if os.path.exists(output_folder_path):
            print_info(f"Output folder already exists: {output_folder_path}. Skipping.")
            continue

        print_info(f"Plotting breadth analysis for file {analysis_file} to {output_folder_path}")

        call_r_script(r_script, species, analysis_file, output_folder_path)

    print_info(f"Finished plotting breadth analysis for species {species}")

def plot_endogenous_reads(species: str):
    print_info(f"Plotting endogenous reads for species {species}")

    analysis_files = get_files_in_folder_matching_pattern(get_folder_path_species_results_endogenous_reads(species), f"*_endogenous_reads{FILE_ENDING_CSV}")

    if len(analysis_files) == 0:
        print_warning(f"No endogenous reads files found for species {species}. Skipping.")
        return

    r_script = get_r_script(R_SCRIPT_PLOT_ENDOGENOUS_READS, FOLDER_REF_GENOME_PROCESSING)

    for analysis_file in analysis_files:

        output_folder_path = get_folder_path_species_results_plots_endogenous_reads(species)

        if os.path.exists(output_folder_path):
            print_info(f"Output folder already exists: {output_folder_path}. Skipping.")
            continue

        print_info(f"Plotting endogenous reads for file {analysis_file} to {output_folder_path}")

        call_r_script(r_script, species, analysis_file, output_folder_path)

    print_info(f"Finished plotting endogenous reads for species {species}")

def species_generate_plots(species: str):
    print_info(f"Generating reference genome plots for species {species}")

    plot_depth_analysis(species)
    plot_breadth_analysis(species)
    plot_endogenous_reads(species)

    print_info(f"Finished generating reference genome plots for species {species}")

def all_species_generate_plots():

    print("Generating reference genome plots for all species")

    for species in FOLDER_SPECIES:
        species_generate_plots(species)

    print_info("Finished generating reference genome plots for all species")

def main():
    all_species_generate_plots()

if __name__ == "__main__":
    main()