import os
import subprocess
import re

from common_aDNA_scripts import *

R1_ADAPTER_SEQUENCE = "AGATCGGAAGAGCACACGTCTGAACTCCAGTCA"
R2_ADAPTER_SEQUENCE = "AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT"

def remove_adapters_and_merge(input_file_path_r1, input_file_path_r2, output_file_path_r1, adapter_sequence_r1:str = R1_ADAPTER_SEQUENCE, adapter_sequence_r2:str = R2_ADAPTER_SEQUENCE, threads:int = THREADS_DEFAULT):

    print_info(f"Removing adapters from {input_file_path_r1} and {input_file_path_r2} ...")

    if not os.path.exists(input_file_path_r1):
        raise Exception(f"Read file {input_file_path_r1[0]} does not exist!")

    if not os.path.exists(input_file_path_r2):
        raise Exception(f"Read file {input_file_path_r2} does not exist!")
    
    if os.path.exists(output_file_path_r1):
        print_info(f"Output file {output_file_path_r1} already exists! Skipping!")
        return
    
    filepath_merge_failed_passed_r1 = output_file_path_r1.replace(FILE_ENDING_ADAPTER_REMOVED_FASTQ_GZ, "_merge_failed_passed_r1.fastq.gz")
    filepath_merge_failed_passed_r2 = output_file_path_r1.replace(FILE_ENDING_ADAPTER_REMOVED_FASTQ_GZ, "_merge_failed_passed_r2.fastq.gz")
    filepath_merge_failed_not_passed_r1 = output_file_path_r1.replace(FILE_ENDING_ADAPTER_REMOVED_FASTQ_GZ, "_merge_failed_not_passed_r1.fastq.gz")
    filepath_merge_failed_not_passed_r2 = output_file_path_r1.replace(FILE_ENDING_ADAPTER_REMOVED_FASTQ_GZ, "_merge_failed_not_passed_r2.fastq.gz")
    filepath_merge_json_report = output_file_path_r1.replace(FILE_ENDING_ADAPTER_REMOVED_FASTQ_GZ, "_report.json")
    filepath_merge_html_report = output_file_path_r1.replace(FILE_ENDING_ADAPTER_REMOVED_FASTQ_GZ, "_report.html")

    #https://github.com/OpenGene/fastp/blob/59cc2f67414e74e99d42774e227b192a3d9bb63a/README.md#all-options
    command_fastp = [
        PROGRAM_PATH_FASTP,
        "--adapter_sequence", adapter_sequence_r1,  # Adapter for R1
        "--adapter_sequence_r2", adapter_sequence_r2,  # Adapter for R2
        "--out1", filepath_merge_failed_passed_r1,
        "--out2", filepath_merge_failed_passed_r2,
        "--unpaired1", filepath_merge_failed_not_passed_r1,
        "--unpaired2", filepath_merge_failed_not_passed_r2,
        "--merged_out", output_file_path_r1,  # Output file for R1
        "--in1", input_file_path_r1,        # Input R1 file
        "--in2", input_file_path_r2,         # Input R2 file
        "--json", filepath_merge_json_report,
        "--html", filepath_merge_html_report,
        "--merge",
        "--thread", str(threads),               # Number of threads

        # length filtering options
        "--length_required" , "15",             #reads shorter than length_required will be discarded, default is 15. (int [=15])
        
        # poly
        "--trim_poly_x", "5",

        # quality filtering options
        "--qualified_quality_phred", "5",       #the quality value that a base is qualified. Default 15 means phred quality >=Q15 is qualified. (int [=15])
        "--unqualified_percent_limit", "40",    #how many percents of bases are allowed to be unqualified (0~100). Default 40 means 40% (int [=40])"
        "--n_base_limit", "5"                  #if one read's number of N base is >n_base_limit, then this read/pair is discarded. Default is 5 (int [=5])
       
    ]
    
    try:
        subprocess.run(command_fastp, check=True)
        print_success(f"Adapters removed from {input_file_path_r1} and {input_file_path_r2}.")
    except subprocess.CalledProcessError as e:
        raise Exception(f"Removed adapters error for {input_file_path_r1} and {input_file_path_r2} : {e}")

def all_species_fastp_adapter_remove_and_merge():

    print("Running adaper removal and merge for all species")
    
    for species in FOLDER_SPECIES:
        adapter_remove_and_merge_for_species(species)

def adapter_remove_and_merge_for_species(species):
    print_info(f"Running adapter removal and merge for species {species}")

    try:
        list_of_read_files = get_raw_paired_reads_list_of_species(species)

        if len(list_of_read_files) == 0:
            print_warning(f"No reads found for species {species}.")
            return

        for read_file_path in list_of_read_files:

            adapter_removed_read_file = get_adapter_removed_path_for_paired_raw_reads(species, read_file_path)
          
            remove_adapters_and_merge(read_file_path[0], read_file_path[1], adapter_removed_read_file)
        
    except Exception as e:
        print_error(e)

def get_adapter_removed_path_for_paired_raw_reads(species, paired_read_file_path_list):
    filename_new = os.path.basename(paired_read_file_path_list[0]).replace("_R1_","_").replace("_R2_","_").replace(FILE_ENDING_FASTQ_GZ, FILE_ENDING_ADAPTER_REMOVED_FASTQ_GZ )
    return os.path.join(get_folder_path_species_processed_adapter_removed(species), filename_new)

def main():

    all_species_fastp_adapter_remove_and_merge()

if __name__ == "__main__":
    main()