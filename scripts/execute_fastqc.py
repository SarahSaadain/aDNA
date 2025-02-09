import os
from common_aDNA_scripts import *

FASTQC_THREADS = 20

def fastqc_before_after(species):
    # before: run fastqc for raw data
    fastqc_for_raw_data(species)

    # after: run fastqc for trimmed data
    fastqc_for_trimmed_data(species)

def fastqc_for_raw_data(species):
    print_info(f"Running fastqc for species {species} raw data")

    #TODO: check if fastqc data exists

    # raw data
    raw_reads_folder = get_folder_path_species_raw_reads(species)
    output_folder = get_folder_path_species_results_qc_fastqc_raw(species)
    run_fastqc(species, raw_reads_folder, output_folder)

    print_success(f"fastqc for species {species} raw data complete")

def fastqc_for_trimmed_data(species):
    print_info(f"Running fastqc for species {species} trimmed data")

    #TODO: check if fastqc data exists    

    #adapter removed data
    trimmed_reads_folder = get_folder_path_species_processed_adapter_removed(species)
    output_folder = get_folder_path_species_results_qc_fastqc_adapter_removed(species)
    run_fastqc(species, trimmed_reads_folder, output_folder)

    print_success(f"fastqc for species {species} trimmed data complete")

def run_fastqc(species, reads_folder, output_folder, threads:int = FASTQC_THREADS):

    command = f"fastqc -o {output_folder} -t {threads} {reads_folder}/*fastq.gz"
    try:
        subprocess.run(command, shell=True, check=True)
    except Exception as e:
        print_error(f"Failed to run fastqc for species {species}: {e}")

def all_species_fastqc_before_after():

    print("Running fastqc for all species before and after adapter removal")

    for species in FOLDER_SPECIES: 
        fastqc_before_after(species)

def all_species_fastqc_raw():
    print("Running fastqc for all species raw data")

    for species in FOLDER_SPECIES: 
        fastqc_for_raw_data(species)

def all_species_fastqc_trimmed():
    print("Running fastqc for all species trimmed data")

    for species in FOLDER_SPECIES: 
       fastqc_for_trimmed_data(species)
        

def main():
    all_species_fastqc_before_after()

if __name__ == "__main__":
    main()
