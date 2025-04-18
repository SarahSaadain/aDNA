import argparse

from common_aDNA_scripts import *

def plot_reads_processing_result(species: list):

    scripts_base_folder = os.path.join(FOLDER_ADDITIONAL_ANALYSIS, FOLDER_SPECIES_COMPARISON)

    species_string = ",".join(species)
    print_info(f"Plotting reads before and after comparison for species {species_string}")
    root_folder_path = PATH_ADNA_PROJECT
    output_folder_path = get_folder_path_results_plots()

    if len(get_files_in_folder_matching_pattern(output_folder_path, f"*{'_'.join(species)}.png")) > 0:
        print_info(f"Plots already exist for species {species_string}. Skipping plot generation.")
        return

    r_script = get_r_script(R_SCRIPT_PLOT_COMPARE_SPECIES_READS_BEFORE_AFTER_PROCESSING, scripts_base_folder)
    call_r_script(r_script, root_folder_path, species_string,  output_folder_path)
    print_info(f"Finished reads before and after comparison for species {species_string}")

def plot_depth_breadth_analysis(species: list):

    scripts_base_folder = os.path.join(FOLDER_ADDITIONAL_ANALYSIS, FOLDER_SPECIES_COMPARISON)

    species_string = ",".join(species)
    print_info(f"Plotting depth and breadth comparison for species {species_string}")
    root_folder_path = PATH_ADNA_PROJECT
    output_folder_path = get_folder_path_results_plots()

    if len(get_files_in_folder_matching_pattern(output_folder_path, f"*{'_'.join(species)}.png")) > 0:
        print_info(f"Plots already exist for species {species_string}. Skipping plot generation.")
        return

    r_script = get_r_script(R_SCRIPT_PLOT_COMPARE_SPECIES_DEPTH_BREADTH, scripts_base_folder)
    call_r_script(r_script, root_folder_path, species_string, output_folder_path)
    print_info(f"Finished plotting depth and breadth comparison for species {species_string}")

def plot_endogenous_reads(species: list):
 
    scripts_base_folder = os.path.join(FOLDER_ADDITIONAL_ANALYSIS, FOLDER_SPECIES_COMPARISON)

    species_string = ",".join(species)
    print_info(f"Plotting endogenous reads comparison for species {species_string}")
    root_folder_path = PATH_ADNA_PROJECT
    output_folder_path = get_folder_path_results_plots()

    if len(get_files_in_folder_matching_pattern(output_folder_path, f"*{'_'.join(species)}.png")) > 0:
        print_info(f"Plots already exist for species {species_string}. Skipping plot generation.")
        return

    r_script = get_r_script(R_SCRIPT_PLOT_COMPARE_SPECIES_ENDOGENOUS_READS, scripts_base_folder)
    call_r_script(r_script, root_folder_path, species_string, output_folder_path)
    print_info(f"Finished plotting endogenous reads comparison for species {species_string}")

def species_generate_comparison_plots(species: list):
    
    plot_reads_processing_result(species)
    plot_depth_breadth_analysis(species)
    plot_endogenous_reads(species)
    print_info(f"Finished generating plots for species {species}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate comparison plots for specified species.")
    parser.add_argument("species", nargs="+", help="List of species to compare (separated by comma).")
    args = parser.parse_args()

    species_list = args.species
    species_generate_comparison_plots(species_list)