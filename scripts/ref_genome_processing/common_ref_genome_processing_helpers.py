import os
import common_aDNA_scripts as common

def get_species_combined_read_path(species: str) -> str:
    output_folder = common.get_folder_path_species_processed_prepared_for_ref_genome(species)
    return os.path.join(output_folder, f"{species}_combined{common.FILE_ENDING_FASTQ_GZ}")

def is_species_combined_reads_file_exists(species: str) -> bool:
    combined_reads_path = get_species_combined_read_path(species)
    return os.path.exists(combined_reads_path)

def get_species_individual_reads_path(species: str, individual: str) -> str:
    output_folder = common.get_folder_path_species_processed_prepared_for_ref_genome(species)
    return os.path.join(output_folder, f"{individual}{common.FILE_ENDING_FASTQ_GZ}")

def is_species_individual_reads_file_exists(species: str, individual: str) -> bool:
    individual_reads_path = get_species_individual_reads_path(species, individual)
    return os.path.exists(individual_reads_path)

def is_species_individual_and_combined_reads_file_exists(species: str, individual: str) -> bool:
    individual_reads_exists = is_species_individual_reads_file_exists(species, individual)
    combined_reads_exists = is_species_combined_reads_file_exists(species)
    
    return individual_reads_exists and combined_reads_exists


def get_individual_from_file(file_path: str) -> str:

    filename = common.get_filename_from_path_without_extension(file_path)
    
    #the indivisual name is expected to be the first part of the filename, e.g. "individual_protocol_R1_001.fastq.gz"
    
    #check if filename has an underscore
    if '_' not in filename:
        raise ValueError(f"Filename '{filename}' does not contain an underscore to separate individual name.")

    parts = filename.split('_')

    return parts[0]  # Assuming the second part is the individual name