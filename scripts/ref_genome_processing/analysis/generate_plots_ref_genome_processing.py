import os
from common_aDNA_scripts import *

import ref_genome_processing.helpers.ref_genome_processing_helper as ref_genome_processing_helper

def plot_depth_analysis(species: str, reference_genome_id: str):
    print_info(f"Plotting depth analysis for species {species}")

    analysis_folder = get_folder_path_species_results_refgenome_coverage(species, reference_genome_id)

    # gives a list with the path and file names
    analysis_files = get_files_in_folder_matching_pattern(analysis_folder, f"*{FILE_ENDING_ANALYSIS_TSV}")

    # here have multiple files, one for each sample, hence the list
    if len(analysis_files) == 0:
        print_warning(f"No depth analysis files found for species {species}. Skipping.")
        return

    r_script = get_r_script(R_SCRIPT_PLOT_DEPTH, FOLDER_REF_GENOME_PROCESSING)

    for analysis_file in analysis_files:

        sample = get_filename_from_path(analysis_file).replace(FILE_ENDING_ANALYSIS_TSV, "")

        output_folder_path = get_folder_path_species_results_refgenome_plots_depth_sample(species, reference_genome_id, sample)

        if os.path.exists(output_folder_path):
            print_info(f"Output folder already exists: {output_folder_path}. Skipping.")
            continue

        print_info(f"Plotting depth analysis for file {analysis_file} to {output_folder_path}")

        call_r_script(r_script, species, analysis_file, output_folder_path)

    print_info(f"Finished plotting depth analysis for species {species}")

def plot_breadth_analysis(species: str, reference_genome_id: str):
    print_info(f"Plotting breadth analysis for species {species}")

    analysis_folder = get_folder_path_species_results_refgenome_coverage(species, reference_genome_id)

    analysis_files = get_files_in_folder_matching_pattern(analysis_folder, f"*{FILE_ENDING_ANALYSIS_TSV}")

    if len(analysis_files) == 0:
        print_warning(f"No breadth analysis files found for species {species}. Skipping.")
        return

    r_script = get_r_script(R_SCRIPT_PLOT_BREADTH, FOLDER_REF_GENOME_PROCESSING)

    for analysis_file in analysis_files:

        sample = get_filename_from_path(analysis_file).replace(FILE_ENDING_ANALYSIS_TSV, "")

        output_folder_path = get_folder_path_species_results_refgenome_plots_breadth_sample(species, reference_genome_id, sample)

        if os.path.exists(output_folder_path):
            print_info(f"Output folder already exists: {output_folder_path}. Skipping.")
            continue

        print_info(f"Plotting breadth analysis for file {analysis_file} to {output_folder_path}")

        call_r_script(r_script, species, analysis_file, output_folder_path)

    print_info(f"Finished plotting breadth analysis for species {species}")

def plot_endogenous_reads(species: str, reference_genome_id: str):
    print_info(f"Plotting endogenous reads for species {species}")

    endogenous_reads_analysis_folder = get_folder_path_species_results_refgenome_endogenous_reads(species, reference_genome_id)

    analysis_files = get_files_in_folder_matching_pattern(endogenous_reads_analysis_folder, f"*_endogenous_reads{FILE_ENDING_CSV}")

    if len(analysis_files) == 0:
        print_warning(f"No endogenous reads files found for species {species}. Skipping.")
        return

    r_script = get_r_script(R_SCRIPT_PLOT_ENDOGENOUS_READS, FOLDER_REF_GENOME_PROCESSING)

    for analysis_file in analysis_files:

        output_folder_path = get_folder_path_species_results_refgenome_plots_endogenous_reads(species, reference_genome_id)

        if os.path.exists(output_folder_path):
            print_info(f"Output folder already exists: {output_folder_path}. Skipping.")
            continue

        print_info(f"Plotting endogenous reads for file {analysis_file} to {output_folder_path}")

        call_r_script(r_script, species, analysis_file, output_folder_path)

    print_info(f"Finished plotting endogenous reads for species {species}")

def species_generate_plots(species: str):
    print_info(f"Generating reference genome plots for species {species}")

    try:
        ref_genome_list = ref_genome_processing_helper.get_reference_genome_file_list_for_species(species)
    except Exception as e:
        print_error(f"Failed to get reference genome files for species {species}: {e}")
        return

    for ref_genome_tuple in ref_genome_list:

        # ref_genome is a tuple of (ref_genome_name without extension, ref_genome_path)
        ref_genome_id = ref_genome_tuple[0]
        #ref_genome_path = ref_genome_tuple[1]

        print_info(f"Generating plots for reference genome {ref_genome_id}")

        plot_depth_analysis(species, ref_genome_id)
        plot_breadth_analysis(species, ref_genome_id)
        plot_endogenous_reads(species, ref_genome_id)

    print_info(f"Finished generating reference genome plots for species {species}")

def all_species_generate_plots():

    print_execution("Generating reference genome plots for all species")

    for species in FOLDER_SPECIES:
        species_generate_plots(species)

    print_info("Finished generating reference genome plots for all species")

def main():
    all_species_generate_plots()

if __name__ == "__main__":
    main()