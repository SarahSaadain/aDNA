# aDNA Pipeline

This project contains a pipeline to analyze raw ancient data, obtained from the sequencing facility. The pipeline includes various scripts to process, analyze, and generate reports on the sequence quality, which helps decide if an aDNA extraction and sequencing was successfull, and further polishes the data for downstream analyses.

## Setup Overview

- Before running the pipeline, ensure you have the necessary dependencies installed. Please refer to the [Requirements](#Requirements) section for the necessary dependencies and installation instructions.
- Raw reads and reference genome must be provided in the relevant folders. 
    - Raw reads shoud be renamed according to the naming convention specified in the [RAW Reads filenames](#RAW-Reads-filenames) section. Also see the [Manually renaming the raw reads files](#Manually-renaming-the-raw-reads-files) section.
    - Reference genome must be provided in the `species/raw/ref_genome/` folder.
    - Species folders must be added to the `FOLDER_SPECIES` variable in the `common_aDNA_scripts.py` file.
    - Please refer to the [Species Folders](#Species-Folders) section for the expected folder structure.
- You need to set the `PATH_ADNA_PROJECT` variable in the `common_aDNA_scripts.py` file to point to the project directory.

## Configuration File (config.yaml)

The `config.yaml` file is used to configure the aDNA pipeline. It contains settings such as project name, project description, default number of threads, adapter sequences for adapter removal, species-specific settings, and paths to external tools.

Example `config.yaml`

```
# config.yaml - Configuration file for aDNA pipeline

# Global settings
project_name: "aDNA_Project"
project_description: "Analysis of ancient DNA data"
threads_default: 50  # Default number of threads to use for parallel processing
path_adna_project: "/mnt/data5/sarah/aDNA" #Main project path
log_level: "INFO"

processing:
  fastqc:
    threads: 25 # separate threads for fastqc due to memory requirements
  adapter_removal:
    adapters:
      r1: "AGATCGGAAGAGCACACGTCTGAACTCCAGTCA"
      r2: "AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT" 

# Species-specific settings
species:
  Bger:
    name: "Blatella germanica"
    folder_name: "Bger"
  Dsim:
    name: "Drosophila simulans"
    folder_name: "Dsim"
  Phortica:
    name: "Phortica"
    folder_name: "Phortica"

# cross-species comparison of depth/breadth, endogenous reads, ...
compare_species:
  Bger_Dsim_comparison: # Unique Name
    Bger:
      reference_genome: "refgenome.fna"
    Dsim:
      reference_genome: "refgenome.fna"
    Bger_Dsim_Phortica_comparison: # Unique Name
      Bger:
        reference_genome: "refgenome.fna"
      Dsim:
        reference_genome: "refgenome.fna"
      Phortica:
        reference_genome: "refgenome.fna"

# Paths to external tools
tools:
  fastp: "fastp"
  sga: "sga"
  multiqc: "multiqc"
  fastqc: "fastqc"
  bwa: "bwa"
  bedtools: "bedtools"
  samtools: "samtools"
  angsd: "angsd"
  seqkit: "seqkit"
```

### Global Settings

*   `project_name`: Name of the project.
*   `project_description`: Description of the project.
*   `threads_default`: Default number of threads to use for parallel processing.
*   `path_adna_project`: Main project path.

### Processing Settings
*   `processing`
    *   `adapter_removal`
        *   `adapters`:
            *   `r1`: Adapter sequence for read 1.
            *   `r2`: Adapter sequence for read 2.

### Species-Specific Settings

*   `species`: A dictionary containing settings for each species.
    *   `name`: The name of the species
    *   `folder_name`: The name of the folder for the species.
    *   `processing`: Optional processing config. If not provided, the default values are used.
        *   `adapter_removal`
            *   `adapters`:
                *   `r1`: Adapter sequence for read 1.
                *   `r2`: Adapter sequence for read 2.

### Comparison of species results
*   `compare_species`
    * `comparison ID/Name`:  First comparison. Unique Name used for file names
        * `species ID 1`: first species 
            * `species_id`: Optional species id. If not provided, the config species ID will be used instead
            * `reference_genome`: Name of reference genome fo comparison. e.g.: "refgenome.fna"
        * `species ID 2`: second species 
            * `species_id`: Optional species id. If not provided, the config species ID will be used instead
            * `reference_genome`: Name of reference genome fo comparison. e.g.: "refgenome.fna"
        * `species ID ...`: ...
            * `reference_genome`: ...
        * `species ID N`: n-th species 
            * `reference_genome`: Name of reference genome fo comparison. e.g.: "refgenome.fna"
    * `comparison ID/Name`:  Second comparison. Unique Name used for file names
        * `species ID 1`: first species 
        * ...

Note: the filed `species_id` can be used optionally to specify a specific species. This is usefull if you want to compare the same species with different reference genomes. If you want to compare different species, then this value can be skipped if the species ID is provided as the parent config node.

### Paths to External Tools

*   `tools`: A dictionary containing paths to external tools used in the pipeline.
    *   `cutadapt`: Path to Cutadapt.
    *   `fastp`: Path to fastp.
    *   `sga`: Path to SGA.
    *   `multiqc`: Path to MultiQC.
    *   `fastqc`: Path to FastQC.
    *   `bwa`: Path to BWA.
    *   `bedtools`: Path to BEDTools.
    *   `samtools`: Path to SAMtools.
    *   `angsd`: Path to ANGSD.
    *   `seqkit`: Path to SeqKit.

Note: If the tools are not provided, default values are used and it is expected that the tool can be called via the command line directly.

## Folder Structure

### Species Folders

The project contains folders for different species, which contain the raw data, processed data, and results for each species.

When adding a new species, make sure to 
- add the folder name to the `config.yaml`
- provide the raw reads in `species/raw/reads/` folder
- provide the reference genome in `species/raw/ref_genome/` folder
- provide mtDNA reads in `species/raw/mtdna/` folder
- all other folders will be created and populated automatically
    - folder `species/processed/` contains the intermediary files during processing
    - folder `species/results/` contains the final results and reports

#### RAW Reads Filenames

The pipeline expects input read files to follow a standardized naming convention:

```
<Individual>_<Protocol>_<Original_Filename>.fastq.gz
```

Following this convention ensures proper organization and automated processing within the pipeline.  

##### Filename Components:
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

### Scripts Folder

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

1. **Raw reads processing** - for more details see [Raw Read Processing](scripts/raw_reads_processing/raw_reads_processing.md)
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

```bash
# Cutadapt - Adapter trimming and removal
conda install -c bioconda cutadapt
```

```bash
# FASTX-Toolkit - FASTA/FASTQ file processing
conda install -c bioconda fastx_toolkit
```

```bash
# SGA - String Graph Assembler
conda install -c bioconda sga
```

```bash
# BEDTools - Genome arithmetic and manipulation
conda install -c bioconda bedtools
```

```bash
# SeqKit - Cross-platform and ultrafast toolkit for FASTA/Q file manipulation
conda install -c bioconda seqkit
```

### Python Packages

Install required Python libraries using pip:

```bash
pip install pysam
```	

```bash
pip install pandas  
```	

```bash
pip install pyyaml
```

### R Packages

The pipeline requires R beeing installed and uses the following R packages:

- ggplot2
- dplyr
- tidyr
- scales
- readr
- tools
- ggpubr
- purrr
- stringr

These packages are used for data manipulation, visualization, and analysis.