import os
import subprocess
import glob

#####################
# Constants
#####################
PATH_ADNA_PROJECT = "/mnt/data2/sarah/aDNA"
#PATH_ADNA_PROJECT = "/Users/ssaadain/Documents/aDNA"

# config
THREADS_DEFAULT = 10

# species folders
FOLDER_BGER = "Bger" # just the species names, could be in /raw or in /processed
FOLDER_DSIM = "Dsim"
FOLDER_PHORTICA = "Phortica"
FOLDER_SEPSIS = "Sepsis"
FOLDER_MMUS = "Mmus"
FOLDER_DMEL = "Dmel"
FOLDER_TRIAL_BGER = "trial_Bger"
FOLDER_TRIAL_DSIM = "trial_Dsim"
FOLDER_TRIAL_PHORTICA = "trial_Phortica"
FOLDER_TRIAL_SEPSIS = "trial_Sepsis"
FOLDER_TRIAL_MMUS = "trial_Mmus"
FOLDER_TRIAL_DMEL = "trial_Dmel"

FOLDER_SPECIES = [FOLDER_BGER, FOLDER_DSIM, FOLDER_PHORTICA, FOLDER_SEPSIS, FOLDER_MMUS, FOLDER_DMEL, FOLDER_TRIAL_BGER, FOLDER_TRIAL_DSIM, FOLDER_TRIAL_PHORTICA, FOLDER_TRIAL_SEPSIS, FOLDER_TRIAL_MMUS, FOLDER_TRIAL_DMEL]

# raw folders
FOLDER_RAW = "raw"
FOLDER_READS = "reads"
FOLDER_REFERENCE_GENOMES = "ref_genome"
FOLDER_MTDNA = "mtdna"

# processed folders
# if there is a follow up step, it is considered processed
FOLDER_PROCESSED = "processed"
FOLDER_CONCATENATED = "concatenated"
FOLDER_NON_CONCATENATED = "non_concatenated"
FOLDER_MAPPED = "mapped"
FOLDER_PREPARED_FOR_REF_GENOME = "prepared_for_ref_genome"
FOLDER_ADAPTER_REMOVED = "adapter_removed"
FOLDER_QUALITY_FILTERED = "quality_filtered"
FOLDER_DUPLICATES_REMOVED = "duplicates_removed"
FOLDER_GENOMEDELTA = "genome_delta"
FOLDER_CONSENSUS_SEQUENCES = "consensus_sequences"
FOLDER_CONSENSUS_SEQUENCES_MAPPED = "consensus_sequences_mapped"
FOLDER_EXTRACTED_SEQUENCES = "extracted_sequences"

# results folders
# if there is no follow up step, it is considered a result
FOLDER_RESULTS = "results"
FOLDER_QUALITYCONTROL = "qualitycontrol"
FOLDER_FASTQC = "fastqc"
FOLDER_MULTIQC = "multiqc"
FOLDER_DEPTH_BREADTH = "depth_breadth"
FOLDER_DEPTH = "depth"
FOLDER_BREADTH = "breadth"
FOLDER_MITOCHONDRIA= "mitochondria"
FOLDER_SPECIAL_SEQUENCES = "special_sequences"
FOLDER_ENDOGENOUS_READS = "endogenous_reads"
FOLDER_PROCESSED_READS = "processed_reads"
FOLDER_READ_LENGTH_DISTRIBUTION = "read_length_distribution"
FOLDER_PLOTS = "plots"
FOLDER_REGIONS = "regions"

# main folders
FOLDER_SCRIPTS = "scripts"
FOLDER_LOGS = "logs"
FOLDER_RESOURCES = "resources"

# files
FILE_NAME_RAW_READS_LIST = "reads_list.csv"

