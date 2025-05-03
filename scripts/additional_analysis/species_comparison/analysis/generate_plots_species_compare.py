import os
from common_aDNA_scripts import *

def plot_reads_processing_result(species: list, reference_genomes: dict):
    """
    Plots the results of read processing (before and after filtering) for the given species.

    Args:
        species (list): A list of species names (strings).
        reference_genomes (dict): A dictionary of species names and their reference genomes.
    """
    scripts_base_folder = os.path.join(FOLDER_ADDITIONAL_ANALYSIS, FOLDER_SPECIES_COMPARISON)
    species_string = ",".join(species)
    print_info(f"Plotting reads before and after comparison for species {species_string}")
    root_folder_path = PATH_ADNA_PROJECT
    output_folder_path = get_folder_path_results_plots()

    analysis_files_to_compare = []

    for species_name in species:

        analysis_folder_path = get_folder_path_species_results_refgenome_coverage(species_name, reference_genomes[species_name])

        combined_file_path = os.path.join(analysis_folder_path, f"{species}_combined_coverage_analysis{FILE_ENDING_CSV}") # Using CSV for combined output

        if not os.path.exists(combined_file_path):
            print_info(f"Combined coverage analysis file not found for {species_name}. Skipping.")
            continue

        analysis_files_to_compare.append(combined_file_path)
        print_info(f"Found combined coverage analysis file for {species_name}: {combined_file_path}")

    # Include comparison name in the output filename to avoid overwriting
    if len(get_files_in_folder_matching_pattern(output_folder_path, f"*{'_'.join(species)}.png")) > 0:
        print_info(f"Plots already exist for species {species_string}. Skipping plot generation.")
        return

    r_script = get_r_script(R_SCRIPT_PLOT_COMPARE_SPECIES_READS_BEFORE_AFTER_PROCESSING, scripts_base_folder)
    # Pass the reference genomes to the R script.  This assumes the R script
    # can accept them as command-line arguments.  You might need to modify
    # the R script as well.
    call_r_script(r_script, root_folder_path, species_string, output_folder_path, reference_genomes)
    print_info(f"Finished reads before and after comparison for species {species_string}")

def plot_depth_breadth_analysis():
    """
    Plots the depth and breadth of coverage for the given species.

    Args:
        species (list): A list of species names (strings).
        reference_genomes (dict): A dictionary of species names and their reference genomes.
    """
    scripts_base_folder = os.path.join(FOLDER_ADDITIONAL_ANALYSIS, FOLDER_SPECIES_COMPARISON)
    
    print_info(f"Plotting depth and breadth comparison.")
    root_folder_path = PATH_ADNA_PROJECT
    output_folder_path = get_folder_path_results_plots()

    r_script = get_r_script(R_SCRIPT_PLOT_COMPARE_SPECIES_DEPTH_BREADTH, scripts_base_folder)
    # Pass the reference genomes to the R script.
    call_r_script(r_script, root_folder_path, config_file_path, output_folder_path)
    print_info(f"Finished plotting depth and breadth comparison.")

def plot_endogenous_reads():
    """
    Plots the comparison of endogenous reads for the given species.

    Args:
        species (list): A list of species names (strings).
        reference_genomes (dict): A dictionary of species names and their reference genomes.
    """
    scripts_base_folder = os.path.join(FOLDER_ADDITIONAL_ANALYSIS, FOLDER_SPECIES_COMPARISON)
    print_info(f"Plotting endogenous reads comparison.")
    root_folder_path = PATH_ADNA_PROJECT
    output_folder_path = get_folder_path_results_plots()

    r_script = get_r_script(R_SCRIPT_PLOT_COMPARE_SPECIES_ENDOGENOUS_READS, scripts_base_folder)
    # Pass the reference genomes to the R script.
    call_r_script(r_script, root_folder_path, config_file_path, output_folder_path)
    print_info(f"Finished plotting endogenous reads comparison.")

def species_generate_comparison_plots():
    
    print_execution("Generating comparison plots for species based on config")

    #plot_reads_processing_result(species, reference_genomes)
    plot_depth_breadth_analysis()
    plot_endogenous_reads()
    print_info(f"Finished generating comparison plots")

def main():
    """
    Main function to parse arguments and run the comparison plot generation.
    """
    species_generate_comparison_plots()

if __name__ == "__main__":
    main()
