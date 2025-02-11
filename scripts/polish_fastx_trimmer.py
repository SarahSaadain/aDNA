import os
from common_aDNA_scripts import *

def fastx_trimmer(species):
    ##TODO
    pass

def all_species_fastx_trimmer():
    for species in FOLDER_SPECIES: 
        fastx_trimmer(species)

def main():
    all_species_fastx_trimmer()

if __name__ == "__main__":
    main()
