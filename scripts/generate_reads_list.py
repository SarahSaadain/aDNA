import subprocess
import os
import argparse

# Use find to get a list of all R1 and R2 files in the given folder
R1_FILE_PATTERN = "*_R1_*.fastq.gz"
R2_FILE_PATTERN = "*_R2_*.fastq.gz"
EXCLUDE_PATTERN = "*/undetermined/*"

def generate_reads_list(folder_path: str, output_file: str, overwrite: bool = False) -> None:
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
    full_command = f'{find_command} | {sort_command} | {awk_command} > {output_file}'
    
    # Run the command
    try:
        subprocess.run(full_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the command: {e}")




def main() -> None:
    """
    Generate a list of read files for all species in the given folder.
    """
    parser = argparse.ArgumentParser(description='Generate a list of read files for all species in the given folder.')
    parser.add_argument('--folder', type=str, required=True, help='The path to the folder containing the read files.')
    parser.add_argument('--overwrite', action='store_true', default=False, help='Whether to overwrite the output file if it already exists.')
    args = parser.parse_args()

    all_species_generate_reads_lists(args.folder, args.overwrite)

def generate_reads_list_for_species(folder: str, species: str, overwrite: bool = False) -> None:
    """
    Generate a list of read files for a given species.

    Args:
        folder (str): The path to the folder containing the read files.
        species (str): The name of the species.
        overwrite (bool, optional): Whether to overwrite the output file if it already exists. Defaults to False.
    """
    reads_list_file = f"{folder}/{species}/reads_list.txt"
    generate_reads_list(f"{folder}/{species}", reads_list_file, overwrite)

def all_species_generate_reads_lists(folder: str, overwrite: bool = False) -> None:
    """
    Generate a list of read files for all species in the given folder.

    Args:
        folder (str): The path to the folder containing the read files.
        overwrite (bool, optional): Whether to overwrite the output file if it already exists. Defaults to False.
    """
    for species in os.listdir(folder):
        generate_reads_list_for_species(folder, species, overwrite)

if __name__ == "__main__":  
    main()
