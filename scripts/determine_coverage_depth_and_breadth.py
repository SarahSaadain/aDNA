import os
import subprocess
import pandas as pd


from common_aDNA_scripts import *

def execute_samtools_detpth(input_file, coverage_output_file, thread:int = THREADS_DEFAULT):

    print_info(f"Executing samtools depth for {input_file}")

    if not os.path.exists(input_file):
        raise Exception(f"Input file {input_file} does not exist!")

    if os.path.exists(coverage_output_file):
        print_info(f"Output file {coverage_output_file} already exists! Skipping!")
        return

    try:
        command = f"samtools depth -a {input_file} > {coverage_output_file}"
        result = subprocess.run( command, shell=True,  check=True  )
        print_success(f"Samtools depth complete for {input_file}")
    except Exception as e:
        print_error(f"Failed to execute samtools depth: {e}")

def determine_coverage_depth_and_breath(species):
    print_info(f"Determine coverage depth and breadth for species {species}")

    input_folder = get_folder_path_species_processed_mapped(species)
    list_of_bam_files = get_files_in_folder_matching_pattern(input_folder, f"*{FILE_ENDING_SORTED_BAM}")

    if len(list_of_bam_files) == 0:
        print_warning(f"No mapped files found for species {species}. Skipping.")
        return
    
    depth_breath_output_folder = get_folder_path_species_results_qc_depth_breath(species)

    for mapped_bam_file in list_of_bam_files:

        mapped_bam_file_base_name = os.path.basename(mapped_bam_file)

        coverage_file_name = mapped_bam_file_base_name.replace(FILE_ENDING_SORTED_BAM, "_samtools_depth.tsv")

        coverage_output_file = os.path.join(depth_breath_output_folder, coverage_file_name)

        execute_samtools_detpth(mapped_bam_file, coverage_output_file)


    print_info(f"Performing extended analysis for species {species}")

    list_of_coverage_files = get_files_in_folder_matching_pattern(depth_breath_output_folder, "*_samtools_depth.tsv")

    if len(list_of_coverage_files) == 0:
        print_error(f"No coverage files found for species {species}. Skipping.")
        return
    
    for coverage_file in list_of_coverage_files:
        coverage_file_base_name = os.path.basename(coverage_file)

        analysis_file = coverage_file_base_name.replace("_samtools_depth.tsv", "_analysis.tsv")
        analysis_file_path = os.path.join(depth_breath_output_folder, analysis_file)

        extended_analysis(coverage_file, analysis_file_path)

    print_success(f"Determine coverage depth and breadth for species {species} complete")

def extended_analysis(coverage_file, analysis_file_path):

    print_info(f"Performing extended analysis for {coverage_file}")

    if os.path.exists(analysis_file_path):
        print_info(f"Output file {analysis_file_path} already exists! Skipping!")
        return

     #read tsv into dataframe
    df = pd.read_csv(coverage_file, sep="\t", header=None, names=["scaffold", "position", "depth"])

    # Group by scaffold and calculate metrics
    summary = df.groupby("scaffold").agg(
        avg_depth=("depth", "mean"),
        max_depth=("depth", "max"),
        covered_bases=("depth", lambda x: (x > 0).sum()),
        total_bases=("depth", "count")
    )

    # Compute coverage percentage
    summary["percent_covered"] = (summary["covered_bases"] / summary["total_bases"]) * 100

    # Save to file
    summary.to_csv(analysis_file_path, sep="\t")

    print_success(f"Extended analysis complete for {coverage_file}")


def all_species_determine_coverage_depth_and_breath():
    print_info("Determine coverage depth and breadth for all species")
    for species in FOLDER_SPECIES: 
        determine_coverage_depth_and_breath(species)

    print_info("Finished determining coverage depth and breadth for all species")

def main():
    all_species_determine_coverage_depth_and_breath()

if __name__ == "__main__":
    main()
