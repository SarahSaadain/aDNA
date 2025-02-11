import os
from common_aDNA_scripts import *


def execute_fastx_quality_filter(input_file_path:str, output_file_path:str):
    print_info(f"Filtering {input_file_path} ...")

    if not os.path.exists(input_file_path):
        raise Exception(f"Read file {input_file_path} does not exist!")
    
    if os.path.exists(output_file_path):
        print_info(f"Output file {output_file_path} already exists! Skipping!")
        return
    
    #https://manpages.debian.org/wheezy/fastx-toolkit/fastq_quality_filter.1.en.html
    command_fastx_quality_filter = [
        PROGRAM_PATH_FASTX_QUALITY_FILTER,
        "-i", input_file_path,
        "-", output_file_path,
        "-q", "30",
        "-p", "75"
    ]
    try:
        subprocess.run(command_fastx_quality_filter, check=True)
    except Exception as e:
        print_error(f"Failed to run fastx_quality_filter for {input_file_path}: {e}")

def fastx_quality_filter_for_species(species):
    reads_folder = get_folder_path_species_processed_adapter_removed(species)
    output_folder = get_folder_path_species_processed_quality_filtered(species)

    reads_files_list = get_files_in_folder_matching_pattern(reads_folder, f"*{FILE_ENDING_ADAPTER_REMOVED_FASTQ_GZ}")
    
    for read_file_path in reads_files_list:
        output_file = os.path.basename(read_file_path).replace(FILE_ENDING_ADAPTER_REMOVED_FASTQ_GZ, FILE_ENDING_QUALITY_FILTERED_FASTQ_GZ)
        output_file_path = os.path.join(output_folder, output_file)
        execute_fastx_quality_filter(read_file_path, output_file_path)

def all_species_fastx_quality_filter():
    for species in FOLDER_SPECIES: 
        fastx_quality_filter_for_species(species)

def main():
    all_species_fastx_quality_filter()

if __name__ == "__main__":
    main()
