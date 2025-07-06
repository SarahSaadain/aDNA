import os
from common_aDNA_scripts import *

import ref_genome_processing.common_ref_genome_processing_helpers as common_rgp

def merge_all_fastq_files(species: str):

    print_info(f"Merging all the FASTQ.GZ files for {species}.")

    # find all raw fastq files
    duplicates_removed_folder = get_folder_path_species_processed_duplicates_removed(species)
    fastq_files = get_files_in_folder_matching_pattern(duplicates_removed_folder, f"*{FILE_ENDING_DUPLICATES_REMOVED_FASTQ_GZ}")

    # if no files are found, exit
    if len(fastq_files) == 0:
        print_warning(f"No duplicate removed FASTQ.GZ files found for species {species}. Exiting.")
        return
    
    print_info(f"Found {len(fastq_files)} relevant FASTQ.GZ files")
    print_debug(f"Files found: {fastq_files}")

    output_file_path = common_rgp.get_species_combined_read_path(species)

    if common_rgp.is_species_combined_reads_file_exists(species):
        print_info(f"Output file {output_file_path} already exists. Skipping.")
        return
    
    # filter out files that contain "LB" or "EB"
    # LB = library blanks
    # EB = extraction blanks
    fastq_files_filtered = [f for f in fastq_files if "LB" not in get_filename_from_path(f) and "EB" not in get_filename_from_path(f)]

    excluded_files = [f for f in fastq_files if f not in fastq_files_filtered]
    if excluded_files:
        print_debug(f"Excluded {len(excluded_files)} files: {[os.path.basename(f) for f in excluded_files]}")

     # if no files are found, exit
    if len(fastq_files_filtered) == 0:
        print_warning(f"No FASTQ.GZ files found for species {species} after filtering. Exiting.")
        return
    
    print_debug(f"Found {len(fastq_files_filtered)} relevant FASTQ.GZ files after filtering")
    print_debug(f"Files found: {fastq_files_filtered}")

    # call cat via subprocess
    try:
        print_info(f"Concatenating {len(fastq_files_filtered)} FASTQ.GZ files (excluding 'LB' and 'EB') for pattern *{FILE_ENDING_DUPLICATES_REMOVED_FASTQ_GZ}")
       
        cat_command = f"cat {' '.join(fastq_files_filtered)} > {output_file_path}"
        print_debug(f"cat command: {cat_command}")
        
        subprocess.run(cat_command, shell=True, check=True)
        print_success(f"Concatenation to {output_file_path} complete")
    except Exception as e:
        print_error(f"Failed to concatenate all FASTQ.GZ files for species {species}: {e}")


def generate_fastq_patterns(file_paths: str) -> dict:
    patterns = {}
    
    for path in file_paths:
        
        # Extract the individual
        individual = common_rgp.get_individual_from_file(path)
        
        # Store the wildcard pattern
        patterns[individual] = f"{individual}*{FILE_ENDING_DUPLICATES_REMOVED_FASTQ_GZ}"

    return patterns

def merge_fastq_by_individual(species: str):

    print_info(f"Merging FASTQ.GZ files for each individual for {species}.")

    # find all raw fastq files
    duplicates_removed_folder = get_folder_path_species_processed_duplicates_removed(species)
    fastq_files = get_files_in_folder_matching_pattern(duplicates_removed_folder, f"*{FILE_ENDING_DUPLICATES_REMOVED_FASTQ_GZ}")

    # if no files are found, exit
    if len(fastq_files) == 0:
        print_warning(f"No duplicate removed FASTQ.GZ files found for species {species}. Exiting.")
        return
    
    for individual, pattern in generate_fastq_patterns(fastq_files).items():
        
        individual_fastq_files_per_pattern = get_files_in_folder_matching_pattern(duplicates_removed_folder, pattern)
        print_info(f"Found {len(individual_fastq_files_per_pattern)} FASTQ.GZ files for pattern {pattern}")
        print_debug(f"Files found: {individual_fastq_files_per_pattern}")

        output_file_path = common_rgp.get_species_individual_reads_path(species, individual)

        if common_rgp.is_species_individual_reads_file_exists(species, individual):
            print_info(f"Output file {output_file_path} already exists. Skipping.")
            continue

        input_pattern_path = os.path.join(duplicates_removed_folder, pattern)

        # call cat via subprocess
        try:
            print_info(f"Concatenating {len(individual_fastq_files_per_pattern)} FASTQ.GZ files for pattern {pattern}")
            cat_command = f"cat {input_pattern_path} > {output_file_path}"
            print_debug(f"cat command: {cat_command}")
            subprocess.run(cat_command, shell=True, check=True)
            print_success(f"Concatenation for pattern {pattern} complete")
        except Exception as e:
            print_error(f"Failed to concatenate FASTQ.GZ files for pattern {pattern}: {e}")

def all_species_prepare():

    print_info(f"Preparing FASTQ.GZ files for ref genome mapping for all species")

    for species in FOLDER_SPECIES: 

        print_info(f"Preparing FASTQ.GZ files for {species} for reference genome mapping")
        
        merge_all_fastq_files(species)
        merge_fastq_by_individual(species)
    
    print_success(f"Finished preparing FASTQ.GZ files for reference genome mapping for all species")
        

def main():
    all_species_prepare()

if __name__ == "__main__":
    main()
