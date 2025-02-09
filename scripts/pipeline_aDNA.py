from common_aDNA_scripts import *

import adapter_remove_aDNA as adapter_remove
import prepare_species_for_processing as prepare
import prepare_reads_for_GD as prepare_reads_for_GD
import execute_multiqc as execute_multiqc

def run_pipeline():
    prepare.all_species_prepare()
    execute_multiqc.all_species_multiqc_raw()

    #prepare_reads_for_GD.all_species_prepare_reads_for_GD()
    prepare_reads_for_GD.species_prepare_reads_for_GD(FOLDER_BGER)

    adapter_remove.all_species_adapter_remove()
    execute_multiqc.all_species_multiqc_trimmed()


def main():
    run_pipeline()

if __name__ == "__main__":  
    main()