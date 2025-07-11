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
        # - gunzip -c: uncompress the files and write to output 
        # Example:
        # gunzip -c file1 file2 file3 > output_file

        command = f"cat {file_string} > {output_file_path}"
        subprocess.run(command, shell=True, check=True)
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
    prepared_for_ref_genome_folder = get_folder_path_species_processed_prepared_for_ref_genome(species)
    list_of_read_files = get_files_in_folder_matching_pattern(prepared_for_ref_genome_folder, "C[1-3].fastq.gz")

    # Create the output file name
    output_file_path = os.path.join(get_folder_path_species_processed_genomedelta(species), f"{species}_combined_all_reads.fastq.gz")

    if len(list_of_read_files) == 0:
        print_warning(f"No reads found for species {species}. Skipping.")
        return

    # Combine the files
    combine_fastq_files(list_of_read_files, output_file_path)

    print_info(f"Reads prepared for species {species}")


def main():
    all_species_prepare_reads_for_GD()


if __name__ == "__main__":
    main()
