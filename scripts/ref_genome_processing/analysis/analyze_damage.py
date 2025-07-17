import os
import subprocess
import common_aDNA_scripts as common_adna
import ref_genome_processing.common_ref_genome_processing_helpers as common_rgp

from multiprocessing import Pool, cpu_count

def execute_mapdamage(bam_file_path: str, ref_genome_path: str, output_folder: str):

    common_adna.print_debug("Entering execute_mapdamage function")

    pid = os.getpid()
    
    common_adna.print_info(f"[PID {pid}] Running mapDamage2 on {bam_file_path} ...")

    if not os.path.exists(bam_file_path):
        raise Exception(f"[PID {pid}] BAM file {bam_file_path} does not exist!")

    if not os.path.exists(ref_genome_path):
        raise Exception(f"[PID {pid}] Reference genome file {ref_genome_path} does not exist!")

    if os.path.exists(os.path.join(output_folder, "misincorporation.txt")):
        common_adna.print_skipping(f"[PID {pid}] mapDamage output already exists in {output_folder}!")
        return

    command = [
        common_adna.PROGRAM_PATH_MAPDAMAGE,
        "-i", bam_file_path,
        "-r", ref_genome_path,
        "--folder", output_folder,
        "--merge-reference-sequences"
    ]

    try:
        common_adna.run_command(
            command, 
            description=f"[PID {pid}] Running mapDamage on {common_adna.get_filename_from_path(bam_file_path)}"
            )
    
    except subprocess.CalledProcessError as e:
        common_adna.print_info(f"[PID {pid}] {e.stdout.strip()}")
        common_adna.print_error(f"[PID {pid}] mapDamage failed for {bam_file_path}")
        common_adna.print_error(f"[PID {pid}] {e.stderr.strip()}")

def run_mapdamage_for_species(species: str):
    common_adna.print_info(f"Running mapDamage for species {species} ...")

    try:
        ref_genome_list = common_rgp.get_reference_genome_file_list_for_species(species)
    except Exception as e:
        common_adna.print_error(f"Failed to get reference genome files for species {species}: {e}")
        return

    for ref_genome_id, ref_genome_path in ref_genome_list:
        common_adna.print_debug(f"Reference genome: {ref_genome_id}")

        mapped_folder = common_adna.get_folder_path_species_processed_refgenome_mapped(species, ref_genome_id)
        list_of_bam_files = common_adna.get_files_in_folder_matching_pattern(mapped_folder, f"*{common_adna.FILE_ENDING_SORTED_BAM}")

        if len(list_of_bam_files) == 0:
            common_adna.print_warning(f"No mapped BAM files found in {mapped_folder} for species {species}.")
            return

        common_adna.print_debug(f"Found {len(list_of_bam_files)} BAM files for species {species}")
        common_adna.print_debug(f"BAM files: {list_of_bam_files}")

        # Prepare parallel task list
        tasks = []
        for sorted_bam_file in list_of_bam_files:
            if not os.path.exists(sorted_bam_file):
                common_adna.print_warning(f"Sorted BAM file {sorted_bam_file} does not exist.")
                continue

            individual_id = common_adna.get_filename_from_path(sorted_bam_file).split(".")[0]
            output_folder = common_adna.get_folder_path_species_results_refgenome_damage_individual(
                species, ref_genome_id, individual_id)
            
            tasks.append((sorted_bam_file, ref_genome_path, output_folder))

        if tasks:
            num_processes = min(common_adna.THREADS_DEFAULT, cpu_count(), len(tasks))
            common_adna.print_info(f"Running mapDamage with max {num_processes} threads ...")

            with Pool(processes=num_processes) as pool:
                pool.starmap(execute_mapdamage, tasks)

    common_adna.print_success(f"mapDamage analysis for species {species} complete")


def all_species_run_mapdamage():
    common_adna.print_execution("Running mapDamage for all species")

    for species in common_adna.FOLDER_SPECIES:
        run_mapdamage_for_species(species)

    common_adna.print_info("mapDamage complete for all species")

def main():
    all_species_run_mapdamage()

if __name__ == "__main__":
    main()
