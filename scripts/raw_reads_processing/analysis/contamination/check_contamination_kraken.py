import os
import subprocess

from common_aDNA_scripts import *

def run_kraken_on_file(species: str, fastq_file_path: str,  Kraken_report_tsv: str, threads: int = THREADS_DEFAULT):
   
    print_info(f"Running Kraken on file: {os.path.basename(fastq_file_path)}")

    # Check if output files already exist
    if os.path.exists(Kraken_report_tsv):
        print_info(f"Output files {Kraken_report_tsv} already exist. Skipping.")
        return
    
    # get the Kraken database path from the config
    Kraken_db = get_processing_settings(RawReadsProcessingSteps.CONTAMINATION_CHECK).get(ContaminationCheckSettings.KRAKEN_DB.value)

    # Ensure Kraken2 database path is set and exists
    if not Kraken_db:
        print_error("Kraken2 database path is not set. Please check your pipeline configuration.")
        return
    
    if not os.path.exists(Kraken_db):
        print_error(f"Kraken2 database path does not exist: {Kraken_db}")
        return

    # Construct the kraken2 command
    # Using --gzip-compressed assumes the input is .gz
    kraken2_command = [
        PROGRAM_PATH_KRAKEN,
        "--db", Kraken_db,
        "--threads", str(threads),
        "--gzip-compressed",
        "--output", Kraken_report_tsv,
        fastq_file_path # Input file
    ]

    print_debug(f"Kraken2 command: {' '.join(kraken2_command)}")

    # Execute the command
    try:
        # Using capture_output=True and text=True to get stdout/stderr in case of errors
        result = subprocess.run(kraken2_command, check=True, capture_output=True, text=True)
        print_success(f"Kraken2 analysis complete for {get_filename_from_path(fastq_file_path)}")
        # Optionally print stdout/stderr for debugging
        # print_debug("Kraken2 stdout:\n" + result.stdout)
        # print_debug("Kraken2 stderr:\n" + result.stderr)
    except subprocess.CalledProcessError as e:
        print_error(f"Kraken2 failed for {get_filename_from_path(fastq_file_path)} with error: {e.returncode}")
        print_error("Kraken2 stdout:\n" + e.stdout)
        print_error("Kraken2 stderr:\n" + e.stderr)
    except FileNotFoundError:
         print_error("Kraken2 command not found. Make sure kraken2 is installed and in your PATH.")
    except Exception as e:
        print_error(f"An unexpected error occurred while running Kraken2 on {get_filename_from_path(fastq_file_path)}: {e}")

def analyze_kraken2_report(report_file_path: str, output_file_path: str):

    print_info(f"Analyzing Kraken2 report: {get_filename_from_path(report_file_path)}")

    # Check if output file already exists
    if os.path.exists(output_file_path):
        print_info(f"Analysis output file {get_filename_from_path(output_file_path)} already exists. Skipping analysis.")
        return

    # Construct the shell command pipeline
    # awk '$1 == "C" {print $3}': Filters lines starting with 'C' and prints the 3rd column (species name)
    # sort: Sorts the species names alphabetically
    # uniq -c: Counts occurrences of each unique species name
    # sort -nr: Sorts the counts in reverse numerical order
    # head -5: Takes the top 5 entries
    analysis_command = f"awk '$1 == \"C\" {{print $3}}' {report_file_path} | sort | uniq -c | sort -nr | head -5 > {output_file_path}"

    print_debug(f"Analysis command: {analysis_command}")

    # Execute the command
    try:
        # Use shell=True because we are using a pipeline with pipes (|) and redirection (>)
        subprocess.run(analysis_command, shell=True, check=True, capture_output=True, text=True)
        print_success(f"Analysis complete. Top 5 species written to {get_filename_from_path(output_file_path)}")
        # Optionally print stdout/stderr for debugging
        # print_debug("Analysis stdout:\n" + result.stdout)
        # print_debug("Analysis stderr:\n" + result.stderr)
    except subprocess.CalledProcessError as e:
        print_error(f"Analysis failed for {get_filename_from_path(report_file_path)} with error: {e.returncode}")
        print_error("Analysis stdout:\n" + e.stdout)
        print_error("Analysis stderr:\n" + e.stderr)
    except Exception as e:
        print_error(f"An unexpected error occurred during analysis of {get_filename_from_path(report_file_path)}: {e}")

def run_Kraken_per_species(species: str):
    print_info(f"Processing species: {species}")

    duplicates_removed_folder = get_folder_path_species_processed_duplicates_removed(species)
    
    fastq_files = get_files_in_folder_matching_pattern(
        duplicates_removed_folder,
        f"*{FILE_ENDING_DUPLICATES_REMOVED_FASTQ_GZ}"
    )

    # if no files are found, skip species
    if not fastq_files:
        print_warning(f"No duplicate removed FASTQ.GZ files found for species {species}. Skipping.")
        return

    print_info(f"Found {len(fastq_files)} relevant FASTQ.GZ files for species {species}")
    print_debug(f"Files found: {fastq_files}")

    # Filter out files that contain "LB" or "EB" (Library Blanks or Extraction Blanks)
    fastq_files_filtered = [
        f for f in fastq_files
        if "LB" not in get_filename_from_path(f) and "EB" not in get_filename_from_path(f)
    ]

    excluded_files = [f for f in fastq_files if f not in fastq_files_filtered]
    if excluded_files:
        print_debug(f"Excluded {len(excluded_files)} files (LB/EB): {[get_filename_from_path(f) for f in excluded_files]}")

    # if no files remain after filtering, skip species
    if not fastq_files_filtered:
        print_warning(f"No FASTQ.GZ files found for species {species} after filtering. Skipping.")
        return

    print_debug(f"Found {len(fastq_files_filtered)} relevant FASTQ.GZ files after filtering")
    print_debug(f"Files to process: {[get_filename_from_path(f) for f in fastq_files_filtered]}")

    # Run Kraken on each filtered file
    for fastq_file in fastq_files_filtered:

        filename_without_ext = get_filename_from_path_without_extension(fastq_file)
        processed_folder = get_folder_path_species_processed_qc_kraken(species)
        results_folder = get_folder_path_species_results_qc_kraken(species)

        # Define output file paths based on the input filename
        kraken_report_tsv = os.path.join(processed_folder, f"{filename_without_ext}{FILE_ENDING_KRAKEN_REPORT_TSV}")
        analysis_output_txt = os.path.join(results_folder, f"{filename_without_ext}{FILE_ENDING_KRAKEN_TOP5_ANALYSIS_TSV}") # Define analysis output path

        run_kraken_on_file(species, fastq_file, kraken_report_tsv)

        analyze_kraken2_report(kraken_report_tsv, analysis_output_txt)

    print_info(f"Finished processing species: {species}")

def all_species_run_Kraken():
    print_execution("Starting Kraken analysis for all species on individual deduplicated FASTQ files.")

    for species in FOLDER_SPECIES:
        run_Kraken_per_species(species)

    print_success("Finished Kraken analysis for all species.")


def main():
    all_species_run_Kraken()

if __name__ == "__main__":
    main()
