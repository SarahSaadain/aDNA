import os
from common_aDNA_scripts import *


def execute_fastx_quality_filter(input_file_path:str, output_file_path:str):
    print_info(f"Filtering {input_file_path} ...")

    if not os.path.exists(input_file_path):
        raise Exception(f"Read file {input_file_path} does not exist!")
    
    if os.path.exists(output_file_path):
        print_info(f"Output file {output_file_path} already exists! Skipping!")
        return
    
    output_file_path_failed = output_file_path.replace(FILE_ENDING_QUALITY_FILTERED_FASTQ_GZ, "_failed.fastq.gz")

    #https://github.com/OpenGene/fastp/blob/59cc2f67414e74e99d42774e227b192a3d9bb63a/README.md#all-options
    command_fastp = [
        PROGRAM_PATH_FASTP, 
        "--disable_adapter_trimming",
        "--disable_length_filtering",
        "--thread", str(10),               # Number of threads
        "--length_required" , "15",             #reads shorter than length_required will be discarded, default is 15. (int [=15])
        "--qualified_quality_phred", "5",
        "--unqualified_percent_limit", "25",
        "--n_base_limit", "5",                  #if one read's number of N base is >n_base_limit, then this read/pair is discarded. Default is 5 (int [=5])
        "--in1", input_file_path,               # Input R1 file
        "--out1", output_file_path,
        "--failed_out", output_file_path_failed
    ]
    
    try:
        subprocess.run(command_fastp, check=True)
        print_success(f"fastp quality filter for {input_file_path} complete")
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to run fastx_quality_filter for {input_file_path}: {e}")

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
        print_success(f"Fastx_quality_filter for {input_file_path} complete")
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
