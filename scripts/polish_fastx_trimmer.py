import os
from common_aDNA_scripts import *

def execute_fastx_trimmer(input_file_path:str, output_file_path:str):
    print_info(f"Trimming {input_file_path} ...")

    if not os.path.exists(input_file_path):
        raise Exception(f"Read file {input_file_path} does not exist!")

    if os.path.exists(output_file_path):
        print_info(f"Output file {output_file_path} already exists! Skipping!")
        return
    # https://manpages.debian.org/wheezy/fastx-toolkit/fastx_trimmer.1.en.html
    command_fastx_trimmer = [
        PROGRAM_PATH_FASTX_TRIMMER,
        "-i", input_file_path,
        "-o", output_file_path,
        "-l", "20"
    ]

    try:
        subprocess.run(command_fastx_trimmer, check=True)
    except Exception as e:
        print_error(f"Failed to run fastx_trimmer for {input_file_path}: {e}")

def fastx_trimmer(species):
    print_info(f"Running fastx_trimmer for species {species}")

    try:
        reads_folder = get_folder_path_species_processed_duplicates_removed(species)
        list_of_read_files = get_files_in_folder_matching_pattern(reads_folder, f"*{FILE_ENDING_DUPLICATES_REMOVED_FASTQ_GZ}")

        for read_file_path in list_of_read_files:
            output_file = os.path.basename(read_file_path).replace(FILE_ENDING_DUPLICATES_REMOVED_FASTQ_GZ, "fastx_trimmed.fastq.gz")
            #output_file_path = os.path.join(get_folder_path_species_processed_fastx_trimmed(species), output_file)
            #execute_fastx_trimmer(read_file_path, output_file_path)

    except Exception as e:
        print_error(e)

def all_species_fastx_trimmer():
    for species in FOLDER_SPECIES: 
        fastx_trimmer(species)

def main():
    all_species_fastx_trimmer()

if __name__ == "__main__":
    main()
