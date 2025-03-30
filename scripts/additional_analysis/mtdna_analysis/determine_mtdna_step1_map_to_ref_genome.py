import os
from common_aDNA_scripts import *

from ref_genome_processing.map_aDNA_to_refgenome import execute_bwa_map_aDNA_to_refgenome
from ref_genome_processing.convert_ref_genome_sam2bam import execute_convert_sam_to_bam

def map_mtdna_to_refgenome_for_species(species: str):
    print_info(f"Mapping mtdna to reference genome for species {species} ...")

    #get reads
    read_folder = get_folder_path_species_raw_mtdna(species)
    list_of_mtrna_files = get_files_in_folder_matching_pattern(read_folder, f"*{FILE_ENDING_FASTA}")

    if len(list_of_mtrna_files) == 0:
        print_warning(f"No mtdna reads found for species {species}. Skipping.")
        return

    # get ref genome
    ref_genome_folder = get_folder_path_species_raw_ref_genome(species)
    ref_genome_files = get_files_in_folder_matching_pattern(ref_genome_folder, f"*{FILE_ENDING_FNA}")

    if len(ref_genome_files) == 0:
        print_warning(f"No reference genome found for species {species}. Skipping.")
        return

    output_folder = get_folder_path_species_processed_mtdna_mapped(species)

    for ref_genome_path in ref_genome_files:

        ref_genome_filename = os.path.splitext(os.path.basename(ref_genome_path))[0]

        for mtrna_read_file_path in list_of_mtrna_files:

            print_info(f"Mapping {mtrna_read_file_path} to reference genome {ref_genome_path} ...")

            read_name = os.path.splitext(os.path.basename(mtrna_read_file_path))[0]
            output_file_path = os.path.join(output_folder, f"{read_name}_{ref_genome_filename}{FILE_ENDING_SAM}")

            try:
                execute_bwa_map_aDNA_to_refgenome(mtrna_read_file_path, ref_genome_path, output_file_path, THREADS_DEFAULT)

                if not os.path.exists(output_file_path):
                    continue

                execute_convert_sam_to_bam(output_file_path, output_folder, THREADS_DEFAULT)
            except Exception as e:
                print_error(f"Failed to map {mtrna_read_file_path} to reference genome {ref_genome_path}: {e}")

    print_success(f"Mapping mtdna to reference genome for species {species} complete")

def all_species_map_mtdna_to_refgenome():
    print("Mapping mtdna to reference genome for all species")

    for species in FOLDER_SPECIES: 
        map_mtdna_to_refgenome_for_species(species)

    print_info("Mapping mtdna to reference genome for all species complete")

def main():
    all_species_map_mtdna_to_refgenome()

if __name__ == "__main__":
    main()