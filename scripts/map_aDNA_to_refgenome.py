import os
import subprocess
from common_aDNA_scripts import *

def execute_map_aDNA_to_refgenome(input_file_path:str, output_file_path:str, threads:int = 20):
    pass

def map_aDNA_to_refgenome_for_species(species):
    print_info(f"Mapping aDNA to reference genome for species {species} ...")

    read_folder = get_folder_path_species_processed_duplicates_removed(species)
    list_of_read_files = get_files_in_folder_matching_pattern(read_folder, f"*{FILE_ENDING_DUPLICATES_REMOVED_FASTQ_GZ}")

    #output_folder = get_folder_path_species_processed_mapped_to_refgenome(species)

    for read_file_path in list_of_read_files:
        continue ##TODO: implement this

    print_success(f"Mapping aDNA to reference genome for species {species} complete")

def all_species_map_aDNA_to_refgenome():
    print_info("Mapping aDNA to reference genome for all species")

    for species in FOLDER_SPECIES: 
        map_aDNA_to_refgenome_for_species(species)

def main():
    all_species_map_aDNA_to_refgenome()

if __name__ == "__main__":
    main()