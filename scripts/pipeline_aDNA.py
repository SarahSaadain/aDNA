from common_aDNA_scripts import *

import adapter_remove_aDNA as adapter_remove
import prepare_species_for_processing as prepare
import prepare_reads_for_GD as prepare_reads_for_GD
import execute_fastqc as execute_fastqc
import execute_multiqc as execute_multiqc
import execute_fastp_adapter_remove_and_merge as execute_fastp_adapter_remove_and_merge
import polish_fastx_quality_filter as polish_fastx_quality_filter
import polish_sga_index_and_remove_duplicates as polish_sga_index_and_remove_duplicates
import polish_fastx_trimmer as polish_fastx_trimmer

def run_pipeline():
    
    prepare.all_species_prepare()
    execute_fastqc.all_species_fastqc_raw()
    execute_multiqc.all_species_multiqc_raw()

    #prepare_reads_for_GD.all_species_prepare_reads_for_GD()
    prepare_reads_for_GD.species_prepare_reads_for_GD(FOLDER_BGER)

    #adapter_remove.all_species_adapter_remove()
    execute_fastp_adapter_remove_and_merge.all_species_fastp_adapter_remove_and_merge()
    execute_fastqc.all_species_fastqc_adapter_removed()
    execute_multiqc.all_species_multiqc_adapter_removed()

    polish_fastx_quality_filter.all_species_fastx_quality_filter()
    execute_fastqc.all_species_fastqc_quality_filtered()
    execute_multiqc.all_species_multiqc_quality_filtered()

    polish_sga_index_and_remove_duplicates.all_species_polish_sga()
    execute_fastqc.all_species_fastqc_duplicates_removed()
    execute_multiqc.all_species_multiqc_duplicates_removed()

    #polish_fastx_trimmer.all_species_fastx_trimmer()
    #execute_fastqc.
    #execute_multiqc.()

def main():
    run_pipeline()

if __name__ == "__main__":  
    main()