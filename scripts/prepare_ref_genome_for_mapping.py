import os
from common_aDNA_scripts import *

def main():
    all_species_prepare_ref_genome()

if __name__ == "__main__":
    main()

def all_species_prepare_ref_genome():
    print_info("Preparing reference genomes for mapping for all species")
    for species in FOLDER_SPECIES:
        species_prepare_ref_genome(species)
    
    print_info("Finished preparing reference genomes for mapping for all species")

def species_prepare_ref_genome(species: str):
    print_info(f"Preparing reference genome for {species} for mapping")

    # get reference genome
    # add fna files to reference genome list
    reference_genome = get_files_in_folder_matching_pattern(get_folder_path_species_raw_ref_genome(species), f"*{FILE_ENDING_FNA}")
    # add fasta files to reference genome list
    reference_genome += get_files_in_folder_matching_pattern(get_folder_path_species_raw_ref_genome(species), f"*{FILE_ENDING_FASTA}")
    # add fa files to reference genome list
    reference_genome += get_files_in_folder_matching_pattern(get_folder_path_species_raw_ref_genome(species), f"*{FILE_ENDING_FA}")

    for reference_genome_path in reference_genome:
        execute_bwa_index_reference_genome(reference_genome_path)

    print_info(f"Finished preparing reference genome for {species} for mapping")

def execute_bwa_index_reference_genome(reference_genome_path: str):
    print_info(f"Indexing reference genome {reference_genome_path} ...")

    # Check if index file already exists
    index_file = f"{reference_genome_path}.bwt"
    if os.path.exists(index_file):
        print_info(f"Index file {index_file} already exists, skipping indexing.")
        return 

    command_bwa = f"bwa index {reference_genome_path}"

    try:
        subprocess.run(command_bwa, shell=True, check=True)
        print_info(f"Finished indexing reference genome {reference_genome_path}")
    except Exception as e:
        print_error(f"Failed to index reference genome {reference_genome_path}: {e}")