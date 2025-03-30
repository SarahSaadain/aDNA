import os
import subprocess
from common_aDNA_scripts import *

def execute_bwa_map_aDNA_to_refgenome(input_file_path:str, ref_genome_path:str, output_file_path:str, threads:int = THREADS_DEFAULT):
    
    print_info(f"Mapping {input_file_path} to reference genome ...")

    if not os.path.exists(input_file_path):
        raise Exception(f"Read file {input_file_path} does not exist!")
    
    if not os.path.exists(ref_genome_path):
        raise Exception(f"Reference genome file {ref_genome_path} does not exist!")
    
    if os.path.exists(output_file_path):
        print_info(f"Output file {output_file_path} already exists! Skipping!")
        return
    
    command_bwa = f"{PROGRAM_PATH_BWA} {PROGRAM_PATH_BWA_MEM} -t {str(threads)} {ref_genome_path} {input_file_path} > {output_file_path}"

    try:
        subprocess.run(command_bwa, shell=True, check=True)
        print_success(f"Mapping {input_file_path} to reference genome complete")
    except Exception as e:
        print_error(f"Failed to run bwa for {input_file_path}: {e}")

def map_aDNA_to_refgenome_for_species(species: str):
    print_info(f"Mapping aDNA to reference genome for species {species} ...")

    #get reads
    read_folder = get_folder_path_species_processed_prepared_for_ref_genome(species)
    list_of_read_files = get_files_in_folder_matching_pattern(read_folder, f"*{FILE_ENDING_FASTQ_GZ}")

    if len(list_of_read_files) == 0:
        print_warning(f"No reads found for species {species}. Skipping.")
        return

    # get ref genome
    ref_genome_folder = get_folder_path_species_raw_ref_genome(species)
    ref_genome_files = get_files_in_folder_matching_pattern(ref_genome_folder, "*.fna")

    if len(ref_genome_files) == 0:
        print_warning(f"No reference genome found for species {species}. Skipping.")
        return

    output_folder = get_folder_path_species_processed_mapped(species)

    for ref_genome_path in ref_genome_files:

        ref_genome_filename = get_filename_from_path_without_extension(ref_genome_path)

        for read_file_path in list_of_read_files:

            print_info(f"Mapping {read_file_path} to reference genome {ref_genome_path} ...")

            read_name = get_filename_from_path_without_extension(read_file_path)
            output_file_path = os.path.join(output_folder, f"{read_name}_{ref_genome_filename}.sam")

            execute_bwa_map_aDNA_to_refgenome(read_file_path, ref_genome_path, output_file_path, THREADS_DEFAULT)
        

    print_success(f"Mapping aDNA to reference genome for species {species} complete")

def all_species_map_aDNA_to_refgenome():
    print("Mapping aDNA to reference genome for all species")

    for species in FOLDER_SPECIES: 
        map_aDNA_to_refgenome_for_species(species)

    print_info("Mapping aDNA to reference genome for all species complete")

def main():
    all_species_map_aDNA_to_refgenome()

if __name__ == "__main__":
    main()