# aDNA Pipeline

This project contains a pipeline to analyze raw ancient data, obtained from the sequencing facility. The pipeline includes various scripts to process, analyze, and generate reports on the sequence quality, which helps decide if an aDNA extraction and sequencing was successfull, and further polishes the data for downstream analyses.

## Project Structure
The scripts folder contains all necessary scripts, which are all executed within pipeline_aDNA.py.
Bger, Dmel/scripts, Mmus/scripts contain a species specific scripts for more detailed analyses.

### Scripts Folder Structure

The `scripts/` folder contains all necessary scripts for the aDNA pipeline, organized into subfolders corresponding to different stages of the analysis.

#### Usage of `common_aDNA_scripts.py`

The `common_aDNA_scripts.py` file contains a collection of helper functions and constants used throughout the aDNA pipeline. These functions and constants provide a common interface for various tasks, such as:

- Managing file and folder paths  
- Printing and logging messages  
- Checking and creating folders  
- Handling file extensions and patterns  
- Executing R scripts  
- Providing various constants such as `THREADS_DEFAULT` and `PATH_ADNA_PROJECT`
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

#### Folder Structure

- **`raw_reads_processing/`** – Scripts for processing raw reads.  
- **`ref_genome_processing/`** – Scripts for processing reads in relation to reference genomes.  
- **`additional_analysis/`** – Scripts for additional analyses, including species comparison and mitochondrial DNA analysis.  

#### Species-Specific Scripts

Species-specific scripts are organized into separate folders:

- **`Bger/`**  
- **`Dmel/`**  
- **`Mmus/`**  

These scripts are executed within the main pipeline script.  


### Demultiplexing  
Sequencing results were demultiplexed with bcl2fastq  


## Requirements

### FastQC
```bash
conda install -c bioconda fastqc 
```

### MultiQC v2.35
```bash
conda install -c bioconda multiqc
```

### fastq  
```bash
conda install bioconda::fastp
```

### bwa-mem2
```bash
conda install bioconda::bwa-mem2
```

### samtools
```bash
conda install bioconda::samtools
```

### angsd
```bash
conda install -c bioconda -c conda-forge angsd
```

### pysam
```bash
pip install pysam
```

### pandas
```bash
pip install pandas
```