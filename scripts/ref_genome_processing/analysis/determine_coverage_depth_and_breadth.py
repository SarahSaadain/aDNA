import os
import subprocess
import pandas as pd

from multiprocessing import Pool, cpu_count

from common_aDNA_scripts import *

import ref_genome_processing.helpers.ref_genome_processing_helper as ref_genome_processing_helper

def execute_samtools_detpth(input_file: str, coverage_output_file: str):

    print_info(f"Executing samtools depth for {input_file}")

    if not os.path.exists(input_file):
        raise Exception(f"Input file {input_file} does not exist!")

    if os.path.exists(coverage_output_file):
        print_info(f"Output file {coverage_output_file} already exists! Skipping!")
        return

    command = f"{PROGRAM_PATH_SAMTOOLS} {PROGRAM_PATH_SAMTOOLS_DEPTH} -a {input_file} > {coverage_output_file}"
    print_debug(f"Samtools depth command: {command}")

    try:
        result = subprocess.run(command, shell=True,  check=True  )
        print_success(f"Samtools depth complete for {input_file}")
    except Exception as e:
        print_error(f"Failed to execute samtools depth: {e}")

def analyze_coverage_file(coverage_file, depth_breath_output_folder):
    """
    Performs extended analysis on a single coverage file.  This is a helper
    function to be used with multiprocessing.
    """
    coverage_file_base_name = get_filename_from_path(coverage_file)
    analysis_file = coverage_file_base_name.replace(FILE_ENDING_SAMTOOLS_DEPTH_TSV, FILE_ENDING_ANALYSIS_TSV)
    analysis_file_path = os.path.join(depth_breath_output_folder, analysis_file)

    if os.path.exists(analysis_file_path):
        print_info(f"Analysis file {analysis_file_path} already exists! Skipping extended analysis for {coverage_file}.")
        return  # Important: Exit the function, not the whole script

    extended_analysis(coverage_file, analysis_file_path)
    print_info(f"Finished analysis of {coverage_file}") # Add print here

def extended_analysis(coverage_file: str, analysis_file_path: str):

    print_info(f"Performing extended analysis for {coverage_file}")

    if not os.path.exists(coverage_file):
        print_error(f"Coverage file {coverage_file} does not exist! Skipping analysis.")
        return

    if os.path.exists(analysis_file_path):
        print_info(f"Output file {analysis_file_path} already exists! Skipping!")
        return

     #read tsv into dataframe
    print_debug(f"Reading coverage file {coverage_file} into DataFrame ...")
    df = pd.read_csv(coverage_file, sep="\t", header=None, names=["scaffold", "position", "depth"])

    if df.empty:
        print_warning(f"Coverage file {coverage_file} is empty or malformed. Skipping analysis.")
        return

    # Group by scaffold and calculate metrics
    print_debug(f"Grouping by scaffold and calculating metrics ...")
    summary = df.groupby("scaffold").agg(
        avg_depth=("depth", "mean"),
        max_depth=("depth", "max"),
        covered_bases=("depth", lambda x: (x > 0).sum()),
        total_bases=("depth", "count")
    )

    # Compute coverage percentage
    print_debug(f"Calculating coverage percentage ...")
    summary["percent_covered"] = (summary["covered_bases"] / summary["total_bases"]) * 100

    # Save to file
    print_debug(f"Saving summary to file {analysis_file_path} ...")
    summary.to_csv(analysis_file_path, sep="\t")

    print_success(f"Extended analysis complete for {coverage_file}")


def determine_coverage_depth_and_breath(species: str):
    """
    Orchestrates the coverage depth and breadth analysis for a single species.
    Executes samtools depth, performs extended analysis, and combines results.
    """
    print_info(f"Processing coverage depth and breadth for species: {species}")

    try:
        ref_genome_list = ref_genome_processing_helper.get_reference_genome_file_list_for_species(species)
    except Exception as e:
        print_error(f"Failed to get reference genome files for species {species}: {e}")
        return

    for ref_genome_tuple in ref_genome_list:

        # ref_genome is a tuple of (ref_genome_name without extension, ref_genome_path)
        ref_genome_id = ref_genome_tuple[0]
        #ref_genome_path = ref_genome_tuple[1]

        print_info(f"Processing coverage depth and breadth for reference genome: {ref_genome_id}")

        # Step 1: Execute samtools depth for each BAM file
        execute_samtools_depth_for_species(species, ref_genome_id)

        # Step 2: Perform extended analysis on each coverage file
        perform_extended_analysis_for_species(species, ref_genome_id)

        # Step 3: Combine the individual analysis files
        combine_analysis_files(species, ref_genome_id)

    print_info(f"Coverage depth and breadth processing complete for species: {species}")

