import os
import subprocess

from common_aDNA_scripts import *
import ref_genome_processing.common_ref_genome_processing_helpers as common_rgp

def execute_convert_sam_to_bam(sam_file: str, bam_file: str, sorted_bam: str, threads: int=THREADS_DEFAULT, delete_sam: bool=True, detlete_unsorted_bam: bool=True):

    if not os.path.exists(sorted_bam):

        if not os.path.exists(bam_file):
            print_info(f"Converting {sam_file} to BAM...")

            if not os.path.exists(sam_file):
                print_error(f"Input SAM file {sam_file} does not exist!")
                return

            try:
                command_sam_to_bam = f"{PROGRAM_PATH_SAMTOOLS} {PROGRAM_PATH_SAMTOOLS_VIEW} -@ {threads} -bS {sam_file} -o {bam_file}"
                print_debug(f"Executing command: {command_sam_to_bam}")
                subprocess.run(command_sam_to_bam, shell=True, check=True)

                if delete_sam and os.path.exists(sam_file):
                    print_info(f"Removing SAM file {sam_file}...")
                    try:
                        os.remove(sam_file)
                    except Exception as e:
                        print_warning(f"Failed to remove SAM file {sam_file}: {e}")
            except Exception as e:
                print_error(f"Failed to convert {sam_file} to BAM: {e}")
                return
        else:
            print_info(f"Conversion for {sam_file} already exists. Skipping.")

        print_info(f"Sorting {bam_file}...")
        
        try:
            command_sort = f"{PROGRAM_PATH_SAMTOOLS} {PROGRAM_PATH_SAMTOOLS_SORT} -@ {threads} {bam_file} -o {sorted_bam}"
            print_debug(f"Executing command: {command_sort}")
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
    indexed_bam = sorted_bam + FILE_ENDING_BAI

    if not os.path.exists(indexed_bam):
        print_info(f"Indexing {sorted_bam}...")
        
        try:
            command_index = f"{PROGRAM_PATH_SAMTOOLS} {PROGRAM_PATH_SAMTOOLS_INDEX} -@ {threads} {sorted_bam} {indexed_bam}" 
            print_debug(f"Executing command: {command_index}")
            subprocess.run(command_index, shell=True, check=True)
            print_success(f"Indexing of {sorted_bam} completed successfully.")
        except Exception as e:
            print_error(f"Failed to index {sorted_bam}: {e}")
            return
    else:
        print_info(f"Index for {sorted_bam} already exists. Skipping.")
    
    print_success(f"Conversion and indexing of {sam_file} completed successfully.")


def convert_ref_genome_mapped_sam_to_bam_for_species(species):
    print_info(f"Converting reference genome mapped sam to bam for species {species}")

    try:
        ref_genome_list = common_rgp.get_reference_genome_file_list_for_species(species)
    except Exception as e:
        print_error(f"Failed to get reference genome files for species {species}: {e}")
        return
    
    number_of_ref_genome_files = len(ref_genome_list)
    count_current = 0

    for ref_genome_tuple in ref_genome_list:

        # ref_genome is a tuple of (ref_genome_name without extension, ref_genome_path)
        ref_genome_id = ref_genome_tuple[0]
        #ref_genome_path = ref_genome_tuple[1]

        print_info(f"Converting mapped SAM files for reference genome {ref_genome_id} for species {species}")

        mapped_folder = get_folder_path_species_processed_refgenome_mapped(species, ref_genome_id)
        sam_files = get_files_in_folder_matching_pattern(mapped_folder, f"*{FILE_ENDING_SAM}")

        number_of_sam_files = len(sam_files)

        if number_of_sam_files == 0:
            print_warning(f"No mapped SAM files found for reference genome {ref_genome_id} for species {species}.")
            return
        
        number_of_sam_files = len(sam_files)
        
        print_debug(f"Found {len(sam_files)} mapped SAM files for reference genome {ref_genome_id} for species {species}.")
        print_debug(f"Mapped SAM files: {sam_files}")

        for sam_file in sam_files:

            count_current += 1
            
            print_info(f"[{count_current}/{number_of_sam_files}] Converting {get_filename_from_path(sam_file)} to BAM for reference genome {ref_genome_id} for species {species} ...")

            bam_file = common_rgp.get_bam_file_path_for_sam_file(species, ref_genome_id, sam_file)
            sorted_bam = common_rgp.get_sorted_bam_file_path_for_bam_file(species, ref_genome_id, bam_file)

            execute_convert_sam_to_bam(sam_file, bam_file, sorted_bam)    


def convert_sam_to_bam_for_species(species):
    print_info(f"Converting sam to bam for species {species}")
    convert_ref_genome_mapped_sam_to_bam_for_species(species)
    print_success(f"Conversion of sam to bam for species {species} executed.")

def all_species_convert_sam_to_bam():
    print_execution("Convert sam to bam files for all species")

    for species in FOLDER_SPECIES: 
        convert_sam_to_bam_for_species(species)

    print_success("Conversion of sam to bam files for all species executed.")

def main():
    all_species_convert_sam_to_bam()

if __name__ == "__main__":
    main()