# paths
# programs
PROGRAM_PATH_CUTADAPT = "cutadapt"
PROGRAM_PATH_FASTP = "fastp"
PROGRAM_PATH_FASTX_TRIMMER = "fastx_trimmer"
PROGRAM_PATH_FASTX_QUALITY_FILTER = "fastq_quality_filter"
PROGRAM_PATH_SGA = "sga"
PROGRAM_PATH_MULTIQC = "multiqc"
PROGRAM_PATH_FASTQC = "fastqc"
PROGRAM_PATH_BWA = "bwa"
PROGRAM_PATH_BEDTOOLS = "bedtools"
PROGRAM_PATH_BWA_MEM = "mem"
PROGRAM_PATH_SAMTOOLS = "samtools"
PROGRAM_PATH_SAMTOOLS_VIEW =  "view"
PROGRAM_PATH_SAMTOOLS_SORT = "sort"
PROGRAM_PATH_SAMTOOLS_INDEX = "index"
PROGRAM_PATH_ANGSD = "angsd"

#"doi.org/10.1093/bioinformatics/btt193" to check damage, include to pipeline

# files
FILE_PATTERN_R1_FASTQ_GZ = "*_R1*.fastq.gz"
FILE_PATTERN_R2_FASTQ_GZ = "*_R2*.fastq.gz"
FILE_PATTERN_UNDETERMINED_FOLDER = "*/undetermined/*"

FILE_ENDING_ADAPTER_REMOVED_FASTQ_GZ = "_merged_trimmed.fastq.gz"
FILE_ENDING_FASTQ_GZ = ".fastq.gz"
FILE_ENDING_FASTA = ".fasta"
FILE_ENDING_FNA = ".fna"
FILE_ENDING_FA = ".fa"
FILE_ENDING_FA_GZ = ".fa.gz"
FILE_ENDING_QUALITY_FILTERED_FASTQ_GZ = "_quality_filtered.fastq.gz"
FILE_ENDING_DUPLICATES_REMOVED_FASTQ_GZ = "_duplicates_removed.fastq.gz"
FILE_ENDING_FASTQC_HTML = "_fastqc.html"
FILE_ENDING_SAM = ".sam"
FILE_ENDING_BAM = ".bam"
FILE_ENDING_SORTED_BAM = "_sorted.bam"
FILE_ENDING_BAI = ".bai"
FILE_ENDING_SORTED_BAI = "_sorted.bai"
FILE_ENDING_CSV = ".csv"
FILE_ENDING_BED = ".bed"
FILE_ENDING_TSV = ".tsv"
FILE_ENDING_PNG = ".png"
FILE_ENDING_HTML = ".html"
FILE_ENDING_SAMTOOLS_DEPTH_TSV = "_samtools_depth.tsv"
FILE_ENDING_ANALYSIS_TSV = "_analysis.tsv"

FILE_PATTERN_LIST_FASTA = [f"*{FILE_ENDING_FNA}", f"*{FILE_ENDING_FASTA}", f"*{FILE_ENDING_FA}"]

#R Scripts
R_SCRIPT_PLOT_READS_BEFORE_AFTER_PROCESSING  ="plot_comparison_reads_before_after_processing.R"
R_SCRIPT_PLOT_DEPTH = "plot_coverage_depth.R"
R_SCRIPT_PLOT_BREADTH = "plot_coverage_breadth.R"
R_SCRIPT_PLOT_ENDOGENOUS_READS = "plot_endogenous_reads.R"
R_SCRIPT_PLOT_SEQUENCE_LENGTH_DISTRIBUTION = "plot_sequence_length_distribution.R"
R_SCRIPT_PLOT_COMPARE_SPECIES_READS_BEFORE_AFTER_PROCESSING = "plot_compare_species_reads_before_after_processing.R"
R_SCRIPT_PLOT_COMPARE_SPECIES_DEPTH_BREADTH = "plot_compare_species_depth_breadth.R"
R_SCRIPT_PLOT_COMPARE_SPECIES_ENDOGENOUS_READS = "plot_compare_species_endogenous_reads.R"


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
            [PROGRAM_PATH_SAMTOOLS, 'view', '-H', sam_file],
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

def is_fasta_file(file_name: str) -> bool:
    return file_name.endswith("fna") or file_name.endswith("fa") or file_name.endswith("fasta")

def is_fasta_gz_file(file_name: str) -> bool:
    return file_name.endswith("fna.gz") or file_name.endswith("fa.gz") or file_name.endswith("fasta.gz") 



#####################
# Print
#####################

# print command to terminal
def print_command(subprocess_command: list):          # prints subprocess commands
    print_info(" ".join(subprocess_command))

