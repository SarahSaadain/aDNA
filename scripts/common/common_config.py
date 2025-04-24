import logging
import common.config_manager as config_manager  # Assuming config_manager.py is in the same directory

from common.common_logging import *

# Load the configuration file (only once)
try:

    print_execution("Loading configuration file ...")
    # Path to your config file. we assume it is in the same directory where this script is located
    config_file_path = 'config.yaml'  

    print_info(f"Loading config file: {config_file_path}")

    config = config_manager.load_config(config_file_path)  # Or however you specify the path
    
    print_success("Config loaded successfully.")
    
    print_info(f"Project path: {config['path_adna_project']}")
    print_info(f"Species: {config['species'].keys()}")
    print_info(f"Threads default: {config['threads_default']}")

    # Set up logging based on the config
    # Assuming the config has a 'log_level' key
    # and you want to set the logging level accordingly
    log_level_str = config.get("log_level", "INFO").upper()
    log_level = getattr(logging, log_level_str, logging.INFO)

    # update the logging level
    logging.getLogger().setLevel(log_level)
    print_info(f"Log level set to {log_level_str}")

    print_debug(f"Loaded Config: {config}") 

except FileNotFoundError:
    print_error("Config file not found.  Exiting.")
    exit(1) #Or handle more gracefully


PATH_ADNA_PROJECT = config['path_adna_project']

# config
THREADS_DEFAULT = config['threads_default']

# species folders
FOLDER_SPECIES = list(config['species'].keys())

# program related constants
PROGRAM_PATH_FASTP = config['tools']['fastp']
PROGRAM_PATH_SGA = config['tools']['sga']
PROGRAM_PATH_MULTIQC = config['tools']['multiqc']
PROGRAM_PATH_FASTQC = config['tools']['fastqc']
PROGRAM_PATH_BEDTOOLS = config['tools']['bedtools']
PROGRAM_PATH_BWA = config['tools']['bwa']
PROGRAM_PATH_BWA_MEM = "mem"
PROGRAM_PATH_BWA_INDEX = "index"
PROGRAM_PATH_SAMTOOLS = config['tools']['samtools']
PROGRAM_PATH_SAMTOOLS_FAIDX =  "faidx"
PROGRAM_PATH_SAMTOOLS_VIEW =  "view"
PROGRAM_PATH_SAMTOOLS_SORT = "sort"
PROGRAM_PATH_SAMTOOLS_INDEX = "index"
PROGRAM_PATH_SAMTOOLS_DEPTH = "depth"
PROGRAM_PATH_ANGSD = config['tools']['angsd']
PROGRAM_PATH_SEQKIT = config['tools']['seqkit']
PROGRAM_PATH_SEQKIT_STATS = "stats"
