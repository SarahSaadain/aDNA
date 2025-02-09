import os
import re
import subprocess
import sys

#####################
# Constants
#####################
PATH_ADNA_PROJECT = "/mnt/data2/sarah/aDNA"

# species folders
FOLDER_BGER = "Bger" # just the species names, could be in /raw or in /processed
FOLDER_DSIM = "Dsim"
FOLDER_PHORTICA = "Phortica"
FOLDER_SEPSIS = "Sepsis"
FOLDER_MMUS = "Mmus"

FOLDER_SPECIES = {FOLDER_BGER, FOLDER_DSIM, FOLDER_PHORTICA, FOLDER_SEPSIS, FOLDER_MMUS}

# raw folders
FOLDER_RAW = "raw"
FOLDER_READS = "reads"
FOLDER_REFERENCE_GENOMES = "ref_genome"

# processed folders
# if there is a follow up step, it is considered processed
FOLDER_PROCESSED = "processed"
FOLDER_CONCATENATED = "concatenated"
FOLDER_NON_CONCATENATED = "non_concatenated"
FOLDER_MAPPED = "mapped"
FOLDER_ADAPTER_REMOVED = "adapter_removed"
FOLDER_GENOMEDELTA = "GenomeDelta"

# results folders
# if there is no follow up step, it is considered a result
FOLDER_RESULTS = "results"
FOLDER_QUALITYCONTROL = "qualitycontrol"
FOlDER_POlY_NT = "poly_nt"
FOLDER_FASTQC = "fastqc"
FOLDER_DEPTH = "depth"
FOLDER_BREADTH = "breadth"
FOLDER_MITOCHONDRIA= "mitochondria"

FOLDER_SCRIPTS = "scripts"
FOLDER_LOGS = "logs"
FOLDER_RESOURCES = "resources"

# files
FILE_NAME_RAW_READS_LIST = "reads_list.csv"

# paths
# programs
PROGRAM_PATH_CUTADAPT = "cutadapt"
#PROGRAM_PATH_BOWTIE = "/home/vetlinux04/Sarah/softwares/bowtie-1.3.0-linux-x86_64/bowtie"
#PROGRAM_PATH_TRIM_GALORE ="/home/vetlinux04/Sarah/softwares/TrimGalore-0.6.10/trim_galore"

#"doi.org/10.1093/bioinformatics/btt193" to check damage, include to pipeline

# files
#FILENAME_SRNA_FILENAME_LIST = "sRNA_target_filenames.txt"


#####################
# Helpers
#####################


