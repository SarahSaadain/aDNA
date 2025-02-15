import os
import shutil
import subprocess
import sys
import csv

sys.path.insert(0, '../../scripts')
from common_aDNA_scripts import *

def generate_fastq_patterns(file_paths):
    patterns = {}
    
    for path in file_paths:
        # Extract the filename
        filename = os.path.basename(path)
        
        # Extract the prefix (C1, C2, C3)
        prefix = filename.split('_')[0]
        
        # Store the wildcard pattern
        patterns[prefix] = f"{prefix}*{FILE_ENDING_DUPLICATES_REMOVED_FASTQ_GZ}"

        # Extract the prefix (C1_##, C2_##, C3_##...) and remove the last charater with [:-1] so it is C1_S ...
        prefix = f"{filename.split('_')[0]}_{filename.split('_')[1][:-1]}"

        patterns[prefix] = f"{prefix}*{FILE_ENDING_DUPLICATES_REMOVED_FASTQ_GZ}"

    return patterns

def prepare():
    print_info("Preparing Bger for ref genome mapping")

    # find all raw fastq files
    duplicates_removed_folder = get_folder_path_species_processed_duplicates_removed(FOLDER_BGER)
    fastq_files = get_files_in_folder_matching_pattern(duplicates_removed_folder, f"*{FILE_ENDING_DUPLICATES_REMOVED_FASTQ_GZ}")

    # if no files are found, exit
    if len(fastq_files) == 0:
        print_error("No duplicate removed fastq files found. Exiting.")
        return
    
    for prefix, pattern in generate_fastq_patterns(fastq_files).items():
        fastq_files_per_pattern = get_files_in_folder_matching_pattern(duplicates_removed_folder, pattern)
        print_info(f"Found {len(fastq_files_per_pattern)} fastq files for pattern {pattern}")

        output_folder = get_folder_path_species_processed_prepared_for_ref_genome(FOLDER_BGER)
        output_file_path = os.path.join(output_folder,f"{prefix}{FILE_ENDING_FASTQ_GZ}")

        if os.path.exists(output_file_path):
            print_info(f"Output file {output_file_path} already exists. Skipping.")
            continue

        input_pattern_path = os.path.join(duplicates_removed_folder, pattern)

        # call cat via subprocess
        try:
            print_info(f"Concatenating {len(fastq_files_per_pattern)} fastq files for pattern {pattern}")
            cat_command = f"cat {input_pattern_path} > {output_file_path}"
            subprocess.run(cat_command, shell=True, check=True)
            print_success(f"Concatenation for pattern {pattern} complete")
        except Exception as e:
            print_error(f"Failed to concatenate fastq files for pattern {pattern}: {e}")