import os
from common_aDNA_scripts import *

FILE_NAME_PREPARE_SCRIPT = "prepare_for_mapping_to_ref_genome.py"

def merge_all_fastq_files(species: str):

    print_info(f"Merging  all the fastq files for {species}.")

    # find all raw fastq files
    duplicates_removed_folder = get_folder_path_species_processed_duplicates_removed(species)
    fastq_files = get_files_in_folder_matching_pattern(duplicates_removed_folder, f"*{FILE_ENDING_DUPLICATES_REMOVED_FASTQ_GZ}")

    # if no files are found, exit
    if len(fastq_files) == 0:
        print_error("No duplicate removed fastq files found. Exiting.")
        return
    
    print_info(f"Found {len(fastq_files)} fastq files")

    output_folder = get_folder_path_species_processed_prepared_for_ref_genome(species)
    output_file_path = os.path.join(output_folder, f"{species}_combined{FILE_ENDING_FASTQ_GZ}")

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


def generate_fastq_patterns(file_paths: str) -> dict:
    patterns = {}
    
    for path in file_paths:
        # Extract the filename
        filename = get_filename_from_path_without_extension(path)
        
        # Extract the individual
        individual = filename.split('_')[0]
        
        # Store the wildcard pattern
        patterns[individual] = f"{individual}*{FILE_ENDING_DUPLICATES_REMOVED_FASTQ_GZ}"

    return patterns

def merge_fastq_by_individual(species: str):

    # find all raw fastq files
    duplicates_removed_folder = get_folder_path_species_processed_duplicates_removed(species)
    fastq_files = get_files_in_folder_matching_pattern(duplicates_removed_folder, f"*{FILE_ENDING_DUPLICATES_REMOVED_FASTQ_GZ}")

    # if no files are found, exit
    if len(fastq_files) == 0:
        print_error("No duplicate removed fastq files found. Exiting.")
        return
    
    for individual, pattern in generate_fastq_patterns(fastq_files).items():
        
        individual_fastq_files_per_pattern = get_files_in_folder_matching_pattern(duplicates_removed_folder, pattern)
        print_info(f"Found {len(individual_fastq_files_per_pattern)} fastq files for pattern {pattern}")

        output_folder = get_folder_path_species_processed_prepared_for_ref_genome(species)
        output_file_path = os.path.join(output_folder,f"{individual}{FILE_ENDING_FASTQ_GZ}")

        if os.path.exists(output_file_path):
            print_info(f"Output file {output_file_path} already exists. Skipping.")
            continue

        input_pattern_path = os.path.join(duplicates_removed_folder, pattern)

        # call cat via subprocess
        try:
            print_info(f"Concatenating {len(individual_fastq_files_per_pattern)} fastq files for pattern {pattern}")
            cat_command = f"cat {input_pattern_path} > {output_file_path}"
            subprocess.run(cat_command, shell=True, check=True)
            print_success(f"Concatenation for pattern {pattern} complete")
        except Exception as e:
            print_error(f"Failed to concatenate fastq files for pattern {pattern}: {e}")

def all_species_prepare():

    print_info("Preparing fastq files for ref genome mapping for all species")

    for species in FOLDER_SPECIES: 

        print_info(f"Preparing fastq files for {species} for ref genome mapping")
        scripts_folder = get_folder_path_species_scripts(species)

        prepare_script_path = os.path.join(scripts_folder, FILE_NAME_PREPARE_SCRIPT)

         # Check if prepare.py exists
        # if os.path.exists(prepare_script_path):
        #     print_info(f"Found {FILE_NAME_PREPARE_SCRIPT} script for species {species}.")
        #     call_prepare_script(species, prepare_script_path)
        # else:
        #     print_info(f"No {FILE_NAME_PREPARE_SCRIPT} script found for species {species}.")
        #     merge_all_fastq_files(species)
        
        merge_all_fastq_files(species)
        merge_fastq_by_individual(species)
    
    print_success("Finished preparing fastq files for ref genome mapping for all species")
        

def main():
    all_species_prepare()

if __name__ == "__main__":
    main()
