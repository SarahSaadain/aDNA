from common_aDNA_scripts import *

#load individual scripts to run within the pipeline
import raw_reads_processing.quality_checking.execute_fastqc as execute_fastqc
import raw_reads_processing.quality_checking.execute_multiqc as execute_multiqc
import raw_reads_processing.execute_fastp_adapter_remove_and_merge as execute_fastp_adapter_remove_and_merge
import raw_reads_processing.polish_fastp_quality_filter as polish_fastp_quality_filter
import raw_reads_processing.polish_fastp_deduplication as polish_fastp_deduplication
import raw_reads_processing.quality_checking.generate_quality_check_report as generate_quality_check_report
import raw_reads_processing.analysis.determine_reads_processing_result as determine_reads_processing_result
import raw_reads_processing.analysis.determine_read_length_distribution as determine_read_length_distribution
import raw_reads_processing.analysis.generate_plots_raw_reads_processing as generate_plots_raw_reads_processing
import raw_reads_processing.analysis.contamination.check_contamination_centrifuge as check_contamination_centrifuge
import raw_reads_processing.analysis.contamination.check_contamination_kraken as check_contamination_kraken

import ref_genome_processing.prepare_ref_genome_for_mapping as prepare_ref_genome_for_mapping
import ref_genome_processing.prepare_species_for_map_to_ref_genome as prepare_species_for_map_to_ref_genome
import ref_genome_processing.map_aDNA_to_refgenome as map_aDNA_to_refgenome
import ref_genome_processing.convert_mapped_sam2bam as convert_mapped_sam2bam
import ref_genome_processing.analysis.determine_endogenous_reads as determine_endogenous_reads
import ref_genome_processing.analysis.extract_special_sequences as extract_special_sequences
import ref_genome_processing.analysis.determine_coverage_depth_and_breadth as determine_coverage_depth_and_breadth
import ref_genome_processing.analysis.generate_plots_ref_genome_processing as generate_plots_ref_genome_processing
import ref_genome_processing.analysis.analyze_damage as analyze_damage

import additional_analysis.species_comparison.analysis.generate_plots_species_compare as generate_plots_species_compare
import additional_analysis.mtdna_analysis.pipeline_mtdna_analysis as pipeline_mtdna_analysis


def run_pipeline_reference_genome_processing():

    print_execution("Starting reference genome processing pipeline ...")
    
    ############################################################
    # Mapping to reference genome
    ############################################################

    # prepare species for mapping to reference genome
    # this step uses the processed reads and prepares them for mapping to the 
    # reference genome by concatenating the reads and creating different fastq files.
    # fastq files are created for the species (all reads), and per individual
    prepare_species_for_map_to_ref_genome.all_species_prepare()

    # prepare reference genome for mapping
    prepare_ref_genome_for_mapping.all_species_prepare_ref_genome()
    
    # map reads to reference genome
    map_aDNA_to_refgenome.all_species_map_aDNA_to_refgenome()

    # convert mapped reads from sam to bam. also sorts the bam file and indexes it
    convert_mapped_sam2bam.all_species_convert_sam_to_bam()

    # run mapDamage on the mapped reads
    # this step analyzes the damage patterns in the mapped reads
    analyze_damage.all_species_run_mapdamage()
    
    # quality control for mapped reads
    # determine endogenous reads
    determine_endogenous_reads.all_species_determine_endogenous_reads()

    # determine coverage depth and breadth
    determine_coverage_depth_and_breadth.all_species_determine_coverage_depth_and_breath()

    # extract special sequences 
    #extract_special_sequences.all_species_extract_special_sequences()

    # generate plots for all species to visualize results
    # these contain 
    # 1. coverage depth and breadth
    # 2. endogenous reads
    generate_plots_ref_genome_processing.all_species_generate_plots()


def run_pipeline_raw_reads_processing():

    print_execution("Starting raw reads processing pipeline ...")

    ############################################################
    # Processing of reads
    ############################################################

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

    # determine reads processing before and after
    determine_reads_processing_result.all_species_determine_determine_reads_processing_result()

    # determine read length distribution
    determine_read_length_distribution.all_species_determine_read_length_distribution()

    # determine contamination using centrifuge
    check_contamination_centrifuge.all_species_run_centrifuge()

    # determine contamination using kraken
    check_contamination_kraken.all_species_run_Kraken()

     # generate plots for all species to visualize results
    # these contain 
    # 1. reads processing results before and after
    # 2. sequence length distribution
    # 3. contamination analysis
    generate_plots_raw_reads_processing.all_species_generate_plots()

def run_pipeline_post_processing():

    print_execution("Starting post processing pipeline ...")

    ############################################################
    # Post processing
    ############################################################
    # determine coi
    pipeline_mtdna_analysis.pipeline_mtdna_analysis()

    ############################################################
    # Generate plots
    ############################################################
    # generate comparison plots for species
    # these contain
    # 1. reads processing results before and after
    # 2. coverage depth and breadth
    # 3. endogenous reads
    generate_plots_species_compare.species_generate_comparison_plots()
    

def run_pipeline():

    pid = os.getpid()

    print_execution(f"Starting pipeline (Main PID: {pid}) ...")
    
    ############################################################
    # Processing of reads
    ############################################################
    run_pipeline_raw_reads_processing()    

    ############################################################
    # Mapping to reference genome
    ############################################################
    run_pipeline_reference_genome_processing()

    ############################################################
    # Post processing
    ############################################################
    run_pipeline_post_processing()

    print_success("Pipeline completed successfully.")


def main():
    run_pipeline()

if __name__ == "__main__":  
    main()