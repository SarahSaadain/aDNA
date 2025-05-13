import os
import subprocess

from common_aDNA_scripts import *


def run_centrifuge_on_file(species: str, fastq_file_path: str, centrifuge_output_txt: str, centrifuge_report_tsv: str, threads: int = THREADS_DEFAULT):
   
    print_info(f"Running Centrifuge on file: {os.path.basename(fastq_file_path)}")

    # get the Centrifuge database path from the config
    centrifuge_db = get_processing_settings(RawReadsProcessingSteps.CONTAMINATION_CHECK).get(ContaminationCheckSettings.CENTRIFUGE_DB.value)

    if not centrifuge_db:
        print_error("Centrifuge database path is not set. Please check your configuration.")
        return

    if not os.path.exists(centrifuge_db):
        print_error(f"Centrifuge database path does not exist: {centrifuge_db}")
        return

    # Construct the centrifuge command
    centrifuge_command = [
        PROGRAM_PATH_CENTRIFUGE,
        "-x", centrifuge_db,
        "-U", fastq_file_path,
        "-S", centrifuge_output_txt,
        "--report-file", centrifuge_report_tsv,
        "-p", str(threads), # Number of threads
        "--verbose",
        "--seed", "999"
    ]

    print_debug(f"Centrifuge command: {' '.join(centrifuge_command)}")

    # Execute the command
    try:
        subprocess.run(centrifuge_command, check=True, capture_output=True, text=True)
        print_success(f"Centrifuge analysis complete for {get_filename_from_path(fastq_file_path)}")
        # Optionally print stdout/stderr for debugging
        # print_debug("Centrifuge stdout:\n" + result.stdout)
        # print_debug("Centrifuge stderr:\n" + result.stderr)
    except subprocess.CalledProcessError as e:
        print_error(f"Centrifuge failed for {get_filename_from_path(fastq_file_path)} with error: {e}")
        print_error("Centrifuge stdout:\n" + e.stdout)
        print_error("Centrifuge stderr:\n" + e.stderr)
    except FileNotFoundError:
         print_error("Centrifuge command not found. Make sure Centrifuge is installed and in your PATH.")
    except Exception as e:
        print_error(f"An unexpected error occurred while running Centrifuge on {get_filename_from_path(fastq_file_path)}: {e}")


def run_centrifuge_per_species(species: str):
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
        print_debug(f"Excluded {len(excluded_files)} files (LB/EB): {[os.path.basename(f) for f in excluded_files]}")

    # if no files remain after filtering, skip species
    if not fastq_files_filtered:
        print_warning(f"No FASTQ.GZ files found for species {species} after filtering. Skipping.")
        return

    print_debug(f"Found {len(fastq_files_filtered)} relevant FASTQ.GZ files after filtering")
    print_debug(f"Files to process: {[os.path.basename(f) for f in fastq_files_filtered]}")

    # Run centrifuge on each filtered file
    for fastq_file in fastq_files_filtered:

        filename_without_ext = get_filename_from_path_without_extension(fastq_file)
        output_folder = get_folder_path_species_results_qc_centrifuge(species)

        # Define output file paths based on the input filename
        centrifuge_output_txt = os.path.join(output_folder, f"{filename_without_ext}{FILE_ENDING_CENTRIFUGE_OUTPUT_TXT}")
        centrifuge_report_tsv = os.path.join(output_folder, f"{filename_without_ext}{FILE_ENDING_CENTRIFUGE_REPORT_TSV}")

         # Check if output files already exist
        if os.path.exists(centrifuge_output_txt) and os.path.exists(centrifuge_report_tsv):
            print_info(f"Output files for {os.path.basename(fastq_file_path)} already exist. Skipping.")
            return

        run_centrifuge_on_file(species, fastq_file, centrifuge_output_txt , centrifuge_report_tsv)

    print_info(f"Finished processing species: {species}")

def all_species_run_centrifuge():
    print_execution("Starting Centrifuge analysis for all species on individual deduplicated FASTQ files.")

    for species in FOLDER_SPECIES:
        run_centrifuge_per_species(species)

    print_success("Finished Centrifuge analysis for all species.")


def main():
    all_species_run_centrifuge()

if __name__ == "__main__":
    main()
