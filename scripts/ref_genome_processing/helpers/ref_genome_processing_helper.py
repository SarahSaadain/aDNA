from common_aDNA_scripts import *

def get_reference_genome_file_list_for_species(species: str) -> list[tuple[str, str]]:
 
    # get ref genome
    ref_genome_folder = get_folder_path_species_raw_ref_genome(species)

    # add fna files to reference genome list
    reference_genome_files = get_files_in_folder_matching_pattern(ref_genome_folder, f"*{FILE_ENDING_FNA}")
    # add fasta files to reference genome list
    reference_genome_files += get_files_in_folder_matching_pattern(ref_genome_folder, f"*{FILE_ENDING_FASTA}")

    # add fa files to reference genome list
    reference_genome_files += get_files_in_folder_matching_pattern(ref_genome_folder, f"*{FILE_ENDING_FA}")

    if len(reference_genome_files) == 0:
        raise Exception(f"No reference genome found for species {species}.")
    
    print_debug(f"Found {len(reference_genome_files)} reference genome files for species {species}.")
    print_debug(f"Reference genome files: {reference_genome_files}")

    # return as tuple of (filename without extension, filepath)
    reference_genome_files_with_filename = [(os.path.splitext(os.path.basename(f))[0], f) for f in reference_genome_files]

    return reference_genome_files_with_filename
