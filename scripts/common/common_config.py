import os
from datetime import datetime
import logging
import common.common_constants as common_constants
import common.common_logging as common_logging
import common.config_manager as config_manager 
from common.common_config_enumerations import ConfigSettings

from enum import Enum

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


def get_config_value(*keys, default=None):
    current_value = config # Access the module-level config
    for key in keys:
        if isinstance(current_value, dict):
            current_value = current_value.get(key, {})
        else:
            return default
    return current_value if current_value != {} else default

def is_setting_enabled(*keys):
    # Navigate to the path and get the value of the 'enabled' key, defaulting to True if not found
    return get_config_value(*keys, default={}).get('enabled', True)

def get_processing_settings(process_key: Enum, species: str = None):
  
    process_key_str = process_key.value
   
    # 1. Construct path for general settings (under 'processing')
    general_path = [ConfigSettings.PROCESSING.value, process_key_str]

    # 2. Retrieve general settings
    general_settings = get_config_value(*general_path, default={})

    # 3. Initialize species settings dictionary
    species_settings = {}

    # 4. If species is provided, construct path and retrieve species-specific settings
    if species:
        species_path = [ConfigSettings.SPECIES.value, species, ConfigSettings.PROCESSING.value, process_key_str]
        species_settings = get_config_value(*species_path, default={})

    # 5. Merge settings: general_settings first, then species_settings to overwrite
    combined_settings = {**general_settings, **species_settings}

    # 6. Ensure the result is a dictionary
    return combined_settings if isinstance(combined_settings, dict) else {}


PATH_ADNA_PROJECT = config['path_adna_project']

# config
THREADS_DEFAULT = get_config_value('threads_default', default=5)

# species folders
FOLDER_SPECIES = list(config['species'].keys())

# program related constants
PROGRAM_PATH_FASTP = get_config_value(ConfigSettings.TOOLS.value, 'fastp', default='fastp')
PROGRAM_PATH_MULTIQC = get_config_value(ConfigSettings.TOOLS.value, 'multiqc', default='multiqc')
PROGRAM_PATH_FASTQC = get_config_value(ConfigSettings.TOOLS.value, 'fastqc', default='fastqc')
PROGRAM_PATH_BEDTOOLS = get_config_value(ConfigSettings.TOOLS.value, 'bedtools', default='bedtools')
PROGRAM_PATH_BAMTOBED = "bamtobed"
PROGRAM_PATH_BWA = get_config_value(ConfigSettings.TOOLS.value, 'bwa', default='bwa')
PROGRAM_PATH_BWA_MEM = "mem"
PROGRAM_PATH_BWA_INDEX = "index"
PROGRAM_PATH_SAMTOOLS = get_config_value(ConfigSettings.TOOLS.value, 'samtools', default='samtools')
PROGRAM_PATH_SAMTOOLS_FAIDX =  "faidx"
PROGRAM_PATH_SAMTOOLS_VIEW =  "view"
PROGRAM_PATH_SAMTOOLS_SORT = "sort"
PROGRAM_PATH_SAMTOOLS_INDEX = "index"
PROGRAM_PATH_SAMTOOLS_DEPTH = "depth"
PROGRAM_PATH_ANGSD = get_config_value(ConfigSettings.TOOLS.value, 'angsd', default='angsd')
PROGRAM_PATH_SEQKIT = get_config_value(ConfigSettings.TOOLS.value, 'seqkit', default='seqkit')
PROGRAM_PATH_SEQKIT_STATS = "stats"
PROGRAM_PATH_CENTRIFUGE = get_config_value(ConfigSettings.TOOLS.value, 'centrifuge', default='centrifuge')
PROGRAM_PATH_KRAKEN = get_config_value(ConfigSettings.TOOLS.value, 'kraken', default='kraken2')
PROGRAM_PATH_MAPDAMAGE = get_config_value(ConfigSettings.TOOLS.value, 'mapdamage', default='mapDamage')

