import contextlib
import io
import os
import importlib.util
from common_aDNA_scripts import *

FILE_NAME_PREPARE_SCRIPT = "prepare_for_mapping_to_ref_genome.py"

def merge_all_fastq_files(species):

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

def call_prepare_script(species, prepare_script_full_path):

    print_info(f"Running {FILE_NAME_PREPARE_SCRIPT} for {species}")

    # Check if prepare.py exists
    if not os.path.exists(prepare_script_full_path):
        print_info(f"No {FILE_NAME_PREPARE_SCRIPT} script found for species {species}.")
        return
    
    print_info(f"Running {FILE_NAME_PREPARE_SCRIPT} script for species {species}.")

    # Import prepare.py
    spec = importlib.util.spec_from_file_location("prepare", prepare_script_full_path)
    prepare_module = importlib.util.module_from_spec(spec)
    
    # Execute prepare.py and capture its output
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        spec.loader.exec_module(prepare_module)
        prepare_module.prepare()

    # Print the captured output
    print(output.getvalue())

    print_info(f"Finished running {FILE_NAME_PREPARE_SCRIPT} script for species {species}.")
        

def all_species_prepare():

    print_info(f"Preparing fastq files for {species} for ref genome mapping")

    for species in FOLDER_SPECIES: 
        scripts_folder = get_folder_path_species_scripts(species)

        prepare_script_path = os.path.join(scripts_folder, FILE_NAME_PREPARE_SCRIPT)

         # Check if prepare.py exists
        if os.path.exists(prepare_script_path):
            print_info(f"Found {FILE_NAME_PREPARE_SCRIPT} script for species {species}.")
            call_prepare_script(species, prepare_script_path)
        else:
            print_info(f"No {FILE_NAME_PREPARE_SCRIPT} script found for species {species}.")
            merge_all_fastq_files(species)

    print_info(f"Finished running {FILE_NAME_PREPARE_SCRIPT} for all species")
        

def main():
    all_species_prepare()

if __name__ == "__main__":
    main()
