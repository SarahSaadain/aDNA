import os
from common_aDNA_scripts import *

def execute_samtools_count_mapped_reads(bam_file: str, threads: int=THREADS_DEFAULT) -> int:
    """Counts the number of mapped reads in a BAM file."""
    try:
        result = subprocess.run(
            [PROGRAM_PATH_SAMTOOLS, PROGRAM_PATH_SAMTOOLS_VIEW, "-@", str(threads), "-c", "-F", "4", bam_file], 
            capture_output=True, text=True, check=True
        )
        return int(result.stdout.strip())
    except Exception as e:
        print_error(f"Failed to count mapped reads in {bam_file}: {e}")
    return 0
def execute_samtools_count_total_reads(bam_file: str, threads: int=THREADS_DEFAULT) -> int:
    """Counts the total number of reads in a BAM file (mapped and unmapped)."""
    try:
        result = subprocess.run(
            [PROGRAM_PATH_SAMTOOLS, PROGRAM_PATH_SAMTOOLS_VIEW, "-@", str(threads), "-c", bam_file], 
            capture_output=True, text=True, check=True
        )
        return int(result.stdout.strip())
    except Exception as e:
        print_error(f"Failed to count total reads in {bam_file}: {e}")
    return 0

def determine_endogenous_reads_for_species(species: str):
    print(f"Determining endogenous reads for species: {species}")
    
    mapped_folder = get_folder_path_species_processed_mapped(species)

    bam_files = get_files_in_folder_matching_pattern(mapped_folder, f"*{FILE_ENDING_SORTED_BAM}")

    if len(bam_files) == 0:
        print_warning(f"No BAM files found for species {species}. Skipping.")
        return

    result_folder = get_folder_path_species_results_endogenous_reads(species)
    result_file_path = os.path.join(result_folder, f"{species}_endogenous_reads{FILE_ENDING_CSV}")

    if os.path.exists(result_file_path):
        print_info(f"Result file already exists for species {species}. Skipping.")
        return
    
    #open result file for writing as csv
    with open(result_file_path, "w") as result_file:

        for bam_file in bam_files:

            bam_filename = os.path.basename(bam_file)

            print_info(f"Determining endogenous reads for {bam_filename}")

            proportion = 0.0
            
            mapped_reads = execute_samtools_count_mapped_reads(bam_file)
            total_reads = execute_samtools_count_total_reads(bam_file)

            if total_reads != 0:
                proportion = mapped_reads / total_reads

            print(f"Endogenous reads for {bam_filename}: {mapped_reads}/{total_reads} -> {proportion:.4f}")
            result_file.write(f"{bam_filename},{mapped_reads},{total_reads},{proportion}\n")

def all_species_determine_endogenous_reads():

    print("Determining endogenous reads for all species")
    for species in FOLDER_SPECIES: 
        determine_endogenous_reads_for_species(species)

def main():
    all_species_determine_endogenous_reads()

if __name__ == "__main__":
    main()
