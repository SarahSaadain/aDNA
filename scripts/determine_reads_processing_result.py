import io
import os
import subprocess
import pandas as pd

from execute_fastp_adapter_remove_and_merge import get_adapter_removed_path_for_paired_raw_reads
from polish_fastp_quality_filter import get_quality_filtered_path_for_adapter_removed_reads
from polish_fastp_deduplication import get_deduplication_path_for_quality_filtered_reads


from common_aDNA_scripts import *

def execute_seqkit_stats_count_reads(input_file, thread:int = THREADS_DEFAULT) -> int:

    print_info(f"Executing seqkit stats for {input_file}")

    if not os.path.exists(input_file):
        raise Exception(f"Input file {input_file} does not exist!")

    try:
        command = f"seqkit stats --threads {thread} {input_file}"
        result = subprocess.run( command, stdout=subprocess.PIPE, shell=True, check=True)

        # Read output into pandas DataFrame
        output = result.stdout

        # Convert output to a DataFrame
        df = pd.read_csv(io.StringIO(output), sep="\t", skiprows=1)

        # Rename columns
        df.columns = ["file", "format", "type", "num_seqs", "sum_len", "min_len", "avg_len", "max_len"]

        # Convert numeric columns
        df[["num_seqs", "sum_len", "min_len", "avg_len", "max_len"]] = df[["num_seqs", "sum_len", "min_len", "avg_len", "max_len"]].apply(pd.to_numeric)

        print_success(f"Seqkit stats complete for {input_file}: {df["num_seqs"].iloc[0]} reads")

        return df["num_seqs"].iloc[0]
    except Exception as e:
        print_error(f"Failed to execute seqkit stats: {e}")

    return -1
    

def determine_reads_processing_result(species):

    print_info(f"Determine reads processing result for {species}")

    paired_raw_reads = get_raw_paired_reads_list_of_species(species)

    if len(paired_raw_reads) == 0:
        print_warning(f"No raw reads found for species {species}. Skipping.")
        return
    
    # create output dataframe
    output_df = pd.DataFrame(columns=["reads_file", "individual", "protocol", "raw_count", "adapter_removed_count", "quality_filtered_count", "duplicates_removed_count"])

    for raw_read in paired_raw_reads:

        r1_count = execute_seqkit_stats_count_reads(raw_read[0])
        r2_count = execute_seqkit_stats_count_reads(raw_read[1])

        raw_count = r1_count + r2_count

        adapter_removed_file = get_adapter_removed_path_for_paired_raw_reads(species, raw_read)
        adapter_removed_count = execute_seqkit_stats_count_reads(adapter_removed_file)

        quality_filtered_file = get_quality_filtered_path_for_adapter_removed_reads(species, adapter_removed_file)
        quality_filtered_count = execute_seqkit_stats_count_reads(quality_filtered_file)

        duplicates_removed_file = get_deduplication_path_for_quality_filtered_reads(species, quality_filtered_file)
        duplicates_removed_count = execute_seqkit_stats_count_reads(duplicates_removed_file)

        reads_id = raw_read[0].split(".")[0]
        individual = reads_id.split("_")[0]
        protocol = reads_id.split("_")[1]

        #write to a df
        new_row = pd.DataFrame({
            "reads_file": [reads_id],
            "individual": [individual],
            "protocol": [protocol],
            "raw_count": [raw_count],
            "adapter_removed_count": [adapter_removed_count],
            "quality_filtered_count": [quality_filtered_count],
            "duplicates_removed_count": [duplicates_removed_count]
        })
        output_df = pd.concat([output_df, new_row], ignore_index=True)

    output_df.to_csv(get_folder_path_species_results_qc_reads_processing(species), sep="\t", index=False)

    print_info(f"Finished determining reads processing result for {species}")


def all_species_determine_determine_reads_processing_result():
    print_info("Determine coverage depth and breadth for all species")
    for species in FOLDER_SPECIES: 
        determine_reads_processing_result(species)

    print_info("Finished determining coverage depth and breadth for all species")

def main():
    all_species_determine_determine_reads_processing_result()

if __name__ == "__main__":
    main()
