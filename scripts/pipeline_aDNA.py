from common_aDNA_scripts import *

import prepare_species_for_processing as prepare
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
import determine_coi_step1_map_to_ref_genome as determine_coi_step1_map_to_ref_genome
import determine_coi_step2_determine_regions as determine_coi_step2_determine_regions
import determine_coi_step3_extract_coi_regions as determine_coi_step3_extract_coi_regions
import determine_coi_step4_create_and_map_consensus_sequence as determine_coi_step4_create_and_map_consensus_sequence


def run_pipeline():

    print("Starting pipeline.")
    
    prepare.all_species_prepare()
    execute_fastqc.all_species_fastqc_raw()
    execute_multiqc.all_species_multiqc_raw()

    #adapter_remove.all_species_adapter_remove()
    execute_fastp_adapter_remove_and_merge.all_species_fastp_adapter_remove_and_merge()
    execute_fastqc.all_species_fastqc_adapter_removed()
    execute_multiqc.all_species_multiqc_adapter_removed()

    polish_fastp_quality_filter.all_species_fastp_quality_filter()
    execute_fastqc.all_species_fastqc_quality_filtered()
    execute_multiqc.all_species_multiqc_quality_filtered()

    polish_fastp_deduplication.all_species_fastp_deduplication()
    execute_fastqc.all_species_fastqc_duplicates_removed()
    execute_multiqc.all_species_multiqc_duplicates_removed()

    generate_quality_check_report.all_species_generate_quality_check_report()

    prepare_species_for_map_to_ref_genome.all_species_prepare()
    
    map_aDNA_to_refgenome.all_species_map_aDNA_to_refgenome()

    convert_sam2bam.all_species_convert_sam_to_bam()

    determine_endogenous_reads.all_species_determine_endogenous_reads()
    determine_reads_processing_result.all_species_determine_determine_reads_processing_result()
    determine_read_length_distribution.all_species_determine_read_length_distribution()
    determine_coverage_depth_and_breadth.all_species_determine_coverage_depth_and_breath()

    determine_coi_step1_map_to_ref_genome.all_species_map_mtdna_to_refgenome()
    determine_coi_step2_determine_regions.all_species_mtdna_get_regions()
    #determine_coi_step3_extract_coi_regions.()
    determine_coi_step4_create_and_map_consensus_sequence.all_species_create_and_map_consensus_sequence()

    extract_special_sequences.all_species_extract_special_sequences()

    generate_plots.all_species_generate_plots()
    
    generate_plots_species_compare.species_generate_comparison_plots([FOLDER_BGER, FOLDER_TRIAL_BGER])
    generate_plots_species_compare.species_generate_comparison_plots([FOLDER_TRIAL_BGER, FOLDER_TRIAL_MMUS])

    print_success("Pipeline completed successfully.")


def main():
    run_pipeline()

if __name__ == "__main__":  
    main()