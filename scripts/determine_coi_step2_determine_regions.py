import os
from common_aDNA_scripts import *

def execute_samtools_get_read_regions(bam_file, output_file, threads=THREADS_DEFAULT):

    if not os.path.exists(bam_file):
        raise Exception(f"BAM file {bam_file} does not exist.")
    
    if os.path.exists(output_file):
        print_warning(f"Output file {output_file} already exists. Skipping.")
        return
    
    command = f"{PROGRAM_PATH_SAMTOOLS} {PROGRAM_PATH_SAMTOOLS_VIEW} -@ {threads} {bam_file} | awk '{{print $3, $4}}' > {output_file}"
  
    try:
      # Execute the command
        subprocess.run(command, shell=True, check=True)
        print(f"Regions have been written to {output_file}")
    except Exception as e:
        print_error(f"Failed to extract regions for {bam_file}: {e}")

def coi_get_regions_for_species(species):
    print_info(f"Determining coi regions for species: {species}")
    
    mapped_folder = get_folder_path_species_processed_mapped(species)

    bam_files = get_files_in_folder_matching_pattern(mapped_folder, f"*{FILE_ENDING_SORTED_BAM}")

    if len(bam_files) == 0:
        print_warning(f"No BAM files found for species {species}. Skipping.")
        return

    result_folder = get_folder_path_species_results_coigene_regions(species)
    result_file_path = os.path.join(result_folder, f"{species}_coi_regions{FILE_ENDING_CSV}")

    if os.path.exists(result_file_path):
        print_info(f"Result file already exists for species {species}. Skipping.")
        return
    
    execute_samtools_get_read_regions(bam_files[0], result_file_path)

    print_info(f"Finished determining coi regions for species {species}")
    
   
def all_species_coi_get_regions():

    print("Determining coi regions for all species")
    for species in FOLDER_SPECIES: 
        coi_get_regions_for_species(species)
    print_info("Finished determining coi regions for all species")

def main():
    all_species_coi_get_regions()

if __name__ == "__main__":
    main()
