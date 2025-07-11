import os
from common_aDNA_scripts import *

def execute_sga_filter(input_file_path:str, output_file_path:str, threads:int = 20):
    print_info(f"Filtering {input_file_path} ...")

    if not os.path.exists(input_file_path):
        raise Exception(f"Read file {input_file_path} does not exist!")
    
    if os.path.exists(output_file_path):
        print_info(f"Output file {output_file_path} already exists! Skipping!")
        return

    command_sga_filter = [
        PROGRAM_PATH_SGA,
        "filter",
        "--no-kmer-check",
        "-t", str(threads),
        "-o", output_file_path,
        input_file_path
    ]

    try:
        subprocess.run(command_sga_filter, check=True)
    except Exception as e:
        print_error(f"Failed to run sga filter for {input_file_path}: {e}")

def execute_sga_index(input_file_path:str, threads:int = 20):
    print_info(f"Indexing {input_file_path} ...")

    if not os.path.exists(input_file_path):
        raise Exception(f"Read file {input_file_path} does not exist!")
    
    #TODO: check if index file already exists
    if os.path.exists(input_file_path + ".index"):
        print_info(f"Index file {input_file_path}.index already exists! Skipping!")
        return

    command_sga_index = [
        PROGRAM_PATH_SGA,
        "index",
        "--algorithm", "ropebwt",
        "--threads", str(threads),
        input_file_path
    ]

    try:
        subprocess.run(command_sga_index, check=True)
    except Exception as e:
        print_error(f"Failed to run sga index for {input_file_path}: {e}")

def polish_sga_for_species(species):
    print_info(f"Running sga for species {species}")
    try:
        reads_folder = get_folder_path_species_processed_quality_filtered(species)
        list_of_read_files = get_files_in_folder_matching_pattern(reads_folder, f"*{FILE_ENDING_QUALITY_FILTERED_FASTQ_GZ}")

        if len(list_of_read_files) == 0:
            print_warning(f"No quality filtered reads found for species {species}. Skipping.")
            return

        output_folder = get_folder_path_species_processed_duplicates_removed(species)

        for read_file_path in list_of_read_files:
            execute_sga_index(read_file_path)

            output_file = os.path.basename(read_file_path).replace(FILE_ENDING_QUALITY_FILTERED_FASTQ_GZ, FILE_ENDING_DUPLICATES_REMOVED_FASTQ_GZ)
            output_file_path = os.path.join(output_folder, output_file)

            execute_sga_filter(read_file_path, output_file_path)
    except Exception as e:
        print_error(e)
    

def all_species_polish_sga():
    for species in FOLDER_SPECIES: 
        polish_sga_for_species(species)

def main():
    all_species_polish_sga()

if __name__ == "__main__":
    main()
