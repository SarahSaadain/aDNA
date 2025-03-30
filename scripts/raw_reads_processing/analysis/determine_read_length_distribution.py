import os
import pandas as pd

import gzip
from collections import Counter
from Bio import SeqIO

from raw_reads_processing.execute_fastp_adapter_remove_and_merge import get_adapter_removed_path_for_paired_raw_reads
from raw_reads_processing.polish_fastp_quality_filter import get_quality_filtered_path_for_adapter_removed_reads
from raw_reads_processing.polish_fastp_deduplication import get_deduplication_path_for_quality_filtered_reads


from common_aDNA_scripts import *


def get_read_length_distribution(fastq_file: str) -> Counter:
    read_lengths = Counter()

    with gzip.open(fastq_file, "rt") as handle:
        for record in SeqIO.parse(handle, "fastq"):
            read_lengths[len(record.seq)] += 1  # Count occurrences of each read length

    return read_lengths
    
def get_file_name_read_length_distribution(species: str) -> str:
    return f"{species}_read_length_distribution{FILE_ENDING_TSV}"

def determine_read_length_distribution(species: str):

    print_info(f"Determine read length distribution for {species}")

    all_dfs = []  # List to store DataFrames for each read file

    raw_reads = get_files_in_folder_matching_pattern(get_folder_path_species_raw_reads(species), FILE_PATTERN_R1_FASTQ_GZ)

    if len(raw_reads) == 0:
        print_warning(f"No raw reads found for species {species}. Skipping.")
        return
    
    output_file_path = os.path.join(get_folder_path_species_results_qc_read_length_distribution(species),  get_file_name_read_length_distribution(species))

    if os.path.exists(output_file_path):
        print_info(f"Reads length distribution file already exists for species {species}. Skipping.")
        return
    
    for raw_read in raw_reads:

        print_info(f"Processing read file {raw_read}")
        raw_distribution = get_read_length_distribution(raw_read)
        #r2_count = execute_seqkit_stats_count_reads(raw_read[1])
        
        # [] to define its a list of ome entry, as the adapter removed still has R1 and R2 (later we have only one file as its merged)
        adapter_removed_file = get_adapter_removed_path_for_paired_raw_reads(species, [raw_read])
        print_info(f"Processing adapter removed file {adapter_removed_file}")
        adapter_removed_distribution = get_read_length_distribution(adapter_removed_file)

        #relies on script before
        quality_filtered_file = get_quality_filtered_path_for_adapter_removed_reads(species, adapter_removed_file)
        print_info(f"Processing quality filtered file {quality_filtered_file}")
        quality_filtered_distribution = get_read_length_distribution(quality_filtered_file)

        #relies on script before
        duplicates_removed_file = get_deduplication_path_for_quality_filtered_reads(species, quality_filtered_file)
        print_info(f"Processing duplicates removed file {duplicates_removed_file}")
        duplicates_removed_distribution = get_read_length_distribution(duplicates_removed_file)

        print_info("Combining read length distributions")

        reads_file = get_filename_from_path_without_extension(raw_read)
        individual = reads_file.split("_")[0]
        protocol = reads_file.split("_")[1]

        # Convert to DataFrames
        df_raw = pd.DataFrame(raw_distribution.items(), columns=["read_length", "read_count_raw"])
        df_adapter = pd.DataFrame(adapter_removed_distribution.items(), columns=["read_length", "read_count_adapter_removed"])
        df_quality = pd.DataFrame(quality_filtered_distribution.items(), columns=["read_length", "read_count_quality_filtered"])
        df_dedup = pd.DataFrame(duplicates_removed_distribution.items(), columns=["read_length", "read_count_duplicates_removed"])

        # Merge on read_length (Outer Join)
        # merges the raw, adapter removed, quality filtered and duplicates removed DataFrames for one read file
        # on to merge next to each other (based on read_length) instead of on top
        df = df_raw.merge(df_adapter, on="read_length", how="outer") \
                .merge(df_quality, on="read_length", how="outer") \
                .merge(df_dedup, on="read_length", how="outer")

        # Fill NaNs with 0 and ensure integer values
        df = df.fillna(0).astype(int)

        # Add read name as the first column
        df.insert(0, "protocol", protocol)
        df.insert(0, "individual", individual)
        df.insert(0, "reads_file", reads_file)

        # Append to list
        all_dfs.append(df)

    # Concatenate all DataFrames into a single one
    # Concatenates the dataframes of all read files into one dataframe
    final_df = pd.concat(all_dfs, ignore_index=True)
    final_df.to_csv(output_file_path, sep="\t", index=False)

    print_info(f"Finished determining read length distribution for {species}")


def all_species_determine_read_length_distribution():
    print_execution("Determine reads processing result for all species")
    for species in FOLDER_SPECIES: 
        determine_read_length_distribution(species)

    print_success("Finished determining reads processing result for all species")

def main():
    all_species_determine_read_length_distribution()

if __name__ == "__main__":
    main()