def execute_samtools_depth_for_species(species: str, reference_genome_id: str):
    """
    Finds all sorted BAM files for a species and executes samtools depth on each.
    """
    print_info(f"Executing samtools depth for all BAM files for species: {species}")

    mapped_folder = get_folder_path_species_processed_refgenome_mapped(species, reference_genome_id)
    list_of_bam_files = get_files_in_folder_matching_pattern(mapped_folder, f"*{FILE_ENDING_SORTED_BAM}")

    if len(list_of_bam_files) == 0:
        print_warning(f"No mapped BAM files found in {mapped_folder} for species {species}. Skipping samtools depth execution.")
        return

    print_debug(f"Found {len(list_of_bam_files)} BAM files for species {species}")
    print_debug(f"BAM files: {list_of_bam_files}")

    depth_breath_output_folder = get_folder_path_species_processed_refgenome_coverage(species, reference_genome_id)

       # Create a pool of worker processes.
    num_processes = THREADS_DEFAULT
    with Pool(processes=num_processes) as pool:
        # Create a list of tuples, where each tuple contains the arguments
        # for the process_bam_file function.
        tasks = [(bam_file, depth_breath_output_folder) for bam_file in list_of_bam_files]
        pool.starmap(process_bam_file, tasks)

    print_info(f"Finished executing samtools depth for species {species}")

def process_bam_file(mapped_bam_file, depth_breath_output_folder):
    """
    Executes samtools depth on a single BAM file.  This helper function is for use with multiprocessing.
    """
    mapped_bam_file_base_name = get_filename_from_path(mapped_bam_file)
    coverage_file_name = mapped_bam_file_base_name.replace(FILE_ENDING_SORTED_BAM, FILE_ENDING_SAMTOOLS_DEPTH_TSV)
    coverage_output_file = os.path.join(depth_breath_output_folder, coverage_file_name)
    execute_samtools_detpth(mapped_bam_file, coverage_output_file)
    
    print_info(f"Finished samtools depth for {mapped_bam_file}") 

def perform_extended_analysis_for_species(species: str, reference_genome_id: str):
    """
    Finds all samtools depth output files for a species and performs extended analysis on each.
    """
    print_info(f"Performing extended analysis on depth files for species: {species}")

    depth_breath_output_folder = get_folder_path_species_processed_refgenome_coverage(species, reference_genome_id)
    list_of_coverage_files = get_files_in_folder_matching_pattern(depth_breath_output_folder, f"*{FILE_ENDING_SAMTOOLS_DEPTH_TSV}")

    if len(list_of_coverage_files) == 0:
        print_warning(f"No samtools depth files found in {depth_breath_output_folder} for species {species}. Skipping extended analysis.")
        return

    print_debug(f"Found {len(list_of_coverage_files)} coverage files for species {species}")
    print_debug(f"Coverage files: {list_of_coverage_files}")

    # Create a pool of worker processes.  Use a context manager (with)
    # to ensure the pool is properly closed.
    # You can specify the number of processes here.
    num_processes = THREADS_DEFAULT
    with Pool(processes=num_processes) as pool:
        # Create a list of tuples, where each tuple contains the arguments
        # for the analyze_coverage_file function.
        tasks = [(file, depth_breath_output_folder) for file in list_of_coverage_files]
        # Use pool.starmap to apply the function to each set of arguments.
        # starmap unpacks the tuples and passes the elements as separate arguments.
        pool.starmap(analyze_coverage_file, tasks)

    print_info(f"Finished performing extended analysis for species {species}")

