import os
import subprocess
import re

from common_aDNA_scripts import *

R1_ADAPTER_SEQUENCE = "AGATCGGAAGAGCACACGTCTGAACTCCAGTCA"
R2_ADAPTER_SEQUENCE = "AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT"

CUTADAPT_THREADS = 20

def remove_adapters_and_merge_paired_reads(input_file_path_r1, input_file_path_r2, output_file_path_r1, adapter_sequence_r1:str = R1_ADAPTER_SEQUENCE, adapter_sequence_r2:str = R2_ADAPTER_SEQUENCE, threads:int = CUTADAPT_THREADS):

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
    command_remove_adapters = [
        PROGRAM_PATH_FASTP,
        "--thread", str(threads),      # Number of threads
        "--adapter_sequence", adapter_sequence_r1,  # Adapter for R1
        "--adapter_sequence_r2", adapter_sequence_r2,  # Adapter for R2
        "--out1", filepath_merge_failed_passed_r1,
        "--out2", filepath_merge_failed_passed_r2,
        "--unpaired1", filepath_merge_failed_not_passed_r1,
        "--unpaired2", filepath_merge_failed_not_passed_r2,
        "--merge",
        "--qualified_quality_phred", "15",      #the quality value that a base is qualified. Default 15 means phred quality >=Q15 is qualified.
        "--unqualified_percent_limit","40",     #how many percents of bases are allowed to be unqualified (0~100). Default 40 means 40% 
        "--length_required" , "15",             #reads shorter than length_required will be discarded, default is 15. (int [=15])
        "--trim_poly_x", "5",
        "--json", filepath_merge_json_report,
        "--html", filepath_merge_html_report,
        "--merged_out", output_file_path_r1,  # Output file for R1
        "--in1", input_file_path_r1,        # Input R1 file
        "--in2", input_file_path_r2         # Input R2 file
    ]
    
    try:
        subprocess.run(command_remove_adapters, check=True)
        print_success(f"Adapters removed from {input_file_path_r1} and {input_file_path_r2}.")
    except subprocess.CalledProcessError as e:
        raise Exception(f"Removed adapters error for {input_file_path_r1} and {input_file_path_r2} : {e}")

def all_species_adapter_remove():

    print("Running adaper removal for all species")
    
    for species in FOLDER_SPECIES:
        adapter_remove_for_species(species)

def adapter_remove_for_species(species):
    print_info(f"Running adapter removal for species {species}")

    try:
        list_of_read_files = get_raw_paired_reads_list_of_species(species)

        if len(list_of_read_files) == 0:
            print_warning(f"No reads found for species {species}.")
            return

        for read_file_path in list_of_read_files:
            
            filename_merged = rename_read_file_to_adapter_trimmed(os.path.basename(read_file_path[0]))

            adapter_removed_read_file = os.path.join(get_folder_path_species_processed_adapter_removed(species), filename_merged)
            
            remove_adapters_and_merge_paired_reads(read_file_path[0], read_file_path[1], adapter_removed_read_file)
        
    except Exception as e:
        print_error(e)

def rename_read_file_to_adapter_trimmed(read_file_path):
    filename_new = os.path.basename(read_file_path).replace("_R1_","_").replace("_R2_","_").replace(".fastq.gz", "_merged_trimmed.fastq.gz")
    return filename_new


def main():

    all_species_adapter_remove()

if __name__ == "__main__":
    main()