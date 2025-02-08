import os
import shutil
import subprocess
import sys
import csv

sys.path.insert(0, '../../scripts')
from common_aDNA_scripts import *

MAPPING_FILENAME_RUNID_TO_NAME = "mapping_runID_to_name.csv"
MAPPING_FILENAME_FOLDER_TO_LANE = "mapping_folder_to_lane.csv"

def prepare():
    print_info("Preparing Bger for processing.")
    print_info("This script will prepare the folder structure and copy the files to the correct places.")
    print_info("It will also create mappings from folder names to lane numbers and from run IDs to sample names.")

    try:

        # find all raw fastq files
        raw_fastq_files = find_fastq_files(os.path.join(get_folder_path_species_raw_reads(FOLDER_BGER), "original"))
        print_info(f"Found {len(raw_fastq_files)} raw fastq files.")

        # if no files are found, exit
        if len(raw_fastq_files) == 0:
            print_error("No raw fastq files found. Exiting.")
            return

        # read mapping of folder names to lane numbers
        print_info(f"Read mapping of folder names to lane numbers from {os.path.join(get_folder_path_species_resources(FOLDER_BGER), MAPPING_FILENAME_FOLDER_TO_LANE)}")
        map_folder_to_lane = get_mapping_folder_to_lane()
        
        # read mapping of run IDs to sample names
        print_info(f"Read mapping of run IDs to sample names from {os.path.join(get_folder_path_species_resources(FOLDER_BGER), MAPPING_FILENAME_RUNID_TO_NAME)}")
        map_runID_to_name = get_mapping_runID_to_name()

        #print(map_folder_to_lane)
        #print(map_runID_to_name)        
        #print(raw_fastq_files)

        for fastq_file_path in raw_fastq_files:
            filename = os.path.basename(fastq_file_path)
            folder_name = os.path.basename(os.path.dirname(fastq_file_path))
            runID = folder_name

            #lane folder is 3 levels up
            folder_name = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(fastq_file_path))))

            try:
                sample_name = map_runID_to_name[runID]
            except:
                sample_name = "unknown"
            
            try:
                lane_number = map_folder_to_lane[folder_name]
            except:
                lane_number = "unknown"

            # new file name: sample name + lane number + R1/R2
            new_filename = f"{sample_name}_L{lane_number}_{filename.split('_')[-2]}.fastq.gz"

            print_info(f"Fastqfile: {filename}, folder name: {folder_name}, run ID: {runID}, Sample name: {sample_name}, lane number: {lane_number}, new filename: {new_filename}")

            # move the file to the correct folder

            move_file(fastq_file_path, get_folder_path_species_raw_reads(FOLDER_BGER), new_filename)

    except Exception as e:
        print_error(e)


def read_csv(file_path):
    data = {}

    # check if file exists
    if not os.path.exists(file_path):
        raise Exception(f"File {file_path} does not exist")

    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data[row[0]] = row[1]
    return data

def get_mapping_runID_to_name():
   
    return read_csv( os.path.join(get_folder_path_species_resources(FOLDER_BGER), MAPPING_FILENAME_RUNID_TO_NAME))

def get_mapping_folder_to_lane():
    return read_csv( os.path.join(get_folder_path_species_resources(FOLDER_BGER), MAPPING_FILENAME_FOLDER_TO_LANE))

# def get_value(data, key):
#     return data.get(key)

# # Example usage:
# file_path = 'example.csv'
# data = read_csv(file_path)
# value = get_value(data, 'key')
# print(value)

def find_fastq_files(directory):
    command = f'find {directory} -type f \\( -name "*_R1_*.fastq.gz" -o -name "*_R2_*.fastq.gz" \\) ! -path "*/undetermined/*"'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.splitlines()

def move_file(source_path,target_path,new_filename=None):
    # Check if source file exists
    if not os.path.exists(source_path):
        raise FileNotFoundError(f"Source file '{source_path}' does not exist")

    # Get the filename from the source path
    filename = os.path.basename(source_path)

    # If a new filename is provided, use it
    if new_filename:
        filename = new_filename

    # Construct the target path with the new filename
    target_file_path = os.path.join(target_path, filename)

    # Check if the target file already exists
    if os.path.exists(target_file_path):
        raise FileExistsError(f"Target file '{target_file_path}' already exists")

    # Move the file
    shutil.move(source_path, target_file_path)

    print_info(f"File moved from '{source_path}' to '{target_file_path}'")