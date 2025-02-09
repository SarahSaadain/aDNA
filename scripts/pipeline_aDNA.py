from common_aDNA_scripts import *

import generate_reads_list as generate_reads_list
#import adapter_remove_aDNA as adapter_remove
import prepare_species_for_processing as prepare
import prepare_reads_for_GD as prepare_reads_for_GD
#import determine_poly_nt_count as determine_poly_nt_count

def run_pipeline():
    prepare.all_species_prepare()
    generate_reads_list.all_species_generate_reads_lists(overwrite = True)
    prepare_reads_for_GD.all_species_prepare_reads_for_GD()
    
    #adapter_remove.all_species_adapter_remove()
    #determine_poly_nt_count.all_species_poly_count()


def main():
    run_pipeline()

if __name__ == "__main__":  
    main()