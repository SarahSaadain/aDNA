import os
from common_aDNA_scripts import *

MULTIQC_THREADS = 20

def multiqc_before_after(species):
    # before: run multiqc for raw data
    multiqc_for_raw_data(species)

    # after: run multiqc for trimmed data
    multiqc_for_trimmed_data(species)

def multiqc_for_raw_data(species):
    print_info(f"Running MultiQC for species {species} raw data")

    #TODO: check if multiqc data exists

    # raw data
    raw_reads_folder = get_folder_path_species_raw_reads(species)
    output_folder = os.path.join(get_folder_path_species_results_qc_multiqc(species),"raw")
    run_multiqc(species, raw_reads_folder, output_folder)

    print_success(f"MultiQC for species {species} raw data complete")

def multiqc_for_trimmed_data(species):
    print_info(f"Running MultiQC for species {species} trimmed data")

    #TODO: check if multiqc data exists    

    #adapter removed data
    raw_reads_folder = get_folder_path_species_processed_adapter_removed(species)
    output_folder = os.path.join(get_folder_path_species_results_qc_multiqc(species),"trimmed")
    run_multiqc(species, raw_reads_folder, output_folder)

    print_success(f"Multiqc for species {species} trimmed data complete")

def run_multiqc(species, reads_folder, output_folder, threads=MULTIQC_THREADS):

    command = f"multiqc --threads {threads} {reads_folder[species]}/*fastq.gz -o {output_folder}"
    try:
        subprocess.run(command, shell=True, check=True)
    except Exception as e:
        print_error(f"Failed to run MultiQC for species {species}: {e}")

def all_species_multiqc_before_after():
    for species in FOLDER_SPECIES: 
        multiqc_before_after(species)

def all_species_multiqc_raw():
    for species in FOLDER_SPECIES: 
        multiqc_for_raw_data(species)

def all_species_multiqc_trimmed():
    for species in FOLDER_SPECIES: 
       multiqc_for_trimmed_data(species)
        

def main():
    all_species_multiqc_before_after()

if __name__ == "__main__":
    main()
