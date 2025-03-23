import os
import subprocess
from common_aDNA_scripts import *

from map_aDNA_to_refgenome import execute_bwa_map_aDNA_to_refgenome

def execute_angsd_create_and_map_consensus_sequence(input_file, output_dir):

    print_info(f"Executing angsd to create consensus sequence for {input_file}")

    if not os.path.exists(input_file):
        raise Exception(f"Input file {input_file} does not exist!")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    base_name = os.path.splitext(os.path.basename(input_file))[0]

    # create consensus fasta
    out_file_path = os.path.join(output_dir, f"{base_name}_consensus.fasta")

    if os.path.exists(out_file_path):
        print_info(f"Consensus sequence {out_file_path} already exists. Skipping.")
        return

    print_info(f"Creating consensus sequence of {input_file}...")
    try:
        subprocess.run([PROGRAM_PATH_ANGSD, "-out", out_file_path, "-i", input_file, "-doFasta", "2", "-doCounts", "1"])
        print_success(f"Consensus sequence of {input_file} created successfully.")
    except Exception as e:
        print_error(f"Failed to create consensus sequence of {input_file}: {e}")

def create_consensus_sequence_for_species(species):
    print_info(f"Mapping aDNA to reference genome for species {species} ...")

    #get reads
    read_folder = get_folder_path_species_processed_mapped(species)
    list_of_mapped_files = get_files_in_folder_matching_pattern(read_folder, f"*{FILE_ENDING_SORTED_BAM}")

    if len(list_of_mapped_files) == 0:
        print_warning(f"No mapped reads found for species {species}. Skipping.")
        return
    
    output_folder_consensus_seq = get_folder_path_species_processed_coigene_consensus_sequences(species)

    for mapped_read_file_path in list_of_mapped_files:

        print_info(f"Creating consensus sequence for {mapped_read_file_path} ...")

        execute_angsd_create_and_map_consensus_sequence(mapped_read_file_path, output_folder_consensus_seq)

    print_info(f"Creating consensus sequence for species {species} complete")


def map_consensus_sequence_for_species(species):
    print_info(f"Mapping aDNA consensus sequence to reference genome for species {species} ...")

    #get reads
    read_folder = get_folder_path_species_processed_coigene_consensus_sequences(species)
    list_of_read_files = get_files_in_folder_matching_pattern(read_folder, f"*{FILE_ENDING_FASTQ_GZ}")

    if len(list_of_read_files) == 0:
        print_warning(f"No reads found for species {species}. Skipping.")
        return
    
    output_folder = get_folder_path_species_processed_coigene_consensus_sequences_mapped(species)

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

    print_info(f"Mapping aDNA consensus sequence to reference genome for species {species} complete")

def create_and_map_consensus_sequence_for_species(species):
    

    create_consensus_sequence_for_species(species)
    map_consensus_sequence_for_species(species)        

    print_info(f"Consensus sequence of {species} created and mapped successfully.")

def all_species_create_and_map_consensus_sequence():
    print("Mapping aDNA to reference genome for all species")

    for species in FOLDER_SPECIES: 
        create_and_map_consensus_sequence_for_species(species)

    print_info("Mapping aDNA to reference genome for all species complete")

def main():
    all_species_create_and_map_consensus_sequence()

if __name__ == "__main__":
    main()