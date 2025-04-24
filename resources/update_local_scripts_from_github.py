import os
import requests
import argparse
import sys

def download_files(file_url: str, target_file: str, force_update: bool=False, check_only: bool=False):

    print(f"Checking for changes: {file_url} ...")

    #print(f'Downloading {file_url} to {target_file} ...')
    try:
        file_content = get_remote_file_content(file_url)
        #print(f"Downloaded {file_url}")

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
        print("Update script updated. Please run it again.")
        sys.exit()

    file_list = [
        "scripts/common_aDNA_scripts.py",    
        "scripts/pipeline_aDNA.py",
        "scripts/common/config_manager.py",
        "scripts/common/common_constants.py",
        "scripts/common/common_config.py",
        "scripts/common/common_folder_functions.py",
        "scripts/common/common_helper_functions.py",
        "scripts/common/common_logging.py",
    
        "scripts/raw_reads_processing/quality_checking/execute_multiqc.py",
        "scripts/raw_reads_processing/quality_checking/execute_fastqc.py",
        "scripts/raw_reads_processing/polish_fastp_quality_filter.py",
        "scripts/raw_reads_processing/polish_fastp_deduplication.py",
        "scripts/raw_reads_processing/execute_fastp_adapter_remove_and_merge.py",
        "scripts/raw_reads_processing/prepare_species_for_processing.py",
        "scripts/raw_reads_processing/quality_checking/generate_quality_check_report.py",
        "scripts/raw_reads_processing/analysis/generate_plots_raw_reads_processing.py",
        "scripts/raw_reads_processing/analysis/determine_reads_processing_result.py",
        "scripts/raw_reads_processing/analysis/determine_read_length_distribution.py",
        "scripts/raw_reads_processing/analysis/plots/plot_comparison_reads_before_after_processing.R",
        "scripts/raw_reads_processing/analysis/plots/plot_sequence_length_distribution.R",

        "scripts/ref_genome_processing/map_aDNA_to_refgenome.py",
        "scripts/ref_genome_processing/convert_ref_genome_sam2bam.py",
        "scripts/ref_genome_processing/prepare_species_for_map_to_ref_genome.py",
        "scripts/ref_genome_processing/prepare_ref_genome_for_mapping.py",
        "scripts/ref_genome_processing/analysis/extract_special_sequences.py",
        "scripts/ref_genome_processing/analysis/determine_endogenous_reads.py",
        "scripts/ref_genome_processing/analysis/determine_coverage_depth_and_breadth.py",
        "scripts/ref_genome_processing/analysis/generate_plots_ref_genome_processing.py",
        "scripts/ref_genome_processing/analysis/plots/plot_coverage_breadth.R",
        "scripts/ref_genome_processing/analysis/plots/plot_coverage_depth.R",
        "scripts/ref_genome_processing/analysis/plots/plot_endogenous_reads.R",

        "scripts/additional_analysis/species_comparison/analysis/generate_plots_species_compare.py",
        "scripts/additional_analysis/species_comparison/analysis/plots/plot_compare_species_depth_breadth.R",
        "scripts/additional_analysis/species_comparison/analysis/plots/plot_compare_species_endogenous_reads.R",
        "scripts/additional_analysis/species_comparison/analysis/plots/plot_compare_species_reads_before_after_processing.R",

        "scripts/additional_analysis/mtdna_analysis/determine_mtdna_step1_map_to_ref_genome.py",
        "scripts/additional_analysis/mtdna_analysis/determine_mtdna_step2_determine_regions.py",
        "scripts/additional_analysis/mtdna_analysis/determine_mtdna_step3_create_and_map_consensus_sequence.py",
        "scripts/additional_analysis/mtdna_analysis/determine_mtdna_step4_extract_coi_regions.py",
        "scripts/additional_analysis/mtdna_analysis/determine_mtdna_step5_check_extracted_regions_for_content.py",

        #"Bger/scripts/prepare_for_processing.py",
        #"Bger/resources/mapping_folder_to_lane.csv",
        #"Bger/resources/mapping_runID_to_name.csv",
        "Bger/raw/mtdna/marker_coi.fasta",

        "trial_Mmus/raw/mtdna/marker_12S_rRNA.fasta",
        "trial_Mmus/raw/mtdna/marker_16S_rRNA.fasta",
        "trial_Mmus/raw/mtdna/marker_ATP6.fasta",
        "trial_Mmus/raw/mtdna/marker_ATP8.fasta",
        "trial_Mmus/raw/mtdna/marker_COI.fasta",
        "trial_Mmus/raw/mtdna/marker_COX2.fasta",
        "trial_Mmus/raw/mtdna/marker_COX3.fasta",
        "trial_Mmus/raw/mtdna/marker_Cyb561.fasta",
        "trial_Mmus/raw/mtdna/marker_cytochrome_b.fasta",
        "trial_Mmus/raw/mtdna/marker_ND1.fasta",
        "trial_Mmus/raw/mtdna/marker_ND2.fasta",
        "trial_Mmus/raw/mtdna/marker_ND3.fasta",
        "trial_Mmus/raw/mtdna/marker_ND4.fasta",
        "trial_Mmus/raw/mtdna/marker_ND4L.fasta",
        "trial_Mmus/raw/mtdna/marker_ND5.fasta",
        "trial_Mmus/raw/mtdna/marker_ND6.fasta",
        "trial_Mmus/raw/mtdna/marker_Ptgs2.fasta",

        "trial_Phortica/raw/mtdna/marker_28S.fasta",
        "trial_Phortica/raw/mtdna/marker_COI3.fasta",
        "trial_Phortica/raw/mtdna/marker_COI5.fasta",
        "trial_Phortica/raw/mtdna/marker_NC_081078.fasta",
        "trial_Phortica/raw/mtdna/marker_ND2.fasta",

        "resources/rename.py",
        "resources/rename.csv"



    ]

    for file in file_list:
        file_url = f"{base_url}/{file}"
        target_file = os.path.join(os.getcwd(), file)
        download_files(file_url, target_file, args.force_update)

if __name__ == "__main__":
    main()
