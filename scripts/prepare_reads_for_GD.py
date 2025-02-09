"""
Prepare all reads for all species for genome delta.

This script takes all the fastq files for each species and combines them
into a single file. The output file is written to the processed species folder.

The script loops over all species and calls the function
`species_prepare_reads_for_genome_delta` for each one.

"""

import subprocess
import os
from common_aDNA_scripts import *


def combine_fastq_files(file_list: list, output_file_path: str):
    """
    Combine a list of fastq files into a single file.

    This function takes a list of fastq files and combines them
    into a single fastq file. The output file is written to the
    specified file path.

    Args:
        file_list (list): A list of file paths to the fastq files
            to be combined.
        output_file_path (str): The path to the output file.

    Raises:
        subprocess.CalledProcessError: If an error occurs while
            combining the files.
    """

    print_info(f"Combining {len(file_list)} files into {output_file_path}")

    # Check if target file exists
    if os.path.exists(output_file_path):
        print_warning(f"Output file {output_file_path} already exists. Skipping.")
        return
    
    # Print the list of files to be combined
    #print_info("List of files to be combined:")
    #print_info(file_list)

    # Create a string of files separated by spaces
    # (gunzip needs the files to be separated by spaces)
    file_string = ' '.join(file_list)

    try:
        # Run the command
        # explanation of the command:
        # - gunzip -c: uncompress the files and write to stdout. stdout is then piped to the next command
        # - gzip: compress the output of gunzip and write to stdout. stdout is then redirected to the output file from subprocess.run()
        # Example:
        # gunzip -c file1 file2 file3 | gzip

        command = f"gunzip -c {file_string}"
        subprocess.run(command, shell=True, stdout=open(output_file_path, "wb"), check=True)
        print_success(f"Files combined into {output_file_path}")
    except subprocess.CalledProcessError as e:
        print_error(f"An error occurred while combining files: {e}")


def all_species_prepare_reads_for_GD():
    """
    Prepare all reads for all species for genome delta.

    This function loops over all species and calls
    `species_prepare_reads_for_GD` for each one.

    """
    print("Preparing reads for genome delta")

    # Loop over all species
    for species in FOLDER_SPECIES:
        # Prepare the reads for this species
        species_prepare_reads_for_GD(species)


def species_prepare_reads_for_GD(species):
    """
    Prepare all reads for a given species for genome delta.

    This function takes a species as input and combines all reads
    for that species into a single file. The output file is
    written to the processed species folder.

    Args:
        species (str): The name of the species.
    """
    print_info(f"Preparing reads for species {species}")

    # Get the list of read files for this species
    list_of_read_files = get_reads_list_of_species(species)

    # Each entry in the list contains 2 (paired) files, we need to flatten the list to get a list of all files individually
    # because the reads_list contains two files in a row and we need to separate them
    file_list = [item for sublist in list_of_read_files for item in sublist]

    # Create the output file name
    output_file_path = os.path.join(get_folder_path_species_processed(species), f"{species}_combined_all_reads.fastq")

    if len(file_list) == 0:
        print_warning(f"No reads found for species {species}. Skipping.")
        return

    # Combine the files
    combine_fastq_files(file_list, output_file_path)


def main():
    all_species_prepare_reads_for_GD()


if __name__ == "__main__":
    main()
