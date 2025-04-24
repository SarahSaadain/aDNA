import os
from common_aDNA_scripts import *


def execute_fastp_deduplication(input_file_path:str, output_file_path:str, threads:int = THREADS_DEFAULT):
    print_info(f"Filtering {input_file_path} ...")

    if not os.path.exists(input_file_path):
        raise Exception(f"Read file {input_file_path} does not exist!")
    
    if os.path.exists(output_file_path):
        print_info(f"Output file {output_file_path} already exists! Skipping!")
        return
    
    filepath_reads_failed = output_file_path.replace(FILE_ENDING_DUPLICATES_REMOVED_FASTQ_GZ, "_failed.fastq.gz")
    filepath_json_report = output_file_path.replace(FILE_ENDING_DUPLICATES_REMOVED_FASTQ_GZ, "_report.json")
    filepath_html_report = output_file_path.replace(FILE_ENDING_DUPLICATES_REMOVED_FASTQ_GZ, "_report.html")

    #https://github.com/OpenGene/fastp/blob/59cc2f67414e74e99d42774e227b192a3d9bb63a/README.md#all-options
    command_fastp = [
        PROGRAM_PATH_FASTP, 
        "--dedup",                              #enable deduplication to drop the duplicated reads/pairs
        "--disable_adapter_trimming",
        "--disable_length_filtering",
        "--disable_quality_filtering",
        "--thread", str(threads),                    # Number of threads
        "--in1", input_file_path,               # Input R1 file
        "--out1", output_file_path,
        "--failed_out", filepath_reads_failed,
        "--json", filepath_json_report,
        "--html", filepath_html_report
    ]

    print_debug(f"Executing command: {' '.join(command_fastp)}")
    
    try:
        subprocess.run(command_fastp, check=True)
        print_success(f"fastp deduplication for {input_file_path} complete")
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to run fastp deduplication for {input_file_path}: {e}")


def fastp_deduplication_for_species(species: str):

    print_info(f"Running fastp deduplication for {species}")

    reads_folder = get_folder_path_species_processed_quality_filtered(species)

    reads_files_list = get_files_in_folder_matching_pattern(reads_folder, f"*{FILE_ENDING_QUALITY_FILTERED_FASTQ_GZ}")

    if len(reads_files_list) == 0:
        print_warning(f"No quality filtered reads found for species {species}. Skipping.")
        return
    
    print_debug(f"Found {len(reads_files_list)} quality filtered reads for species {species}.")
    print_debug(f"Quality filtered reads: {reads_files_list}")
    
    for read_file_path in reads_files_list:
        output_file_path = get_deduplication_path_for_quality_filtered_reads(species, read_file_path)
        execute_fastp_deduplication(read_file_path, output_file_path)

    print_info(f"fastp deduplication for {species} complete")

def get_deduplication_path_for_quality_filtered_reads(species: str, quality_filtered_file_path: str) -> str:
    output_file = os.path.basename(quality_filtered_file_path).replace(FILE_ENDING_QUALITY_FILTERED_FASTQ_GZ, FILE_ENDING_DUPLICATES_REMOVED_FASTQ_GZ)
    return os.path.join(get_folder_path_species_processed_duplicates_removed(species), output_file)

def all_species_fastp_deduplication():
    print_execution("Running fastp deduplication for all species")

    for species in FOLDER_SPECIES: 
        fastp_deduplication_for_species(species)

    print_info("fastp deduplication for all species complete")

def main():
    all_species_fastp_deduplication()

if __name__ == "__main__":
    main()
