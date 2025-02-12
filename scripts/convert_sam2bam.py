import os
import subprocess
import argparse

from common_aDNA_scripts import *

def execute_convert_sam_to_bam(sam_file, output_dir, threads=THREADS_DEFAULT):
    base_name = os.path.splitext(os.path.basename(sam_file))[0]
    
    # Convert SAM to BAM
    bam_file_base_name = os.path.splitext(os.path.basename(sam_file))[0]

    bam_file = os.path.join(output_dir, f"{bam_file_base_name}{FILE_ENDING_BAM}")
    
    print(f"Converting {sam_file} to BAM...")

    try:
        command_sam_to_bam = f"samtools view -@ {threads} -bS {sam_file} -o {bam_file}"
        subprocess.run(command_sam_to_bam, shell=True, check=True)
    except Exception as e:
        print_error(f"Failed to convert {sam_file} to BAM: {e}")
        return
   
    # Sort BAM file
    sorted_bam = os.path.join(output_dir, f"{bam_file_base_name}_sorted{FILE_ENDING_BAM}")
    print(f"Sorting {bam_file}...")
    
    try:
        command_sort = f"samtools sort -@ {threads} {bam_file} -o {sorted_bam}"
        subprocess.run(command_sort, shell=True, check=True)
    except Exception as e:
        print_error(f"Failed to sort {bam_file}: {e}")
        return
    
    # Index the sorted BAM file
    indexed_bam = os.path.join(output_dir, f"{bam_file_base_name}_sorted.bai")

    print(f"Indexing {sorted_bam}...")
    
    try:
        comand_index = f"samtools index -@ {threads} -o {indexed_bam} {sorted_bam}" 
        subprocess.run(comand_index, shell=True, check=True)
    except Exception as e:
        print_error(f"Failed to index {sorted_bam}: {e}")
        return

    # Optional cleanup of intermediate BAM file
    #os.remove(bam_file)

def convert_ref_genome_mapped_sam_to_bam_for_species(species):
    print_info(f"Converting ref genome mapped sam to bam for species {species}")

    mapped_folder = get_folder_path_species_processed_mapped(species)
    sam_files = get_files_in_folder_matching_pattern(mapped_folder, FILE_ENDING_SAM)

    if len(sam_files) == 0:
        print_warning(f"No SAM ref genome files found for species {species}. Skipping.")
        return

    for sam_file in sam_files:
        execute_convert_sam_to_bam(sam_file, mapped_folder)    


def convert_sam_to_bam_for_species(species):
    print_info(f"Converting sam to bam for species {species}")
    convert_ref_genome_mapped_sam_to_bam_for_species(species)

def all_species_convert_sam_to_bam():
    print("Convert sam to bam files for all species")

    for species in FOLDER_SPECIES: 
        convert_sam_to_bam_for_species(species)

def main():
    all_species_convert_sam_to_bam()

if __name__ == "__main__":
    main()
