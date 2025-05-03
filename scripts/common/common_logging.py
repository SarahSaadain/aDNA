import os
import logging
from datetime import datetime


import common.common_folder_functions as common_folder_functions

#####################
# Log
#####################

log_dir = common_folder_functions.get_folder_path_logs()

# Generate a timestamped filename
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
log_filename = os.path.join(log_dir, f'{timestamp}_pipeline.log')

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S (%Z)',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)

# INFO is the default level, so it will log all messages at this level and above (WARNING, ERROR, CRITICAL)
# if you want to log DEBUG messages, change the level to logging.DEBUG
def print_command(subprocess_command: list):  # prints subprocess commands
    logging.info(" ".join(subprocess_command))

def print_info(message: str):
    logging.info(message)

def print_error(message: str):
    logging.error(message)

def print_success(message: str):
    highlight = "***"
    logging.info(f"{highlight} SUCCESS: {message} {highlight}")

def print_warning(message: str):
    logging.warning(message)

def print_debug(message: str):
    logging.debug(message)

def print_execution(message: str):
    print_headline(message)

def print_headline(message: str):
    """Logs a headline message with separators."""
    separator = "=" * (len(message) + 4) # Adjust length as needed
    logging.info(separator)
    logging.info(f"  {message}  ")
    logging.info(separator)