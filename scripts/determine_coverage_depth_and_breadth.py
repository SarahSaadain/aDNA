import os
from common_aDNA_scripts import *

def determine_coverage_depth_and_breath(species):
    ##TODO
    pass

def all_species_determine_coverage_depth_and_breath():
    for species in FOLDER_SPECIES: 
        determine_coverage_depth_and_breath(species)

def main():
    all_species_determine_coverage_depth_and_breath()

if __name__ == "__main__":
    main()
