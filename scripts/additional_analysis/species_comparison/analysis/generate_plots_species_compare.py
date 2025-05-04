import os
from common_aDNA_scripts import *

def plot_comparison_reads_processing_results():
    scripts_base_folder = os.path.join(FOLDER_ADDITIONAL_ANALYSIS, FOLDER_SPECIES_COMPARISON)

    print_info(f"Plotting reads before and after comparison")
    root_folder_path = PATH_ADNA_PROJECT
    output_folder_path = get_folder_path_results_plots()

    r_script = get_r_script(R_SCRIPT_PLOT_COMPARE_SPECIES_READS_BEFORE_AFTER_PROCESSING, scripts_base_folder)

    call_r_script(r_script, root_folder_path, config_file_path, output_folder_path)
    print_info(f"Finished reads before and after comparison")

def plot_comparison_depth_breadth_analysis():
    scripts_base_folder = os.path.join(FOLDER_ADDITIONAL_ANALYSIS, FOLDER_SPECIES_COMPARISON)
    
    print_info(f"Plotting depth and breadth comparison.")
    root_folder_path = PATH_ADNA_PROJECT
    output_folder_path = get_folder_path_results_plots()

    r_script = get_r_script(R_SCRIPT_PLOT_COMPARE_SPECIES_DEPTH_BREADTH, scripts_base_folder)
    # Pass the reference genomes to the R script.
    call_r_script(r_script, root_folder_path, config_file_path, output_folder_path)
    print_info(f"Finished plotting depth and breadth comparison.")

def plot_comparison_endogenous_reads():
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

    plot_comparison_reads_processing_results()
    plot_comparison_depth_breadth_analysis()
    plot_comparison_endogenous_reads()
    print_info(f"Finished generating comparison plots")

def main():
    """
    Main function to parse arguments and run the comparison plot generation.
    """
    species_generate_comparison_plots()

if __name__ == "__main__":
    main()
