import os
import subprocess

from common_aDNA_scripts import *

def execute_convert_sam_to_bam(sam_file: str, output_dir: str, threads: int=THREADS_DEFAULT, detlete_unsorted_bam: bool=True):

    # Convert SAM to BAM
    bam_file_base_name = get_filename_from_path_without_extension(sam_file)
    
    bam_file = os.path.join(output_dir, f"{bam_file_base_name}{FILE_ENDING_BAM}")
    sorted_bam = os.path.join(output_dir, f"{bam_file_base_name}{FILE_ENDING_SORTED_BAM}")

    if not os.path.exists(sorted_bam):

        if not os.path.exists(bam_file):
            print_info(f"Converting {sam_file} to BAM...")

            try:
                command_sam_to_bam = f"{PROGRAM_PATH_SAMTOOLS} {PROGRAM_PATH_SAMTOOLS_VIEW} -@ {threads} -bS {sam_file} -o {bam_file}"
                subprocess.run(command_sam_to_bam, shell=True, check=True)
            except Exception as e:
                print_error(f"Failed to convert {sam_file} to BAM: {e}")
                return
        else:
            print_info(f"Conversion for {sam_file} already exists. Skipping.")

   
        print_info(f"Sorting {bam_file}...")
        
        try:
            command_sort = f"{PROGRAM_PATH_SAMTOOLS} {PROGRAM_PATH_SAMTOOLS_SORT} -@ {threads} {bam_file} -o {sorted_bam}"
            subprocess.run(command_sort, shell=True, check=True)

            print_success(f"Conversion and sorting of {sam_file} completed successfully.")
             # Optional cleanup of intermediate BAM file if the sorted was created
            if detlete_unsorted_bam and os.path.exists(sorted_bam):
                print_info(f"Removing unsorted BAM file {bam_file}...")
                os.remove(bam_file)

        except Exception as e:
            print_error(f"Failed to sort {bam_file}: {e}")
            return
    else:
        print_info(f"Sort for {bam_file} already exists. Skipping.")
    
    # Index the sorted BAM file
    indexed_bam = os.path.join(output_dir, f"{bam_file_base_name}{FILE_ENDING_SORTED_BAI}")

    if not os.path.exists(indexed_bam):
        print_info(f"Indexing {sorted_bam}...")
        
        try:
            command_index = f"{PROGRAM_PATH_SAMTOOLS} {PROGRAM_PATH_SAMTOOLS_INDEX} -@ {threads} {sorted_bam} {indexed_bam}" 
            subprocess.run(command_index, shell=True, check=True)
            print_success(f"Indexing of {sorted_bam} completed successfully.")
        except Exception as e:
            print_error(f"Failed to index {sorted_bam}: {e}")
            return
    else:
        print_info(f"Index for {sorted_bam} already exists. Skipping.")
    
    print_success(f"Conversion and indexing of {sam_file} completed successfully.")


def convert_ref_genome_mapped_sam_to_bam_for_species(species):
    print_info(f"Converting ref genome mapped sam to bam for species {species}")

    mapped_folder = get_folder_path_species_processed_mapped(species)
    sam_files = get_files_in_folder_matching_pattern(mapped_folder, f"*{FILE_ENDING_SAM}")

    if len(sam_files) == 0:
        print_warning(f"No SAM ref genome files found for species {species}. Skipping.")
        return

    for sam_file in sam_files:
        execute_convert_sam_to_bam(sam_file, mapped_folder)    


def convert_sam_to_bam_for_species(species):
    print_info(f"Converting sam to bam for species {species}")
    convert_ref_genome_mapped_sam_to_bam_for_species(species)
    print_info(f"Conversion of sam to bam for species {species} completed successfully.")

def all_species_convert_sam_to_bam():
    print_execution("Convert sam to bam files for all species")

    for species in FOLDER_SPECIES: 
        convert_sam_to_bam_for_species(species)

    print_info("Conversion of sam to bam files for all species completed successfully.")

def main():
    all_species_convert_sam_to_bam()

if __name__ == "__main__":
    main()
