import os
import subprocess
from common_aDNA_scripts import *

from map_aDNA_to_refgenome import execute_bwa_map_aDNA_to_refgenome
from convert_sam2bam import execute_convert_sam_to_bam

def map_coi_to_refgenome_for_species(species):
    print_info(f"Mapping coi to reference genome for species {species} ...")

    #get reads
    read_folder = get_folder_path_species_raw_coigene(species)
    list_of_read_files = get_files_in_folder_matching_pattern(read_folder, f"*{FILE_ENDING_FNA}")

    if len(list_of_read_files) == 0:
        print_warning(f"No reads found for species {species}. Skipping.")
        return

    # get ref genome
    ref_genome_folder = get_folder_path_species_raw_ref_genome(species)
    ref_genome_files = get_files_in_folder_matching_pattern(ref_genome_folder, f"*{FILE_ENDING_FNA}")

    if len(ref_genome_files) == 0:
        print_warning(f"No reference genome found for species {species}. Skipping.")
        return

    output_folder = get_folder_path_species_processed_coigene_mapped(species)

    for ref_genome_path in ref_genome_files:

        ref_genome_filename = os.path.splitext(os.path.basename(ref_genome_path))[0]

        for read_file_path in list_of_read_files:

            print_info(f"Mapping {read_file_path} to reference genome {ref_genome_path} ...")

            read_name = os.path.splitext(os.path.basename(read_file_path))[0]
            output_file_path = os.path.join(output_folder, f"{read_name}_{ref_genome_filename}{FILE_ENDING_SAM}")

            execute_bwa_map_aDNA_to_refgenome(read_file_path, ref_genome_path, output_file_path, THREADS_DEFAULT)

            execute_convert_sam_to_bam(output_file_path, output_folder, THREADS_DEFAULT)

    print_success(f"Mapping coi to reference genome for species {species} complete")

def all_species_map_coi_to_refgenome():
    print("Mapping coi to reference genome for all species")

    for species in FOLDER_SPECIES: 
        map_coi_to_refgenome_for_species(species)

    print_info("Mapping coi to reference genome for all species complete")

def main():
    all_species_map_coi_to_refgenome()

if __name__ == "__main__":
    main()