import os
import subprocess
import re

from common_aDNA_scripts import *

R1_ADAPTER_SEQUENCE = "AGATCGGAAGAGCACACGTCTGAACTCCAGTCA"
R2_ADAPTER_SEQUENCE = "AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT"

CUTADAPT_THREADS = 20

def remove_adapters(input_file_path_r1, input_file_path_r2, output_file_path_r1, output_file_path_r2, adapter_sequence_r1:str = R1_ADAPTER_SEQUENCE, adapter_sequence_r2:str = R2_ADAPTER_SEQUENCE, threads:int = CUTADAPT_THREADS):

    print_info(f"Removing adapters from {input_file_path_r1} and {input_file_path_r2} ...")

    if not os.path.exists(input_file_path_r1):
        raise Exception(f"Read file {input_file_path_r1[0]} does not exist!")

    if not os.path.exists(input_file_path_r2):
        raise Exception(f"Read file {input_file_path_r2} does not exist!")
    
    if os.path.exists(output_file_path_r1):
        print_info(f"Output file {output_file_path_r1} already exists! Skipping!")
        return

    if os.path.exists(output_file_path_r2):
        print_info(f"Output file {output_file_path_r2} already exists! Skipping!")
        return

    command_remove_adapters = [
        PROGRAM_PATH_CUTADAPT,
        "-j", str(threads),      # Number of threads
        "-a", adapter_sequence_r1,  # Adapter for R1
        "-g", adapter_sequence_r2,  # Adapter for R2
        "-e", "0.1",             # Error rate
        "-O", "3",               # Minimum overlap
        "-m", "15",               # Minimum length after trimming
        "-q", "5",               # Quality trimming
        "--poly-a",                 # Remove poly-A
        "-o", output_file_path_r1,  # Output file for R1
        "-p", output_file_path_r2,  # Output file for R2
        input_file_path_r1,        # Input R1 file
        input_file_path_r2         # Input R2 file
    ]
    
    try:
        subprocess.run(command_remove_adapters, check=True)
        print_success(f"Adapters removed from {input_file_path_r1} and {input_file_path_r2}.")
    except subprocess.CalledProcessError as e:
        raise Exception(f"Removed adapters error for {input_file_path_r1} and {input_file_path_r2} : {e}")

def all_species_adapter_remove():

    print("Running adaper removal for all species")
    
    for species in FOLDER_SPECIES:
        adapter_remove_for_species(species)

def adapter_remove_for_species(species):
    print_info(f"Running adapter removal for species {species}")

    try:
        list_of_read_files = get_raw_paired_reads_list_of_species(species)

        if len(list_of_read_files) == 0:
            print_warning(f"No reads found for species {species}.")
            return

        for read_file_path in list_of_read_files:
            
            filename_new_R1 = rename_read_file_to_adapter_trimmed(os.path.basename(read_file_path[0]))
            filename_new_R2 = rename_read_file_to_adapter_trimmed(os.path.basename(read_file_path[1]))

            adapter_removed_read_file_R1 = os.path.join(get_folder_path_species_processed_adapter_removed(species), filename_new_R1)
            adapter_removed_read_file_R2 = os.path.join(get_folder_path_species_processed_adapter_removed(species), filename_new_R2)

            remove_adapters(read_file_path[0], read_file_path[1], adapter_removed_read_file_R1, adapter_removed_read_file_R2)
        
    except Exception as e:
        print_error(e)

def rename_read_file_to_adapter_trimmed(read_file_path):
    filename_new = os.path.basename(read_file_path).replace(".fastq.gz", "_trimmed.fastq.gz")
    return filename_new


def main():

    all_species_adapter_remove()

if __name__ == "__main__":
    main()