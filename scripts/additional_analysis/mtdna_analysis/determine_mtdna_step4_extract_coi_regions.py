import os
import subprocess
from common_aDNA_scripts import *

def get_region_from_bed_file(file_path):

    if not os.path.exists(file_path):
        raise Exception(f"BED file {file_path} does not exist.")
    
    if not file_path.endswith(FILE_ENDING_BED):
        raise Exception(f"File {file_path} is not a BED file.")

    with open(file_path, 'r') as bed_file:
        lines = [line.strip().split() for line in bed_file if line.strip()]
    
    if len(lines) == 0:
        raise Exception(f"BED file {file_path} is empty.")
    
    if len(lines) > 1:
        raise Exception(f"BED file {file_path} contains more than one line.")
    
    scaffold, start, end, *_ = lines[0]
    position = f"{scaffold}:{start}-{end}"
    return position

def execute_samtools_extract_region_by_bed_file(fasta_file_path: str, mtdna_region_bed_file_path: str, output_dir: str):
    
    if not os.path.exists(fasta_file_path):
        raise Exception(f"FASTA file {fasta_file_path} does not exist.")
    
    if not os.path.exists(mtdna_region_bed_file_path):
        raise Exception(f"mtDNA region BED file {mtdna_region_bed_file_path} does not exist.")
    
    if not os.path.exists(output_dir):
        raise Exception(f"Output directory {output_dir} does not exist.")
                        
    # Extract the base name of the BAM file (without path and extension)
    base_name_fasta_file = get_filename_from_path_without_extension(fasta_file_path)
    base_name_bed_file = get_filename_from_path_without_extension(mtdna_region_bed_file_path)

    mtdna_fasta = os.path.join(output_dir, f"{base_name_fasta_file}_{base_name_bed_file}{FILE_ENDING_FASTA}")

    if os.path.exists(mtdna_fasta):
        print_info(f"mtDNA FASTA file already exists: {mtdna_fasta}")
        return

    # Get the mtDNA region from the BED file
    try:
        mtdna_region = get_region_from_bed_file(mtdna_region_bed_file_path)
        print_info(f"Extracting mtDNA region: {mtdna_region}")
    except Exception as e:
        print_error(f"Failed to get mtDNA region from BED file {mtdna_region_bed_file_path}: {e}")
        return

    command = f"{PROGRAM_PATH_SAMTOOLS} {PROGRAM_PATH_SAMTOOLS_FAIDX} {fasta_file_path} {mtdna_region} -i  > {mtdna_fasta}"

     # Filter the BAM file for reads that map to the mtDNA region
    try:
        print_info(f"Extracting mtDNA {mtdna_region} region from {fasta_file_path} to {mtdna_fasta}...")
        subprocess.run(command, shell=True, check=True)
        print_success(f"Extracted mtDNA region {mtdna_region} from {fasta_file_path} to {mtdna_fasta}")
    except Exception as e:
        print_error(f"Failed to extract mtDNA region {mtdna_region} from {fasta_file_path}: {e}")
        return

def extract_mtdna_region_for_species(species: str):
    print_info(f"Extracting mtDNA regions for species: {species}")
    
    consensus_sequences_folder = get_folder_path_species_processed_mtdna_consensus_sequences(species)
    fasta_files = get_files_in_folder_matching_pattern(consensus_sequences_folder, f"*{FILE_ENDING_FA_GZ}")

    if len(fasta_files) == 0:
        print_warning(f"No consensus sequence files found for species {species}. Skipping.")
        return
    
    bed_folder = get_folder_path_species_results_mtdna_regions(species)
    bed_files = get_files_in_folder_matching_pattern(bed_folder, f"*{FILE_ENDING_BED}")
    
    if len(bed_files) == 0:
        print_warning(f"No BED files found for species {species}. Skipping.")
        return

    result_folder = get_folder_path_species_processed_mtdna_extracted_sequence(species)

    for fasta_file in fasta_files:
        for bed_file in bed_files:
            execute_samtools_extract_region_by_bed_file(fasta_file, bed_file, result_folder)

    print_info(f"Finished determining mtDNA regions for species {species}")

def all_species_extract_mtdna_region():

    print_execution("Extracting mtDNA regions for all species")
    for species in FOLDER_SPECIES: 
        extract_mtdna_region_for_species(species)
    print_info("Finished extracting mtDNA regions for all species")

def main():
    all_species_extract_mtdna_region()

if __name__ == "__main__":
    main()
