import os
from common_aDNA_scripts import *
import ref_genome_processing.helpers.ref_genome_processing_helper as ref_genome_processing_helper

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

    try:
        ref_genome_files = ref_genome_processing_helper.get_reference_genome_file_list_for_species(species)

        for ref_genome in ref_genome_files:
            # ref_genome is a tuple of (ref_genome_name without extension, ref_genome_path)
            ref_genome_file_path = ref_genome[1]
            execute_bwa_index_reference_genome(ref_genome_file_path)

        print_info(f"Finished preparing reference genome for {species} for mapping")

    except Exception as e:
        print_error(f"Failed to get reference genome files for species {species}: {e}")
        return

    

def execute_bwa_index_reference_genome(reference_genome_path: str):
    print_info(f"Indexing reference genome {reference_genome_path} ...")

    # Check if index file already exists
    index_file = f"{reference_genome_path}.bwt"
    if os.path.exists(index_file):
        print_info(f"Index file {index_file} already exists, skipping indexing.")
        return 

    command_bwa = f"{PROGRAM_PATH_BWA} {PROGRAM_PATH_BWA_INDEX} {reference_genome_path}"
    print_debug(f"Command: {command_bwa}")

    try:
        subprocess.run(command_bwa, shell=True, check=True)
        print_info(f"Finished indexing reference genome {reference_genome_path}")
    except Exception as e:
        print_error(f"Failed to index reference genome {reference_genome_path}: {e}")