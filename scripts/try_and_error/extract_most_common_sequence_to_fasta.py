import pysam
import os
import argparse
from collections import Counter

def extract_sequences(bam_file_path, output_folder, minimum_sequence_length, depth_threshold):
    output_filename = os.path.join(output_folder, f"{os.path.basename(bam_file_path).replace('.bam', '')}_filtered.fasta")
    print(f"Processing BAM file: {bam_file_path}")
    print(f"Writing output to: {output_filename}")
    
    with pysam.AlignmentFile(bam_file_path, 'rb') as bamfile, open(output_filename, 'w') as txtfile:

        current_sequence = ""
        current_start_position = None
        current_depth_values = []
        current_scaffold = None
        total_sequences = 0

        for pileup_column in bamfile.pileup():
            position = pileup_column.reference_pos + 1
            scaffold = bamfile.get_reference_name(pileup_column.reference_id)
            depth = pileup_column.nsegments

            # If we are at a new scaffold, or depth is below threshold, output the current sequence (if any)
            if scaffold != current_scaffold or depth < depth_threshold:
                if current_sequence:
                    avg_depth = round(sum(current_depth_values) / len(current_depth_values), 2)
                    max_depth = max(current_depth_values)
                    txtfile.write(f">{current_scaffold}:{current_start_position}-{position - 1};{avg_depth};{max_depth}\n")
                    txtfile.write(f"{current_sequence}\n")
                    total_sequences += 1
                    print(f"Outputted sequence for scaffold {current_scaffold} from position {current_start_position} to {position - 1} with average depth {avg_depth} (Max: {max_depth})")
                    current_sequence = ""  # Reset sequence
                    current_start_position = None
                    current_depth_values = []

            if depth >= depth_threshold:
                # Start a new sequence if we're not currently building one
                if not current_sequence:
                    current_start_position = position
                    current_scaffold = scaffold

                # Count occurrences of each base at this position
                bases = [pileup_read.alignment.query_sequence[pileup_read.query_position]
                         for pileup_read in pileup_column.pileups if pileup_read.query_position is not None]
                if bases:
                    most_common_base, _ = Counter(bases).most_common(1)[0]
                    current_sequence += most_common_base
                    current_depth_values.append(depth)
            else:
                current_scaffold = scaffold  # Update the scaffold

        # If a sequence is still being built at the end, output it
        if current_sequence:
            avg_depth = round(sum(current_depth_values) / len(current_depth_values), 2)
            max_depth = max(current_depth_values)
            txtfile.write(f">{current_scaffold}:{current_start_position}-{position - 1};{avg_depth};{max_depth}\n")
            txtfile.write(f"{current_sequence}\n")
            total_sequences += 1
            print(f"Outputted final sequence for scaffold {current_scaffold} from position {current_start_position} to {position} with average depth {avg_depth} (Max: {max_depth})")

    print(f"Total sequences written for {bam_file_path}: {total_sequences}\n")

def main():
    parser = argparse.ArgumentParser(description="Extract continuous sequences from BAM files based on depth threshold.")
    parser.add_argument('-i', '--input', required=True, help="Input BAM file or folder containing BAM files")
    parser.add_argument('-o', '--output', required=True, help="Output folder to store results")
    parser.add_argument('-t', '--threshold', type=int, required=True, help="Depth threshold for filtering")

    args = parser.parse_args()

    # Ensure the output directory exists
    os.makedirs(args.output, exist_ok=True)

    # Process BAM files
    if os.path.isdir(args.input):
        bam_files = [os.path.join(args.input, f) for f in os.listdir(args.input) if f.endswith('.bam')]
    else:
        bam_files = [args.input]

    print(f"Starting sequence extraction with depth threshold: {args.threshold}")
    for bam_file in bam_files:
        extract_sequences(bam_file, args.output, args.threshold)
    print("All files processed.")

if __name__ == "__main__":
    main()
