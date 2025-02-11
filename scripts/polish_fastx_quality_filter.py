import os
from common_aDNA_scripts import *

def fastx_quality_filter(species):
    ##TODO
    pass

def all_species_fastx_quality_filter():
    for species in FOLDER_SPECIES: 
        fastx_quality_filter(species)

def main():
    all_species_fastx_quality_filter()

if __name__ == "__main__":
    main()
