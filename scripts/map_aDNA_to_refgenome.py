import os
import subprocess
from common_aDNA_scripts import *

def execute_map_aDNA_to_refgenome(input_file_path:str, ref_genome_path:str, output_file_path:str, threads:int = THREADS_DEFAULT):
    
    print_info(f"Mapping {input_file_path} to reference genome ...")

    if not os.path.exists(input_file_path):
        raise Exception(f"Read file {input_file_path} does not exist!")
    
    if not os.path.exists(ref_genome_path):
        raise Exception(f"Reference genome file {ref_genome_path} does not exist!")
    
    if os.path.exists(output_file_path):
        print_info(f"Output file {output_file_path} already exists! Skipping!")
        return
    
    command_bwa = f"bwa mem -t {str(threads)} {ref_genome_path} {input_file_path} > {output_file_path}"

    try:
        subprocess.run(command_bwa, shell=True, check=True)
    except Exception as e:
        print_error(f"Failed to run bwa for {input_file_path}: {e}")

def map_aDNA_to_refgenome_for_species(species):
    print_info(f"Mapping aDNA to reference genome for species {species} ...")

    read_folder = get_folder_path_species_processed_duplicates_removed(species)
    list_of_read_files = get_files_in_folder_matching_pattern(read_folder, f"*{FILE_ENDING_DUPLICATES_REMOVED_FASTQ_GZ}")

    if len(list_of_read_files) == 0:
        print_warning(f"No reads found for species {species}. Skipping.")
        return
    
    

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