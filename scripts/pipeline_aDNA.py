from common_aDNA_scripts import *

#load individual scripts to run within the pipeline
import prepare_species_for_processing as prepare_species_for_processing
import execute_fastqc as execute_fastqc
import execute_multiqc as execute_multiqc
import execute_fastp_adapter_remove_and_merge as execute_fastp_adapter_remove_and_merge
import polish_fastp_quality_filter as polish_fastp_quality_filter
import polish_fastp_deduplication as polish_fastp_deduplication
import prepare_species_for_map_to_ref_genome as prepare_species_for_map_to_ref_genome
import map_aDNA_to_refgenome as map_aDNA_to_refgenome
import convert_sam2bam as convert_sam2bam
import determine_endogenous_reads as determine_endogenous_reads
import extract_special_sequences as extract_special_sequences
import determine_coverage_depth_and_breadth as determine_coverage_depth_and_breadth
import determine_reads_processing_result as determine_reads_processing_result
import determine_read_length_distribution as determine_read_length_distribution
import generate_quality_check_report as generate_quality_check_report
import generate_plots as generate_plots
import generate_plots_species_compare as generate_plots_species_compare
import mtdna_analysis.determine_mtdna_step1_map_to_ref_genome as determine_mtdna_step1_map_to_ref_genome
import mtdna_analysis.determine_mtdna_step2_determine_regions as determine_mtdna_step2_determine_regions
import scripts.mtdna_analysis.determine_mtdna_step4_extract_coi_regions as determine_mtdna_step4_extract_coi_regions
import scripts.mtdna_analysis.determine_mtdna_step3_create_and_map_consensus_sequence as determine_mtdna_step3_create_and_map_consensus_sequence


def run_pipeline():

    print("Starting pipeline ...")
    
    ############################################################
    # Processing of reads
    ############################################################

    # prepare species for processing
    # this step is optional anc uses a separate prepare.py script to prepare the species
    # for processing. This mostly includes copying the raw reads to the correct folder 
    # and renaming them accordingly if necessary.
    prepare_species_for_processing.all_species_prepare()

    # quality control for raw reads using fastqc and multiqc
    execute_fastqc.all_species_fastqc_raw()
    execute_multiqc.all_species_multiqc_raw()

    # adapter removal
    # this step uses fastp to remove adapters from the raw reads
    # it can handle single and paired end reads. paired end reads are merged
    execute_fastp_adapter_remove_and_merge.all_species_fastp_adapter_remove_and_merge()

    # quality control for adapter removed reads using fastqc and multiqc
    execute_fastqc.all_species_fastqc_adapter_removed()
    execute_multiqc.all_species_multiqc_adapter_removed()

    # apply quality filtering to adapter removed reads
    # this step uses fastp to apply quality filtering to the adapter removed reads
    polish_fastp_quality_filter.all_species_fastp_quality_filter()

    # quality control for quality filtered reads using fastqc and multiqc
    execute_fastqc.all_species_fastqc_quality_filtered()
    execute_multiqc.all_species_multiqc_quality_filtered()

    # remove duplicates from quality filtered reads
    polish_fastp_deduplication.all_species_fastp_deduplication()

    # quality control for duplicates removed reads
    execute_fastqc.all_species_fastqc_duplicates_removed()
    execute_multiqc.all_species_multiqc_duplicates_removed()

    # generate quality check report (html) to easily access all qc results
    generate_quality_check_report.all_species_generate_quality_check_report()

    ############################################################
    # Mapping to reference genome
    ############################################################

    # prepare species for mapping to reference genome
    # this step uses the processed reads and prepares them for mapping to the 
    # reference genome by concatenating the reads and creating different fastq files.
    # fastq files are created for the species (all reads), and per individual
    prepare_species_for_map_to_ref_genome.all_species_prepare()
    
    # map reads to reference genome
    map_aDNA_to_refgenome.all_species_map_aDNA_to_refgenome()

    # convert mapped reads from sam to bam. also sorts the bam file and indexes it
    convert_sam2bam.all_species_convert_sam_to_bam()

    # quality control for mapped reads
    # determine endogenous reads
    determine_endogenous_reads.all_species_determine_endogenous_reads()
    
    # determine reads processing before and after
    determine_reads_processing_result.all_species_determine_determine_reads_processing_result()

    # determine read length distribution
    determine_read_length_distribution.all_species_determine_read_length_distribution()

    # determine coverage depth and breadth
    determine_coverage_depth_and_breadth.all_species_determine_coverage_depth_and_breath()

    ############################################################
    # Post processing
    ############################################################

    # determine coi
    determine_mtdna_step1_map_to_ref_genome.all_species_map_mtdna_to_refgenome()
    determine_mtdna_step2_determine_regions.all_species_mtdna_get_regions()
    #determine_coi_step3_extract_coi_regions.()
    determine_mtdna_step3_create_and_map_consensus_sequence.all_species_create_and_map_consensus_sequence()

    # extract special sequences 
    extract_special_sequences.all_species_extract_special_sequences()

    ############################################################
    # Generate plots
    ############################################################

    # generate plots for all species to visualize results
    # these contain 
    # 1. reads processing results before and after
    # 2. coverage depth and breadth
    # 3. endogenous reads
    # 4. sequence length distribution
    generate_plots.all_species_generate_plots()
    
    # generate comparison plots for species
    # these contain
    # 1. reads processing results before and after
    # 2. coverage depth and breadth
    # 3. endogenous reads
    generate_plots_species_compare.species_generate_comparison_plots([FOLDER_BGER, FOLDER_TRIAL_BGER])
    generate_plots_species_compare.species_generate_comparison_plots([FOLDER_TRIAL_BGER, FOLDER_TRIAL_MMUS])

    print_success("Pipeline completed successfully.")


def main():
    run_pipeline()

if __name__ == "__main__":  
    main()