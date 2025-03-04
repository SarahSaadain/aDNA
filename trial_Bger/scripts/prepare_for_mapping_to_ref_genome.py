import os
import shutil
import subprocess
import sys
import csv

sys.path.insert(0, '../../scripts')
from common_aDNA_scripts import *

def prepare():
    print_info("Preparing Bger for ref genome mapping")

    # find all raw fastq files
    duplicates_removed_folder = get_folder_path_species_processed_duplicates_removed(FOLDER_TRIAL_BGER)
    fastq_files = get_files_in_folder_matching_pattern(duplicates_removed_folder, f"*{FILE_ENDING_DUPLICATES_REMOVED_FASTQ_GZ}")

    # if no files are found, exit
    if len(fastq_files) == 0:
        print_error("No duplicate removed fastq files found. Exiting.")
        return
    
    print_info(f"Found {len(fastq_files)} fastq files")

    output_folder = get_folder_path_species_processed_prepared_for_ref_genome(FOLDER_TRIAL_BGER)
    output_file_path = os.path.join(output_folder, f"Mmus_combined{FILE_ENDING_FASTQ_GZ}")

    if os.path.exists(output_file_path):
        print_info(f"Output file {output_file_path} already exists. Skipping.")
        return

    input_pattern_path = os.path.join(duplicates_removed_folder, f"*{FILE_ENDING_DUPLICATES_REMOVED_FASTQ_GZ}")

    # call cat via subprocess
    try:
        print_info(f"Concatenating {len(fastq_files)} fastq files for pattern {input_pattern_path}")
        cat_command = f"cat {input_pattern_path} > {output_file_path}"
        subprocess.run(cat_command, shell=True, check=True)
        print_success(f"Concatenation for pattern {input_pattern_path} complete")
    except Exception as e:
        print_error(f"Failed to concatenate fastq files for pattern {input_pattern_path}: {e}")