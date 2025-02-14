# aDNA

This project contains a pipeline to analyze ancient DNA (aDNA) data. The pipeline includes various scripts to process, analyze, and generate reports on aDNA sequences.

## Project Structure

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
