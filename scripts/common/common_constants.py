# raw folders
FOLDER_RAW = "raw"
FOLDER_READS = "reads"
FOLDER_REFERENCE_GENOMES = "ref_genome"
FOLDER_MTDNA = "mtdna"

# script folders
FOLDER_SCRIPTS = "scripts"
FOLDER_ANALYSIS = "analysis"
FOLDER_RAW_READS_PROCESSING = "raw_reads_processing"
FOLDER_REF_GENOME_PROCESSING = "ref_genome_processing"
FOLDER_ADDITIONAL_ANALYSIS = "additional_analysis"
FOLDER_MTDNA_ANALYSIS = "mtdna_analysis"
FOLDER_SPECIES_COMPARISON = "species_comparison"
FOLDER_PLOTS = "plots"

# processed folders
# if there is a follow up step, it is considered processed
FOLDER_PROCESSED = "processed"
FOLDER_CONCATENATED = "concatenated"
FOLDER_NON_CONCATENATED = "non_concatenated"
FOLDER_MAPPED = "mapped"
FOLDER_PREPARED_FOR_REF_GENOME = "prepared_for_ref_genome"
FOLDER_ADAPTER_REMOVED = "adapter_removed"
FOLDER_QUALITY_FILTERED = "quality_filtered"
FOLDER_DUPLICATES_REMOVED = "duplicates_removed"
FOLDER_GENOMEDELTA = "genome_delta"
FOLDER_CONSENSUS_SEQUENCES = "consensus_sequences"
FOLDER_CONSENSUS_SEQUENCES_MAPPED = "consensus_sequences_mapped"
FOLDER_EXTRACTED_SEQUENCES = "extracted_sequences"

# results folders
# if there is no follow up step, it is considered a result
FOLDER_RESULTS = "results"
FOLDER_QUALITYCONTROL = "qualitycontrol"
FOLDER_FASTQC = "fastqc"
FOLDER_MULTIQC = "multiqc"
FOLDER_DEPTH_BREADTH = "coverage_depth_breadth"
FOLDER_DEPTH = "depth"
FOLDER_BREADTH = "breadth"
FOLDER_MITOCHONDRIA= "mitochondria"
FOLDER_SPECIAL_SEQUENCES = "special_sequences"
FOLDER_ENDOGENOUS_READS = "endogenous_reads"
FOLDER_PROCESSED_READS = "processed_reads"
FOLDER_READ_LENGTH_DISTRIBUTION = "read_length_distribution"

FOLDER_REGIONS = "regions"

# main folders
FOLDER_LOGS = "logs"
FOLDER_RESOURCES = "resources"

# files
FILE_NAME_RAW_READS_LIST = "reads_list.csv"

# files
FILE_PATTERN_R1_FASTQ_GZ = "*_R1*.fastq.gz"
FILE_PATTERN_R2_FASTQ_GZ = "*_R2*.fastq.gz"
FILE_PATTERN_UNDETERMINED_FOLDER = "*/undetermined/*"

FILE_ENDING_ADAPTER_REMOVED_FASTQ_GZ = "_merged_trimmed.fastq.gz"
FILE_ENDING_FASTQ_GZ = ".fastq.gz"
FILE_ENDING_FASTA = ".fasta"
FILE_ENDING_FNA = ".fna"
FILE_ENDING_FA = ".fa"
FILE_ENDING_FA_GZ = ".fa.gz"
FILE_ENDING_QUALITY_FILTERED_FASTQ_GZ = "_quality_filtered.fastq.gz"
FILE_ENDING_DUPLICATES_REMOVED_FASTQ_GZ = "_duplicates_removed.fastq.gz"
FILE_ENDING_FASTQC_HTML = "_fastqc.html"
FILE_ENDING_SAM = ".sam"
FILE_ENDING_BAM = ".bam"
FILE_ENDING_SORTED_BAM = "_sorted.bam"
FILE_ENDING_BAI = ".bai"
FILE_ENDING_SORTED_BAI = "_sorted.bai"
FILE_ENDING_CSV = ".csv"
FILE_ENDING_BED = ".bed"
FILE_ENDING_TSV = ".tsv"
FILE_ENDING_PNG = ".png"
FILE_ENDING_HTML = ".html"
FILE_ENDING_SAMTOOLS_DEPTH_TSV = f"_samtools_depth{FILE_ENDING_TSV}"
FILE_ENDING_ANALYSIS_TSV = f"_analysis{FILE_ENDING_TSV}"
FILE_ENDING_ANALYSIS_CSV = f"_analysis{FILE_ENDING_CSV}"
FILE_ENDING_COMBINED_COVERAGE_ANALYSIS_CSV = f"_combined_coverage{FILE_ENDING_ANALYSIS_CSV}"

FILE_ENDING_ENDOGENOUS_READS_CSV = f"_endogenous_reads{FILE_ENDING_CSV}"

FILE_PATTERN_LIST_FASTA = [f"*{FILE_ENDING_FNA}", f"*{FILE_ENDING_FASTA}", f"*{FILE_ENDING_FA}"]

#R Scripts
R_SCRIPT_PLOT_READS_BEFORE_AFTER_PROCESSING  ="plot_comparison_reads_before_after_processing.R"
R_SCRIPT_PLOT_DEPTH = "plot_coverage_depth.R"
R_SCRIPT_PLOT_BREADTH = "plot_coverage_breadth.R"
R_SCRIPT_PLOT_ENDOGENOUS_READS = "plot_endogenous_reads.R"
R_SCRIPT_PLOT_SEQUENCE_LENGTH_DISTRIBUTION = "plot_sequence_length_distribution.R"
R_SCRIPT_PLOT_COMPARE_SPECIES_READS_BEFORE_AFTER_PROCESSING = "plot_compare_species_reads_before_after_processing.R"
R_SCRIPT_PLOT_COMPARE_SPECIES_DEPTH_BREADTH = "plot_compare_species_depth_breadth.R"
R_SCRIPT_PLOT_COMPARE_SPECIES_ENDOGENOUS_READS = "plot_compare_species_endogenous_reads.R"