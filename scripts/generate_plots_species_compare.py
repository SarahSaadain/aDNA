import os
import subprocess
import argparse

from common_aDNA_scripts import *
import generate_plots as generate_plots

def plot_reads_processing_result(species):
    species_string = ",".join(species)
    print_info(f"Plotting reads before and after comparison for species {species_string}")
    root_folder_path = PATH_ADNA_PROJECT
    output_folder_path = get_folder_path_results_plots()
    r_script = get_r_script(R_SCRIPT_PLOT_COMPARE_SPECIES_READS_BEFORE_AFTER_PROCESSING)
    generate_plots.call_r_script(r_script, root_folder_path, species_string,  output_folder_path)
    print_info(f"Finished reads before and after comparison for species {species_string}")

def plot_depth_breadth_analysis(species: list):
    species_string = ",".join(species)
    print_info(f"Plotting depth and breadth comparison for species {species_string}")
    root_folder_path = PATH_ADNA_PROJECT
    output_folder_path = get_folder_path_results_plots()
    r_script = get_r_script(R_SCRIPT_PLOT_COMPARE_SPECIES_DEPTH_BREADTH)
    generate_plots.call_r_script(r_script, root_folder_path, species_string, output_folder_path)
    print_info(f"Finished plotting depth and breadth comparison for species {species_string}")

def plot_endogenous_reads(species: list):
    species_string = ",".join(species)
    print_info(f"Plotting endogenous reads comparison for species {species_string}")
    root_folder_path = PATH_ADNA_PROJECT
    output_folder_path = get_folder_path_results_plots()
    r_script = get_r_script(R_SCRIPT_PLOT_COMPARE_SPECIES_ENDOGENOUS_READS)
    generate_plots.call_r_script(r_script, root_folder_path, species_string, output_folder_path)
    print_info(f"Finished plotting endogenous reads comparison for species {species_string}")

def species_generate_comparison_plots(species: list):
    
    plot_reads_processing_result(species)
    plot_depth_breadth_analysis(species)
    plot_endogenous_reads(species)
    print_info(f"Finished generating plots for species {species}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate comparison plots for specified species.")
    parser.add_argument("species", nargs="+", help="List of species to compare.")
    args = parser.parse_args()

    species_list = args.species
    species_generate_comparison_plots(species_list)