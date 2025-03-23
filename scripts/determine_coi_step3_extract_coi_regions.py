import os
import subprocess
from common_aDNA_scripts import *

##todo


def execute_samtools_extract_region_by_bed_file(bam_file_path, mtdna_region_bed_file_path, output_dir):
    
    if not os.path.exists(bam_file_path):
        raise Exception(f"BAM file {bam_file_path} does not exist.")
    
    if not os.path.exists(mtdna_region_bed_file_path):
        raise Exception(f"mtDNA region BED file {mtdna_region_bed_file_path} does not exist.")
    
    if not os.path.exists(output_dir):
        raise Exception(f"Output directory {output_dir} does not exist.")
                        
    # Extract the base name of the BAM file (without path and extension)
    base_name_bam_file = os.path.splitext(os.path.basename(bam_file_path))[0]
    base_name_bed_file = os.path.splitext(os.path.basename(mtdna_region_bed_file_path))[0]

    # Filter the BAM file for reads that map to the mtDNA region
    print_info(f"Filtering {bam_file_path} for reads mapped to mtDNA region...")
    mtdna_bam = os.path.join(output_dir, f"{base_name_bam_file}_{base_name_bed_file}.bam")

    if os.path.exists(mtdna_bam):
        print_info(f"mtDNA BAM file already exists: {mtdna_bam}")
        return

    command = (
        f"{PROGRAM_PATH_SAMTOOLS} {PROGRAM_PATH_SAMTOOLS_VIEW} -b --region-file {mtdna_region_bed_file_path} {bam_file_path} > {mtdna_bam}"
    )

    try:
        subprocess.run(command, shell=True, check=True)
    except Exception as e:
        print_error(f"Failed to filter BAM file {bam_file_path} for mtDNA region: {e}")
        return
    
    # Index the filtered BAM file
    print(f"Indexing {mtdna_bam}...")
    subprocess.run(["samtools", "index", mtdna_bam])

    print(f"Filtered and indexed BAM file created: {mtdna_bam}")

def extract_mtdna_region_for_species(species):
    print_info(f"Extracting mtDNA regions for species: {species}")
    
    mapped_folder = get_folder_path_species_processed_mtdna_consensus_sequences_mapped(species)
    bam_files = get_files_in_folder_matching_pattern(mapped_folder, f"*{FILE_ENDING_SORTED_BAM}")

    if len(bam_files) == 0:
        print_warning(f"No BAM files found for species {species}. Skipping.")
        return
    
    bed_folder = get_folder_path_species_results_mtdna_regions(species)
    bed_files = get_files_in_folder_matching_pattern(bed_folder, f"*{FILE_ENDING_BED}")
    
    if len(bed_files) == 0:
        print_warning(f"No BED files found for species {species}. Skipping.")
        return

    result_folder = get_folder_path_species_processed_mtdna_extracted_sequence(species)

    for bam_file in bam_files:
        for bed_file in bed_files:
            execute_samtools_extract_region_by_bed_file(bam_file, bed_file, result_folder)

    print_info(f"Finished determining mtDNA regions for species {species}")

def all_species_extract_mtdna_region():

    print("Extracting mtDNA regions for all species")
    for species in FOLDER_SPECIES: 
        extract_mtdna_region_for_species(species)
    print_info("Finished extracting mtDNA regions for all species")

def main():
    all_species_extract_mtdna_region()

if __name__ == "__main__":
    main()