def print_info(message: str):
    print(f"[INFO] {message}")

def print_error(message: str):
    print(f"[ERROR] {message}")

def print_success(message: str):
    print(f"[SUCCESS] {message}")

def print_warning(message: str): 
    print(f"[WARNING] {message}")

#####################
# Folder paths
#####################

def is_species_folder(folder_name: str) -> bool:
    return folder_name in FOLDER_SPECIES

def check_folder_exists_or_create(folder_path: str) -> None:
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def get_folder_aDNA() -> str:
    return PATH_ADNA_PROJECT

def get_folder_path_results() -> str:
    path = os.path.join(get_folder_aDNA(), FOLDER_RESULTS)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_results_plots() -> str:
    path = os.path.join(get_folder_path_results(), FOLDER_PLOTS)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_scripts() -> str:
    path = os.path.join(get_folder_aDNA(), FOLDER_SCRIPTS)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_scripts_plots() -> str:
    path = os.path.join(get_folder_path_scripts(), FOLDER_PLOTS)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_raw(species: str) -> str:
    if not is_species_folder(species):
        raise Exception(f"Invalid species folder: {species}")

    path = os.path.join(get_folder_aDNA(), species, FOLDER_RAW)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species(species: str) -> str:
    if not is_species_folder(species):
        raise Exception(f"Invalid species folder: {species}")

    path = os.path.join(get_folder_aDNA(), species)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_processed(species: str) -> str:
    path = os.path.join(get_folder_path_species(species), FOLDER_PROCESSED)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_results(species: str) -> str:
    path = os.path.join(get_folder_path_species(species), FOLDER_RESULTS)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_scripts(species: str) -> str:
    path = os.path.join(get_folder_path_species(species), FOLDER_SCRIPTS)
    check_folder_exists_or_create(path)
    return path


def get_folder_path_species_logs(species: str) -> str:
    path = os.path.join(get_folder_path_species(species), FOLDER_LOGS)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_resources(species: str) -> str:
    path = os.path.join(get_folder_path_species(species), FOLDER_RESOURCES)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_raw_reads(species: str) -> str:
    path = os.path.join(get_folder_path_species_raw(species), FOLDER_READS)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_raw_mtdna(species: str) -> str:
    path = os.path.join(get_folder_path_species_raw(species), FOLDER_MTDNA)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_raw_ref_genome(species: str) -> str:
    path = os.path.join(get_folder_path_species_raw(species), FOLDER_REFERENCE_GENOMES)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_processed_mapped(species: str) -> str:
    path = os.path.join(get_folder_path_species_processed(species), FOLDER_MAPPED)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_processed_mtdna(species: str) -> str:
    path = os.path.join(get_folder_path_species_processed(species), FOLDER_MTDNA)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_processed_mtdna_extracted_sequence(species: str) -> str:
    path = os.path.join(get_folder_path_species_processed_mtdna(species), FOLDER_EXTRACTED_SEQUENCES)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_processed_mtdna_mapped(species: str) -> str:
    path = os.path.join(get_folder_path_species_processed_mtdna(species), FOLDER_MAPPED)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_processed_mtdna_consensus_sequences(species: str) -> str:
    path = os.path.join(get_folder_path_species_processed_mtdna(species), FOLDER_CONSENSUS_SEQUENCES)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_processed_mtdna_consensus_sequences_mapped(species: str) -> str:
    path = os.path.join(get_folder_path_species_processed_mtdna(species), FOLDER_CONSENSUS_SEQUENCES_MAPPED)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_processed_adapter_removed(species: str) -> str:
    path = os.path.join(get_folder_path_species_processed(species), FOLDER_ADAPTER_REMOVED)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_processed_quality_filtered(species: str) -> str:
    path = os.path.join(get_folder_path_species_processed(species), FOLDER_QUALITY_FILTERED)
    check_folder_exists_or_create(path)
    return path 

