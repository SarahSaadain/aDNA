# pipeline_steps_enum.py

from enum import Enum

class ConfigSettings(Enum):
    PROCESSING = 'processing'
    SPECIES = 'species'
    TOOLS = 'tools'

# Define Enums for pipeline stages
class PipelineStages(Enum):
    RAW_READS_PROCESSING = 'raw_reads_processing'
    REFERENCE_GENOME_PROCESSING = 'reference_genome_processing' # Corrected name
    POST_PROCESSING = 'post_processing'

# Define Enums for pipeline steps within each stage
class RawReadsProcessingSteps(Enum):
    QC = 'qc'
    ADAPTER_REMOVE_AND_MERGE = 'adapter_remove_and_merge' # Corrected name
    QUALITY_FILTER = 'quality_filter' # Corrected name
    DEDUPLICATION = 'deduplication' # Corrected name
    GENERATE_QUALITY_CHECK_REPORT = 'generate_quality_check_report'
    DETERMINE_READS_PROCESSING_RESULT = 'determine_reads_processing_result'
    DETERMINE_READ_LENGTH_DISTRIBUTION = 'determine_read_length_distribution'
    GENERATE_RAW_READS_PLOTS = 'generate_raw_reads_plots'
    CONTAMINATION_CHECK = 'contamination_check'

# Define Enums for QC steps specifically under raw_reads_processing.qc
class RawReadsQualityControlSteps(Enum):
    QC_RAW = 'qc_raw'
    QC_ADAPTER_REMOVED = 'qc_adapter_removed'
    QC_QUALITY_FILTERED = 'qc_quality_filtered'
    QC_DUPLICATES_REMOVED = 'qc_duplicates_removed'


class ReferenceGenomeProcessingSteps(Enum):
    PREPARE_SPECIES_FOR_MAPPING = 'prepare_species_for_mapping'
    PREPARE_REFERENCE_GENOME = 'prepare_reference_genome' # Corrected name
    MAP_READS_TO_REFERENCE_GENOME = 'map_reads_to_reference_genome' # Corrected name
    CONVERT_SAM_TO_BAM = 'convert_sam_to_bam'
    DETERMINE_ENDOGENOUS_READS = 'determine_endogenous_reads'
    DETERMINE_COVERAGE_DEPTH_AND_BREADTH = 'determine_coverage_depth_and_breadth'
    EXTRACT_SPECIAL_SEQUENCES = 'extract_special_sequences'
    GENERATE_REF_GENOME_PLOTS = 'generate_ref_genome_plots'


class PostProcessingSteps(Enum):
    # Added 'mtdna_analysis' key
    MTDNA_ANALYSIS = 'mtdna_analysis'
    GENERATE_SPECIES_COMPARISON_PLOTS = 'generate_species_comparison_plots'

# Define Enums for mtDNA analysis steps specifically under post_processing.mtdna_analysis
class MtdnaAnalysisSteps(Enum):
    MTDNA_MAP_TO_REF_GENOME = 'mtdna_map_to_ref_genome'
    MTDNA_DETERMINE_REGIONS = 'mtdna_determine_regions'
    MTDNA_CREATE_AND_MAP_CONSENSUS = 'mtdna_create_and_map_consensus'
    MTDNA_EXTRACT_COI_REGIONS = 'mtdna_extract_coi_regions'
    MTDNA_CHECK_EXTRACTED_REGIONS = 'mtdna_check_extracted_regions'

class AdapterRemovalSettings(Enum):
    ADAPTERS = 'adapters'
    ADAPTERS_R1 = 'r1'
    ADAPTERS_R2 = 'r2'

class ContaminationCheckSettings(Enum):
    CENTRIFUGE_DB = 'centrifuge_db'    
    KRAKEN_DB = 'kraken_db'

class QualityControlSettings(Enum):
    THREADS = 'threads'

# You might also want a mapping from stage key strings to their step Enums
STAGE_STEP_ENUM_MAP = {
    PipelineStages.RAW_READS_PROCESSING.value: RawReadsProcessingSteps,
    PipelineStages.REFERENCE_GENOME_PROCESSING.value: ReferenceGenomeProcessingSteps,
    PipelineStages.POST_PROCESSING.value: PostProcessingSteps,
}