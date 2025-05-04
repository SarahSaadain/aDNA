import os
from common_aDNA_scripts import *

# This function runs an R script that generates comparison plots
# showing the number of reads before and after processing for each species.
def plot_comparison_reads_processing_results():
    # Build the path to the folder where R scripts for species comparisons are stored.
    scripts_base_folder = os.path.join(FOLDER_ADDITIONAL_ANALYSIS, FOLDER_SPECIES_COMPARISON)

    print_info(f"Plotting reads before and after comparison")

    # Define the root folder of the aDNA project and the output folder for plots.
    adna_project_folder_path = PATH_ADNA_PROJECT
    output_folder_path_for_plot = get_folder_path_results_plots()

    # Construct the full path to the specific R script to be used for this plot.
    r_script = get_r_script(R_SCRIPT_PLOT_COMPARE_SPECIES_READS_BEFORE_AFTER_PROCESSING, scripts_base_folder)

    # Call the R script with the required arguments (project root, config, output folder).
    call_r_script(r_script, adna_project_folder_path, config_file_path, output_folder_path_for_plot)

    print_info(f"Finished reads before and after comparison")

# This function runs an R script to generate plots comparing sequencing depth and breadth
# across multiple species as defined in the configuration.
def plot_comparison_depth_breadth_analysis():
    # Build the base folder path for R scripts related to comparisons.
    scripts_base_folder = os.path.join(FOLDER_ADDITIONAL_ANALYSIS, FOLDER_SPECIES_COMPARISON)

    print_info(f"Plotting depth and breadth comparison.")

    # Define root and output folders.
    adna_project_folder_path = PATH_ADNA_PROJECT
    output_folder_path_for_plot = get_folder_path_results_plots()

    # Get the R script that performs depth/breadth comparison.
    r_script = get_r_script(R_SCRIPT_PLOT_COMPARE_SPECIES_DEPTH_BREADTH, scripts_base_folder)

    # Execute the R script.
    call_r_script(r_script, adna_project_folder_path, config_file_path, output_folder_path_for_plot)

    print_info(f"Finished plotting depth and breadth comparison.")

# This function runs an R script that plots comparisons of endogenous read counts
# (i.e., reads mapped to reference genome) across species.
def plot_comparison_endogenous_reads():
    # Set path to the scripts directory for species comparisons.
    scripts_base_folder = os.path.join(FOLDER_ADDITIONAL_ANALYSIS, FOLDER_SPECIES_COMPARISON)

    print_info(f"Plotting endogenous reads comparison.")

    # Set root and output directories.
    adna_project_folder_path = PATH_ADNA_PROJECT
    output_folder_path_for_plot = get_folder_path_results_plots()

    # Retrieve the R script that compares endogenous reads.
    r_script = get_r_script(R_SCRIPT_PLOT_COMPARE_SPECIES_ENDOGENOUS_READS, scripts_base_folder)

    # Call the R script with required parameters.
    call_r_script(r_script, adna_project_folder_path, config_file_path, output_folder_path_for_plot)

    print_info(f"Finished plotting endogenous reads comparison.")

# Master function that runs all three comparison plot scripts.
def species_generate_comparison_plots():
    print_execution("Generating comparison plots for species based on config")

    # Run plotting functions for each analysis type.
    plot_comparison_reads_processing_results()
    plot_comparison_depth_breadth_analysis()
    plot_comparison_endogenous_reads()

    print_info(f"Finished generating comparison plots")

# Main function entry point.
# This is the function that runs if the script is executed directly.
def main():
    """
    Main function to parse arguments and run the comparison plot generation.
    """
    species_generate_comparison_plots()

# Ensures the script only runs when executed directly (not when imported as a module).
if __name__ == "__main__":
    main()
