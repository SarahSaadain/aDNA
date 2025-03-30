import os
from common_aDNA_scripts import *

def execute_samtools_get_read_regions(bam_file: str, output_file: str, threads: int=THREADS_DEFAULT):

    if not os.path.exists(bam_file):
        raise Exception(f"BAM file {bam_file} does not exist.")
    
    if os.path.exists(output_file):
        print_warning(f"Output file {output_file} already exists. Skipping.")
        return
    
    command = (
        f"{PROGRAM_PATH_SAMTOOLS} {PROGRAM_PATH_SAMTOOLS_VIEW} -h -@ {threads} {bam_file} | "
        f"{PROGRAM_PATH_BEDTOOLS} bamtobed -i - > {output_file}"
    )
    #print_info(f"Running command: {command}")
    
    try:
      # Execute the command
        subprocess.run(command, shell=True, check=True)
        print_success(f"Regions for {bam_file} have been written to {output_file}")
    except Exception as e:
        print_error(f"Failed to extract regions for {bam_file}: {e}")

def mtdna_get_regions_for_species(species):
    print_info(f"Determining mtdna regions for species: {species}")
    
    mapped_folder = get_folder_path_species_processed_mtdna_mapped(species)
    
    bam_files = get_files_in_folder_matching_pattern(mapped_folder, f"*{FILE_ENDING_SORTED_BAM}")

    if len(bam_files) == 0:
        print_warning(f"No BAM files found for species {species}. Skipping.")
        return
    
    for bam_file in bam_files:
        print_info(f"Determining mtdna regions for {bam_file}")

        bam_file_name_wo_ext = get_filename_from_path_without_extension(bam_file)

        result_folder = get_folder_path_species_results_mtdna_regions(species)
        result_file_path = os.path.join(result_folder, f"{bam_file_name_wo_ext}_mtdna_region{FILE_ENDING_BED}")

        if os.path.exists(result_file_path):
            print_info(f"Result file {result_file_path} already exists for species {species}. Skipping.")
            return
        
        execute_samtools_get_read_regions(bam_file, result_file_path)

    print_info(f"Finished determining mtdna regions for species {species}")
    
   
def all_species_mtdna_get_regions():

    print_execution("Determining mtdna regions for all species")
    for species in FOLDER_SPECIES: 
        mtdna_get_regions_for_species(species)
    print_info("Finished determining mtdna regions for all species")

def main():
    all_species_mtdna_get_regions()

if __name__ == "__main__":
    main()
