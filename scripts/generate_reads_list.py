import subprocess
import os
import argparse
from common_aDNA_scripts import *

# Use find to get a list of all R1 and R2 files in the given folder
R1_FILE_PATTERN = "*_R1*.fastq.gz"
R2_FILE_PATTERN = "*_R2*.fastq.gz"
EXCLUDE_PATTERN = "*/undetermined/*"
READS_LIST_FILENAME = "reads_list.csv"

def generate_paired_reads_list(folder_path: str, output_file: str, overwrite: bool = False) -> None:
    """
    Generate a list of read files from a given folder path, sorted by sample ID.

    Args:
        folder_path (str): The path to the folder containing the read files.
        output_file (str): The path to the output file.
        overwrite (bool, optional): Whether to overwrite the output file if it already exists. Defaults to False.
    """
    if os.path.exists(output_file) and not overwrite:
        print(f"Skipping generation because {output_file} already exists.")
        return

    find_command = f'find {folder_path} -type f \\( -name "{R1_FILE_PATTERN}" -o -name "{R2_FILE_PATTERN}" \\) ! -path "{EXCLUDE_PATTERN}"'
    
    # Sort the list of files by sample ID
    sort_command = 'sort'
    
    # Use awk to format the list of files as a comma-separated list
    awk_command = 'awk \'NR%2{printf "%s,", $0} NR%2==0{print $0}\''
    
    # Combine the commands into a single command string
    full_command = f'{find_command} | {sort_command} | {awk_command}'
    
    # Run the command
    try:
        print_info(f"Running command: {full_command}")
        subprocess.run(full_command, shell=True, stdout=open(output_file, "w"), check=True)
    except subprocess.CalledProcessError as e:
        print_error(f"An error occurred while running the command: {e}")
        return

def main() -> None:
    """
    Generate a list of read files for all species in the given folder.
    """
    parser = argparse.ArgumentParser(description='Generate a list of read files for all species.')
    parser.add_argument('--overwrite', action='store_true', default=False, help='Whether to overwrite the output file if it already exists.')
    args = parser.parse_args()

    all_species_generate_reads_lists(args.overwrite)

def generate_reads_list_for_species(species: str, overwrite: bool = False) -> None:
    """
    Generate a list of read files for a given species.

    Args:
        folder (str): The path to the folder containing the read files.
        species (str): The name of the species.
        overwrite (bool, optional): Whether to overwrite the output file if it already exists. Defaults to False.
    """

    print(f"Generating reads list for species {species}")

    reads_list_file = os.path.join(get_folder_path_species_raw_reads(species), READS_LIST_FILENAME)
    generate_paired_reads_list(get_folder_path_species_raw_reads(species), reads_list_file, overwrite)

def all_species_generate_reads_lists(overwrite: bool = False) -> None:
    """
    Generate a list of read files for all species in the given folder.

    Args:
        folder (str): The path to the folder containing the read files.
        overwrite (bool, optional): Whether to overwrite the output file if it already exists. Defaults to False.
    """

    print("Generating reads list for all species")

    for species in FOLDER_SPECIES:
        generate_reads_list_for_species(species, overwrite)

if __name__ == "__main__":  
    main()
