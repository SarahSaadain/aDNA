import os
from common_aDNA_scripts import *


def execute_fastp_quality_filter(input_file_path:str, output_file_path:str, threads:int = THREADS_DEFAULT):
    print_info(f"Filtering {input_file_path} ...")

    if not os.path.exists(input_file_path):
        raise Exception(f"Read file {input_file_path} does not exist!")
    
    if os.path.exists(output_file_path):
        print_info(f"Output file {output_file_path} already exists! Skipping!")
        return
    
    filepath_failed_reads    = output_file_path.replace(FILE_ENDING_QUALITY_FILTERED_FASTQ_GZ, "_failed.fastq.gz")
    filepath_json_report = output_file_path.replace(FILE_ENDING_QUALITY_FILTERED_FASTQ_GZ, "_report.json")
    filepath_html_report = output_file_path.replace(FILE_ENDING_QUALITY_FILTERED_FASTQ_GZ, "_report.html")

    #https://github.com/OpenGene/fastp/blob/59cc2f67414e74e99d42774e227b192a3d9bb63a/README.md#all-options
    command_fastp = [
        PROGRAM_PATH_FASTP, 
        "--thread", str(THREADS_DEFAULT),                    # Number of threads
        "--disable_adapter_trimming",
        "--qualified_quality_phred", "15",      #the quality value that a base is qualified. Default 15 means phred quality >=Q15 is qualified.
        "--length_required" , "15",             #reads shorter than length_required will be discarded, default is 15. (int [=15])
        "--unqualified_percent_limit","40",     #how many percents of bases are allowed to be unqualified (0~100). Default 40 means 40% 
        "--n_base_limit", "5",                  #if one read's number of N base is >n_base_limit, then this read/pair is discarded. Default is 5 (int [=5])
        "--in1", input_file_path,               # Input R1 file
        "--out1", output_file_path,
        "--failed_out", filepath_failed_reads,
        "--json", filepath_json_report,
        "--html", filepath_html_report
    ]
    
    try:
        subprocess.run(command_fastp, check=True)
        print_success(f"fastp quality filter for {input_file_path} complete")
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to run fastp_quality_filter for {input_file_path}: {e}")


def fastp_quality_filter_for_species(species: str):

    print_info(f"Running fastp quality filter for {species}")

    reads_folder = get_folder_path_species_processed_adapter_removed(species)
    output_folder = get_folder_path_species_processed_quality_filtered(species)

    reads_files_list = get_files_in_folder_matching_pattern(reads_folder, f"*{FILE_ENDING_ADAPTER_REMOVED_FASTQ_GZ}")
    
    for read_file_path in reads_files_list:
        output_file_path = get_quality_filtered_path_for_adapter_removed_reads(species, read_file_path)
        execute_fastp_quality_filter(read_file_path, output_file_path)

    print_info(f"fastp quality filter for {species} complete")

def get_quality_filtered_path_for_adapter_removed_reads(species: str, adapter_removed_file_path: str) -> str:
    output_file = os.path.basename(adapter_removed_file_path).replace(FILE_ENDING_ADAPTER_REMOVED_FASTQ_GZ, FILE_ENDING_QUALITY_FILTERED_FASTQ_GZ)
    return os.path.join(get_folder_path_species_processed_quality_filtered(species), output_file)

def all_species_fastp_quality_filter():

    print("Running fastp quality filter for all species")

    for species in FOLDER_SPECIES: 
        fastp_quality_filter_for_species(species)

    print_info("fastp quality filter for all species complete")

def main():
    all_species_fastp_quality_filter()

if __name__ == "__main__":
    main()
