import os
import subprocess
from common_aDNA_scripts import *

import determine_reads_processing_result as determine_reads_processing_result


if __name__ == "__main__":
    main()

def main():
    all_species_generate_plots()

def all_species_generate_plots():

    print("Generating plots for all species")

    for species in FOLDER_SPECIES:
        species_generate_plots(species)

    print_info("Finished generating plots for all species")

def species_generate_plots(species):
    print_info(f"Generating plots for species {species}")

    plot_reads_processing_result(species)


    print_info(f"Finished generating plots for species {species}")
    

def plot_reads_processing_result(species):

    R_SCRIPT_FUNCTION = "plot_sequence_length_distribution"

    print_info(f"Plotting reads processing result for species {species}") 

    input_file_path = os.path.join(get_folder_path_species_results_qc_reads_processing(species), f"{species}_reads_processing_result{FILE_ENDING_TSV}")

    output_folder_path = get_folder_path_species_results_plots_reads_processing(species)

    r_script = get_r_script(species, R_SCRIPT_PLOT_READS_BEFORE_AFTER_PROCESSING)

    call_r_script(r_script, R_SCRIPT_FUNCTION, input_file_path, output_folder_path)



def call_r_script(script_path, function, *args):
    """
    Calls an R script with optional arguments.
    
    :param script_path: Path to the R script (e.g., "script.R").
    :param args: Additional arguments to pass to the R script.
    :return: None (raises an error if execution fails).
    """

    if not os.path.exists(script_path):
        raise FileNotFoundError(f"R script not found: {script_path}")

    command = ["Rscript", function, script_path] + list(args)
    try:
        subprocess.run(command, check=True)
        print(f"Successfully executed {script_path} with arguments {args}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing {script_path}: {e}")