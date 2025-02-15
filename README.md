# aDNA Pipeline

This project contains a pipeline to analyze raw ancient data, obtained from the sequencing facility. The pipeline includes various scripts to process, analyze, and generate reports on the sequence quality, which helps decide if an aDNA extraction and sequencing was successfull, and further polishes the data for downstream analyses.

## Project Structure
The scripts folder contains all necessary scripts, which are all executed within pipeline_aDNA.py.
Bger, Dmel/scripts, Mmus/scripts contain a species specific scripts for more detailed analyses.


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

### pysam
```bash
pip install pysam
```