def get_folder_path_species_processed_duplicates_removed(species: str) -> str:
    path = os.path.join(get_folder_path_species_processed(species), FOLDER_DUPLICATES_REMOVED)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_processed_prepared_for_ref_genome(species: str) -> str:
    path = os.path.join(get_folder_path_species_processed(species), FOLDER_PREPARED_FOR_REF_GENOME)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_processed_genomedelta(species: str) -> str:
    path = os.path.join(get_folder_path_species_processed(species), FOLDER_GENOMEDELTA)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_processed_concatenated(species: str) -> str:
    path = os.path.join(get_folder_path_species_processed(species), FOLDER_CONCATENATED)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_processed_non_concatenated(species: str) -> str:
    path = os.path.join(get_folder_path_species_processed(species), FOLDER_NON_CONCATENATED)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_results_genomedelta(species: str) -> str:
    path = os.path.join(get_folder_path_species_results(species), FOLDER_GENOMEDELTA)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_results_mtdna(species: str) -> str:
    path = os.path.join(get_folder_path_species_results(species), FOLDER_MTDNA)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_results_mtdna_regions(species: str) -> str:
    path = os.path.join(get_folder_path_species_results_mtdna(species), FOLDER_REGIONS)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_results_qc(species: str) -> str:
    path = os.path.join(get_folder_path_species_results(species), FOLDER_QUALITYCONTROL)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_results_qc_fastqc(species: str) -> str:
    path = os.path.join(get_folder_path_species_results_qc(species), FOLDER_FASTQC)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_results_qc_fastqc_raw(species: str) -> str:
    path = os.path.join(get_folder_path_species_results_qc_fastqc(species), FOLDER_RAW)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_results_qc_fastqc_adapter_removed(species: str) -> str:
    path = os.path.join(get_folder_path_species_results_qc_fastqc(species), FOLDER_ADAPTER_REMOVED)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_results_qc_fastqc_quality_filtered(species: str) -> str:
    path = os.path.join(get_folder_path_species_results_qc_fastqc(species), FOLDER_QUALITY_FILTERED)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_results_qc_fastqc_duplicates_removed(species: str) -> str:
    path = os.path.join(get_folder_path_species_results_qc_fastqc(species), FOLDER_DUPLICATES_REMOVED)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_results_qc_multiqc(species: str) -> str:
    path = os.path.join(get_folder_path_species_results_qc(species), FOLDER_MULTIQC)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_results_qc_multiqc_raw(species: str) -> str:
    path = os.path.join(get_folder_path_species_results_qc_multiqc(species), FOLDER_RAW)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_results_qc_multiqc_adapter_removed(species: str) -> str:
    path = os.path.join(get_folder_path_species_results_qc_multiqc(species), FOLDER_ADAPTER_REMOVED)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_results_qc_multiqc_quality_filtered(species: str) -> str:
    path = os.path.join(get_folder_path_species_results_qc_multiqc(species), FOLDER_QUALITY_FILTERED)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_results_qc_multiqc_duplicates_removed(species: str) -> str:
    path = os.path.join(get_folder_path_species_results_qc_multiqc(species), FOLDER_DUPLICATES_REMOVED)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_results_qc_depth_breath(species: str) -> str:
    path = os.path.join(get_folder_path_species_results_qc(species), FOLDER_DEPTH_BREADTH)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_results_mitochondria(species: str) -> str:
    path = os.path.join(get_folder_path_species_results(species), FOLDER_MITOCHONDRIA)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_results_plots(species: str) -> str:
    path = os.path.join(get_folder_path_species_results(species), FOLDER_PLOTS)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_results_plots_reads_processing(species: str) -> str:
    path = os.path.join(get_folder_path_species_results_plots(species), FOLDER_PROCESSED_READS)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_results_plots_depth(species: str) -> str:
    path = os.path.join(get_folder_path_species_results_plots(species), FOLDER_DEPTH)
    check_folder_exists_or_create(path) 
    return path

def get_folder_path_species_results_plots_depth_sample(species: str, sample_name: str) -> str:
    path = os.path.join(get_folder_path_species_results_plots_depth(species), sample_name)
    check_folder_exists_or_create(path) 
    return path


def get_folder_path_species_results_plots_breadth(species: str) -> str:
    path = os.path.join(get_folder_path_species_results_plots(species), FOLDER_BREADTH)
    check_folder_exists_or_create(path) 
    return path

def get_folder_path_species_results_plots_breadth_sample(species: str, sample_name: str) -> str:
    path = os.path.join(get_folder_path_species_results_plots_breadth(species), sample_name)
    check_folder_exists_or_create(path) 
    return path

