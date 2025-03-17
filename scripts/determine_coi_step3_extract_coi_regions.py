import os
import subprocess
import argparse

##todo


def process_single_bam(bam_file_path, coi_region_bed, output_dir):
    # Extract the base name of the BAM file (without path and extension)
    base_name = os.path.splitext(os.path.basename(bam_file_path))[0]

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Filter the BAM file for reads that map to the COI region
    print(f"Filtering {bam_file_path} for reads mapped to COI region...")
    coi_bam = os.path.join(output_dir, f"{base_name}_COI.bam")
    subprocess.run(["samtools", "view", "-b", "--region-file", coi_region_bed, bam_file_path], stdout=open(coi_bam, 'wb'))

    # Index the filtered BAM file
    print(f"Indexing {coi_bam}...")
    subprocess.run(["samtools", "index", coi_bam])

    print(f"Filtered and indexed BAM file created: {coi_bam}")