def combine_analysis_files(species: str, reference_genome_id: str):
    """
    Combines the individual extended analysis files for a species into a single summary file.
    Calculates overall metrics per BAM file from the per-scaffold analysis results.
    """
    print_info(f"Combining extended analysis files for species: {species}")
    individual_files_folder = get_folder_path_species_processed_refgenome_coverage(species, reference_genome_id)
    analysis_folder = get_folder_path_species_results_refgenome_coverage(species, reference_genome_id)
    
    combined_file_path = os.path.join(analysis_folder, f"{species}_combined_coverage_analysis{FILE_ENDING_CSV}") # Using CSV for combined output

    # Find all individual analysis files
    individual_analysis_files = get_files_in_folder_matching_pattern(individual_files_folder, f"*{FILE_ENDING_ANALYSIS_TSV}")

    if not individual_analysis_files:
        print_warning(f"No individual analysis files found to combine for species {species} in {analysis_folder}. Skipping combining step.")
        return

    print_debug(f"Found {len(individual_analysis_files)} analysis files to combine for species {species}")
    print_debug(f"Analysis files: {individual_analysis_files}")

    combined_data = []

    for analysis_file in individual_analysis_files:
        try:
            # Read the individual analysis file (per-scaffold summary)
            # Assuming the analysis file has columns: scaffold, avg_depth, max_depth, covered_bases, total_bases, percent_covered
            df_analysis = pd.read_csv(analysis_file, sep="\t")

            if df_analysis.empty:
                print_warning(f"Analysis file {analysis_file} is empty. Skipping.")
                continue

            # Calculate overall metrics for this BAM file from the per-scaffold data
            # Overall average depth: weighted average by total bases per scaffold
            total_bases_sum = df_analysis['total_bases'].sum()
            overall_avg_depth = (df_analysis['avg_depth'] * df_analysis['total_bases']).sum() / total_bases_sum if total_bases_sum > 0 else 0

            # Overall max depth: max of max depths across scaffolds
            overall_max_depth = df_analysis['max_depth'].max() if not df_analysis['max_depth'].empty else 0

            # Overall covered bases: sum of covered bases across scaffolds
            overall_covered_bases = df_analysis['covered_bases'].sum()

            # Overall total bases: sum of total bases across scaffolds
            overall_total_bases = total_bases_sum

            # Overall percent covered: total covered bases / total bases * 100
            overall_percent_covered = (overall_covered_bases / overall_total_bases) * 100 if overall_total_bases > 0 else 0

            # Determine the original BAM filename from the analysis filename
            # Use the new helper function
            original_bam_base = get_filename_from_path(analysis_file).replace(FILE_ENDING_ANALYSIS_TSV, "")
            original_bam_filename = original_bam_base + FILE_ENDING_SORTED_BAM


            # Append the overall metrics for this BAM file to the combined data list
            combined_data.append({
                "Filename": original_bam_filename,
                "OverallAvgDepth": overall_avg_depth,
                "OverallMaxDepth": overall_max_depth,
                "OverallCoveredBases": overall_covered_bases,
                "OverallTotalBases": overall_total_bases,
                "OverallPercentCovered": overall_percent_covered
            })

        except FileNotFoundError:
            print_error(f"Analysis file not found: {analysis_file}. Skipping.")
        except pd.errors.EmptyDataError:
            print_warning(f"Analysis file is empty or malformed: {analysis_file}. Skipping.")
        except Exception as e:
            print_error(f"An error occurred processing analysis file {analysis_file}: {e}")

    if not combined_data:
        print_warning(f"No valid data found in analysis files to create combined summary for species {species}.")
        return

    # Create a DataFrame from the combined data
    df_combined = pd.DataFrame(combined_data)

    # Save the combined DataFrame to a new CSV file
    try:
        df_combined.to_csv(combined_file_path, index=False)
        print_success(f"Successfully created combined coverage analysis file: {combined_file_path}")
    except IOError as e:
        print_error(f"Failed to write combined coverage analysis file at {combined_file_path}: {e}")
    except Exception as e:
        print_error(f"An unexpected error occurred while writing the combined file for {species}: {e}")

def all_species_determine_coverage_depth_and_breath():
    print_execution("Determine coverage depth and breadth for all species")
    for species in FOLDER_SPECIES: 
        determine_coverage_depth_and_breath(species)

    print_info("Finished determining coverage depth and breadth for all species")

def main():
    all_species_determine_coverage_depth_and_breath()

if __name__ == "__main__":
    main()