def get_folder_path_species_results_plots_endogenous_reads(species: str) -> str:
    path = os.path.join(get_folder_path_species_results_plots(species), FOLDER_ENDOGENOUS_READS)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_results_plots_read_length_distribution(species: str) -> str:    
    path = os.path.join(get_folder_path_species_results_plots(species), FOLDER_READ_LENGTH_DISTRIBUTION)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_results_special_sequences(species: str) -> str:
    path = os.path.join(get_folder_path_species_results(species), FOLDER_SPECIAL_SEQUENCES)
    check_folder_exists_or_create(path) 
    return path

def get_folder_path_species_results_endogenous_reads(species: str) -> str:
    path = os.path.join(get_folder_path_species_results(species), FOLDER_ENDOGENOUS_READS)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_results_qc_reads_processing(species: str) -> str:
    path = os.path.join(get_folder_path_species_results_qc(species), FOLDER_PROCESSED_READS)
    check_folder_exists_or_create(path)
    return path

def get_folder_path_species_results_qc_read_length_distribution(species: str) -> str:
    path = os.path.join(get_folder_path_species_results_qc(species), FOLDER_READ_LENGTH_DISTRIBUTION)
    check_folder_exists_or_create(path)
    return path


#####################
# File paths
#####################

def get_r_script(r_script_name: str) -> str:

    r_script_path = os.path.join(get_folder_path_scripts_plots(), r_script_name)

    if not os.path.exists(r_script_path):
        raise Exception(f"Invalid R script: {r_script_path}")   
    
    return r_script_path


def get_raw_reads_list_of_species(species: str) -> list:
     
    if not is_species_folder(species):
        raise Exception(f"Invalid species folder: {species}")
    
    raw_reads_folder = get_folder_path_species_raw_reads(species)

    return get_files_in_folder_matching_pattern(raw_reads_folder, "*.fastq.gz")
   

def get_files_in_folder_matching_pattern(folder: str, pattern: str) -> list:
     
    if not os.path.exists(folder):
        raise Exception(f"Invalid folder: {folder}")
    
    #read all reads from folder into list
    files = glob.glob(os.path.join(folder, pattern))

    return files

def get_raw_paired_reads_list_of_species(species: str) -> list:

    if not is_species_folder(species):
        raise Exception(f"Invalid species folder: {species}")

    folder_path = get_folder_path_species_raw_reads(species)

    #def generate_paired_reads_list(folder_path: str, output_file: str, overwrite: bool = False) -> None:
    """
    Generate a list of read files from a given folder path, sorted by sample ID.

    Args:
        folder_path (str): The path to the folder containing the read files.
        output_file (str): The path to the output file.
        overwrite (bool, optional): Whether to overwrite the output file if it already exists. Defaults to False.
    """

    find_command = f'find {folder_path} -type f \\( -name "{FILE_PATTERN_R1_FASTQ_GZ}" -o -name "{FILE_PATTERN_R2_FASTQ_GZ}" \\) ! -path "{FILE_PATTERN_UNDETERMINED_FOLDER}"'
    
    # Sort the list of files by sample ID
    sort_command = 'sort'
    
    # Use awk to format the list of files as a comma-separated list
    awk_command = 'awk \'NR%2{printf "%s,", $0} NR%2==0{print $0}\''
    
    # Combine the commands into a single command string
    full_command = f'{find_command} | {sort_command} | {awk_command}'
    
    # Run the command and return the list of files
    command_result = subprocess.run(full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)

    try:
        #print_info(f"Running command: {full_command}")
        command_result = subprocess.run(full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    except subprocess.CalledProcessError as e:
        raise Exception(f"An error occurred while running the command: {e}")
        
    #convert output into list of files
    lines = command_result.stdout.splitlines()

    # Split each line by the comma, strip the paths to remove any extra spaces or newlines, and make them absolute paths
    file_paths = [
        [os.path.abspath(os.path.join(folder_path, paths[0].strip())),
        os.path.abspath(os.path.join(folder_path, paths[1].strip()))]
        for line in lines
        for paths in [line.strip().split(',')]  # Split the line by the comma
    ]

    return file_paths