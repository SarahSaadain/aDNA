import csv
import os
import gzip
import re
from common_aDNA_scripts import *
import scripts.try_and_error.adapter_remove_aDNA as adapter_remove_script

# Output file for the CSV results
output_file = "poly_counts.csv"


# Function to count poly-nucleotides in a file
def count_polys(file_path, label) -> list:

    print_info(f"Counting poly-nucleotides in {file_path} ...")

    if not os.path.exists(file_path):
        raise Exception(f"File {file_path} does not exist.")

    results = []

    poly_types = ["A", "T", "C", "G"]
    base_filename = os.path.basename(file_path)  # Get only the filename without the path

    with gzip.open(file_path, "rt") as file:
        count_poly_total = 0
        count_poly_lines = 0
        number_of_sequences = 0
        length_of_sequences = 0
        average_length_of_sequences = 0
        for i, line in enumerate(file):
            if i % 4 == 1:
                poly_count_T_total, poly_count_T_lines = get_poly_nt_from_string("T", line)
                poly_count_A_total, poly_count_A_lines = get_poly_nt_from_string("A", line)
                poly_count_C_total, poly_count_C_lines = get_poly_nt_from_string("C", line)
                poly_count_G_total, poly_count_G_lines = get_poly_nt_from_string("G", line)
                 
                number_of_sequences += 1
                length_of_sequences += len(line)

        average_length_of_sequences = length_of_sequences / number_of_sequences

        #add results to list
        results.append([base_filename, label, number_of_sequences, length_of_sequences, average_length_of_sequences, poly_count_T_total, poly_count_T_lines, poly_count_A_total, poly_count_A_lines, poly_count_C_total, poly_count_C_lines, poly_count_G_total, poly_count_G_lines])

    return results

def get_poly_nt_from_string(poly, line, poly_threshold=10):

    count_poly_total = 0
    count_poly_lines = 0    

    matches = re.findall(poly + "{"+poly_threshold+",}", line)
                ## count total number of poly-nucleotides
    count_poly_total += len(matches)
                ## count if at least one poly is found
    if len(matches) > 0:
        count_poly_lines += 1

    return count_poly_total, count_poly_lines

def poly_count_per_species(species):

    results = []
    output_file = os.path.join(get_folder_path_species_results_qualitycontrol_poly_nt(species), f"{species}_poly_counts.csv")

    if os.path.exists(output_file):
        print_warning(f"Output file {output_file} already exists. Skipping.")
        return

    list_of_read_files = get_reads_list_of_species(species)

    if len(list_of_read_files) == 0:
        print_warning(f"No reads found for species {species}.")
        return

     # Each entry in the list contains 2 (paired) files, we need to flatten the list to get a list of all files individually
    file_list = [item for sublist in list_of_read_files for item in sublist]

    # Process before trimming files
    for file in file_list:

        try:
            counts_before_results = count_polys(file, "before")
            results += counts_before_results
        except Exception as e:
            print_error(e)

        try:
            adapter_removed_file = adapter_remove_script.rename_read_file_to_adapter_trimmed(os.path.basename(file))
            adapter_removed_file_path = os.path.join(get_folder_path_species_processed_adapter_removed(species), adapter_removed_file)

            counts_after_results = count_polys(adapter_removed_file_path, "after")

            results += counts_after_results
        except Exception as e:
            print_error(e)


    if len(results) == 0:
        print_warning(f"No results found for species {species}.")
        return

    #write results to csv file
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["filename", "label", "poly", "count_total", "count_lines"])
        writer.writerows(results)

    print(f"Poly-nucleotide counts saved in {output_file}.")

def all_species_poly_count():
    """
    Count poly-nucleotides for all species.
    """
    print("Counting poly-nucleotides for all species")

    # Loop over all species
    for species in FOLDER_SPECIES:
        # Count poly-nucleotides for this species
        poly_count_per_species(species)

def main():
    all_species_poly_count()

if __name__ == "__main__":
    main()

