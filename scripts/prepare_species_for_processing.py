import contextlib
import io
import os
import importlib.util
from common_aDNA_scripts import *

FILE_NAME_PREPARE_SCRIPT = "prepare.py"

def call_prepare_script(species, prepare_script_full_path):

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
    print(output.getvalue())
        

def all_species_prepare():

    for species in FOLDER_SPECIES: 
        scripts_folder = get_folder_path_species_scripts(species)

        prepare_script_path = os.path.join(scripts_folder, FILE_NAME_PREPARE_SCRIPT)
        call_prepare_script(species, prepare_script_path)
        

def main():
    all_species_prepare()

if __name__ == "__main__":
    main()
