# aDNA Pipeline

This project contains a pipeline to analyze raw ancient data, obtained from the sequencing facility. The pipeline includes various scripts to process, analyze, and generate reports on the sequence quality, which helps decide if an aDNA extraction and sequencing was successfull, and further polishes the data for downstream analyses.

## Project Structure

### Species Folders

The project contains folders for different species, such as `Bger`, `Dsim`, `Phortica`, `Sepsis`, `Mmus`, and `Dmel`. These folders contain the raw data, processed data, and results for each species.

When adding a new species, make sure to 
- add the folder name to the `FOLDER_SPECIES` variable in the `common_aDNA_scripts.py` file
- provide the raw reads in `species/raw/reads/` folder
- provide the reference genome in `species/raw/ref_genome/` folder
- provide mtDNA reads in `species/raw/mtdna/` folder
- all other folders will be created and populated automatically
    - folder `species/processed/` contains the intermediary files during processing
    - folder `species/results/` contains the final results and reports

#### RAW Reads filenames

The pipeline expects input read files to follow a standardized naming convention:

```
<Individual>_<Protocol>_<Original_Filename>.fastq.gz
```

Following this convention ensures proper organization and automated processing within the pipeline.  

##### Components:
- **`<Individual>`** – A unique identifier for the sample or individual.  
- **`<Protocol>`** – The sequencing or library preparation protocol used (e.g., shotgun, capture).  
- **`<Original_Filename>`** – The original filename assigned by the sequencing platform.  
- **`.fastq.gz`** – The expected file extension, indicating compressed FASTQ format.  

#### Example:

```
Bger1_S_326862_S37_R1_001.fastq.gz
```

#### Manually renaming the raw reads files

For manually renaming the raw read files, use the `rename.py` script located in the `resources/` folder in the root directory of the project.  

##### Usage  

The script reads a CSV file containing old and new filename mappings and renames the files accordingly in the specified folder. 

**How It Works**
- The script reads the CSV file and stores the old-to-new name mappings.
- It scans the specified folder for filenames that contain any of the old names.
- If a match is found, the filename is updated accordingly.
- If --test is enabled, it prints the changes without renaming the files.

This ensures efficient and structured renaming of raw read files within the pipeline.

###### CSV Format  

The CSV file should have two columns:  
- **Column 1:** The original filename or a substring to be replaced.  
- **Column 2:** The new filename or replacement substring.  

**Example (`rename_list.csv`):**  

```
344209,Dsim19_2trial_344209
344210,Dsim19_2trial_344210
```

##### Running the Script  

Navigate to the project root and execute the script:  

```bash
python resources/rename.py rename_list.csv path/to/raw_reads/
```

This will rename the files in `path/to/raw_reads/` based on the mappings in `rename_list.csv`.

##### Test Mode
To preview the changes without renaming files, use the `--test` flag:

```bash
python resources/rename.py rename_list.csv path/to/raw_reads/ --test
```

This will print the planned renaming actions without modifying any files.

### Scripts Folder Structure

The `scripts/` folder contains all necessary scripts for the aDNA pipeline, organized into subfolders corresponding to different stages of the analysis.

#### Usage of `common_aDNA_scripts.py`

The `common_aDNA_scripts.py` file contains a collection of helper functions and constants used throughout the aDNA pipeline. These functions and constants provide a common interface for various tasks, such as:

- Managing file and folder paths  
- Printing and logging messages  
- Checking and creating folders  
- Handling file extensions and patterns  
- Executing R scripts  
- Providing various constants
- Providing various helper functions

This file is intended to be imported and used by other scripts in the pipeline, providing a centralized location for shared functionality and reducing code duplication.  

#### Usage of `pipeline_aDNA.py`

The `pipeline_aDNA.py` file is the main entry point for the aDNA pipeline. It orchestrates the execution of various scripts and tasks, guiding the pipeline through its different stages.

##### Pipeline Stages

The pipeline is divided into several stages, executed sequentially:

1. **Raw reads processing**  
2. **Reference genome processing**  
3. **Additional analysis**   

The pipeline automatically manages dependencies and workflow execution.

##### Running the Pipeline

To run the pipeline, navigate to the root directory containing the scripts folder and execute:

```sh
python scripts/pipeline_aDNA.py
```

#### Notes for running the Pipeline

##### Running the Pipeline in the Background

Depending on the size of the data, it may take some time to complete the pipeline. Thus it is recommended to run the pipeline in the background. You can do this by running the following command:

```bash
nohup python -u scripts/pipeline_aDNA.py > pipeline.log 2>&1 &
```

##### Restarting the Pipeline

The pipeline will always start from the first stage, even if it was previously completed. The individual steps recognize the state of the pipeline and will start from the last completed stage. Completed steps will be skipped. 

If you want to restart the pipeline from the beginning, you can delete the relevant folders and re-run the pipeline. This will lead to a complete re-processing of the data.

##### Parallelization

Some stages support parallelization. The number of threads can be adjusted in the `common_aDNA_scripts.py` file.

#### Folder Structure

- **`raw_reads_processing/`** – Scripts for processing raw reads.  
- **`ref_genome_processing/`** – Scripts for processing reads in relation to reference genomes.  
- **`additional_analysis/`** – Scripts for additional analyses, including species comparison and mitochondrial DNA analysis.  

#### Species-Specific Scripts

Species-specific can be used to prepare the reads for processing. These scripts are organized into separate folders:

- **`species/scripts`**

These scripts are executed within the main pipeline script if provided.  

## Requirements

The following dependencies are required to run the aDNA pipeline. You can install them using `conda` or `pip` as specified below.

Make sure conda and pip are installed and properly configured before running these commands.

### Conda Packages

Install the necessary tools using `conda`:

```bash
# FastQC - Quality control for high-throughput sequence data
conda install -c bioconda fastqc  
```	
```bash
# MultiQC v2.35 - Aggregate results from bioinformatics analyses
conda install -c bioconda multiqc  
```	

```bash
# fastp - Fast and efficient FASTQ preprocessor
conda install -c bioconda fastp 
```	 

```bash
# BWA-MEM2 - Alignment algorithm optimized for large genomes
conda install -c bioconda bwa-mem2  
```	

```bash
# SAMtools - Utilities for manipulating alignments in the SAM/BAM format
conda install -c bioconda samtools  
```	

```bash
# ANGSD - Analysis of Next Generation Sequencing Data
conda install -c bioconda -c conda-forge angsd  
```	

### Python Packages

Install required Python libraries using pip:

```bash
pip install pysam
```	

```bash
pip install pandas  
```	