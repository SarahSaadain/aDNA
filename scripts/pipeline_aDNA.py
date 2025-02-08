from common_aDNA_scripts import *

import generate_reads_list as grl
import adapter_remove_aDNA as ar

def main():

    grl.all_species_generate_reads_lists()
    ar.all_species_adapter_remove()