def is_sam_file_sorted(sam_file: str) -> bool:
    """
    Checks if a SAM file is sorted by coordinate.

    :param sam_file: The path to the SAM file
    :return: True if the SAM file is sorted by coordinate, False otherwise
    """
    try:
        # Check the header for sorting status
        result = subprocess.run(
            ['samtools', 'view', '-H', sam_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        for line in result.stdout.splitlines():
            if line.startswith('@HD') and 'SO:coordinate' in line:
                # The SAM file is sorted by coordinate
                return True
        # The SAM file is not sorted by coordinate
        return False
    except subprocess.CalledProcessError as e:
        print(f"Error reading header: {e}")
        # Return False in case of an error
        return False

def convert_sam_to_bam(sam_file, bam_file, threads=20):

    print_info(f"Converting SAM to BAM: {sam_file} -> {bam_file}")

    try:

        if is_sam_file_sorted(sam_file):
            print(f"{sam_file} is already sorted. Skipping sorting step.")
            # Convert directly to BAM if needed
            subprocess.run(
                ['samtools', 'view', '-bS', sam_file, '-o', bam_file],
                check=True
            )
        else:
            # Convert and sort SAM to BAM in one step
            subprocess.run(
                ['samtools', 'sort', '-@', str(threads), '-o', bam_file, sam_file],
                check=True
            )
            print("SAM to BAM conversion and sorting completed.")

        # Index the BAM file using samtools index with multiple threads
        subprocess.run(
            ['samtools', 'index', '-@', str(threads), bam_file], 
            check=True, 
            stderr=sys.stderr
        )
        
        print(f"Conversion and indexing of {sam_file} completed successfully with {threads} threads.")

    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}", file=sys.stderr)

def is_fasta_file(file_name):
    return file_name.endswith("fna") or file_name.endswith("fa") or file_name.endswith("fasta")


#####################
# Print
#####################

# print command to terminal
def print_command(subprocess_command):          # prints subprocess commands
    print_info(" ".join(subprocess_command))

def print_info(message):
    print(f"[INFO] {message}")

def print_error(message):
    print(f"[ERROR] {message}")

def print_success(message):
    print(f"[SUCCESS] {message}")

def print_warning(message): 
    print(f"[WARNING] {message}")

#####################
# Folder paths
#####################

def is_species_folder(folder_name):
    return folder_name in FOLDER_SPECIES

def check_folder_exists_or_create(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def get_folder_aDNA():
    return PATH_ADNA_PROJECT
def get_folder_path_species_raw(species):
    if not is_species_folder(species):
        raise Exception(f"Invalid species folder: {species}")

    path = os.path.join(get_folder_aDNA(), species, FOLDER_RAW)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species(species):
    if not is_species_folder(species):
        raise Exception(f"Invalid species folder: {species}")

    path = os.path.join(get_folder_aDNA(), species)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_processed(species):
    path = os.path.join(get_folder_path_species(species), FOLDER_PROCESSED)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_results(species):
    path = os.path.join(get_folder_path_species(species), FOLDER_RESULTS)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_scripts(species):
    path = os.path.join(get_folder_path_species(species), FOLDER_SCRIPTS)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_logs(species):
    path = os.path.join(get_folder_path_species(species), FOLDER_LOGS)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_resources(species):
    path = os.path.join(get_folder_path_species(species), FOLDER_RESOURCES)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_raw_reads(species):
    path = os.path.join(get_folder_path_species_raw(species), FOLDER_READS)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_raw_ref_genome(species):
    path = os.path.join(get_folder_path_species_raw(species), FOLDER_REFERENCE_GENOMES)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_processed_mapped(species):
    path = os.path.join(get_folder_path_species_processed(species), FOLDER_MAPPED)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_processed_adapter_removed(species):
    path = os.path.join(get_folder_path_species_processed(species), FOLDER_ADAPTER_REMOVED)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_processed_concatenated(species):
    path = os.path.join(get_folder_path_species_processed(species), FOLDER_CONCATENATED)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_processed_non_concatenated(species):
    path = os.path.join(get_folder_path_species_processed(species), FOLDER_NON_CONCATENATED)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_results_qualitycontrol(species):
    path = os.path.join(get_folder_path_species_results(species), FOLDER_QUALITYCONTROL)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_results_qualitycontrol_poly_nt(species):
    path = os.path.join(get_folder_path_species_results_qualitycontrol(species), FOlDER_POlY_NT)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_results_qualitycontrol_fastqc(species):
    path = os.path.join(get_folder_path_species_results_qualitycontrol(species), FOLDER_FASTQC)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_results_qualitycontrol_depth(species):
    path = os.path.join(get_folder_path_species_results_qualitycontrol(species), FOLDER_DEPTH)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_results_qualitycontrol_breadth(species):
    path = os.path.join(get_folder_path_species_results_qualitycontrol(species), FOLDER_BREADTH)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_results_mitochondria(species):
    path = os.path.join(get_folder_path_species_results(species), FOLDER_MITOCHONDRIA)
    check_folder_exists_or_create(path)
    return path

#####################
# File paths
#####################

# def get_reference_genome_path_by_name(species, ref_genome_name):

#     raw_species_ref_genome_directory = get_folder_path_species_raw_ref_genome(species)

#     # look for ref genome file in directory of species
#     for ref_genome_file_name in os.listdir(raw_species_ref_genome_directory):

#         # check if file matches, if yes return, otherwise continue
#         if ref_genome_file_name.startswith(ref_genome_name):
#             return os.path.join(raw_species_ref_genome_directory, ref_genome_file_name)

#     #if we reach this point, we did not find a ref genome -> Error
#     raise RuntimeError(f"No reference genome found with name {ref_genome_name} for species {species}")

def get_reads_list_of_species(species):
     
    if not is_species_folder(species):
        raise Exception(f"Invalid species folder: {species}")
    
    raw_reads_folder = get_folder_path_species_raw_reads(species)

    if not os.path.exists(raw_reads_folder):
        raise Exception(f"Folder {raw_reads_folder} does not exist")
    
    raw_reads_list_file = os.path.join(raw_reads_folder, FILE_NAME_RAW_READS_LIST)

    if not os.path.exists(raw_reads_list_file):
        raise Exception(f"File {raw_reads_list_file} does not exist")
    
    with open(raw_reads_list_file, 'r') as file:
        lines = file.readlines()
        
    # Split each line by the comma, strip the paths to remove any extra spaces or newlines, and make them absolute paths
    file_paths = [
        [os.path.abspath(os.path.join(raw_reads_folder, paths[0].strip())),
        os.path.abspath(os.path.join(raw_reads_folder, paths[1].strip()))]
        for line in lines
        for paths in [line.strip().split(',')]  # Split the line by the comma
    ]

    return file_paths