# Raw Read Processing

## Adapter Removal

* Program: `fastp`
* Purpose: Remove adapters from raw reads
* Input: Raw reads
* Output: Adapter-removed reads
* Script: `scripts/raw_reads_processing/execute_fastp_adapter_remove_and_merge.py`
* Parameters:
	+ Paired-end reads:
		- `-i`: Input file (R1 and R2)
		- `-o`: Output file (merged)
		- `--adapter_sequence`: Adapter sequence
		- `--length_required`: Minimum length of reads to keep (set to `15`)
		- `--trim_poly_x`: Trim poly-X tails (set to `5`)
		- `--qualified_quality_phred`: Minimum quality score to keep (set to `5`)
		- `--unqualified_percent_limit`: Maximum percentage of unqualified bases (set to `40`)
		- `--n_base_limit`: Maximum number of N bases allowed (set to `5`)
	+ Single-end reads:
		- `-i`: Input file
		- `-o`: Output file
		- `--adapter_sequence`: Adapter sequence (not specified)
		- `--length_required`: Minimum length of reads to keep (set to `15`)
		- `--trim_poly_x`: Trim poly-X tails (set to `5`)
		- `--qualified_quality_phred`: Minimum quality score to keep (set to `5`)
		- `--unqualified_percent_limit`: Maximum percentage of unqualified bases (set to `40`)
		- `--n_base_limit`: Maximum number of N bases allowed (set to `5`)

## Quality Filtering

* Program: `fastp`
* Purpose: Filter reads based on quality scores
* Input: Adapter-removed reads
* Output: Quality-filtered reads
* Script: `scripts/raw_reads_processing/execute_fastp_quality_filter.py`
* Parameters:
	+ `-i`: Input file
	+ `-o`: Output file
	+ `-q`: Minimum quality score to keep (set to `30`)
	+ `-p`: Minimum percent of bases that must have `-q` quality (set to `75`)
	+ `--length_required`: Minimum length of reads to keep (set to `15`)
	+ `--trim_poly_x`: Trim poly-X tails (set to `5`)
	+ `--qualified_quality_phred`: Minimum quality score to keep (set to `5`)
	+ `--unqualified_percent_limit`: Maximum percentage of unqualified bases (set to `40`)
	+ `--n_base_limit`: Maximum number of N bases allowed (set to `5`)

## Deduplication

* Program: `fastp`
* Purpose: Remove duplicate reads
* Input: Quality-filtered reads
* Output: Deduplicated reads
* Script: `scripts/raw_reads_processing/execute_fastp_deduplication.py`
* Parameters:
	+ `-i`: Input file
	+ `-o`: Output file
	+ `--dedup`: Enable deduplication (set to `True`)
	+ `--length_required`: Minimum length of reads to keep (set to `15`)
	+ `--trim_poly_x`: Trim poly-X tails (set to `5`)
	+ `--qualified_quality_phred`: Minimum quality score to keep (set to `5`)
	+ `--unqualified_percent_limit`: Maximum percentage of unqualified bases (set to `40`)
	+ `--n_base_limit`: Maximum number of N bases allowed (set to `5`)


# FastQC and MultiQC

FastQC and MultiQC are used to generate quality control reports for raw reads, adapter-removed reads, quality-filtered reads, and deduplicated reads. The reports are saved in the `species/results/quality_control/fastqc` and `species/results/quality_control/multiqc` folders, respectively.

# Plots

* Read length distribution plots are generated for raw reads, adapter-removed reads, quality-filtered reads, and deduplicated reads.
* Plots are created to visualize the distribution of read lengths at each processing step, allowing for quality control and assessment of the processing pipeline's performance.