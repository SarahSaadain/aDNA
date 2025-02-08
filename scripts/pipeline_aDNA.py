from common_aDNA_scripts import *

import generate_reads_list as generate_reads_list
import adapter_remove_aDNA as adapter_remove
import prepare_species_for_processing as prepare

def run_pipeline():
    prepare.all_species_prepare()
    generate_reads_list.all_species_generate_reads_lists(overwrite = True)
    adapter_remove.all_species_adapter_remove()

def main():
    run_pipeline()

if __name__ == "__main__":  
    main()