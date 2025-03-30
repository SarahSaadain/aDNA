import os
import requests
import argparse
import sys

def download_files(file_url: str, target_file: str, force_update: bool=False, check_only: bool=False):
    print(f'Downloading {file_url} to {target_file} ...')
    try:
        file_content = get_remote_file_content(file_url)
        print(f"Downloaded {file_url}")

        if os.path.exists(target_file):
            with open(target_file, 'rb') as f:
                if f.read() == file_content:
                    print(f"File {target_file} is up to date")
                    return False  # No update needed

        if check_only:
            return True  # Indicates that the file has changed

        if os.path.exists(target_file) and not force_update:
            print(f"File {target_file} already exists. Do you want to overwrite it? (y/n)")
            choice = input().lower()
            if choice != 'y':
                print("File not overwritten")
                return False

        target_dir = os.path.dirname(target_file)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        with open(target_file, 'wb') as f:
            f.write(file_content)
        print(f"Updated {target_file}")
        return True
    except Exception as e:
        print(f"Failed to download file: {e}")
        return False

def get_remote_file_content(file_url: str):
    response = requests.get(file_url)
    if response.status_code != 200:
        raise Exception('Failed to download file')
    return response.content

def main():
    parser = argparse.ArgumentParser(description="This script downloads the latest version of the scripts from GitHub")
    parser.add_argument("--force_update", "-u", help="force update files", default=False, action="store_true")
    args = parser.parse_args()

    if not os.getcwd().endswith("aDNA"):
        print("Please run this script in the aDNA folder")
        exit()

    base_url = "https://raw.githubusercontent.com/SarahSaadain/aDNA/refs/heads/main"
    update_script = "resources/update_local_scripts_from_github.py"
    update_script_url = f"{base_url}/{update_script}"
    update_script_target = os.path.join(os.getcwd(), update_script)

    print("Checking if update script has changed...")
    if download_files(update_script_url, update_script_target, force_update=args.force_update, check_only=True):
        print("Update script has changed. Updating only itself and exiting.")
        download_files(update_script_url, update_script_target, force_update=True)
        sys.exit()

    file_list = [
        "scripts/common_aDNA_scripts.py",                
        "scripts/determine_coverage_depth_and_breadth.py",
        "scripts/determine_coi_step4_create_and_map_consensus_sequence.py",
        "scripts/map_aDNA_to_refgenome.py",
        "scripts/execute_multiqc.py",
        "scripts/execute_fastqc.py",
        "scripts/pipeline_aDNA.py",
        "scripts/polish_fastp_quality_filter.py",
        "scripts/polish_fastp_deduplication.py",
        "scripts/execute_fastp_adapter_remove_and_merge.py",
        "scripts/convert_sam2bam.py",
        "scripts/extract_special_sequences.py",
        "scripts/determine_endogenous_reads.py",
        "scripts/determine_reads_processing_result.py",
        "scripts/determine_read_length_distribution.py",
        "scripts/generate_quality_check_report.py",
        "scripts/prepare_reads_for_GD.py",
        "scripts/prepare_species_for_processing.py",
        "scripts/prepare_species_for_map_to_ref_genome.py",
        "scripts/prepare_ref_genome_for_mapping.py",
        "scripts/generate_plots.py",
        "scripts/generate_plots_species_compare.py",

        "scripts/plots/plot_comparison_reads_before_after_processing.R",
        "scripts/plots/plot_coverage_breadth.R",
        "scripts/plots/plot_coverage_depth.R",
        "scripts/plots/plot_endogenous_reads.R",
        "scripts/plots/plot_sequence_length_distribution.R",
        "scripts/plots/plot_compare_species_depth_breadth.R",
        "scripts/plots/plot_compare_species_endogenous_reads.R",
        "scripts/plots/plot_compare_species_reads_before_after_processing.R",

        "scripts/mtdna_analysis/determine_mtdna_step1_map_to_ref_genome.py",
        "scripts/mtdna_analysis/determine_mtdna_step2_determine_regions.py",
        "scripts/mtdna_analysis/determine_mtdna_step3_create_and_map_consensus_sequence.py",
        "scripts/mtdna_analysis/determine_mtdna_step4_extract_coi_regions.py",

        "Bger/scripts/prepare_for_processing.py",
        "Bger/resources/mapping_folder_to_lane.csv",
        "Bger/resources/mapping_runID_to_name.csv",

        "resources/rename.py",
        "resources/rename.csv"
    ]

    for file in file_list:
        file_url = f"{base_url}/{file}"
        target_file = os.path.join(os.getcwd(), file)
        download_files(file_url, target_file, args.force_update)

if __name__ == "__main__":
    main()
