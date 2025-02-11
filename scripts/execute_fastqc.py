import os
from common_aDNA_scripts import *

FASTQC_THREADS = 20

def fastqc_for_species(species):
    # run fastqc for raw data
    fastqc_for_raw_data(species)

    # run fastqc for trimmed data
    fastqc_for_adapter_removed_data(species)

    # run fastqc for quality filtered data
    fastqc_for_quality_filtered_data(species)

    # run fastqc for duplicates removed data
    fastqc_for_duplicates_removed_data(species)

def fastqc_for_raw_data(species):
    print_info(f"Running fastqc for species {species} raw data")

    # raw data
    raw_reads_folder = get_folder_path_species_raw_reads(species)
    output_folder = get_folder_path_species_results_qc_fastqc_raw(species)

    raw_reads_files = get_files_in_folder_matching_pattern(raw_reads_folder, f"*{FILE_ENDING_FASTQ_GZ}")

    files_list = get_files_in_folder_matching_pattern(output_folder, f"*{FILE_ENDING_FASTQC_HTML}")

    if len(files_list) > 0:
        print_warning(f"Fastqc data already exists for species {species}. Skipping.")
        return

    for raw_read_file in raw_reads_files:
        execute_fastqc(species, raw_read_file, output_folder)

    print_success(f"fastqc for species {species} raw data complete")

def fastqc_for_quality_filtered_data(species):
    print_info(f"Running fastqc for species {species} quality filtered data")

    quality_filtered_reads_folder = get_folder_path_species_processed_quality_filtered(species)
    output_folder = get_folder_path_species_results_qc_fastqc_quality_filtered(species)

    quality_filtered_reads = get_files_in_folder_matching_pattern(quality_filtered_reads_folder, f"*{FILE_ENDING_QUALITY_FILTERED_FASTQ_GZ}")

    files_list = get_files_in_folder_matching_pattern(output_folder, f"*{FILE_ENDING_FASTQC_HTML}")

    if len(files_list) > 0:
        print_warning(f"Fastqc data already exists for species {species}. Skipping.")
        return

    for filtered_read in quality_filtered_reads:
        execute_fastqc(species, filtered_read, output_folder)

    print_success(f"fastqc for species {species} quality filtered data complete")

def fastqc_for_adapter_removed_data(species):
    print_info(f"Running fastqc for species {species} trimmed data")

    #adapter removed data
    trimmed_reads_folder = get_folder_path_species_processed_adapter_removed(species)
    output_folder = get_folder_path_species_results_qc_fastqc_adapter_removed(species)

    adapter_removed_reads = get_files_in_folder_matching_pattern(trimmed_reads_folder, f"*{FILE_ENDING_ADAPTER_REMOVED_FASTQ_GZ}")

    files_list = get_files_in_folder_matching_pattern(output_folder, f"*{FILE_ENDING_FASTQC_HTML}")

    if len(files_list) > 0:
        print_warning(f"fastqc data already exists for species {species}. Skipping.")
        return
    
    for trimmed_read in adapter_removed_reads:
        execute_fastqc(species, trimmed_read, output_folder)

    print_success(f"fastqc for species {species} trimmed data complete")

def fastqc_for_duplicates_removed_data(species):
    print_info(f"Running fastqc for species {species} duplicates removed data")

    duplicates_removed_reads_folder = get_folder_path_species_processed_duplicates_removed(species)
    output_folder = get_folder_path_species_results_qc_fastqc_duplicates_removed(species)

    duplicates_removed_reads = get_files_in_folder_matching_pattern(duplicates_removed_reads_folder, f"*{FILE_ENDING_DUPLICATES_REMOVED_FASTQ_GZ}")

    files_list = get_files_in_folder_matching_pattern(output_folder, f"*{FILE_ENDING_FASTQC_HTML}")

    if len(files_list) > 0:
        print_warning(f"Fastqc data already exists for species {species}. Skipping.")
        return
    
    for duplicates_removed_read in duplicates_removed_reads:
        execute_fastqc(species, duplicates_removed_read, output_folder)

    print_success(f"fastqc for species {species} duplicates removed data complete")

def execute_fastqc(species, reads_file, output_folder, threads:int = FASTQC_THREADS):

    print_info(f"Running fastqc for reads file {reads_file}")

    if not os.path.exists(reads_file):
        raise Exception(f"Read file {reads_file} does not exist!")

    command = f"{PROGRAM_PATH_FASTQC} -o {output_folder} -t {threads} {reads_file}"
    try:
        subprocess.run(command, shell=True, check=True)
        print_success(f"Fastqc for {reads_file} complete")
    except Exception as e:
        print_error(f"Failed to run fastqc for species {species}: {e}")

def all_species_fastqc():

    print("Running fastqc for all species before and after adapter removal")

    for species in FOLDER_SPECIES: 
        fastqc_for_species(species)

def all_species_fastqc_raw():
    print("Running fastqc for all species raw data")

    for species in FOLDER_SPECIES: 
        fastqc_for_raw_data(species)

def all_species_fastqc_adapter_removed():
    print("Running fastqc for all species trimmed data")

    for species in FOLDER_SPECIES: 
       fastqc_for_adapter_removed_data(species)

def all_species_fastqc_quality_filtered():
    print("Running fastqc for all species quality filtered data")

    for species in FOLDER_SPECIES: 
        fastqc_for_quality_filtered_data(species)

def all_species_fastqc_duplicates_removed():
    print("Running fastqc for all species duplicates removed data")

    for species in FOLDER_SPECIES: 
        fastqc_for_duplicates_removed_data(species)


def main():
    all_species_fastqc()

if __name__ == "__main__":
    main()
