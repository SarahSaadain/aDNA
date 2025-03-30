import contextlib
import io
import os
import importlib.util
from common_aDNA_scripts import *

FILE_NAME_PREPARE_SCRIPT = "prepare_for_processing.py"

def call_prepare_script(species: str, prepare_script_full_path: str):

    # Check if prepare.py exists
    if not os.path.exists(prepare_script_full_path):
        print_info(f"No {FILE_NAME_PREPARE_SCRIPT} script found for species {species}.")
        return
    
    print_info(f"Running {FILE_NAME_PREPARE_SCRIPT} script for species {species}.")

    # Import prepare.py
    spec = importlib.util.spec_from_file_location("prepare", prepare_script_full_path)
    prepare_module = importlib.util.module_from_spec(spec)
    
    # Execute prepare.py and capture its output
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        spec.loader.exec_module(prepare_module)
        prepare_module.prepare()

    # Print the captured output
    print_info(output.getvalue())

    print_info(f"Finished running {FILE_NAME_PREPARE_SCRIPT} script for species {species}.")
        

def all_species_prepare():

    print_execution(f"Running {FILE_NAME_PREPARE_SCRIPT} for all species")

    for species in FOLDER_SPECIES: 
        scripts_folder = get_folder_path_species_scripts(species)

        prepare_script_path = os.path.join(scripts_folder, FILE_NAME_PREPARE_SCRIPT)
        call_prepare_script(species, prepare_script_path)

    print_info(f"Finished running {FILE_NAME_PREPARE_SCRIPT} for all species")
        

def main():
    all_species_prepare()

if __name__ == "__main__":
    main()
