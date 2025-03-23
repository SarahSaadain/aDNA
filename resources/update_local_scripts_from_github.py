import os
import requests
import argparse

def download_files(file_url, target_file, force_update=False):

    print(f'Downloading {file_url} to {target_file} ...')

    try:
        # Download the file
        file_content = get_remote_file_content(file_url)

        print(f"Downloaded {file_url}")
        #print(f"Content: {file_content}")

        #check if content of the file is up to date 
        if os.path.exists(target_file):
            with open(target_file, 'rb') as f:
                if f.read() == file_content:
                    print(f"File {target_file} is up to date")
                    return
                
        # if file already exists and must be update. get confirmation by the user
        if os.path.exists(target_file) and not force_update:
            print(f"File {target_file} already exists. Do you want to overwrite it? (y/n)")
            choice = input().lower()    
            if choice != 'y':
                print("File not overwritten")    
                return
            
        #check if directory exists, if not create it
        target_dir = os.path.dirname(target_file)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        # Save the file to the target directory
        with open(target_file, 'wb') as f:
            f.write(file_content)
    except Exception as e:
        print(f"Failed to download file: {e}")

def get_remote_file_content(file_url):
    response = requests.get(file_url)
    if response.status_code != 200:
        raise Exception('Failed to download file')
    return response.content

def main():

    #argparse to allow user to force update files. also provide information about the script

    parser = argparse.ArgumentParser(description="This script downloads the latest version of the scripts from GITHub")
    parser.add_argument("--force_update", "-u", help="force update files", default=False, action="store_true")
    args = parser.parse_args()
    
    # check if script is run in the folder aDNA
    if not os.getcwd().endswith("aDNA"):
        print("Please run this script in the aDNA folder")
        exit()

    if args.force_update:
        print("Forcing update of all files")
    

    # Example usage:
    path = "https://raw.githubusercontent.com/SarahSaadain/aDNA/refs/heads/main"

    file_list = [
        #'scripts/adapter_remove_aDNA.py',
        "scripts/common_aDNA_scripts.py",
        #"scripts/determine_poly_nt_count.py",
        "scripts/determine_coi_step1_map_to_ref_genome.py",
        "scripts/determine_coi_step2_determine_regions.py",
        "scripts/determine_coi_step3_extract_coi_regions.py",
        "scripts/determine_coverage_depth_and_breadth.py",
        "scripts/determine_coi_step4_create_and_map_consensus_sequence.py",
        #"scripts/extract_most_common_sequence_to_fasta.py"
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
        "scripts/generate_plots_compare.py",

        "scripts/plots/plot_comparison_reads_before_after_processing.R",
        "scripts/plots/plot_coverage_breadth.R",
        "scripts/plots/plot_coverage_depth.R",
        "scripts/plots/plot_endogenous_reads.R",
        "scripts/plots/plot_sequence_length_distribution.R",
        "scripts/plots/plot_compare_species_depth_breadth.R",
        "scripts/plots/plot_compare_species_endogenous_reads.R",
        "scripts/plots/plot_compare_species_reads_before_after_processing.R",

        "Bger/scripts/prepare_for_processing.py",
        "Bger/resources/mapping_folder_to_lane.csv",
        "Bger/resources/mapping_runID_to_name.csv",

        "resources/update_local_scripts_from_github.py",
        "resources/rename.py",
        "resources/rename.csv"

    ]

    for file in file_list:
        file_url = f"{path}/{file}"

        #get path from file
        relative_path = os.path.relpath(file_url, path)

        # set script folder of current folder as target directory
        target_dir = os.path.join(os.getcwd(), relative_path)

        download_files(file_url, target_dir, args.force_update)

if __name__ == "__main__":
    main()





