import os
from datetime import datetime
import logging
import common.common_constants as common_constants
import common.common_logging as common_logging
import common.config_manager as config_manager 

# Load the configuration file (only once)
try:
    common_logging.print_execution("Loading configuration file ...")
    # Path to your config file. we assume it is in the same directory where this script is located
    config_file_path = 'config.yaml'  

    common_logging.print_info(f"Loading config file: {config_file_path}")

    config = config_manager.load_config(config_file_path)  # Or however you specify the path
    
    common_logging.print_info("Config loaded successfully.")
    
    common_logging.print_info(f"Project path: {config['path_adna_project']}")
    common_logging.print_info(f"Species: {config['species'].keys()}")
    common_logging.print_info(f"Threads default: {config['threads_default']}")

    # Set up logging based on the config
    # Assuming the config has a 'log_level' key
    # and you want to set the logging level accordingly#
    # --- Update Log Level (if in config) ---
    if 'log_level' in config:
        log_level_str = config.get("log_level", "INFO").upper()
        log_level = getattr(logging, log_level_str, common_logging.print_info)

        # update the logging level
        logging.getLogger().setLevel(log_level)
        common_logging.print_info(f"Log level set to {log_level_str}")

    # --- Add File Handler ---
    log_dir = os.path.join(config['path_adna_project'], common_constants.FOLDER_LOGS)
    os.makedirs(log_dir, exist_ok=True)

    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_filename = os.path.join(log_dir, f'{timestamp}_pipeline.log')

    common_logging.print_info(f"Log file: {log_filename}")

    file_handler = logging.FileHandler(log_filename)
    file_handler.setFormatter(logging.Formatter(common_logging.LOG_FORMAT, datefmt=common_logging.LOG_DATE_FORMAT))
    
    logging.getLogger().addHandler(file_handler)

    common_logging.print_debug(f"Loaded Config: {config}") 

except FileNotFoundError:
    common_logging.print_error("Config file not found.  Exiting.")
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
